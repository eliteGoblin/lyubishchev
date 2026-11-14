# Clockify API Reference (Extracted from https://docs.clockify.me/)

## General

- **Base URL**: `https://api.clockify.me/api/v1`
- **Auth**: `X-Api-Key` header or `X-Addon-Token` header
- **Rate limit**: 50 requests/second (per addon per workspace, using X-Addon-Token)
- **Pagination**: `page` (1-indexed, default 1), `pageSize`/`page-size` (default 50). Response includes `Last-Page` header (`true`/`false`)
- **Regional prefixes**: EU=`euc1`, USA=`use2`, UK=`euw2`, AU=`apse2`

## Time Entry Endpoints

### GET /v1/workspaces/{workspaceId}/user/{userId}/time-entries
Get time entries for a user on a workspace.

**Path Parameters:**
- `workspaceId` (required): Workspace identifier
- `userId` (required): User identifier

**Query Parameters:**
- `description` (string): Search by description keywords
- `start` (string): Start date `yyyy-MM-ddThh:mm:ssZ`
- `end` (string): End date `yyyy-MM-ddThh:mm:ssZ`
- `project` (string): Filter by project ID
- `task` (string): Filter by task ID
- `tags` (array of strings): Filter by tag IDs
- `project-required` (boolean): Only entries with a project
- `task-required` (boolean): Only entries with a task
- `hydrated` (boolean, default false): Include additional info (project/tag details)
- `page` (integer, default 1): Page number
- `page-size` (integer, default 50): Page size
- `in-progress` (boolean): Filter only in-progress entries
- `get-week-before` (string): Filter within week before given datetime

**Response (200):**
```json
[
  {
    "billable": true,
    "costRate": { "amount": 10500, "currency": "USD" },
    "customFieldValues": [
      {
        "customFieldId": "...",
        "name": "TIN",
        "timeEntryId": "...",
        "type": "WORKSPACE",
        "value": "..."
      }
    ],
    "description": "This is a sample time entry description.",
    "hourlyRate": { "amount": 10500, "currency": "USD" },
    "id": "64c777ddd3fcab07cfbb210c",
    "isLocked": true,
    "kioskId": "94c777ddd3fcab07cfbb210d",
    "projectId": "25b687e29ae1f428e7ebe123",
    "tagIds": ["321r77ddd3fcab07cfbb567y", "44x777ddd3fcab07cfbb88f"],
    "taskId": "54m377ddd3fcab07cfbb432w",
    "timeInterval": {
      "duration": "8000",
      "end": "2021-01-01T00:00:00Z",
      "start": "2020-01-01T00:00:00Z"
    },
    "type": "BREAK",
    "userId": "5a0ab5acb07987125438b60f",
    "workspaceId": "64a687e29ae1f428e7ebe303"
  }
]
```

**Notes:**
- When `hydrated=true`, response includes full `tags` array (with `id`, `name`, `workspaceId`) and `project` object instead of just IDs
- Results are returned in **descending** order (newest first)
- `timeInterval.end` is `null` for currently running entries

### POST /v1/workspaces/{workspaceId}/time-entries
Add a new time entry.

**Request Body:**
```json
{
  "billable": true,
  "description": "Description text",
  "end": "2021-01-01T00:00:00Z",
  "projectId": "25b687e29ae1f428e7ebe123",
  "start": "2020-01-01T00:00:00Z",
  "tagIds": ["tag-id-1", "tag-id-2"],
  "taskId": "54m377ddd3fcab07cfbb432w",
  "type": "REGULAR"
}
```

**Fields:**
- `billable` (boolean)
- `description` (string, max 3000 chars)
- `end` (string, date-time, `yyyy-MM-ddThh:mm:ssZ`)
- `projectId` (string)
- `start` (string, date-time, `yyyy-MM-ddThh:mm:ssZ`)
- `tagIds` (array of strings)
- `taskId` (string)
- `type` (enum: `REGULAR`, `BREAK`)
- `customAttributes` (array, 0-10 items)
- `customFields` (array, 0-50 items)

### POST /v1/workspaces/{workspaceId}/user/{userId}/time-entries
Add a new time entry for another user on workspace.

Same body as above.

### PUT /v1/workspaces/{workspaceId}/time-entries/{id}
Update time entry on a workspace.

### DELETE /v1/workspaces/{workspaceId}/time-entries/{id}
Delete a time entry.

### PATCH /v1/workspaces/{workspaceId}/user/{userId}/time-entries
Stop a currently running timer.

**Request Body:**
```json
{
  "end": "2021-01-01T00:00:00Z"
}
```

### GET /v1/workspaces/{workspaceId}/time-entries/{id}
Get a specific time entry.

**Query:** `hydrated` (boolean, default false)

### GET /v1/workspaces/{workspaceId}/time-entries/status/in-progress
Get all in-progress time entries on a workspace.

### PUT Bulk edit time entries
### POST Duplicate a time entry

## Tag Endpoints

### GET /v1/workspaces/{workspaceId}/tags
Find tags on a workspace.

**Query Parameters:**
- `name` (string): Filter by tag name
- `strict-name-search` (boolean): Exact match vs contains
- `excluded-ids` (string): Exclude specific tag IDs
- `sort-column` (enum: `ID`, `NAME`)
- `sort-order` (enum: `ASCENDING`, `DESCENDING`)
- `page` (integer, default 1)
- `page-size` (integer, default 50)
- `archived` (boolean): Filter archived status

**Response (200):**
```json
[
  {
    "archived": true,
    "id": "21s687e29ae1f428e7ebe404",
    "name": "Sprint1",
    "workspaceId": "64a687e29ae1f428e7ebe303"
  }
]
```

### POST /v1/workspaces/{workspaceId}/tags
Add a new tag.

**Request Body:**
```json
{ "name": "Sprint1" }
```

### DELETE /v1/workspaces/{workspaceId}/tags/{id}
Delete a tag.

### GET /v1/workspaces/{workspaceId}/tags/{id}
Get a tag by ID.

### PUT /v1/workspaces/{workspaceId}/tags/{id}
Update a tag.

**Request Body:**
```json
{ "archived": true, "name": "Sprint1" }
```

## User Endpoints

### GET /v1/user
Get currently logged-in user's info.

**Query:** `include-memberships` (boolean)

### GET /v1/workspaces/{workspaceId}/member-profile/{userId}
Get a member's profile.

### GET /v1/workspaces/{workspaceId}/users
Find all users on a workspace.

**Query Parameters:** `email`, `project-id`, `status`, `name`, `sort-column`, `sort-order`, `page`, `page-size`, `memberships`, `include-roles`

## Workspace Endpoints

### GET /v1/workspaces
Get all my workspaces.

### GET /v1/workspaces/{workspaceId}
Get workspace info (not shown, but implied from structure).

## Project Endpoints

### GET /v1/workspaces/{workspaceId}/projects
Find projects on a workspace (implied from API structure).

## Reports API (separate base URL)

Base URL: `https://reports.api.clockify.me/v1`

### POST /v1/workspaces/{workspaceId}/reports/detailed
Generate a detailed report.

### POST /v1/workspaces/{workspaceId}/reports/summary
Generate a summary report.

### POST /v1/workspaces/{workspaceId}/reports/weekly
Generate a weekly report.

## Key Notes for This Project

1. **Only the GET time-entries endpoint is currently used** by `ClockifyFetcher`
2. **`hydrated=true` is required** to get full tag names (not just IDs) - the project parses tag names to extract labels and event types
3. **Results come in descending order** - the code reverses them to ascending
4. **Timestamps use Z suffix** format: `yyyy-MM-ddThh:mm:ssZ`
5. **Tags encode domain semantics**: `event_type=wakeup`, `jog`, `project=work` etc. are all Clockify tags
6. **A single time entry can represent both a TimeInterval and an Event** when it has event-type tags
