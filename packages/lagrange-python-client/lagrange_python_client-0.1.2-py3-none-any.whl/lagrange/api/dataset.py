import logging

import requests


def get_dataset(client, dataset_name):
    url = client.domain + "/datasets/" + dataset_name

    payload = {}
    files = {}

    response = requests.request("GET", url, data=payload, files=files)

    logging.info(response.text)
