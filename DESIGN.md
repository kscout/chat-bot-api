# Design
API design.

# Table Of Contents
- [Overview](#overview)
- [Data Model](#data-model)
- [Endpoints](#endpoints)
  - [App Endpoints](#app-endpoints)
    - [Send Messages](#send-messages)
	- [New App Upload](#new-app-upload)
  - [Meta Endpoints](#meta-endpoints)
	- [Health Check](#health-check)

# Overview
HTTP RESTful API.  

Requests pass data via JSON encoded bodies except for in GET requests where data
will be passed via URL and query parameters.

Responses will always return JSON.

# Data Model
## Context Model
`contexts` collection.


Schema:

- `user_id` (String)
- `context` (JSON)


# Endpoints

The endpoints do not require authentication.  

Endpoints which specify a response of `None` will return the 
JSON: `{"ok": true}`.

## Chatbot Endpoints
### Send Messages
`POST /messages`

Send Messages to chatbot

If no text is provided , it sends Empty Message error

Request:

- `user` (String): Unique user id
- `text` (List[String]): Message sent by the user

Response:

- `message_resp` (Json)

### New App Upload
`POST /newapp`

Stores meta data of new app to send it to watson for training

Request:

- `apps` ([App Model])  New app submitted to the hub

Response:

- `success Message` (JsonString)

### Get Session id
`GET /session`

Unique session id for users.

Request:

- None

Response:

- `session_id` (Json)

## Meta Endpoints
### Health Check
`GET /health`

Used to determine if server is operating fully.

Request: None

Response: None

