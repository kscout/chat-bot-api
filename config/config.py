import ibm_watson
import os
import logging

service = ibm_watson.AssistantV1(
    version='2019-02-28',
    iam_apikey=os.environ['API_KEY'],
)


logger = logging.getLogger('chat_api_logger')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# Stores context of previous message

USER_CONTEXT=""

user_map = {}

db_config={}
db_config["DB_HOST"] = "localhost"
db_config["DB_PORT"] = 27017
db_config["DB_USER"] = os.environ['MONGO_INITDB_ROOT_USERNAME']
db_config["DB_PASSWORD"] = os.environ['MONGO_INITDB_ROOT_PASSWORD']
db_config["DB_NAME"] = os.environ['MONGO_INITDB_DATABASE']
db_config["CURRENT"] = "curent-conversation"