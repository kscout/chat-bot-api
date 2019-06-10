from controllers import search
from config import config
import os
import json
from flask import session


def identify_actions(response: json, message: str) -> str:
    if 'actions' in response['output'] and response['output']['actions'][0]['type'] == 'client':
        if 'search' == response['output']['actions'][0]['name']:
            # message = response['context']['context_1']
            return search.search_apps(message)


def identify_generic_output(response: json) -> str:
    if response['output']['generic']:
        if response['output']['generic'][0]['response_type'] == 'text':
            return json.dumps(response['output']['generic'][0])
        if response['output']['generic'][0]['options']:
            return json.dumps(response['output']['generic'][0])


def process_message(message: str) -> str:
    # User input
    message_input = {
        'message_type:': 'text',
        'text': message
    }
    print(message_input)

    print(config.USER_CONTEXT)
    if(not config.USER_CONTEXT):
        response = config.service.message(
            workspace_id=os.environ['WORKSPACE_ID'],
            input=message_input).get_result()
    else:
        # Response from watson api
        print("*************")
        print(config.USER_CONTEXT)
        response = config.service.message(
            workspace_id=os.environ['WORKSPACE_ID'],
            input=message_input, context=config.USER_CONTEXT).get_result()

    config.USER_CONTEXT = response['context']

    print(response)

    return identify_actions(response, message) or identify_generic_output(response)
