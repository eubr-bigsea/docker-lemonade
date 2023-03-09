import requests
import json


def get_models_limonero(id=None):
    url = "http://localhost:23456/api/v1/limonero/models"
    if id is not None:
        url += f"/{id}"
    headers = {'X-Auth-Token': "123456"}
    r = requests.get(url, headers=headers)
    return json.loads(r.text)


def get_datasources_limonero(id=None):
    url = "http://localhost:23456/api/v1/limonero/datasources"
    if id is not None:
        url += f"/{id}"
    headers = {'X-Auth-Token': "123456"}
    r = requests.get(url, headers=headers)
    return json.loads(r.text)


def get_workflows_tahiti(id=None):
    url = "http://localhost:23456/api/v1/tahiti/workflows"
    if id is not None:
        url += f"/{id}"
    headers = {'X-Auth-Token': "123456"}
    r = requests.get(url, headers=headers)
    return json.loads(r.text)


