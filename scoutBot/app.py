from flask import Flask
from flask import request
import message

app = Flask(__name__)


@app.route('/message1/<message_text>', methods = ['GET', 'POST'])
def receive_messages(message_text):

    if request.method == 'POST':
        return message.process_message(message_text)
    else:
        return message


if __name__ == '__main__':
    app.run()
