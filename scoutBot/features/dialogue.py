import config
import json
import os

class Dialogue:

    def create_dialogue(self,dialogueNodeData):
        """

        :param dialogueNodeData: json file from DialogueNodes folder containing all parameters to define dialogue
        :return: json dump of created node
        """
        response = config.service.create_dialog_node(dialogueNodeData)
        return json.dumps(response)

    def list_dialogue(self):
        """
        :return: list of all dialogue nodes in the given workspace
        """
        response = config.service.list_dialog_nodes(workspace_id=os.environ['WORKSPACE_ID'])
        return json.dumps(response)

    def get_dialogue(self,dialogue_id):
        """

        :param dialogue_id: Unique id of the dialogue
        :return: json dump of retrived node
        """
        response= config.service.get_dialog_node(workspace_id=os.environ['WORKSPACE_ID'], dialog_node=dialogue_id)
        return json.dumps(response)

    def update_dialogue(self,dialogueNodeData):
        """

        :param dialogueNodeData: json file from DialogueNodes folder containing all parameters to define dialogue
        :return: json dump of updated node
        """
        response = config.service.update_dialog_node(dialogueNodeData)
        return json.dumps(response)

    def delete_dialogue(self,dialogue_id):
        """

        :param dialogue_id: unique id of the dialogue node
        :return: json dump of the deleted node
        """
        response= config.service.delete_dialog_node(workspace_id=os.environ['WORKSPACE_ID'], dialog_node=dialogue_id)
        return json.dumps(response)

