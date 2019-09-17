# Settings

Settings are stored in the database for syncing between multiple devices.

## Fetch a user's settings

`GET /settings`

### Example Response

```json
{
  "id": "b6aff5e1-e777-4485-b932-b62a6905d062",
  "daily_reminder": {
    "enabled": true,
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

```javascript
{
  "daily_reminder": {
    "enabled": true, // Whether or not to send reminders to the user
    "hour": 22,
    "minute": 30
  }
}
```
