import requests


def request_get(url, *args):
    try:
        return requests.get(url, args)
    except requests.exceptions.ConnectionError as exc:
        print(exc)
        return None


def request_post(url, data: dict):
    try:
        return requests.post(url, json=data)
    except requests.exceptions.ConnectionError as exc:
        print(exc)
        return None
