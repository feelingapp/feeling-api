# Users

## Check if a User Exists

Searches if a user exists given an email

`GET /user/exists`

**Note:** As this is a GET request, all parameters should be sent as query parameters in the URL.

| Parameter | Type     | Description                                               |
| --------- | -------- | --------------------------------------------------------- |
| `email`   | `string` | **Required**. The email needed to check if a user exists. |
