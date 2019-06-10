from flask import Flask, Response
from flask import request
import processmessage
from config import errors
import nltk
import json
app = Flask(__name__)

# Setting up NLTK
nltk.data.path.append('/srv/bot_api/nltk_data/')


# Function to receive messages from client application

@app.route('/messages', methods=['GET', 'POST'])
def receive_messages() -> str:
    if request.method == 'POST':
        try:
            message_text = request.get_json()['text']
            return processmessage.process_message(message_text)
        except IndexError:
            return errors.INVALID_FORMAT_ERR
    else:
        return errors.EMPTY_MESSAGE_ERR


@app.route('/health', methods=['GET', 'POST'])
def health_probe() -> str:
    status={}
    status["ok"]=True
    return Response(json.dumps(status), status=200, mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0',port=5000)