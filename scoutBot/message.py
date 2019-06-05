from scoutBot import config, search
import os

def process_message(message):
    # User input
    message_input = {
        'message_type:': 'text',
        'text': message
    }

    # Response from watson api
    response = config.service.message(
        workspace_id=os.environ['WORKSPACE_ID'],
        input= message_input).get_result()


    # Return generic output
    if response['output']['generic']:
        if response['output']['generic'][0]['response_type'] == 'text':
            return response['output']['generic'][0]['text']

    # Identify actions in response response after action
    if 'actions' in response['output'] and response['output']['actions'][0]['type'] == 'client':
        if('search' == response['output']['actions'][0]['name']):
            return search.search_apps(message)

        #Return Functions not yet defined
        elif('deploy' == response['output']['actions'][0]['name']):
            return
        else:
            return