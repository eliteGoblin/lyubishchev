# CLAUDE.md

## IMPORTANT: Keeping This File Current

**This file is the single source of truth for Claude Code context.** Any implementation that changes architecture, data flow, APIs, categories, CLI commands, or adds/removes modules MUST update the relevant sections below. Any new or changed requirements MUST be reflected in the Key References section. Future sessions depend on this file for full context -- stale info here means broken assumptions later.

When to update:
- Added/removed/renamed a Python module or class -> update Package Structure
- Changed Clockify tag mapping or activity categories -> update Activity Categories
- Added/changed CLI commands -> update CLI Commands
- Added/changed habit implementations -> update Habits System
- Changed validation rules -> update DayRecord Validation
- New external API endpoints used -> update Clockify Integration Details
- New requirement docs created -> update Key References

## Key References

| Document | Path | Purpose |
|---|---|---|
| Vision (user-authored) | `requirements/0_vision_brainstorm.md` | **Source of truth** for project direction. Takes priority over all other docs. |
| Requirements: CLI | `requirements/0_lyu_cli.md` | CLI feature requirements |
| Target architecture & roadmap | `topics/architecture/target_architecture.md` | DB-first architecture, schema, phased roadmap |
| Current architecture (snapshot) | `topics/current_architecture.md` | Documents the existing Clockify+Jupyter solution as a starting point |
| Clockify API overview | `topics/clockify/overview.md` | How this project uses Clockify, tag encoding |
| Clockify API reference | `topics/clockify/clockify_api_reference.md` | Structured endpoint docs (time entries, tags, etc.) |
| Clockify API full dump | `topics/clockify/clockify_api_full_text.txt` | Complete API text from https://docs.clockify.me/ |

## Project Overview

Lyubishchev is a personal time and metric tracking system inspired by Alexander Alexandrovich Lyubishchev's time statistics method. It fetches time tracking data from Clockify API and generates visualizations and reports in Jupyter notebooks.

## Environment Setup

```bash
# Setup virtual environment
sudo rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -r requirements.txt
```

Required environment variables in `.dotenv/myenv`:
```bash
export CLOCKIFY_USER_ID=xxx
export CLOCKIFY_WORKSPACE_ID=xxx
export CLOCKIFY_API_KEY=xxx
```

## Common Commands

### Running the Application
```bash
# Start Jupyter notebook server
./scripts/notebook_server_run.sh

# Open browser with report notebooks
./scripts/report.sh
```

### Testing
```bash
# Run all unit tests
py.test -s -rX -vv tests/unit/

# Run single test file
py.test -s -rX -vv tests/unit/path/to/test_file.py

# Run tests with focus marker (what's being developed)
py.test -s -rX -vv -m focus
```

### Code Quality
```bash
# Run full CI pipeline (format check, style, type check, tests)
./scripts/ci/ci

# Individual checks:
./scripts/ci/run-format-checker  # Runs isort + black, fails if code needs formatting
./scripts/ci/stylecheck           # Runs pycodestyle + pylint
./scripts/ci/typecheck            # Runs mypy with strict mode
./scripts/ci/unittest             # Runs pytest on unit tests
./scripts/ci/intgtest             # Runs integration tests

# Format code (auto-fix)
isort ./lyubishchev ./time_report_notebook ./tests
black ./lyubishchev ./time_report_notebook ./tests
```

### Pre-commit Hook
The pre-commit hook clears notebook outputs and runs full CI:
```bash
cd .git/hooks
ln -s ../../scripts/precommit_check.sh pre-commit -f
```

## Current Implementation Status

### What exists and works
- **Data fetching**: ClockifyFetcher pulls time entries via Clockify REST API (single endpoint, paginated)
- **Data parsing**: Raw JSON -> TimeInterval + Event objects -> DayRecord (with 6-step validation)
- **Reporting**: DayRangeReport aggregates DayRecords, provides categorized metrics, sleep data, event timestamps
- **Habits**: 6 habit implementations (getup, bed, event count, interval duration, interval count, interval oneof)
- **Highlights**: Duration summaries (work, self-improving, regret, sleep, exercise, calm) and habit frequency stats
- **Visualization**: 5 Jupyter notebooks (SingleDay, WeekReport, MonthReport, habit, DayRangeReport) using Plotly/calplot
- **CLI**: 4 Typer commands (dayrange, last, relative_week, relative_month) -- currently returns DayRangeReport objects but no terminal output
- **CI**: Full pipeline (isort, black, pycodestyle, pylint, mypy strict, pytest)

### What the CLI does NOT do yet
- The CLI commands return `DayRangeReport` objects but do not print/render anything to the terminal
- No terminal-based report output (tables, summaries, charts)
- See `requirements/0_lyu_cli.md` for planned CLI features

## Architecture

### Core Data Model

The system uses a time-series based data model with three key concepts:

1. **TimeInterval** - Represents a time period with duration and metadata (labels/annotations)
2. **Event** - Represents a point-in-time occurrence with metadata
3. **DayRecord** - Aggregates intervals and events for a single day

A "day" is defined by biological rhythm (wakeup -> bed), not calendar boundaries (00:00-23:59).

#### DayRecord Structure
- Range: `[wakeup_timestamp, bed_timestamp)`
- Includes: `last_night_sleep_minutes`, `time_intervals`, `events`
- Key timestamps: `wakeup_timestamp`, `getup_timestamp`, `bed_timestamp`
- Validation ensures: proper time ordering, reasonable duration ranges, and 85%+ time coverage

#### Metadata System
- **Labels**: String key-value pairs for filtering (e.g., `{"type": "work", "project": "lyubishchev"}`)
- **Annotations**: Arbitrary JSON values for additional data (e.g., `{"duration": 120, "note": "meeting"}`)
- Labels are used for searching/filtering, annotations for supplementary information

### Package Structure

```
lyubishchev/
├── config/             # Global config (timezone: Australia/Sydney, date lower bound)
├── clockify_fetcher/   # Fetches data from Clockify API
├── data_model/         # Core data structures and validation
│   ├── core_data_structure.py  # Label, Annotation, Metadata definitions
│   ├── time_interval.py        # TimeInterval class
│   ├── event.py                # Event class
│   ├── event_data.py           # Event type/tag constants and validation
│   ├── day.py                  # DayRecord, DayEvents, and 6 validators
│   ├── day_parser.py           # Parses raw data into DayRecords
│   ├── data_validator.py       # Pre-parsing validation (time order, coverage)
│   ├── data_fetcher.py         # TimeIntervalFetcher ABC
│   ├── data_reader.py          # DataReader ABC
│   ├── date_time_utils.py      # Date/time helpers (ranges, conversions)
│   └── search_time_series.py   # Binary search for time series
├── habit/              # Habit tracking implementations
│   ├── habit_protocol.py               # Habit protocol definition
│   ├── getup_habit.py                  # GetupHabit, BedHabit (TimeHabit base)
│   ├── time_event_habit.py             # TimeEventHabit (event count/day)
│   ├── time_interval_habit.py          # TimeIntervalHabit (duration/day)
│   ├── time_interval_counter_habit.py  # TimeIntervalCounterHabit (count/day)
│   └── time_interval_oneof_habit.py    # TimeIntervalOneofHabit (multi-key match)
├── report/             # Report generation
│   ├── report.py               # DayRangeReport class + get_match_dict()
│   ├── highlights.py           # Summary statistics (duration/habit highlights)
│   ├── time_intervals.py       # Hierarchical time aggregation tree
│   ├── constants.py            # Virtual label name constants
│   └── report_utils.py         # Dict helpers (prune, sum)
├── search/             # Search utilities for time series
│   └── search.py               # Match class + tree-based label matching
└── cli/                # Command-line interface
    ├── report_cli.py           # Typer-based CLI (dayrange, last, relative_week, etc.)
    ├── report.py               # get_report() pipeline function
    └── time_intervals.py       # fetch_time_intervals_events_since_wakeup()
```

### Data Flow

```
Clockify API (time entries endpoint)
    |
    v
ClockifyFetcher.fetch_raw_time_series()     -- paginated HTTP GET, reversed to asc order
    |
    v
generate_time_interval_from_time_series()   -- raw JSON -> TimeInterval
generate_event_from_time_series()           -- raw JSON -> Event (if event tags present)
    |
    v
parse_and_generate_day_records()            -- splits by day using wakeup/bed events
    |- get_events_for_single_day()          -- finds [prev_bed .. current_bed] events
    |- get_time_intervals_for_single_day()  -- finds intervals within wakeup..bed
    |- parse_and_generate_day_record()      -- creates DayRecord
    |   |- must_single_day_events()         -- pre-parse validation
    |   |- must_single_day_time_intervals() -- pre-parse validation
    |   '- DayEvents helpers               -- extract wakeup/getup/bed timestamps
    '- validate_day_record()               -- 6 validators run in sequence
    |
    v
list[DayRecord]
    |
    v
DayRangeReport                              -- aggregates DayRecords
    |- get_interval_metrics()               -- categorized time per day
    |- get_event_metrics()                  -- wakeup/getup/bed timestamps
    |- get_sleep_spans_minute()             -- night sleep + nap per day
    |- get_long_format_data_list()          -- for stacked bar charts
    '- Habit.data()                         -- individual habit metrics
    |
    v
Jupyter Notebooks (Plotly, calplot, pandas)
```

## Clockify Integration Details

### API Endpoint Used
```
GET https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries
```
- **Auth**: `X-Api-Key` header
- **Params**: `start`, `end` (ISO timestamps with Z suffix), `page-size` (50), `page`, `hydrated=true`
- **Pagination**: Auto-paginated, results returned in descending order (reversed to ascending in code)
- **Retry**: 5 retries with exponential backoff on 500/502/503/504
- **Full API docs**: see `topics/clockify/docs/`

### How Clockify Tags Map to Internal Data

Each Clockify time entry has **tags** that encode labels and events:

**Tag formats:**
- `key=value` format -> becomes a Label (e.g., `project=lyubishchev`, `event_type=wakeup`)
- `key` only (no `=`) -> becomes a tag (stored as `{key: ""}` in label)

**Event detection:**
- Tags with `event_type=<type>` create Event objects
- Valid event types: `wakeup`, `getup`, `bed`, `partner_period`, `unwell`, `recover_unwell`
- Tags like `cold`, `injured` (no `=`) become event tags for unwell/recover events
- Event timestamp assignment: `bed` events use `timeInterval.end`; all others use `timeInterval.start`
- A single Clockify entry can produce BOTH a TimeInterval AND an Event

**Project assignment:**
- If a Clockify entry has a `project`, it's added as `{"project": project_name}` to the label

### Activity Categories (get_match_dict)

Activities are categorized via the `get_match_dict()` function in `report/report.py`. These define how raw Clockify tags map to report categories:

| Category | Tags (Clockify labels) |
|---|---|
| `calm` | meditation, walk |
| `self_improving` | lyubishchev, oj, software, audible, reading |
| `self_improving_tech` | job, lyubishchev, oj, software |
| `self_improving_non_tech` | audible, reading |
| `work_all` | work, job |
| `sex_all` | sex, mbate |
| `exercise` | jog, swim, anaerobic |
| `intangible` | friends, family, lisha, dating |
| `regret` | pmo, numb, dispute, video, game, internet, novel |
| `routine_all` | cook, self_routine, housework, meal |
| `solitude` | karaoke |

The hierarchical aggregation tree (`time_intervals.py`) groups these into a sunburst-compatible structure:
```
effective_output/
    self_improving/
        tech/     (job, lyubishchev, oj, software)
        non_tech/ (audible, reading)
    work_all/     (work, job)
calm/             (meditation, walk)
exercise/         (jog, swim, anaerobic)
intangible/       (friends, family, lisha, dating)
regret/           (pmo, numb, dispute, video, game, internet, novel)
routine_all/      (cook, self_routine, housework, meal)
sex_all/          (sex, mbate)
solitude/         (karaoke)
sleep_all/        (night_sleep, nap)
other/            (unrecorded time)
```

## Tree-Based Label Matching (search/search.py)

The `Match` class uses a dict-tree to match TimeInterval labels:
- **Siblings** (keys at same level) = **OR** semantics
- **Path to leaf** (keys along a path) = **AND** semantics
- Leaf value is `None`; non-leaf value is a nested dict

Example: `{"a": None, "b": {"c": None}}` matches label if `a` is present OR (`b` AND `c` are both present).

`Match.from_dict({"jog": None, "swim": None})` matches any interval tagged with `jog` or `swim`.

## DayRecord Validation

Six validators run sequentially (fail-fast):

1. **validate_required_fields** - wakeup/getup/bed timestamps, last_night_sleep, time_intervals must exist
2. **validate_value_range** - wakeup/getup: 03:00-13:00, bed: 19:00-08:00 (next day), sleep: 3h-13h, day length: 10h-20h
3. **validate_time_order** - wakeup <= getup < bed
4. **validate_time_intervals_order** - intervals in ascending order, no overlaps
5. **validate_events** - events in order, no wakeup/getup/bed events (those become DayRecord fields)
6. **validate_time_intervals_match_events** - first interval >= wakeup, last interval <= bed, recorded >= 85% of day length

## Habits System

All habits implement `Habit` protocol: `def data(self) -> pandas.Series[int]`

Returns pandas Series with DatetimeIndex (for calplot heatmap compatibility).

| Habit Class | What it measures | Score/Value |
|---|---|---|
| `GetupHabit(TimeHabit)` | Getup time vs target | (target - actual) minutes; positive = early |
| `BedHabit(TimeHabit)` | Bed time vs target | -(actual - target) minutes; positive = early |
| `TimeEventHabit` | Event occurrence count | Count of events/day matching a label key |
| `TimeIntervalHabit` | Activity duration | Total minutes/day of intervals matching key |
| `TimeIntervalCounterHabit` | Activity count | Count of intervals/day matching key |
| `TimeIntervalOneofHabit` | Multi-key duration | Total minutes/day matching ANY key in list |

`BedHabit` uses `wakeup_timestamp` as reference for target time construction (handles midnight crossing).

## Report Highlights

`highlights.py` provides two summary DataFrames:

- **`get_duration_highlights()`**: daily_average + total_hours for work (weekday avg), self_improving, regret, night_sleep, nap, exercise, calm
- **`get_habbits_highlight()`**: frequency + avg_minutes_per_activity + avg_minutes_per_day + total_hours for sex_all, walk, meditation, nap, exercise

## CLI Commands

Typer-based CLI (`python -m lyubishchev`):

| Command | Args | Description |
|---|---|---|
| `dayrange` | `start_date end_date` | Report for `[start_date, end_date)` |
| `last` | `last_days` | Report for `[today - N, today)` |
| `relative_week` | `week_offset` | 0 = current week (Sun-today), -1 = last week |
| `relative_month` | `month_offset` | 0 = current month (1st-today), -1 = last full month |

The `get_report()` pipeline: creates ClockifyFetcher -> fetches with 1-day buffer -> parses into DayRecords -> wraps in DayRangeReport.

## Notebook Reports

Located in `time_report_notebook/`:
- `SingleDay.ipynb` - Single day: pie chart, Gantt chart, sunburst of time breakdown
- `WeekReport.ipynb` - Weekly: stacked bars, sunburst, wakeup/bed time plots, highlights
- `MonthReport.ipynb` - Monthly summary with same visualizations
- `habit.ipynb` - Habit heatmaps using calplot
- `DayRangeReport.ipynb` - Custom date range analysis

Notebook helpers in `time_report_notebook/nb_helper_*.py`:
- `nb_helper_util.py` - Generic charting (bar charts, sunburst, dict-to-tree conversion, minutes-to-hours)
- `nb_helper_sleep.py` - Sleep stacked bar charts
- `nb_helper_event.py` - Wakeup/bed time line plots (handles midnight crossing)
- `nb_helper_time_stats.py` - Pie charts from interval metrics
- `nb_helper_aggregate_time_intervals.py` - Sunburst + Gantt charts for time intervals
- `nb_helper_effective_output.py` - Effective output bar/sunburst charts

## Key Design Decisions

- **Biological day**: A day spans wakeup to bed, may cross midnight. Date determined by wakeup event's local date.
- **Sleep tracking**: `last_night_sleep_minutes` = previous bed -> wakeup. Kept separate from daytime activities.
- **All timestamps are Arrow objects** (timezone-aware), converted to `Australia/Sydney` at API boundary.
- **Strict validation**: 6 validators, fail-fast. 85% time coverage required per day.
- **Data starts from 2023-03-12** (`config.get_date_lower_bound()`).
- **Tags are the encoding mechanism**: Clockify tags with `key=value` format encode labels; plain tags encode boolean flags. Event types are embedded in the same time entry as `event_type=<type>`.

## Development Notes

- Python 3.12+ required (recently upgraded from 3.10)
- Type checking is strict mode enabled
- Test marker `@pytest.mark.focus` for tests under active development
- DayRecord validation is comprehensive and fail-fast by design
- Timezone handling uses Arrow library with IANA timezone names from config
- All notebooks should have outputs cleared before commit (enforced by pre-commit hook)
