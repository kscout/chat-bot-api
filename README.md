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
For local development, create a `Wastson Assitant` instance in a IBM Cloud Catalog. The instance will be created in a `default` resource group.
Launch the Watson Assistant using dashboard and import training data available in https://github.com/knative-scout/chat-bot-api/tree/master/training  


Configuration is passed via environment variables.
- `BOTUSER_KEY` : API key assigned to the bot
- `WORKSPACE_ID` :Unique id given to the created skill

You can create and inject your own training data / skill by using functions in https://github.com/knative-scout/chat-bot-api/tree/master/training/features


## Run
Start the server by running:

```
pip install -r requirements.txt
```

```
python app.py
```

# Deployment
