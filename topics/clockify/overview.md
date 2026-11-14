# Clockify Overview

## What is Clockify?
Clockify is a free time tracking app (https://clockify.me). It provides a web UI, desktop apps, and a REST API for tracking time entries with projects, tags, and descriptions.

## How This Project Uses Clockify

### Data Entry (Manual in Clockify UI)
The user manually tracks time in Clockify using:
- **Time entries**: Each has a start/end time, optional project, description, and tags
- **Tags**: Encode domain semantics (activities, events) in the tag name itself

### Tag Encoding Convention
Clockify tags are used as a key-value encoding mechanism:

| Tag Format | Meaning | Example |
|---|---|---|
| `key=value` | Label (key-value pair) | `event_type=wakeup`, `project=lyubishchev` |
| `key` (no `=`) | Tag (boolean flag) | `jog`, `meditation`, `cold` |

A single Clockify time entry can encode:
1. **A TimeInterval** (always) - the time period with activity labels
2. **An Event** (optionally) - if `event_type=<type>` tag is present

### Event Types Encoded in Tags
| Clockify Tag | Internal Event | Timestamp Used |
|---|---|---|
| `event_type=wakeup` | Wakeup event | `timeInterval.start` |
| `event_type=getup` | Getup event | `timeInterval.start` |
| `event_type=bed` | Bed event | `timeInterval.end` |
| `event_type=partner_period` | Partner period | `timeInterval.start` |
| `event_type=unwell` | Illness start | `timeInterval.start` |
| `event_type=recover_unwell` | Recovery | `timeInterval.start` |

### Activity Tags (become labels)
Activities are tracked as plain tags (no `=`):
- `jog`, `swim`, `anaerobic` (exercise)
- `meditation`, `walk` (calm)
- `work`, `job` (work)
- `lyubishchev`, `oj`, `software`, `audible`, `reading` (self-improving)
- `cook`, `self_routine`, `housework`, `meal` (routine)
- `nap` (sleep)
- etc.

### API Endpoint Used
```
GET https://api.clockify.me/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries
  ?start=<ISO>&end=<ISO>&page-size=50&page=<N>&hydrated=true
```

- `hydrated=true` is essential - it returns full tag objects with names (not just IDs)
- Results come in descending order (newest first) - reversed in code
- Pagination: page size 50, auto-increments until empty response

### Authentication
- `X-Api-Key` header with API key from Clockify profile settings
- Env vars: `CLOCKIFY_API_KEY`, `CLOCKIFY_WORKSPACE_ID`, `CLOCKIFY_USER_ID`

## Files in This Folder
- `overview.md` - This file
- `clockify_api_reference.md` - Structured API reference for key endpoints
- `clockify_api_full_text.txt` - Complete API docs text dump from https://docs.clockify.me/
