import config
import json
import os

class Entity:

    def create_entity(self, entityData):
        response = config.service.create_entity(entityData)
        return json.dumps(response)

    def list_entities(self):
        response = config.service.list_entities(workspace_id=os.environ['WORKSPACE_ID'])
        return json.dumps(response)

    def get_entity(self, entity_id):
        response = config.service.get_entity(workspace_id=os.environ['WORKSPACE_ID'], entity=entity_id, export=True)
        return json.dumps(response)

    def update_entity(self,newEntityData):
        response = config.service.update_entity(newEntityData)
        return json.dumps(response)

    def delete_entity(self,entity_id):
        response = config.service.delete_entity(workspace_id=os.environ['WORKSPACE_ID'], entity=entity_id)
        return json.dumps(response)


