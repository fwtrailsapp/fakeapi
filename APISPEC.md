# API Overview

## POST Requests

For POST, all params are sent as a JSON object in the body of the request. These headers should contain `Content-Type: application/json`.

## Auth Token

After **POST login**, the server will send back an auth token. Clients should send this token when making ANY future requests so the server knows with which user it’s dealing. The headers for all other requests should contain it like `Trails-Api-Key: ab83920bdc826bdaf`

## Auth Considerations

The authorization tokens will most likely (depending on our implementation) come with some sort of expiration time. Once the tokens are expired, new tokens will need to be requested by the application. The solution to this problem is to save the username/password combination that the user logged in with initially on the device, and simply - in the background - use those credentials to re-request new auth tokens by sending new **POST login** requests. 

Users will have an username/password auto-fill option for the login screen (e.g. a ‘Remember Me’ checkbox). If this option is selected, the username/password combination will be permanently stored on the device such that the username and password fields will be filled automatically when the screen is displayed. If the box is unchecked, the username/password combination will be deleted from the device once the application is closed.

## HTTP Status Codes

* HTTP 200: The request has completed successfully.
* HTTP 400: The request is invalid. The format of the sent data is invalid or doesn’t include all required fields.
* HTTP 401: The auth token was not included in the request headers. For POST login, The username and password are incorrect.
* HTTP 419: The auth token is no longer (or never was) valid and should be re-obtained before making any more requests.

## Date Format

All absolute dates are sent in [ISO 8601][1] format. This is a standard which has support from all of our platforms.

## Nullable

If a request parameter has "nullable" in the documentation, the value can be set to null based on the context of the request. The keys should still be included, but the values are free to be set to null. And I mean actually null, not a string with the characters "null". See the [JSON spec][2] for more information on that. An example of nullable is in **POST register**, which doesn't require a weight or a height, among others.

  [1]: https://en.wikipedia.org/wiki/ISO_8601
  [2]: http://www.json.org/

## Data Types

* `ExerciseType` can be `bike` or `run` or `walk`.
* `LineString` is a string where a point is float lat and float long, separated by a comma, and each point is separated with by a space. Example: `20.3323,70.4531 21.3323,71.4531 22.3323,72.4531`

# API SPEC v1

## POST /trails/api/1/login

Attempts login by authenticating username and password. For valid username/password combinations, the server returns an authorization token that is necessary for all subsequent API calls. The authorization token will be used both for authorization and for identification. See the overview section for how to include it.

### Params

* username - string
* password - string

### Responses

* HTTP 200 - Logged in successfully
  * authtoken - string, a long hexadecimal string to identify this user’s requests
* HTTP 401 - Incorrect username/password

## POST /trails/api/1/account/create

This request creates a new account; it does not require an authtoken. You will likely want to immediately POST login after this request to receive an authtoken.

### Params

* username - string
* password - string
* dob - int, birth year, nullable
* weight - float, pounds, nullable
* sex - string, "male" or "female", nullable
* height - float, inches, nullable

### Responses

* HTTP 200 - Account created successfully
* HTTP 401 - Username or password was rejected or already in use

## GET /trails/api/1/account

Requests the account information of the user. The user's identification is stored within **authtoken**.

### Responses

* HTTP 200
  * dob - string, ISO 8601 date, nullable
  * weight - float, pounds, nullable
  * sex - string, "male" or "female", nullable
  * height - float, inches, nullable

## POST /trails/api/1/account/edit

Modifies the specified fields of the user’s account.

### Parameters

* dob - string, ISO 8601 date, nullable
* weight - float, pounds, nullable
* sex - string, "male" or "female", nullable
* height - float, inches, nullable

### Response

* HTTP 200

## POST /trails/api/1/activity

Store a new activity, after it has been completed.

### Parameters

* time_started - string, ISO 8601 date
* time_ended - string, ISO 8601 date
* mileage - float
* calories_burned - float
* exercise_type - string, an ExcerciseType datatype
* path - array of linestrings, because an activity can be paused

### Response

* HTTP 200

## GET /trails/api/1/activity

Returns all of the activities for the current user. Does not include paths.

### Response

* HTTP 200
  * array:
    * time_started - string, ISO 8601 date
    * time_ended - string, ISO 8601 date
    * mileage - float
    * calories_burned - float
    * exercise_type - string, an ExcerciseType datatype

## GET /trails/api/1/achievement

Returns all of the achievements. The earned date for an achievement will be “null” if the current user has not earned it.

### Response

* HTTP 200
  * array:
    * id - **TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO**
    * description - string
    * date_earned - ISO 8601 date, null if not earned

## GET /trails/api/1/statistics

Returns the aggregate of all of the activities for the user.

### Response

* HTTP 200
  * account_created_at - ISO 8601 date, time the user opened the account
  * total_duration - [ISO 8601 duration][1], amount of time user has spent in activities
  * total_distance - float, in miles, distance traveled in activities
  * total_calories - float, calories burned in activities
  * total_achievements - **TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO**

  [1]: https://en.wikipedia.org/wiki/ISO_8601#Durations

## GET /trails/api/1/statistics/{exercise_type}

Returns the aggregate of all the activities for the user for the specified exercise type, where
"exercise_type" is one of the possible exercise types (see overview section).

### Response

* HTTP 200
  * total_duration - [ISO 8601 duration][3], amount of time user has spent in activities of this type
  * total_distance - float, in miles, distance traveled in activities of this type
  * total_calories - float, calories burned in activities of this type
