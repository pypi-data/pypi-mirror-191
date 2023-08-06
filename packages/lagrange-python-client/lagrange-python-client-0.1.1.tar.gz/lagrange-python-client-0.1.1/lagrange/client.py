import logging


class Client(object):
    def __init__(self, api_key, access_token, chain_name=None, login=True):
        self.token = None
        if chain_name is None:
            chain_name = "hyperspace.testnet"
        self.chain_name = chain_name
        self.api_key = api_key
        self.access_token = access_token
        if login:
            self.api_key_login()

    def api_key_login(self):
        logging.info("Connect to Lagrange Computing Network successfully.")