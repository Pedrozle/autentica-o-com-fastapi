import secrets

class TokenGenerator():
    def __init__(self):
        self. token = 0
    
    def gen(self):
        self.token = secrets.randbits(20) 
        return self.token