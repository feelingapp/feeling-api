# Responses

## Response Codes

| Code | Description           |
| ---- | --------------------- |
| 200  | Success               |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 405  | Method Not Allowed    |
| 500  | Internal Server Error |

## Errors

Responses that return `400` error codes also include a body of the following format:

```json
{
  "errors": [
    {
      "type": "wrong_password",
      "message": "the password for the account is incorrect"
    },
    {
      "type": "already_registered_email",
      "message": "the email is used by another account"
    }
  ]
}
```
