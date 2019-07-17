class CurrentConversation():
    def __init__(self, user_id):
        self.user_id = user_id
        self.context = {}

class UserQuery():
    def __init__(self,user_id):
        self.user_id = user_id
        self.message = []