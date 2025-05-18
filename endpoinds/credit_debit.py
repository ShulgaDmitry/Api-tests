from endpoinds.hash import get_hash_credit_debit
from endpoinds.post_method import post_method
from configuration import game_data
import allure


@allure.feature('CreditDebit')
def post_credit_debit(get_game_url, request):
    data = {
        "betSum": int(request.config.getoption("--BetSum")),
        "token": get_game_url[0],
        "hash": get_hash_credit_debit(get_game_url, request)
    }
    response = post_method(data=data, url=get_game_url[1], prefix=game_data('settings.toml')['CreditUrl'])
    with (allure.step(f'CreditDebit response {response}')):
        return response
