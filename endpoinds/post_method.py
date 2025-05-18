import requests


def get_method(base_url, params):

    response = requests.request('GET', base_url, params=params, timeout=10).text
    return response


def post_method(data, url, prefix):

    response = requests.request(
        'POST',
        f'{url}.api.perfecttlos.com/{prefix}',
        json=data,
        timeout=10
    ).json()
    return response
