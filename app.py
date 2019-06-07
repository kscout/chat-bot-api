from flask import Flask
from flask import request
import processmessage
from config import errors

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()
