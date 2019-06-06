from scoutBot import config
import json
import os

class Intent:

    def create_intent(self, intentData):
        # :param intentData: json file from intentData folder containing all parameters to define dialogue
        # :return: json dump of created node
        response = config.service.create_intent(intentData)
        return json.dumps(response)

    def list_intents(self):
        # :return: json dump of all nodes
        response = config.service.list_intents(workspace_id=os.environ['WORKSPACE_ID'], export=True)
        return json.dumps(response)

    def update_intent(self, updateIntentData):
        # :param intentData: json file from intentData folder containing all parameters to define dialogue
        # :return: json dump of updated node
        response = config.service.update_intent(updateIntentData)
        return json.dumps(response)

    def get_intent(self,intent):
        # :param intent: unique intent name
        # :return: json dump of given node
        response =  config.service.get_intent(workspace_id=os.environ['WORKSPACE_ID'], intent=intent, export=True)
        return json.dumps(response)

    def delete_intent(self, intent):
        # :param intent: unique intent name
        # :return: json dump of given node
        response= config.service.delete_intent(workspace_id=os.environ['WORKSPACE_ID'], intent=intent)
        return json.dumps(response)



