# Example 1: sets up service wrapper, sends initial message, and
# receives response.

import ibm_watson
import os
import json

service = ibm_watson.AssistantV1(

    iam_apikey = os.environ['API_KEY'],
    version = '2019-02-28'
)
current_action=''
message_input = {
    'message_type:': 'text',
    'text': ''
    }

# Simple greeting and end of conversation

# Main input/output loop
while current_action != 'end_conversation':
    response = service.message(
        workspace_id=os.environ['WORKSPACE_ID'],
        input= message_input).get_result()
    if response['output']['generic']:
        if response['output']['generic'][0]['response_type'] == 'text':
            print(response['output']['generic'][0]['text'])
    # If we're not done, prompt for next round of input.
    if current_action != 'end_conversation':
        user_input = input('>> ')
        message_input = {
            'text': user_input
        }
