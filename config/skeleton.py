class Context():
    def __init__(self):
        self.conversation_id = ""
        self.system = {}

class CurrentConversation():
    def __init__(self, user_id):
        self.user_id = user_id
        self.context = Context()