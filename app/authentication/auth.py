class Auth:
    def __init__(self, token: str):
        self.token = token
    
    def authenticate(self, provided_token: str) -> bool:
        return provided_token == self.token
