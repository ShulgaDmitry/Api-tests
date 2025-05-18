from configuration import update_toml
from configuration import game_data


def pytest_addoption(parser):
    parser.addoption("--GameId", action='store', nargs='+', type=int, default=game_data('settings.toml')['allGameId'])
    parser.addoption("--ClientGuid", action='store', default="229d579a-672e-440a-9d91-740728462ffc")
    parser.addoption("--UserId", action='store', default=7775)
    parser.addoption("--Currency", action='store', default="BAT")
    parser.addoption("--Lang", action='store', default="EN")
    parser.addoption("--BetSum", action='store', default="1")
    parser.addoption("--NumberSpin", action='store', type=int, default=10)


def pytest_configure(config):
    data = {'GameId': config.getoption('--GameId'), 'NumberSpin': config.getoption('--NumberSpin')}
    update_toml(data)

