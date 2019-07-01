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


## Watson Assistant API
chatbot-api makes use of IBM`s watson api to create conversations. It uses natural language understanding, and integrated dialog tools to create conversation flows between serverless-registry-api and users.


# Development
The Chatbot API server can be run locally. Visit [DESIGN.md](DESIGN.md) to see all endpoints and corresponding responses.

Follow the steps in the [Database](#database), [Configuration](#configuration),
and [Run](#run) sections.

## Database
Start a local MongoDB server by running:

```
make db

```

## Configuration
For local development, create a `Wastson Assitant` instance in a IBM Cloud Catalog. The instance will be created in a `default` resource group.
Launch the Watson Assistant using dashboard and import training data available in https://github.com/knative-scout/chat-bot-api/tree/master/training  


Configuration is passed via environment variables.
- `BOTUSER_KEY` : API key assigned to the bot
- `WORKSPACE_ID` :Unique id given to the created skill
- `APP_DB_HOST` : Database host
- `APP_DB_NAME` : Database name
- `APP_DB_USER` : User for this database
- `APP_DB_PASSWORD` : Database user password

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

# Examples

## Search :

1. Search by selecting `searching apps` option

```
>>user: Hey

>>scout: Hi! I am Scout. I can help you with :
         - Searching apps
         - Deploy apps
         - Learn serverless

>>user: (<Selects seraching apps option>)

>>scout: What type of app?

>>user: serverless apps

>>scout: (<List of all serverless apps>)
         
```

2. Direct Search

``` 
>>user: get me serverless apps

>>scout: (<List of all serverless apps>)

```

## Deploy

1. Search by selecting `deploy apps` option with access to cluster

```
>>user: Hey

>>scout: Hi! I am Scout. I can help you with :
         - Searching apps
         - Deploy apps
         - Learn serverless

>>user: (<Selects deploy apps option>)

>>scout: What type of app?

>>user: serverless apps

>>scout: (<List of all serverless apps to deploy>)

>>user: (< Selects an app from list to deploy >)

>>scout: I remember the app you have selected. Please confirm that  you have knative installed on a cluster and have access to that cluster.

>>user: Yes

>>scout: Your app id is <App id>. 
        < Provides command to deploy app on cluster>
         
```

2. Direct Deploy cluster with access to cluster

```
>>user: Deploy serverless apps

>>scout: (<List of all serverless apps to deploy>)

>>user: (< Selects an app from list to deploy >)

>>scout: I remember the app you have selected. Please confirm that  you have knative installed on a cluster and have access to that cluster.

>>user: Yes

>>scout: Your app id is <App id>. 
        < Provides command to deploy app on cluster>
         
```
 
3. Deploy with no access to cluster

```

>>user: Deploy serverless apps

>>scout: (<List of all serverless apps to deploy>)

>>user: (< Selects an app from list to deploy >)

>>scout: I remember the app you have selected. Please confirm that  you have knative installed on a cluster and have access to that cluster.

>>user: No, I don`t have a cluster

>>scout: To learn how to get your own cluster with knative, visit https://docs.openshift.com/container-platform/3.3/getting_started/administrators.html. 
          Do you want to save this app to deploy later?

>>user: Yes (< User goes away and creates the cluster >)

>>user: Deploy saved app.

>>scout: Sure. Please confirm you have access to cluster.

>>user: yes

>>scout: Your app id is <App id>. 
        < Provides command to deploy app on cluster>
         
```
## Learn 

1. Ask questions by selecting `learn serverless` option

```
>>user: Hey

>>scout: Hi! I am Scout. I can help you with :
         - Searching apps
         - Deploy apps
         - Learn serverless

>>user: (<Selects learn serverless option>)

>>scout: What do you want to learn ?

>>user: What are serverless architectures?

>>scout: (< Text providing an explanation and link to the resource >)
         
```

2. Ask questions directly

``` 
>>user: What are serverless architectures?

>>scout: (< Text providing an explanation and link to the resource >)
         
```

## Start over

User can ask to `start over` at any point in conversation

```
>>user: Deploy serverless apps

>>scout: (<List of all serverless apps to deploy>)

>>user: (< Selects an app from list to deploy >)

>>scout: I remember the app you have selected. Please confirm that  you have knative installed on a cluster and have access to that cluster.

>>user: start over

>>scout: Hi! I am Scout. I can help you with :
         - Searching apps
         - Deploy apps
         - Learn serverless


```

## Quit

User can ask to `quit` at any point in conversation

```
>>user: Deploy serverless apps

>>scout: (<List of all serverless apps to deploy>)

>>user: (< Selects an app from list to deploy >)

>>scout: I remember the app you have selected. Please confirm that  you have knative installed on a cluster and have access to that cluster.

>>user: Forget it

>>scout: Okay. Action aborted.

```