from configuration import game_data
from endpoinds.post_method import get_method
import allure


@allure.feature('Testpartner')
def get_url(GameId, request):
    with allure.step('Generating a token'):
        params = {
            "GameUrl": game_data('settings.toml')['GameUrl'],
            "FrontUrl": game_data('settings.toml')['FrontUrl'],
            "PartnerUrl": game_data('settings.toml')['PartnerUrl'],
            "ClientGuid": request.config.getoption("--ClientGuid"),
            "GameId": GameId,
            "UserId": request.config.getoption("--UserId"),
            "Currency": request.config.getoption("--Currency"),
            "Lang": game_data('settings.toml')['Lang'],
            "TestPartnerUrl": game_data('settings.toml')['TestPartnerUrl']
        }
        response = get_method(base_url=game_data('settings.toml')['BaseUrl'], params=params)
        get_token = response.split("token=")[1].split("&")[0]
        game_url = response.split(".")[0]
        with (allure.step(f'Testpartner response {response}')):
            return get_token, game_url
