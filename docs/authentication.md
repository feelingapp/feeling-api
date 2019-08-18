# Authentication

## Authorization

Generate an authorization code (you should create a code verifier and code challenge using a PKCE generator beforehand).

**Note:** As this is a GET request, all parameters should be sent as query parameters in the URL. Furthermore, this should not be accessed as an API request. Redirect the user to this URL in their browser, so they can sign in.

`/authorize`

| Parameter               | Type     | Description                                                   |
| ----------------------- | -------- | ------------------------------------------------------------- |
| `client_id`             | `string` | **Required**. The 3rd party sign in provider.                 |
| `response_type`         | `string` | **Required**. Will always be `code`.                          |
| `redirect_uri`          | `string` | **Required**. The callback location of the app to authorize.  |
| `code_challenge_method` | `string` | **Required**. The hash method used to generate the challenge. |
| `code_challenge`        | `string` | **Required**. The code challenge used for PKCE.               |
| `state`                 | `string` | **Required**. A random string used to prevent CSRF attacks.   |

### Example Request

```json
{
  "client_id": "0oabygpxgk9lXaMgF0h7",
  "response_type": "code",
  "redirect_uri": "myapp://callback",
  "code_challenge_method": "S256",
  "code_challenge": "qjrzSW9gMiUgpUvqgEPE4_-8swvyCtfOVvg55o5S_es",
  "state": "ahg84hek2n"
}
```

### Example Response

```json
{
  "authorization_code": "CKA9Utz2GkWlsrmnqehz",
  "state": "ahg84hek2n"
}
```

## Sign In

Used internally by [feeling-website](https://github.com/pavsidhu/feeling-website) to let users sign in.

`POST /sign-in`

| Parameter               | Type     | Description                                                              |
| ----------------------- | -------- | ------------------------------------------------------------------------ |
| `client_id`             | `string` | **Required**. The 3rd party sign in provider.                            |
| `response_type`         | `string` | **Required**. Will always be `code`.                                     |
| `redirect_uri`          | `string` | **Required**. The callback location of the app to authorize.             |
| `code_challenge_method` | `string` | **Required**. The hash method used to generate the challenge.            |
| `code_challenge`        | `string` | **Required**. The code challenge used for PKCE.                          |
| `state`                 | `string` | **Required**. A 10 character length string used to prevent CSRF attacks. |
| `email`                 | `string` | **Required**. The user's email for their account.                        |
| `password`              | `string` | **Required**. The user's password for their account.                     |

### Example Request

```json
{
  "client_id": "0oabygpxgk9lXaMgF0h7",
  "response_type": "code",
  "redirect_uri": "myapp://callback",
  "code_challenge_method": "SHA256",
  "code_challenge": "qjrzSW9gMiUgpUvqgEPE4_-8swvyCtfOVvg55o5S_es",
  "state": "ahg84hek2n",
  "email": "michael_lee@gmail.com",
  "password": "foobar"
}
```

### Example Response

```json
{
  "authorization_code": "CKA9Utz2GkWlsrmnqehz",
  "expires_in": 300,
  "state": "ahg84hek2n"
}
```

## Register

`POST /register`

| Parameter               | Type     | Description                                                              |
| ----------------------- | -------- | ------------------------------------------------------------------------ |
| `client_id`             | `string` | **Required**. The 3rd party sign in provider.                            |
| `response_type`         | `string` | **Required**. Will always be `code`.                                     |
| `redirect_uri`          | `string` | **Required**. The callback location of the app to authorize.             |
| `code_challenge_method` | `string` | **Required**. The hash method used to generate the challenge.            |
| `code_challenge`        | `string` | **Required**. The code challenge used for PKCE.                          |
| `state`                 | `string` | **Required**. A 10 character length string used to prevent CSRF attacks. |
| `email`                 | `string` | **Required**. The user's email for their account.                        |
| `password`              | `string` | **Required**. The user's password for their account.                     |
| `first_name`            | `string` | **Required**. The user's first name.                                     |
| `last_name`             | `string` | **Required**. The user's last name.                                      |

### Example Request

```json
{
  "client_id": "0oabygpxgk9lXaMgF0h7",
  "response_type": "code",
  "redirect_uri": "myapp://callback",
  "code_challenge_method": "S256",
  "code_challenge": "qjrzSW9gMiUgpUvqgEPE4_-8swvyCtfOVvg55o5S_es",
  "state": "ahg84hek2n",
  "email": "michael_lee@gmail.com",
  "password": "foobar",
  "first_name": "Michael",
  "last_name": "Lee"
}
```

### Example Response

```json
{
  "authorization_code": "CKA9Utz2GkWlsrmnqehz",
  "expires_in": 300,
  "state": "ahg84hek2n"
}
```

Used internally by [feeling-website](https://github.com/pavsidhu/feeling-website) to let users register a new account.

## Getting an Access/Refresh Token

Generate an access token from an authorization code or refresh token.

**Note:** As this is a GET request, all parameters should be sent as query parameters in the URL).

`GET /token`

| Parameter       | Type     | Description                                                                                                                |
| --------------- | -------- | -------------------------------------------------------------------------------------------------------------------------- |
| `grant_type`    | `string` | **Required**. Will always be either `authorization_code` or `refresh_token`.                                               |
| `code`          | `string` | **Required if `grant_type` is `authorization_code`.** The authorization code.                                              |
| `refresh_token` | `string` | **Required if `grant_type` is `refresh_token`.** The `refresh_token`.                                                      |
| `code_verifier` | `string` | **Required if `grant_type` is `authorization_code`.** The PKCE code verifier that your app generated before authorization. |
| `state`         | `string` | **Required**. A 10 character length string used to prevent CSRF attacks.                                                   |

### Example Request (Authorization Code Grant Type)

```json
{
  "grant_type": "authorization_code",
  "client_id": "0oabygpxgk9lXaMgF0h7",
  "code": "CKA9Utz2GkWlsrmnqehz",
  "code_verifier": "M25iVXpKU3puUjFaYWg3T1NDTDQtcW1ROUY5YXlwalNoc0hhakxifmZHag",
  "state": "ahg84hek2n"
}
```

### Example Request (Refresh Token Grant Type)

```json
{
  "grant_type": "refresh_token",
  "refresh_token": "abOhb[...]Owvg",
  "state": "ahg84hek2n"
}
```

### Example Response

```json
{
  "access_token": "eyJhb[...]Hozw",
  "expires_in": 3600,
  "token_type": "Bearer",
  "refresh_token": "abOhb[...]Owvg",
  "state": "ahg84hek2n"
}
```

## Using an Access Token

After authorization, all requests should include an `Authorization` header with an access token:

```json
Authorization: Bearer ACCESS_TOKEN_HERE
```
