import ibm_watson
import os
import logging

# Configuring IBM-Watson Assistant
service = ibm_watson.AssistantV1(
    version='2019-02-28',
    iam_apikey=os.environ['API_KEY'],
)

# Stores context of previous message
USER_CONTEXT = ""


## Logger Configuration ##
logger = logging.getLogger('Logger')
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


# Configuring Database ENV
db_config = dict()
db_config["DB_HOST"] = os.environ['APP_DB_HOST']
db_config["DB_PORT"] = 27017
db_config["DB_USER"] = os.environ['APP_DB_USER']
db_config["DB_PASSWORD"] = os.environ['APP_DB_PASSWORD']
db_config["DB_NAME"] = os.environ['APP_DB_NAME']
db_config["CURRENT"] = "currentconversation"