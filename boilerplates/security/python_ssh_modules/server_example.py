HOST_KEY = paramiko.RSAKey(filename='test_rsa.key')
USERNAME = 'buffy'
PASSWORD = 'killvampires'

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        
    def check_auth_password(self, username, password):
        if (username == USERNAME) and (password == PASSWORD):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED