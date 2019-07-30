# Accounts

## Check if an Account Exists

An account is created if one does not exist.

`GET /account/exists`

**Note:** As this is a GET request, all parameters should be sent as query parameters in the URL.

| Parameter | Type     | Description                                                   |
| --------- | -------- | ------------------------------------------------------------- |
| `email`   | `string` | **Required**. The email needed to check if an account exists. |
