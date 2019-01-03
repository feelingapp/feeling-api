# Authentication

## Authorization

Generate an authorization code (you should create a code verifier and code challenge using a PKCE generator beforehand).

**Note:** As this is a GET request, all parameters should be sent as query parameters in the URL).

`GET /authorize`

| Parameter               | Type     | Description                                                   |
| ----------------------- | -------- | ------------------------------------------------------------- |
| `client_id`             | `string` | **Required**. The 3rd party sign in provider.                 |
| `response_type`         | `string` | **Required**. Will always be `code`.                          |
| `redirect_uri`          | `string` | **Required**. The callback location of the app to authorize.  |
| `code_challenge_method` | `string` | **Required**. The hash method used to generate the challenge. |
| `code_challenge`        | `string` | **Required**. The code challenge used for PKCE.               |

### Example Request

```json
{
  "client_id": "0oabygpxgk9lXaMgF0h7",
  "response_type": "code",
  "redirect_uri": "myapp://callback",
  "code_challenge_method": "S256",
  "code_challenge": "qjrzSW9gMiUgpUvqgEPE4_-8swvyCtfOVvg55o5S_es"
}
```

### Example Response

```json
{
  "authorization_code": "CKA9Utz2GkWlsrmnqehz"
}
```

## Getting an Access Token

Generate an access token from an authorization code or refresh token.

**Note:** As this is a GET request, all parameters should be sent as query parameters in the URL).

`GET /token`

| Parameter       | Type     | Description                                                                                                                |
| --------------- | -------- | -------------------------------------------------------------------------------------------------------------------------- |
| `grant_type`    | `string` | **Required**. Will always be either `authorization_code` or `refresh_token`.                                               |
| `redirect_uri`  | `string` | **Required**. The callback location of the app to authorize.                                                               |
| `code`          | `string` | **Required if `grant_type` is `authorization_code`.** The authorization code.                                              |
| `refresh_token` | `string` | **Required if `grant_type` is `refresh_token`.** The `refresh_token`.                                                      |
| `code_verifier` | `string` | **Required if `grant_type` is `authorization_code`.** The PKCE code verifier that your app generated before authorization. |

### Example Request (Authorization Code Grant Type)

```json
{
  "grant_type": "authorization_code",
  "redirect_uri": "myapp://callback",
  "code": "CKA9Utz2GkWlsrmnqehz",
  "code_verifier": "M25iVXpKU3puUjFaYWg3T1NDTDQtcW1ROUY5YXlwalNoc0hhakxifmZHag"
}
```

### Example Request (Refresh Token Grant Type)

```json
{
  "grant_type": "refresh_token",
  "redirect_uri": "myapp://callback",
  "token": "abOhb[...]Owvg"
}
```

### Example Response

```json
{
  "access_token": "eyJhb[...]Hozw",
  "expires_in": 3600,
  "id_token": "eyJhb[...]jvCw",
  "token_type": "Bearer"
}
```

## Using an Access Token

After authorization, all requests should include an `Authorization` header with an access token:

```json
{
  "Authorization": "Bearer ACCESS_TOKEN_HERE"
}
```
