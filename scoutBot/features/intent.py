import config
import json
import os

class Intent:

    def create_intent(self, intentData):
        response = config.service.create_intent(intentData)
        return json.dumps(response)

    def list_intents(self):
        response = config.service.list_intents(workspace_id=os.environ['WORKSPACE_ID'], export=True)
        return json.dumps(response)
