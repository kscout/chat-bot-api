# chat-bot-api
API which manages user conversation with virtual assistant


# Table Of Contents
- [Overview](#overview)
- [Development](#development)
- [Deployment](#deployment)

# Overview
HTTP RESTful API.

Requests pass data via JSON encoded bodies except for in GET requests where data will be passed via URL and query parameters.

Responses will always return JSON.

A user can make use of chatbot to fulfill three major purposes:
- <b>Learn :</b> Users can ask chatbot questions regarding serverless, knative, openshift and related queries.
- <b>Search :</b> Users can search for apps on https://www.kscout.io platform using chatbot
- <b>Deploy :</b> Users can ask chatbot to deploy apps that are available on the platform.

## Watson Assistant API
chatbot-api makes use of IBM`s watson api to create conversations. It uses natural language understanding, and integrated dialog tools to create conversation flows between serverless-registry-api and users.


# Development
The Chatbot API server can be run locally.  

Follow the steps in the [Database](#database), [Configuration](#configuration),
and [Run](#run) sections.

## Database
Start a local MongoDB server by running:



## Configuration
For local development, create a 


Configuration is passed via environment variables.



## Run
Start the server by running:


# Deployment
## Kubernetes
1. Set secrets
  - Create copy of `deploy/secrets.ex.yaml` named `deploy/secrets.yaml`
  - Replace the placeholder values with the correct base64 encoded values
2. Deploy
   - Deploy the database:
     ```
	 ./deploy/deploy.sh up db
	 ```
   - Deploy the app API server:
     ```
	 ./deploy/deploy.sh up app
	 ```

## Temporary Open Shift
The `tmpk` script wraps `kubectl` with the required arguments to connect to the
48 hour Open Shift clusters.

Set the `TMPK_TOKEN` and `TMPK_N` environment variables. See the `tmpk` file 
for details about what to set these environment variables to.

Use the `tmpk` script as if it was `kubectl`:

```
./tmpk get all
```

## GitHub
### Webhook
A webhook should exist for the
[app-repository](https://github.com/knative-scout/app-repository/settings/hooks/new).  
This webhook should send pull request events to the app pull request 
webhook endpoint.

### API Token
Generate an API token which has repository read access only.  
Provide to application via `APP_GH_TOKEN` environment variable.
