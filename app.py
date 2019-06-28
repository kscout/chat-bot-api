from flask import Flask, Response
from config.loggingfilter import *
import processmessage
from config import config
import nltk
import json
from pymongo import MongoClient
import uuid

# Setting up NLTK
nltk.data.path.append("/srv/bot_api/nltk_data/")


# Connecting to MondoDB
client = MongoClient(config.db_config["DB_HOST"], config.db_config["DB_PORT"], username=config.db_config["DB_USER"],
                    password=config.db_config["DB_PASSWORD"], connect=False)  # Connection to MongoDB
database = config.db_config["DB_NAME"]
currentConversation = config.db_config["CURRENT"]
db = client[database][currentConversation]
config.logger.info("Connection to Database: "+str(db))
if db.insert_one({'user_id': "xxx_xxx_xxx_xxx_test"}).inserted_id:
    try:
        db.delete_many({'user_id': "xxx_xxx_xxx_xxx_test"})
    except Exception as e:
        config.logger.info("Error Connecting to Database: "+str(e))
    config.logger.info("Connection to Database Successful")
else:
    config.logger.info("Error Connecting to Database")


app = Flask(__name__)

# Function to receive messages from client application
@app.route('/messages', methods=['GET', 'POST'])
def receive_messages():
    if request.method == 'POST':
        try:
            message_text = request.get_json()['text']
            user = request.get_json()['user']
            config.logger.info("POST request on /messages")
            api_response =  processmessage.process_message(message_text, user)
            return Response(json.dumps(api_response), status=200, mimetype='application/json')
        except IndexError:
            status = {}
            status["error"] = "Index Error"
            return Response(json.dumps(status), status=400, mimetype='application/json')
        except Exception as e:
            status = {}
            status["error"] = str(e)
            return Response(json.dumps(status), status=400, mimetype='application/json')

    else:
        status = {}
        status["error"] = "Wrong Request Type"
        return Response(json.dumps(status), status=400, mimetype='application/json')


@app.route('/session', methods=['GET'])
def create_sessions():
    if request.method == 'GET':
        try:
            unique_id = {}
            unique_id['session_id']  = str(uuid.uuid1())
            print(unique_id)
            return Response(json.dumps(unique_id), status=200, mimetype='application/json')
        except:
            status ={}
            status["error"] = "Could not generate unique id: " + str(e)
            return Response(json.dumps(status), status=400, mimetype='application/json')
    else:
        status = {}
        status["error"] = "Wrong Request Type"
        return Response(json.dumps(status), status=400, mimetype='application/json')

@app.route('/health', methods=['GET', 'POST'])
@disable_logging
def health_probe() -> Response:
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
    nltk.data.path.append('/srv/bot_api/nltk_data/')

