# Architecture: Current Solution

## Overview

The current solution is a **Clockify API + Jupyter Notebook** pipeline. Time data is manually entered in the Clockify web/desktop app. A Python backend fetches that data via Clockify's REST API, parses it into a domain model centered on "biological days" (wakeup-to-bed), and generates visualizations in Jupyter notebooks using Plotly and calplot.

```
┌──────────────┐     REST API      ┌──────────────────┐     Parse/Validate     ┌─────────────┐
│   Clockify   │ ──────────────>   │  ClockifyFetcher  │ ──────────────────>   │  DayRecord   │
│  (Manual UI) │   GET time-entries │  (fetcher.py)     │   day_parser.py       │  (domain)    │
└──────────────┘                   └──────────────────┘                        └──────┬──────┘
                                                                                      │
                                                                              DayRangeReport
                                                                                      │
                               ┌──────────────────────────────────────────────────────┤
                               │                              │                       │
                        ┌──────▼──────┐              ┌────────▼──────┐        ┌───────▼──────┐
                        │  Notebooks  │              │   Habits      │        │  Highlights  │
                        │  (Plotly)   │              │  (calplot)    │        │  (DataFrames)│
                        └─────────────┘              └───────────────┘        └──────────────┘
```

## System Components

### 1. Data Source: Clockify

The user manually tracks activities in Clockify using time entries with **tags** as the encoding mechanism:

| What the user enters in Clockify | What it becomes internally |
|---|---|
| Tag `event_type=wakeup` on a time entry | Event object (TYPE_WAKEUP) |
| Tag `event_type=bed` on a time entry | Event object (TYPE_BED), timestamp = entry end |
| Tag `jog` on a time entry | TimeInterval with label `{"jog": ""}` |
| Tag `project=lyubishchev` on a time entry | TimeInterval with label `{"project": "lyubishchev"}` |
| Clockify project "work" assigned to entry | TimeInterval with label `{"project": "work"}` |

A single Clockify time entry can produce **both** a TimeInterval and an Event (e.g. a 5-minute entry tagged `event_type=wakeup` + `self_routine` produces a wakeup Event and a self_routine TimeInterval).

### 2. Data Fetching: ClockifyFetcher

**File:** `lyubishchev/clockify_fetcher/fetcher.py`

Single API endpoint used:
```
GET https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries
    ?start=<ISO>&end=<ISO>&page-size=50&page=<N>&hydrated=true
```

- `hydrated=true` returns full tag objects with names (critical -- without it, only tag IDs are returned)
- Results come in **descending** order; code reverses to ascending
- Paginated (50 per page), auto-fetches all pages
- Retries 5x with exponential backoff on 5xx errors

Each raw JSON entry is processed by two functions:
- `generate_time_interval_from_time_series()` -> always produces a TimeInterval (or None if entry is still running)
- `generate_event_from_time_series()` -> produces an Event only if `event_type=*` tag exists

### 3. Data Model: Biological Days

**Key files:** `lyubishchev/data_model/day.py`, `day_parser.py`

A "day" is **not** a calendar day (00:00-23:59). It's a biological day: wakeup to bed. This may cross midnight (e.g. wakeup 7:00 Jan 5, bed 01:30 Jan 6 -- this is Jan 5's day).

**DayRecord** structure:
```
DayRecord
├── wakeup_timestamp    (Arrow, 03:00-13:00)
├── getup_timestamp     (Arrow, 03:00-13:00, >= wakeup)
├── bed_timestamp       (Arrow, 19:00-08:00 next day, > getup)
├── last_night_sleep_minutes  (int, 3h-13h range)
├── time_intervals      (list[TimeInterval], ascending, no overlaps, >= 85% coverage)
└── events              (list[Event], ascending, no wakeup/getup/bed events)
```

**Parsing pipeline** (`parse_and_generate_day_records()`):
1. Takes a flat list of Events + TimeIntervals for a date range
2. For each day in range:
   - `get_events_for_single_day()` -- finds [prev_bed .. current_bed] events
   - `get_time_intervals_for_single_day()` -- finds intervals within wakeup..bed
   - `parse_and_generate_day_record()` -- assembles DayRecord
3. Each DayRecord is validated by 6 sequential validators (fail-fast):
   - Required fields exist
   - Value ranges (wakeup 03-13, bed 19-08, sleep 3-13h, day length 10-20h)
   - Time ordering (wakeup <= getup < bed)
   - Interval ordering (ascending, no overlaps)
   - Event validity (no wakeup/getup/bed in event list)
   - Coverage (recorded time >= 85% of day length)

### 4. Reporting: DayRangeReport

**File:** `lyubishchev/report/report.py`

`DayRangeReport` wraps a `list[DayRecord]` and provides aggregation methods:

| Method | Returns | Used by |
|---|---|---|
| `get_interval_metrics()` | Dict of per-day minutes by category (effective_output, exercise, sleep, calm, etc.) | Pie charts, highlights |
| `get_event_metrics()` | Dict of per-day Arrow timestamps (wakeup, getup, bed) | Wakeup/bed plots |
| `get_sleep_spans_minute()` | (night_sleeps[], naps[]) per day | Sleep charts |
| `get_long_format_data_list()` | Long-format dicts for stacked bars | Stacked bar charts |
| `get_time_intervals()` | Flat list of all TimeIntervals | Sunburst, Gantt |
| `get_total_minutes()` | Total minutes in range | "Other" category calculation |

**Activity categorization** is defined in `get_match_dict()`:
```
calm           = {meditation, walk}
self_improving = {lyubishchev, oj, software, audible, reading}
work_all       = {work, job}
exercise       = {jog, swim, anaerobic}
intangible     = {friends, family, lisha, dating}
regret         = {pmo, numb, dispute, video, game, internet, novel}
routine_all    = {cook, self_routine, housework, meal}
sex_all        = {sex, mbate}
solitude       = {karaoke}
```

**Highlights** (`highlights.py`):
- `get_duration_highlights()` -- DataFrame: daily_average + total_hours for work, self_improving, regret, sleep, exercise, calm
- `get_habbits_highlight()` -- DataFrame: frequency + avg per activity + avg per day + total for sex, walk, meditation, nap, exercise

### 5. Habits System

**Files:** `lyubishchev/habit/*.py`

All implement `Habit` protocol: `def data(self) -> pandas.Series[int]`

Returns Series with DatetimeIndex (calplot compatibility) where each value is a per-day score:

| Class | Measures | Score |
|---|---|---|
| GetupHabit | Getup time vs target "HH:MM" | (target - actual) minutes |
| BedHabit | Bed time vs target "HH:MM" | -(actual - target) minutes |
| TimeEventHabit | Event occurrence | Count per day |
| TimeIntervalHabit | Activity duration | Total minutes per day |
| TimeIntervalCounterHabit | Activity count | Count per day |
| TimeIntervalOneofHabit | Multi-key duration | Total minutes matching any key |

### 6. Visualization: Jupyter Notebooks

**Location:** `time_report_notebook/`

#### Notebooks

| Notebook | Scope | Key Charts |
|---|---|---|
| `SingleDay.ipynb` | Today + past 4 days | Sunburst (time hierarchy), Gantt (timeline) per day |
| `WeekReport.ipynb` | Current week (Sun-today) | Duration/habit tables, sunburst, stacked bars, wakeup/bed scatter, per-category breakdowns |
| `MonthReport.ipynb` | Current month | Same as WeekReport but monthly scope |
| `DayRangeReport.ipynb` | Custom range via `last(N)` | Same as above + pie chart |
| `habit.ipynb` | Long-range (configurable) | 15+ calplot calendar heatmaps (positive habits in green, negative in red) |

#### Visualization Types

| Chart Type | Library | Helper Function | Purpose |
|---|---|---|---|
| Sunburst | Plotly | `sunburst_time_intervals()`, `sunburst_effective_output()`, `sunburst_tree_depth_2()` | Hierarchical time breakdown |
| Gantt | Plotly | `gantt_time_intervals()` | Daily activity timeline |
| Stacked Bar | Plotly | `stack_bar()`, `stack_bar_sleep_all()`, `stack_bar_effective_output()` | Daily comparison by sub-category |
| Grouped Bar | Plotly | `draw_bars_chart()`, `draw_bars_effective_output()` | Side-by-side daily comparison |
| Scatter/Line | Plotly | `draw_wakeup_plot()`, `draw_bed_plot()` | Wakeup/bed time trends |
| Pie | Plotly | `plot_piechart()` | Overall time distribution |
| Calendar Heatmap | calplot | Habit classes `.data()` | Long-range habit tracking |

#### Helper Modules

| Module | Purpose |
|---|---|
| `nb_helper_util.py` | Generic: bar charts, sunburst, dict-to-tree, minutes-to-hours |
| `nb_helper_sleep.py` | Sleep stacked bar (night + nap) |
| `nb_helper_event.py` | Wakeup/bed time scatter plots (handles midnight crossing) |
| `nb_helper_time_stats.py` | Pie charts from interval metrics |
| `nb_helper_aggregate_time_intervals.py` | Sunburst + Gantt for time intervals |
| `nb_helper_effective_output.py` | Effective output bar/sunburst charts |

### 7. CLI

**Files:** `lyubishchev/cli/report_cli.py`, `report.py`, `time_intervals.py`

Typer-based CLI invoked via `python -m lyubishchev`:

| Command | Example | Date Range |
|---|---|---|
| `dayrange` | `dayrange 2024-01-01 2024-01-31` | [start, end) |
| `last` | `last 7` | [today-7, today) |
| `relative_week` | `relative_week 0` | Current week Sun-yesterday |
| `relative_month` | `relative_month -1` | Last full month |

**Current limitation:** Commands return `DayRangeReport` objects but produce no terminal output. The CLI is a skeleton -- all actual visualization happens in Jupyter notebooks.

### 8. CI Pipeline

**Scripts:** `scripts/ci/`

Pre-commit hook (`scripts/precommit_check.sh`):
1. Clear all notebook outputs (enforces clean VCS)
2. `git add .`
3. Run full CI pipeline

CI pipeline (`scripts/ci/ci`) -- sequential, fail-fast:
1. `run-format-checker` -- isort + black (fails if code needs reformatting)
2. `stylecheck` -- pycodestyle + pylint
3. `typecheck` -- mypy strict mode
4. `unittest` -- `pytest tests/unit/`
5. `intgtest` -- `pytest tests/integration/` (only when `is_CI` env var is set)
6. `check_notebook_output` -- validates notebooks have cleared outputs

## User Workflow

```
┌── Daily Use ──────────────────────────────────────────────────────────┐
│                                                                       │
│   1. Track time in Clockify app (web/desktop)                         │
│      - Start/stop timers with tags: jog, work, event_type=wakeup...  │
│                                                                       │
│   2. Start Jupyter:  ./scripts/notebook_server_run.sh                 │
│      - Activates venv, sources .dotenv/myenv, starts notebook server  │
│                                                                       │
│   3. View reports:   ./scripts/report.sh                              │
│      - Opens SingleDay, WeekReport, MonthReport, habit in browser     │
│      - Run All Cells in each notebook to fetch data + render charts   │
│                                                                       │
│   4. (Optional) CLI:  python -m lyubishchev last 7                    │
│      - Currently returns DayRangeReport object, no terminal output    │
│                                                                       │
└── Development ────────────────────────────────────────────────────────┘
│                                                                       │
│   5. Edit code, run tests:  py.test -s -rX -vv tests/unit/           │
│   6. Format: isort + black                                            │
│   7. Commit: pre-commit hook runs full CI pipeline automatically      │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

## Data Flow (End to End)

```
Clockify UI (user enters time entries with tags)
      │
      ▼
Clockify REST API
GET /v1/workspaces/{id}/user/{id}/time-entries?hydrated=true
      │ (paginated JSON, descending order)
      ▼
ClockifyFetcher.fetch_raw_time_series()
      │ (reverse to ascending)
      ▼
┌─────────────────────────────────────┐
│ For each raw JSON time entry:       │
│  ├─ generate_time_interval_from_*() │ ──> TimeInterval (always)
│  └─ generate_event_from_*()         │ ──> Event (if event_type tag)
└─────────────────────────────────────┘
      │
      ▼
list[TimeInterval] + list[Event]  (ascending by timestamp)
      │
      ▼
parse_and_generate_day_records(start_date, end_date, events, intervals)
      │
      │  For each day in [start, end):
      │   ├─ get_events_for_single_day()         [prev_bed .. bed]
      │   ├─ get_time_intervals_for_single_day()  [wakeup .. bed]
      │   ├─ parse_and_generate_day_record()
      │   │    ├─ must_single_day_events()         (pre-parse validation)
      │   │    ├─ must_single_day_time_intervals()  (pre-parse validation)
      │   │    └─ DayEvents helpers                 (extract timestamps)
      │   └─ validate_day_record()                  (6 validators, fail-fast)
      ▼
list[DayRecord]
      │
      ▼
DayRangeReport(day_records)
      │
      ├──────────────────────┬──────────────────────┬──────────────
      ▼                      ▼                      ▼
 get_interval_metrics()  get_event_metrics()   Habit.data()
 get_sleep_spans()       get_long_format_*()   get_duration_highlights()
 get_time_intervals()    get_total_minutes()   get_habbits_highlight()
      │                      │                      │
      ▼                      ▼                      ▼
 nb_helper_*.py functions                      calplot heatmaps
      │
      ▼
 Plotly charts: sunburst, Gantt, stacked bar, scatter, pie
      │
      ▼
 Jupyter notebook output (interactive, browser-based)
```

## Hierarchical Time Aggregation Tree

The sunburst charts use this hierarchy (defined in `report/time_intervals.py`):

```
24-hour day
├── effective_output
│   ├── self_improving
│   │   ├── tech        (job, lyubishchev, oj, software)
│   │   └── non_tech    (audible, reading)
│   └── work_all        (work, job)
├── calm                 (meditation, walk)
├── exercise             (jog, swim, anaerobic)
├── intangible           (friends, family, lisha, dating)
├── regret               (pmo, numb, dispute, video, game, internet, novel)
├── routine_all          (cook, self_routine, housework, meal)
├── sex_all              (sex, mbate)
├── solitude             (karaoke)
├── sleep_all
│   ├── night_sleep
│   └── nap
└── other                (unrecorded time = total - all above)
```

## Habit Tracking (Calendar Heatmaps)

The `habit.ipynb` notebook renders 15+ calplot heatmaps:

**Positive habits (green colormap):**
- 7AM Club (GetupHabit, target 07:00)
- Bedtime (BedHabit, target 21:00)
- Diary, Swim, Meditation, Anaerobic, Dance, OJ
- ReadingSelfHelp (reading + audible combined)
- LearnTech (software)
- Sex (counter-based)

**Negative habits (red colormap):**
- Quarrel (quarrel + bicker)
- Porn, Video, Game

Each cell shows a year-long calendar where color intensity = time spent (or score for time-target habits).

## Key Design Constraints

1. **Biological day model** -- wakeup-to-bed, not 00:00-23:59. Date = wakeup date.
2. **85% coverage rule** -- recorded time must be >= 85% of waking hours per day.
3. **Tags are the only data channel** -- all domain semantics (activities, events) are encoded in Clockify tag names. No Clockify custom fields or descriptions are used for structured data.
4. **Single API endpoint** -- only `GET /time-entries` is used. No write-back to Clockify.
5. **Timezone: Australia/Sydney** -- hardcoded in `config/config.py`. All Arrow timestamps converted at API boundary.
6. **Data starts 2023-03-12** -- lower bound in config; earlier data is skipped.
7. **Notebooks are the primary output** -- the CLI exists but doesn't render reports to terminal.
