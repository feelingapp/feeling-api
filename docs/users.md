# Users

## Get the Current User

Gets the current user using the user ID found in the access token

`GET /user/me`

### Example Response

```json
{
  "id": "b6aff5e1-e777-4485-b932-b62a6905d062",
  "first_name": "Michael",
  "last_name": "Lee",
  "email": "michael_lee@example.com",
  "verified": true,
  "created_at": "2019-01-04T00:02:51",
  "updated_at": "2019-01-04T00:02:51"
}
```

## Check if a User Exists

Searches if a user exists given an email

`GET /user/exists`

**Note:** As this is a GET request, all parameters should be sent as query parameters in the URL.

| Parameter | Type     | Description                                               |
| --------- | -------- | --------------------------------------------------------- |
| `email`   | `string` | **Required**. The email needed to check if a user exists. |
