from controllers import search, learn
from config import config
from config.skeleton import CurrentConversation
import os
import json
import jsonpickle
from pymongo import MongoClient
from training.features.entity import Entity
from controllers import  deploy
# MongoDB is not fork() safe, thus need to create a new instance for every child process in order to stop deadlock.
# see MongoDB FAQ for more information
# Connecting to MondoDB
client = MongoClient(config.db_config["DB_HOST"], config.db_config["DB_PORT"], username=config.db_config["DB_USER"],
                     password=config.db_config["DB_PASSWORD"], connect=False)  # Connection to MongoDB
database = config.db_config["DB_NAME"]
currentConversation = config.db_config["CURRENT"]
db = client[database][currentConversation]


def identify_actions(response: json, message: str) -> str:
    try:
        if 'actions' in response['output'] and response['output']['actions'][0]['type'] == 'client':
            if 'search' == response['output']['actions'][0]['name']:
                return search.search_apps(message)
            if 'deploy' == response['output']['actions'][0]['name']:
                return deploy.deploy_app(response['context']['app_id'])
    except Exception as e:
        status = {"Exception in identifying actions": str(e)}
        raise Exception(status)


def identify_generic_output(response: json) -> str:
    try:
        if response['output']['generic']:
            if response['output']['generic'][0]['response_type'] == 'text':
                return json.dumps(response['output']['generic'][0])
            if response['output']['generic'][0]['options']:
                return json.dumps(response['output']['generic'][0])
    except Exception as e:
        status = {"Exception in identifying Generic Output": str(e)}
        raise Exception(status)


# function to get response from watson api
def process_message(message: str, user):
    # User input
    message_input = {
        'message_type:': 'text',
        'text': message
    }

    try:
        entry = db.find_one({'user_id': user})
    except Exception as e:
        status = {"error in querying database": str(e)}
        raise Exception(status)

    try:
        if not entry:
            response = config.service.message(
                workspace_id=os.environ['WORKSPACE_ID'],
                input=message_input).get_result()

        else:
            context = entry["context"]
            response = config.service.message(
                workspace_id=os.environ['WORKSPACE_ID'],
                input=message_input, context=context).get_result()
    except Exception as e:
        status = {"error in watson": str(e)}
        raise Exception(status)

    try:
        # creating class for json file here
        convo = CurrentConversation(user)
        convo.context = response['context']

        # inserting json into database
        convojson = jsonpickle.encode(convo)

    except Exception as e:
        status = {"error in creating json for database": str(e)}
        raise Exception(status)

    try:
        db.replace_one({'user_id': user}, json.loads(convojson), upsert=True)
    except Exception as e:
        status = {"error while inserting/updating database": str(e)}
        raise Exception(status)

    try:
        actions = identify_actions(response, message)
        text = identify_generic_output(response)
        if actions and text:
            merged_response = {**json.loads(text),**json.loads(actions)}
            return json.dumps(merged_response)
        return actions or text
    except Exception as e:
        status = {"error in creating response": str(e)}
        raise Exception(status)


# update meta data of the new app by creating new values in the entities

def update_entity_multiple_values(entity_name, new_values):
    updated_entity = Entity()
    get_entity = updated_entity.get_entity(entity_name)
    get_value = get_entity.result["values"]

    # create separate value of tags/categories entity for each new tag/ category

    for value in new_values:
        flag = 0
        for i in range(len(get_value)):

            if get_entity.result["values"][i]["value"] == value:
                flag = 0
                break
            else:
                flag = 1
                continue
        if flag or not get_value:
            new_value = {
                "type": "synonyms",
                "value": value,
                "synonyms": []
            }
            get_value.append(new_value)

    try:
        return updated_entity.update_entity_values(entity_name, get_value)

    except Exception as e:
        status = {"Tags not updated": str(e)}
        raise Exception(status)


# function to update tags, categories and ids
def store_app_data(app):
    try:
        # Update app_ids
        update_entity_multiple_values("app_ids", [app["app_id"]])

        # Update tags
        update_entity_multiple_values("tags", app["tags"])

        # Update categories
        update_entity_multiple_values("categories", app["categories"])

        return {"message": "Data updated successfully"}

    except Exception as e:
        status = {"Missing tags, app_id or categories": str(e)}
        raise Exception(status)
