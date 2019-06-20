# OAuth2.0 Description


app - feeling

authorisation server - auth.feeling

api - api.feeling


## Step 1
User wants to access app which needs API. 
feeling generates a code challenge
App opens up browser and makes
a request (containing a return POST link)
to the authorisation server

`GET /authorize`

| Parameter               | Type     | Description                                                   |
| ----------------------- | -------- | -------------------------------------------------------------                              |
| `client_id`             | `string` | to begin with only the feeling app will have a client ID                                   |
| `response_type`         | `string` | Will always be `code` to specify authorisation code                                        |
| `redirect_uri`          | `string` | Where the authcode will be sent to and where the client is redirected to                   |
| `code_challenge_method` | `string` | Can use (S256) SHA256                                         |
| `code_challenge`        | `string` | The code challenge used for PKCE.                             |
| `state`                 | `string` | Used to verify the correct callback                           |



## Step 2
User enters login and password into
browser and it's verified by the 
authorisation server

Once verified it inserts an 
authorisation code into the API 
database and sends the user back
to the app by redirecting the browser
back to the app with the authcode as
a parameter


Request sent by browser to api.feeling

| Parameter               | Type     | Description                   |
| ----------------------- | -------- | ------------------------------|
| `username`              | `string` | users entered username        |
| `password`              | `string` | users entered password        |


Redirect parameters received from api.feeling

| Parameter               | Type     | Description                   |
| ----------------------- | -------- | ------------------------------|
| `authorisation_code`    | `string` | authcode from server          |
| `state`                 | `string` | the state string you sent over earlier (for verification)|





## Step 3
the app can now get an access token
from the API using the authcode.

The authcode is sent back from 
the app to the server in a GET request
and the server will check the code
and send back a token which can be used
to make API requests.

Request from app to the API

`GET /token`


| Parameter       | Type     | Description                                                                                                                |
| --------------- | -------- | -------------------------------------------------------------------------------------------------------------------------- |
| `grant_type`    | `string` | **Required**. Will always be either `authorization_code` or `refresh_token`.                                               |
| `redirect_uri`  | `string` | **Required**. The callback location of the app to authorize.                                                               |
| `code`          | `string` | **Required if `grant_type` is `authorization_code`.** The authorization code.                                              |
| `refresh_token` | `string` | **Required if `grant_type` is `refresh_token`.** The `refresh_token`.                                                      |
| `code_verifier` | `string` | **Required if `grant_type` is `authorization_code`.** The PKCE code verifier that your app generated before authorization. |

Response from the API

| Parameter       | Type     | Description                                                                                                                |
| --------------- | -------- | -------------------------------------------------------------------------------------------------------------------------- |
| `token`         | `string` |  access token                                        |
| `token_life`    | `Integer`|  how long the token is valid for                 |
| `refresh_token` | `string` |  refresh token                                      |
|`refresh_token_life`| `Integer`| how long the refresh token will last
