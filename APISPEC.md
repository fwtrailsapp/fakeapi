# API SPEC v1

## POST /trails/api/1/login

Attempts login by authenticating username and password. For valid username/password combinations, the server returns an authorization token that is necessary for all subsequent API calls. The authorization token will be used both for authorization and for identification. See the overview section for how to embed it.

### Params

* email - string
* password - string

### Responses

* HTTP 200 - Logged in successfully
  * authtoken - string, a long hexadecimal string to identify this user’s requests
* HTTP 401 - Incorrect email/password

## POST /trails/api/1/account/create

This request creates a new account; it does not require an authtoken. You will likely want to immediately POST login after this request to receive an authtoken.

### Params

* email - string
* password - string
* dob - string, ISO 8601 date, nullable
* weight - float, pounds, nullable
* sex - string, "male" or "female", nullable
* height - float, inches, nullable

### Responses

* HTTP 200 - Account created successfully
* HTTP 401 - Email or password was rejected or already in use
