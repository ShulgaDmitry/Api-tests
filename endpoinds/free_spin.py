from endpoinds.hash import get_hash_free_spin
from endpoinds.post_method import post_method
from configuration import game_data
import allure


@allure.feature('FreeSpin')
def post_free_spin(get_game_url, result_id, spin_id):
    data = {
        "token": get_game_url[0],
        "hash": get_hash_free_spin(get_game_url, result_id, spin_id),
        "ResultId": result_id,
        "SpinId": spin_id
    }
    response = post_method(data=data, url=get_game_url[1], prefix=game_data('settings.toml')['FreeSpin'])
    with (allure.step(f'FreeSpin response {response}')):
        return response
