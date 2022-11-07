

## Active time entry

```json
{
    "id": "60c058bd0deb1f668d1649bc",
    "description": "lyubishchev",
    "tags": [
      {
        "id": "5e86fe02fbe9b56304197ee4",
        "name": "selfImproving",
        "workspaceId": "5e86fab7183a8475e0c7a757",
        "archived": false
      }
    ],
    "user": {
      "id": "5e86fab6183a8475e0c7a755",
      "email": "elitegoblinrb@gmail.com",
      "name": "Sun Frank",
      "memberships": [],
      "profilePicture": "https://img.clockify.me/no-user-image.png",
      "activeWorkspace": "5e86fab7183a8475e0c7a757",
      "defaultWorkspace": "5e86fab7183a8475e0c7a757",
      "settings": {
        "weekStart": "MONDAY",
        "timeZone": "Australia/Sydney",
        "timeFormat": "HOUR12",
        "dateFormat": "MM/DD/YYYY",
        "sendNewsletter": false,
        "weeklyUpdates": true,
        "longRunning": false,
        "timeTrackingManual": false,
        "summaryReportSettings": {
          "group": "TAG",
          "subgroup": "TIME_ENTRY"
        },
        "isCompactViewOn": false,
        "dashboardSelection": "ME",
        "dashboardViewType": "PROJECT",
        "dashboardPinToTop": false,
        "projectListCollapse": 50,
        "collapseAllProjectLists": false,
        "groupSimilarEntriesDisabled": false,
        "myStartOfDay": "09:00",
        "projectPickerTaskFilter": false
      },
      "status": "ACTIVE"
    },
```

## Finished

```json
 {
    "id": "60c0580e789c2030f4adb5a8",
    "description": "record",
    "tags": [
      {
      }
    ],
    "user": {
    },
    "billable": false,
    "task": null,
    "project": {
    },
    "timeInterval": {
    },
    "workspaceId": "5e86fab7183a8475e0c7a757",
    "hourlyRate": null,
    "userId": "5e86fab6183a8475e0c7a755",
    "customFieldValues": null,
    "projectId": "5f39f0ea803448349949e545",
    "isLocked": false
  },
```


## Timezone

> If provided, only time entries that started after the specified datetime will be returned. Datetime must be in ISO-8601 format (eg. "2019-04-16T05:15:32.998Z"). You send time according to your account's timezone (from Profile Settings) and get response with time in UTC.


https://clockify.me/developers-api


Users in different time zones: 
Clockify uses several time zones to record and display time values:

Time zone from your Profile Settings (when you record time in the web app)
Time zone from your device (when you record time in desktop/mobile app)
UTC (stored in the database)
Time zone from your Profile Settings (when displaying recorded time)

https://clockify.me/help/users/time-zones