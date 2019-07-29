from controllers import search, log_data
from config import config
from config.skeleton import CurrentConversation
import os
import json
import jsonpickle
from pymongo import MongoClient
from training.features.entity import Entity
from controllers import deploy

# MongoDB is not fork() safe, thus need to create a new instance for every child process in order to stop deadlock.
# see MongoDB FAQ for more information
# Connecting to MondoDB
client = MongoClient(config.db_config["DB_HOST"], config.db_config["DB_PORT"], username=config.db_config["DB_USER"],
                     password=config.db_config["DB_PASSWORD"], connect=False)  # Connection to MongoDB
database = config.db_config["DB_NAME"]
currentConversation = config.db_config["CURRENT"]
userQuery = config.db_config["USER_QUERY"]
db = client[database][currentConversation]
db_query = client[database][userQuery]


def identify_actions(response: json, user: str) -> str:
    try:
        if 'actions' in response['output'] and response['output']['actions'][0]['type'] == 'client':
            if 'search' == response['output']['actions'][0]['name']:
                return search.search_apps(response, response['input']['text'])
            if 'deploy' == response['output']['actions'][0]['name']:
                return deploy.deploy_app(response['context']['app_id'])
            if 'unknown' == response['output']['actions'][0]['name']:
                log_data.new_user_query(user, response['input']['text'])

    except Exception as e:
        status = {"Exception in identifying actions": str(e)}
        raise Exception(status)


def format_text(response: json) -> str:
    multitext = ""

    if 'generic' in response['output']:
        for i in range(len(response['output']['generic'])):
            if response['output']['generic'][i]['response_type'] == 'text':
                multitext += response['output']['generic'][i]['text'] + '<br>'

    return multitext


def identify_generic_output(response: json) -> str:
    try:
        if response['output']['generic']:
            if response['output']['generic'][0]['response_type'] == 'text':
                multitext = format_text(response)
                text_response = {'response_type': 'text', 'text': multitext}
                return json.dumps(text_response)
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
        actions = identify_actions(response, user)
        text = identify_generic_output(response)
        if actions and text:
            merged_response = {**json.loads(text), **json.loads(actions)}
            return json.dumps(merged_response)
        return actions or text
    except Exception as e:
        status = {"error in creating response": str(e)}
        raise Exception(status)


def extract_data(apps):
    app_ids_list = []
    categories_list = []
    tags_list = []
    taglines = []

    for i in range(len(apps)):
        app_ids_list.append(apps[i]['app_id'])
        categories_list += apps[i]['categories']
        tags_list += apps[i]['tags']
        taglines.append(apps[i]['tagline'])
    return app_ids_list, list(set(categories_list)), list(set(tags_list)), taglines


def recreate_single_entity(value_list, entity_name):
    new_entity = Entity()

    try:
        new_entity.delete_entity(entity_name)
        entity_values = []
        for i in range(len(value_list)):
            entity_values.append({'value': value_list[i][:64], 'synonyms': list(search.process_text(value_list[i]))})
        response = new_entity.create_entity(entity_name, entity_values)
        # response = {}

        return response

    except Exception as e:
        status = {"Entity not recreated": str(e)}
        raise Exception(status)


# Create entity with no synonyms for unique app ids
def recreate_app_ids(value_list, entity_name):
    new_entity = Entity()

    try:
        new_entity.delete_entity(entity_name)
        entity_values = []
        for i in range(len(value_list)):
            entity_values.append({'value': value_list[i][:64]})
        response = new_entity.create_entity(entity_name, entity_values)
        return response

    except Exception as e:
        status = {"Entity not recreated": str(e)}
        raise Exception(status)


# function to update tags, categories and ids
def store_app_data(apps):
    try:
        app_ids_list, categories_list, tags_list, taglines = extract_data(apps)

        # recreate app_ids
        recreate_app_ids(app_ids_list, 'app_ids')

        # recreate categories
        recreate_single_entity(categories_list, 'categories')

        # recreate tags
        recreate_single_entity(tags_list, 'tags')

        # recreate taglines
        recreate_single_entity(taglines, 'tagline')

        return {"message": "Data updated successfully"}

    except Exception as e:
        status = {"Missing tags, app_id , taglines or categories": str(e)}
        raise Exception(status)


def verify_request(verification_token):
    if verification_token != os.environ['X_BOT_API_SECRET']:
        status = {"Unauthorized Request"}
        raise Exception(status)
