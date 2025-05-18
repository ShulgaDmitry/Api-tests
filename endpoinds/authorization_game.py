from endpoinds.hash import get_hash_authorization_debit
from endpoinds.post_method import post_method
from configuration import game_data
import allure


@allure.feature('Authorization')
def post_authorization_game(get_game_url):
    data = {
        "Device": "Windows",
        "hash": get_hash_authorization_debit(get_game_url),
        "MobilePlatform": False,
        "token": get_game_url[0]
    }
    response = post_method(data=data, url=get_game_url[1], prefix=game_data('settings.toml')['AuthorizationUrl'])
    with (allure.step(f'Authorization response {response}')):
        return response
