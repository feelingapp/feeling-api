# Settings

Settings are stored in the database for syncing between multiple devices.

## Fetch a user's settings

`GET /settings`

### Example Response

```json
{
  "daily_reminder": {
    "enabled": True,
    "hour": 20,
    "minute": 0
  }
}
```

## Update a user's settings

`POST /settings`

| Parameter        | Type     | Description                                                           |
| ---------------- | -------- | --------------------------------------------------------------------- |
| `daily_reminder` | `object` | Details on sending reminders to the user to log how they are feeling. |

### Example Request

```json
{
  "daily_reminder": {
    "enabled": True, // Whether or not to send reminders to the user
    "hour": 22,
    "minute": 30
  }
}
```
