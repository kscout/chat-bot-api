from config import config
import json
import os

class Entity:

    def create_entity(self, entityData):
        # :param entityData: json file containing all parameters to define entity
        # :return: json dump of response

        response = config.service.create_entity(entityData)
        return json.dumps(response)

    def list_entities(self):
        # :return: all entities in the given workspace

        response = config.service.list_entities(workspace_id=os.environ['WORKSPACE_ID'])
        return response

    def get_entity(self, entity_id):

        # :param entity_id: Unique name of the entity
        # :return: required entity in the given workspace

        response = config.service.get_entity(workspace_id=os.environ['WORKSPACE_ID'], entity=entity_id, export=True)
        return response

    def update_entity(self,newEntityData):
        # :param newEntityData: json file containing all parameters to define entity
        # :return: json dump of response
        response = config.service.update_entity(newEntityData)
        return response

    def update_entity_values(self, entity_name : str, new_values : json):
        response = config.service.update_entity(
            workspace_id=os.environ['WORKSPACE_ID'],
            entity=entity_name, new_values=new_values)
        return response

    def delete_entity(self,entity_id):
        # :param entity_id: Unique name of the entity
        # :return: json dump
        response = config.service.delete_entity(workspace_id=os.environ['WORKSPACE_ID'], entity=entity_id)
        return response

