# Ideas (icebox)

Speculative, uncommitted ideas. Absorbed from `docs/ideas.md` (kept untouched) plus the 2026-08-15 conversation. Maturity: [raw] → [exploring] → [ready-to-spec] → promoted / [rejected]. Promotion requires a feature spec + ADR and owner sign-off.

## Output measurement per project type — [exploring]

- Idea: measure output, not just time — pages read, notes/blogs written, lines of code — per project type; the mission quote "花了xx时间, 产出xx事情".
- Why valuable: the heart of the Lyubishchev method ("用产出倒逼输入"); turns time stats into productivity truth.
- Tensions: needs per-project-type output definitions and merging of same-project entries — real modeling work; competes with habit-rebuild focus (ADR-007).
- Dependencies: local storage (annotations carry output units — fits ADR-004 "keys, not columns").
- Open question to resolve first: which single project type gets measured first, and what is its one honest unit?

## Hierarchical project tree + epic links — [exploring]

- Idea: projects form a tree (math → LA / probability → reading), independent of time data; entries point to a leaf project; tree nodes can link to epics.
- Why valuable: enables Lyubishchev-style nested monthly breakdowns.
- Tensions: earlier requirement explicitly warned that forced hierarchy makes tags hard to change; per ADR-004 a project gets a table only when it gains identity.
- Dependencies: local storage; stable project IDs.
- Open question: is a flat project label enough for the first year of data?

## Agile / external tracker integration (zenhub, gitlab, GitHub) — [raw]

- Idea: link entries to tickets/epics; pull GitHub code activity ("贡献多少代码, 什么语言"); burndown/velocity views.
- Why valuable: more context per unit of time; progress tracking toward goals.
- Tensions: third-party dependency, exactly what local-first is moving away from; L3-adjacent scope.
- Open question: which single integration would Frank actually look at weekly?

## Commercialization: multi-user product, web/native UI — [raw]

- Idea: turn the personal tool into a product (auth, billing, mobile).
- Why valuable: long-term vision; the owner is "user and CEO".
- Tensions: directly conflicts with near-term habit-rebuild focus; all L3-deferred (ADR-006). Prerequisite evidence: the method must first demonstrably work for user #1.
- Open question: what proof (months of sustained habit + data) is required before spending anything here?

## Device sync — [raw]

- Idea: same data available across machines/devices.
- Tensions: single-device SQLite is the deliberate near-term choice; sync is where local-first designs get hard.
- Open question: is a simple backup/restore story enough until multi-device becomes a real pain?

## Timer UI app — [raw]

- Idea: a dedicated timer application (desktop/mobile) for start/stop/switch.
- Tensions: ADR-003 says CLI first, UI only when the CLI proves insufficient; phase 4 (React UI) partially covers this and also serves the owner's React upskilling goal.
- Open question: after phase 1, is the CLI's friction actually too high, measured by habit adherence?
