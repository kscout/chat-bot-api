from controllers import search,learn
from config import config
from config.skeleton import CurrentConversation
import os
import json
import jsonpickle


def identify_actions(response: json, message: str) -> str:
    if 'actions' in response['output'] and response['output']['actions'][0]['type'] == 'client':
        if 'search' == response['output']['actions'][0]['name']:
            return search.search_apps(message)
        if 'learn' == response['output']['actions'][0]['name']:
            return learn.answer_query(message)


def identify_generic_output(response: json) -> str:
    if response['output']['generic']:
        if response['output']['generic'][0]['response_type'] == 'text':
            return json.dumps(response['output']['generic'][0])
        if response['output']['generic'][0]['options']:
            return json.dumps(response['output']['generic'][0])


def process_message(message: str, user, db):
    # User input
    message_input = {
        'message_type:': 'text',
        'text': message
    }

    entry = db.find_one({'user_id': user})
    if not entry:
        response = config.service.message(
            workspace_id=os.environ['WORKSPACE_ID'],
            input=message_input).get_result()

    else:
        context = entry.context
        response = config.service.message(
            workspace_id=os.environ['WORKSPACE_ID'],
            input=message_input, context=context).get_result()

    # creating class for json file here
    convo = CurrentConversation(user)
    convo.context = response['context']

    # inserting json into database
    convojson = jsonpickle.encode(convo)
    print("convojson ", str(convojson))

    insertid= db.insert_one(json.loads(convojson)).inserted_id
    print("insertid",insertid)

    actions = identify_actions(response, message)
    text = identify_generic_output(response)
    if actions and text:
        merged_response = {**json.loads(actions), **json.loads(text)}
        return json.dumps(merged_response)
    return actions or text
