from config import config
from config.skeleton import UserQuery
import json
import jsonpickle
from pymongo import MongoClient
from config.logger import logger

client = MongoClient(config.db_config["DB_HOST"], config.db_config["DB_PORT"], username=config.db_config["DB_USER"],
                     password=config.db_config["DB_PASSWORD"], connect=False)  # Connection to MongoDB
database = config.db_config["DB_NAME"]
userQuery = config.db_config["USER_QUERY"]
db_query = client[database][userQuery]


# Add new queries to collection
def new_user_query(user_id, message):
    try:
        entry = db_query.find_one({'user_id': user_id})
    except Exception as e:
        status = {"error in querying database": str(e)}
        raise Exception(status)

    try:
        # creating class for json file here
        uquery = UserQuery(user_id)

        if entry:
            uquery.message = entry['message'] + [message]
        else:
            uquery.message = [message]

        # inserting json into database
        uqueryjson = jsonpickle.encode(uquery)

    except Exception as e:
        status = {"error in creating json for database": str(e)}
        raise Exception(status)

    try:
        db_query.replace_one({'user_id': user_id}, json.loads(uqueryjson), upsert=True)
        logger.info("New query added to the userQuery collection")

    except Exception as e:
        status = {"error while inserting/updating database": str(e)}
        raise Exception(status)
