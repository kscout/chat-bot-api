from controllers import search
from config import config
import os
import json


def identify_actions(response: json, message: str) -> str:
    if 'actions' in response['output'] and response['output']['actions'][0]['type'] == 'client':
        if 'search' == response['output']['actions'][0]['name']:
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

    # Response from watson api
    response = config.service.message(
        workspace_id=os.environ['WORKSPACE_ID'],
        input=message_input).get_result()

    return identify_actions(response, message) or identify_generic_output(response)
