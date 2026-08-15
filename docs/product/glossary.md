# Glossary

- **Time interval**: a recorded span of time with a start, a duration, and labels/tags describing what it was. The atomic unit of the system.
- **Event**: a point-in-time record with no duration (e.g. getup, bed, a happiness rating).
- **Day**: the reporting unit, bounded by the getup event and the bed event — not by calendar midnight. Sleep credited to a day = the previous night plus daytime naps.
- **Label / annotation**: key-value metadata on an interval or event. Labels are for filtering; annotations carry richer values (e.g. output units). A key-only label acts as a **tag**.
- **Type**: an exclusive label — each interval has exactly one type (self-improvement, work, routine, exercise, relax, distracted, ...).
- **Project**: what a unit of work belongs to; the thing whose output is worth measuring. Corresponds to an epic in kanban terms.
- **Effective time**: time genuinely spent on self-improvement/core work, in Lyubishchev's sense (his ceiling: roughly 5 hours/day).
- **Habit**: a scored recurring behavior derived from the data (e.g. getup time vs target; earlier = higher score).
- **Storage seam**: the data-access boundary through which reports/habits consume data, allowing the storage backend to be swapped (owner's term: "TimeIntervalFetcher").
- **Critical path**: the owner's phrase for committed scope — "log a day, query a week".
- **Task-switch primitive**: one action (`lyu switch`) that closes the current interval and opens the next.
- **Provenance**: a record of where a data row came from (Clockify import vs natively logged).
