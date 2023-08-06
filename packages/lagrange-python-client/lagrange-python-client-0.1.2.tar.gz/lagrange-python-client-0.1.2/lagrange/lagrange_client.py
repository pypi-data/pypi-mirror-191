import logging

import requests

from lagrange.common.dataset import Dataset


class LagrangeClient(object):
    def __init__(self, api_key=None, access_token=None, chain_name=None, login=True):
        self.token = None
        self.domain = "http://lagrangedao.org:5000"
        if chain_name is None:
            chain_name = "hyperspace.testnet"
        self.chain_name = chain_name
        self.api_key = api_key
        self.access_token = access_token
        if login:
            self.api_key_login()

    def api_key_login(self):

        logging.info("Connect to Lagrange Computing Network successfully.")

    def get_dataset(self, dataset_name):
        url = self.domain + "/datasets/" + dataset_name
        payload = {}
        files = {}
        response = requests.request("GET", url, data=payload, files=files)
        data = response.json()['data']['dataset']
        if data:
            dataset: Dataset = Dataset(name=data['name'], is_public=data['is_public'], license=data['license'],
                                       status=data['status'], created_at=data['created_at'],
                                       updated_at=data['updated_at'])
        else:
            dataset = None
        return dataset
