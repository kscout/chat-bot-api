from flask import Flask, Response
from config.loggingfilter import *
import processmessage
from config import config
import nltk
import json
from pymongo import MongoClient

# Setting up NLTK
nltk.data.path.append("/srv/bot_api/nltk_data/")

app = Flask(__name__)


# Connecting to MondoDB
client = MongoClient(config.db_config["DB_HOST"], config.db_config["DB_PORT"], username=config.db_config["DB_USER"],
                    password=config.db_config["DB_PASSWORD"],)  # Connection to MongoDB
database = config.db_config["DB_NAME"]
currentConversation = config.db_config["CURRENT"]
db = client[database][currentConversation]   # Switching to Database with name 'project'
config.logger.info("Connection to Database: "+str(db))

# Function to receive messages from client application
@app.route('/messages', methods=['GET', 'POST'])
def receive_messages():
    if request.method == 'POST':
        try:
            message_text = request.get_json()['text']
            user = request.get_json()['user']
            config.logger.info(message_text)
            return processmessage.process_message(message_text, user, db)
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



@app.route('/health', methods=['GET', 'POST'])
@disable_logging
def health_probe() -> Response:
    status = {}
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
    nltk.data.path.append('/srv/bot_api/nltk_data/')

