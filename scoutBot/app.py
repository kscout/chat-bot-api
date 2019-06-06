from flask import Flask
from flask import request
from scoutBot import message

app = Flask(__name__)


@app.route('/messages', methods = ['GET', 'POST'])
def receive_messages():

# Handle messages from client
    if request.method == 'POST':
        message_text = request.get_json()['text']
        return (message.process_message(message_text))
    else:
        return ("No message received")


if __name__ == '__main__':
    app.run()


#TODO: Error Handling
#TODO: Deployment Script