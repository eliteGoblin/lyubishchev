# Handoff: Lyubishchev rebuild, state on 2026-11-15

This file lets a new Claude Code session, on any machine, continue the rebuild without the old session transcript. It records what was decided, what exists, what is open, and the exact next step. Written at the end of the design sessions of 2026-11-01 to 2026-11-15. Sources: the ADRs, `CONTEXT.md`, the repo docs, the design artifact comments, and the session transcript of 2026-11-08.

How to resume on another machine:

1. Clone `https://github.com/eliteGoblin/lyubishchev` and open Claude Code in the repo root.
2. Tell Claude: "Read `docs/handoff_nov_15.md`, then `CONTEXT.md` and the three files in `docs/adr/`. `CLAUDE.md` describes the old Python system and is stale for the rebuild."
3. Continue from section 12 (Exact next steps).

---

## 1. What the project is

Lyubishchev is a personal time tracker in the style of Alexander Lyubishchev: every span of the day gets a record of what was done, and reports over any range say where the time went and what it produced. Today the data lives in Clockify and the reports are Jupyter notebooks fed by the Python code in `lyubishchev/`. The main pain (Frank, `docs/requirements/0_vision_brainstorm.md`): logging in Clockify is slow, days are backfilled late, and backfilling costs time and energy.

The rebuild (decided 2026-11-07 and 2026-11-08) is a local web app:

- A SQLite database owns the data.
- A Log page where Frank logs time by chatting, with a running timer for the current activity, like Clockify.
- A read-only Stats page with charts.
- Start as a minimal MVP for one user, with the seams for many users and social login later.

Vision for later (from the same doc): more users with their own accounts (Google, GitHub, Microsoft, email), AI insight from chat, full ownership of the data, web first and maybe a CLI later.

---

## 2. Status snapshot on 2026-11-15

| Item | State | Evidence |
|---|---|---|
| New TypeScript code | None. No `apps/`, no `packages/`, no `package.json` at root | repo root listing |
| Python code | Still in place in `lyubishchev/`, `tests/`, `time_report_notebook/`. Not moved to `archive/python/` yet | repo root listing |
| Design docs | Committed and pushed: ADRs 0001 to 0003, `CONTEXT.md`, `docs/requirements/`, `requirements/`, `topics/` | commits `2f5583f` and `3f6464a`, 2026-11-14 |
| UI mock source | `docs/design/ui-mock/Main.dc.html`, `Stats.dc.html`, `canvas.json`, same as artifact version 10 | commit `3f6464a`; markers `day-input`, `class="day"` and the grey box present |
| UI mock artifact | https://claude.ai/artifact/RxiHGsjwjEtUjPtH7P3ADy, version 10, private to Frank | Artifact publish result 2026-11-08 |
| Git | `master` equals `origin/master`. Four notebook files have uncommitted output changes, about 48,000 added lines: `MonthReport`, `SingleDay`, `WeekReport`, `habit`. Do not commit them with outputs; the pre-commit hook clears outputs | `git status`, `git diff --stat`, 2026-11-15 |
| Repo visibility | PUBLIC | `gh repo view`, 2026-11-15 |
| Remote URL | Clean, no token | `git remote -v`, 2026-11-15 |
| `CLAUDE.md` | Describes the Python system. Stale for the rebuild. Lists Frank's personal activity categories, now public | file content |
| Session alias | None created | SessionStart hook message |

---

## 3. Which documents to trust

Precedence when documents disagree:

1. Frank's words in the current session.
2. This handoff and the ADRs in `docs/adr/` (2026-11-08).
3. `CONTEXT.md` glossary (2026-11-08, updated 2026-11-14).
4. `docs/design/ui-mock/` (the MVP UI, version 10, example data only).
5. `docs/requirements/0_vision_brainstorm.md` (Frank's vision, April 2026).
6. `topics/architecture/target_architecture.md` and `topics/core_data_model_review.md` (April 2026). Still useful for the agent tool design, the schema sketch and the roadmap reasoning, but superseded in these points:

| April 2026 doc said | Decision of 2026-11-08 |
|---|---|
| CLI first, web app in phase 5 | Web app with chat first; no CLI in the MVP |
| Tags are labels with value `""`; the activity is a label | Every TimeEntry and Event has exactly one mandatory `type`; labels are key=value context |
| `annotations` JSON holds description and source ids | `description` is its own JSON field; numbers go in `measures`; source ids are a fixed column |
| `event_type` column | `type` on both tables |
| `time_intervals` table with `duration_minutes` | TimeEntry has `start` and `end`; duration is derived |
| Day rejected when a validator fails (85% coverage rule) | Day has a status (complete or incomplete, with reasons); only overlap and `start >= end` block a write |
| `is_valid` on `day_records` | Day is computed, not stored |

7. `CLAUDE.md` for the old Python system only.

---

## 4. Decisions made

### 4.1 Recorded as ADRs (all accepted 2026-11-08)

- **ADR 0001** `docs/adr/0001-sqlite-is-source-of-truth.md`: SQLite is the source of truth from day 1. Clockify is an import source only: one full import, repeatable without duplicates. Chat and UI write only to SQLite. Schema stays PostgreSQL-compatible.
- **ADR 0002** `docs/adr/0002-typescript-monorepo-python-archived.md`: TypeScript monorepo with a Next.js app. Python code moves to `archive/python/` with `git mv`, read-only reference. Layout: `apps/web`, `packages/core`, `packages/db`, `packages/clockify`, `packages/agent`, `archive/python`. Tooling: pnpm workspaces, strict TypeScript, Vitest, ESLint with a rule that `packages/core` imports no other workspace package. No Turborepo yet.
- **ADR 0003** `docs/adr/0003-json-fields-with-schema-version.md`: fixed columns plus JSON columns `labels`, `measures`, `description`. Code checks the JSON at write time; the database does not. Readers ignore unknown keys. Integer `schema_version` per row. Rename or move of a key is "expand then contract" with a `migrate` command that reports counts.

### 4.2 Decided in conversation, not yet in an ADR

- **Method**: light domain-driven design (glossary in `CONTEXT.md`, ADRs for hard-to-reverse choices), ports and adapters (hexagonal). `packages/core` holds entities, pure functions, use cases and port interfaces, with no I/O dependency. Adapters live in `db`, `clockify`, `agent` and `apps/web`.
- **Agent design**: the LLM orchestrates; deterministic tools compute. Tools run server-side, take and return structured data, do all date math, queries, validation and writes. The LLM never states a fact that did not come from a tool result. No raw database or shell access for the model. Least privilege per tool (OWASP "Excessive Agency").
- **Writes need a confirm card**: every tool that changes data shows the parsed entry in the chat (time, type, labels, measures, note) with Add and Edit buttons. Nothing is written before Frank presses Add.
- **Chat is the only input in the MVP** (Frank's check comment, 2026-11-08): one sentence becomes type, time, labels, measures and note. No form, no label picker.
- **Day status instead of rejection** (Q4, accepted): a Day can be incomplete; the UI shows gaps and asks Frank to fill them, but never blocks.
- **Multi-user seams, no auth code** (Q8, agreed): `user_id` on every table and in every query; a `CurrentUser` port that returns `"default"` in the MVP; every use case and tool takes `userId` as input. Provider choice (Auth.js, Better Auth, Clerk, Keycloak) deferred to a later ADR.
- **MVP scope rule** (Frank, 2026-11-08): "KISS, start simple, avoid too many things I did not ask but you suggest, less is more." Build only what Frank asked or drew. Name an extra in one line and let him decide.
- **UI feedback loop**: Frank sketches in Excalidraw (Chrome tab, Claude screenshots it with the chrome-devtools MCP) or edits and comments on the design artifact; Claude redraws the artboards. Figma was tried and dropped: Claude cannot draw in Figma from the session.

### 4.3 Proposed, not confirmed by Frank

- **Q5 Stats page content**: proposed last 7 days with coverage per day and gap list, category totals as stacked bars, wakeup and bed times, sleep hours; later habit heatmaps, month view, sunburst. The mock then went a different way (section 8.2). Frank has not reviewed the Stats artboard in detail.
- **Q6 Chat scope**: proposed read tools for questions about the data, add entries, backfill one gap at a time with pattern suggestions, correct or delete entries the chat added, confirm card before each write; not in v1: editing imported Clockify entries, changing categories. Frank confirmed only that chat fills all fields. The rest is not confirmed.
- **Q7 Claude access**: proposed an Anthropic API key in `.env.local`, model Sonnet. Not confirmed.
- **Requirements document**: proposed `docs/requirements/1_mvp_requirements.md` with the statement "a report says what I did and produced, not only how long". Frank has not said yes.
- **Gate 1**: the clarify skill ends with a short summary that Frank confirms. This has not happened.

---

## 5. Domain model

Terms are defined in `CONTEXT.md`. This section adds the rules and examples that were agreed on 2026-11-08.

### 5.1 Foundation

**TimeEntry**: `[start, end)`, exactly one `type`, optional `labels`, optional `measures`, optional `description`.

```json
{
  "start": "2026-11-08T11:00:00+11:00",
  "end": "2026-11-08T11:40:00+11:00",
  "type": "read",
  "labels": { "book": "deep_work" },
  "measures": { "chapters": 2 },
  "description": "on the train"
}
```

**Event**: one `timestamp`, exactly one `type`, optional `labels`, optional `description`. Examples: `wakeup`, `getup`, `bed`, `unwell`, `recover_unwell`, `partner` (Frank: "just partner is enough"), `done`.

**Type**: the one word that says what the entry or event was. Mandatory. From a user-managed list. Frank chose the name `type` over `activity` ("type is more intuitive name for me").

**Label**: key with optional value, context only, never the type. Examples: `project=cba`, `book=deep_work`, `item=gap_finder`, `partner`. Keys from a user-managed list, values free but reused.

**Measure**: a named number that reports add up: `chapters: 2`, `km: 8`. Duration is never a measure.

**Description**: free text for reading and for narrative summaries. Never matched or counted.

Rules:

- A write is rejected only when `start >= end` or the entry overlaps an existing one.
- Unknown label keys or measure names are rejected at write time by the code (planned: Zod schemas). The lists of known types and keys are per user.
- Everything optional is optional; there are no fixed labels or measures.

### 5.2 Helpers

**Subject**: the record behind a short label value: kind (`book`, `project`, `course`), key (`deep_work`), title and details. It answers "what book is `deep_work`" without putting the full title into every entry. Entries refer to the key only.

**Category** and **CategoryTree**: one named tree per user. A node holds either child categories or a rule. A rule is a list of patterns that select TimeEntries by `type`, and later by label too. Leaves are categories with rules, not types. Entries are never stored in the tree; the tree is applied at report time, so editing it regroups history and changes no entry. Example:

```
root
  effective_output
    self_improving
      tech        rule: type in [lyu, oj, software]
      non_tech    rule: type in [audible, read]
    work          rule: type in [work, job]
  exercise        rule: type in [jog, swim, anaerobic]
  routine         rule: type in [cook, self_routine, housework, meal]
  other           everything not matched
```

### 5.3 Derived

**Day**: from a `wakeup` Event to the next `bed` Event. May cross midnight; its date is the local date of the wakeup. Holds its TimeEntries, Events, last night's sleep, **Coverage** (share of the Day covered by entries), **Gaps** (spans with no entry) and a status: complete or incomplete with reasons. Computed, not stored. The exact list of incompleteness reasons is not yet defined; the Python validators in `lyubishchev/data_model/day.py` (value ranges, order, 85% coverage) are the starting list.

**Report**: totals over a range per category, type, label or measure, the finished items, and an optional narrative built from descriptions. The requirement behind it (Frank): a range report must say what he did and produced, for example hours per project, chapters read per book, work items done, and a short narrative.

---

## 6. Storage model

From ADR 0003 and the conversation:

| Table | Fixed columns | JSON columns |
|---|---|---|
| `time_entries` | `id`, `user_id`, `start`, `end`, `type`, `external_id`, `schema_version` | `labels`, `measures`, `description` |
| `events` | `id`, `user_id`, `timestamp`, `type`, `external_id`, `schema_version` | `labels`, `description` |
| `subjects` | `id`, `user_id`, `kind`, `key`, `title` | `meta` |
| `category_trees` | `id`, `user_id`, `name`, `version`, `updated_at` | `tree` |
| `users` | `id` (`"default"` in the MVP), `timezone`, `created_at` | |

Rules:

- Timestamps as ISO 8601 text with offset; timezone `Australia/Sydney` from the Python config.
- The import deduplicates on the Clockify entry id. ADR 0001 names the columns `source` and `source_id`; ADR 0003 names one column `external_id`. One name must be chosen before the schema is written (open item, section 11).
- Adding a key: no migration. Renaming a key: one `UPDATE` over the rows, or expand then contract when the change must be gradual. `schema_version` is an integer set on every write.
- Readers accept the current version and the one before it. A `migrate` command converts old rows in batches and reports how many changed and how many remain.
- No semver inside the JSON (Frank first asked for it, then accepted the integer column with a support window).
- Table names above are proposals that follow the glossary; the April doc used `time_intervals`, `day_records`, `category_configs`, `import_sources`.

---

## 7. Architecture

### 7.1 Packages (ADR 0002)

```
apps/web/            Next.js: pages (Log, Stats), API routes, chat UI
packages/core/       entities, pure functions, use cases, ports; no I/O imports
packages/db/         SQLite adapter, migrations, migrate command
packages/clockify/   Clockify import adapter (read-only against Clockify)
packages/agent/      tool schemas and handlers, chat loop, Claude client
archive/python/      old code, moved with git mv, never imported
```

### 7.2 Ports (interfaces in `packages/core`, proposed names)

- `TimeEntryRepository`, `EventRepository`, `SubjectRepository`, `CategoryTreeRepository`
- `CurrentUser { getUserId(): string }`, returns `"default"` in the MVP
- `Clock { now(): Date }` for testable timer and day logic
- `Importer` for Clockify

### 7.3 Chat tools (from `topics/architecture/target_architecture.md` section "Agent Tool Design", renamed to the glossary)

Read tools: `find_gaps(start_date, end_date)`, `get_day_summary(date)`, `get_patterns(weekday, time_range)`, `list_known_types_and_labels()`, `get_week_overview(week_offset)`.

Write tools (confirm card first): `validate_entry`, `add_entry`, `add_event`, `start_timer`, `stop_timer`, and later `correct_entry`, `delete_entry` for entries the chat added.

Reliability rules: the LLM never generates facts; all date math in tools; pattern suggestions are asked, never asserted; one gap at a time; validation before every write; Frank confirms every write; "I don't remember" is a valid answer and the gap is skipped.

The running timer is a TimeEntry with no `end` yet, or a separate `running_activity` record. Not decided (section 11).

### 7.4 Claude client

Proposed: Anthropic API key in `.env.local`, model Sonnet, bare Messages API with tool use, no agent framework in the MVP (`target_architecture.md` section "AI Agent Framework Decision"). Not confirmed (Q7).

---

## 8. MVP UI, from the mock version 10

Source: `docs/design/ui-mock/`. Example data only. Frank's sketch came from Excalidraw; the mock went through four redraws on 2026-11-08.

### 8.1 Log page (`Main.dc.html`)

- Header: title and two nav links, Log and Stats.
- Timer bar across the top, like Clockify: a text input with the current activity (`work · project=cba`), "since 13:20", a running clock `00:42:15`, a red STOP button.
- Left, wide: the entry list for one day.
  - A date picker with previous and next day arrows (Frank: "need to be a date picker").
  - A summary line: wakeup time, logged hours of day length, coverage percent, gap count. A thin coverage bar with red segments for gaps.
  - Rows: time range, type in bold, label chips (`project=cba`), measure chips (`chapters 2`), a short note, duration on the right.
  - Gap rows: red dashed rows "gap · nothing logged" with the duration (Frank: "I need some gap indicator").
  - The list continues across days: a day divider, the previous day's last entries, the `bed` event, `night_sleep`, then the `wakeup` event and today (Frank: "should be able to scroll up or down to entries before or after this day, since sleep, getup may get different day").
  - A grey box under the list, drawn by Frank on the canvas. Its meaning is unknown (open item).
- Right, narrow: the chat.
  - User messages, a confirm card (`11:00–11:40 read · book=deep_work · chapters 2` with Add and Edit), a bot reply "Started work · project=cba at 13:20."
  - Input "What did you do?" and Send.
- Frank's feedback applied: chat moved from the wide left to the narrow right ("chat not need this [space]"); no charts on this page (Claude's view, not contradicted).

### 8.2 Stats page (`Stats.dc.html`)

- Header, same nav.
- Tabs: Time stat and Habits. Under Time stat: Daily, Weekly, Month; Weekly active in the mock, with the date range.
- Share of the week: pie with legend (hours and percent per category).
- Sleep per night: line chart, 7 nights.
- Hours per day: stacked bars per day, one color per category.
- Habits tab: not drawn.
- Frank has not commented on this page yet.

### 8.3 Artifact mechanics

- The artifact is one Design-type canvas; every publish adds a version to the same link. Claude republishes with `url` plus `root` set to the folder that holds `project/Main.dc.html`, `project/Stats.dc.html`, `project/canvas.json`. On a new machine, copy `docs/design/ui-mock/*` into a folder named `project/` under a scratch root, read the artifact first, then publish.
- Frank's own edits on the canvas (drawn shapes, boxes) are saved as a new version; Claude must read the live file and merge before publishing, or the publish is refused.
- Comments: a comment sent with "Send to Claude" wakes the session and posts an automatic text reply. That reply never changes the mock and has twice suggested things outside the MVP scope. For a change, Frank tells Claude in the chat. Claude reads threads with the ArtifactComments tool, answers in one or two lines, and resolves the thread after acting.
- An earlier test page for comments exists: https://claude.ai/artifact/QKwYfTefAFGN3H6sC5iaYV. Not needed.

---

## 9. Clarify (grill) status

Round 1 had eight questions. Outcome:

| Q | Topic | Outcome |
|---|---|---|
| Q1 | Source of truth | Accepted (a): SQLite, Clockify import only. ADR 0001 |
| Q2 | Code layout | Frank chose the monorepo and archiving Python, not the recommended single app. ADR 0002 |
| Q3 | Core data model | Accepted as base, then changed: mandatory `type`, `labels` key=value, `measures`, `description`, Subject, CategoryTree. `CONTEXT.md` |
| Q4 | Day definition | Accepted (a): biological day, status instead of rejection |
| Q5 | Stats page content | Proposed; the mock is the current answer; not confirmed |
| Q6 | Chat scope | Only "chat fills all fields" confirmed |
| Q7 | Claude access | Proposed API key and Sonnet; not confirmed |
| Q8 | Multi-user seams | Agreed |

Gate 1 (Frank confirms the shared understanding in a few lines) is not done.

---

## 10. Working agreements with Frank

These were learned in this project and live in Claude's local memory on the Mac, which does not travel. Repeated here.

- Less is more. Build and draw only what Frank asked or drew. Name an extra in one line; do not add it.
- In design discussions, one short spoken-English answer per question. No tables, rule lists or metaphors unless asked. Frank: "you speaking too much will distract my thoughts."
- A question is not an instruction. Answer, give one line of recommendation if useful, then stop until Frank says go.
- Any myclaude side task (complaint, rule edit, PR) runs in a background subagent, never inline in the main session.
- Big work: first reply is a plan gist of at most 5 lines, then wait for go.
- Commit or push only when Frank asks. No AI attribution in commits or PRs.
- Frank's global rules are in `~/.claude/rules/frank/` on the Mac and in `~/devel/myclaude`; they must be installed on the other machine with `node myclaude.js sync`.

---

## 11. Open items and risks

1. Grey box under the Log entry list: Frank drew it on 2026-11-08 and has not said what it is.
2. Q5, Q6, Q7 not confirmed; Gate 1 not done.
3. Column name for the import dedup key: `source` + `source_id` (ADR 0001) or `external_id` (ADR 0003). Choose one and fix the other ADR.
4. Running timer representation: open TimeEntry without `end`, or a separate record.
5. Day incompleteness reasons: not listed yet; start from the Python validators.
6. `CONTEXT.md` holds a "Current state" section (added 2026-11-14). The domain-modeling rule says `CONTEXT.md` is a glossary only. Suggest moving that section into this handoff and deleting it there.
7. `CLAUDE.md` is stale and must be rewritten when the monorepo exists.
8. Repo is public. `CLAUDE.md` and the docs carry personal activity categories and example data. Frank's call whether to make it private.
9. Four notebooks have uncommitted outputs (about 48,000 lines). Clear outputs before any commit, or discard the changes.
10. `myclaude sync` reports a CONFLICT on `skills/complaints/SKILL.md` (installed copy differs from the repo). Frank to run `node ~/devel/myclaude/myclaude.js diff --content`. Do not force.
11. `myclaude-open-items.md` line 25 (in `~/devel/myclaude`) says the lyubishchev remote once carried a GitHub token. On 2026-11-15 the remote URL is clean; whether that token was revoked is not verified.
12. The Ubuntu VM has an old copy of the repo (2025-08-17) and no sessions. Nothing to recover there.
13. Session alias "lyubishchev" for Claude Code sessions: offered, not created.

---

## 12. Exact next steps, in order

1. Frank answers: the grey box, Q5, Q6, Q7. Claude posts the Gate 1 summary in at most 10 lines; Frank confirms.
2. Write `docs/requirements/1_mvp_requirements.md`: the two pages, the chat-only input, the confirm card, the timer, the Day status, and the report statement "what I did and produced, not only how long". Fix the ADR 0001 and 0003 column name (item 3 above).
3. Move the Python code: `git mv lyubishchev tests time_report_notebook scripts requirements*.txt ... archive/python/`, keep the Python CI files with it, and make the old CI stop running on the root.
4. Scaffold the monorepo per ADR 0002: pnpm workspaces, `apps/web` (Next.js, TypeScript strict), `packages/core`, `packages/db`, `packages/clockify`, `packages/agent`, Vitest, ESLint with the core boundary rule. Rewrite `CLAUDE.md` as the root map: packages, commands, rules.
5. `packages/core`: TimeEntry, Event, Type and Label lists, Subject, CategoryTree, Day computation (wakeup to bed, gaps, coverage, status), write validation. Port the Python tests in `tests/unit/` as the spec.
6. `packages/db`: SQLite schema from section 6, migrations, repositories, `migrate` command.
7. `packages/clockify`: import with dedup, mapping of Clockify tags to `type`, `labels`, `measures`, `description`, and events (`event_type=` tags become Event types). Reference: `lyubishchev/clockify_fetcher/` and `CLAUDE.md` section "Clockify Integration Details".
8. `packages/agent` and the Log page: timer bar, entry list with gaps and date picker, chat with tools and confirm card.
9. Stats page: Weekly first (pie, sleep line, hours per day), then Daily and Month, then Habits.
10. Each step: run it end to end before calling it done; tests pass; Frank sees it in the browser.

---

## 13. Environment notes

- Clockify credentials for the import: `.dotenv/myenv` with `CLOCKIFY_USER_ID`, `CLOCKIFY_WORKSPACE_ID`, `CLOCKIFY_API_KEY` (from `CLAUDE.md`). Not in git.
- Planned Claude key: `.env.local` in `apps/web`, not committed. Model proposed: Sonnet.
- Node and pnpm versions: not chosen yet.
- Timezone: `Australia/Sydney`. Data starts 2023-03-12 (`lyubishchev/config`).
- Chrome DevTools MCP is used to screenshot Frank's Excalidraw tab; it needs Chrome open with remote debugging on the machine where Claude runs.
