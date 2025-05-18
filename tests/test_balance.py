import pytest
from endpoinds.credit_debit import post_credit_debit
from endpoinds.authorization_game import post_authorization_game
from endpoinds.free_spin import post_free_spin
from endpoinds.testpartner import get_url
import allure
from loguru import logger
from configuration import game_data, update_toml


@allure.feature('Check balance')
@pytest.mark.parametrize("GameId", game_data('game_data.toml')['GameId'])
def test_balance(GameId, request):
    logger.info(f'Start test')
    with (allure.step(f'Check balance of {game_data("game_data.toml")["NumberSpin"]} spins from CreditDebit')):
        data = {}
        get_game_url = get_url(GameId, request)
        logger.info(f'Get token and game url for {GameId}')
        response = post_authorization_game(get_game_url)
        data['AuthorizationData'] = dict(Balance=int(response['Balance']))
        initial_balance = data['AuthorizationData']['Balance']
        logger.info(f'Check balance after {game_data("game_data.toml")["NumberSpin"]} spin for {GameId}')
        logger.info(f'Initial balance for {GameId}: {initial_balance}')
        update_toml(data)
        for x in range(game_data("game_data.toml")["NumberSpin"]):
            with allure.step('Calculating the balance taking into account the bet and winnings'):
                logger.info(f'Test Credit Debit spin number {x} for {GameId}')
                response = post_credit_debit(get_game_url, request)
                if "GameFreeSpins" in response and response["GameFreeSpins"]:
                    with allure.step('Calculating the balance taking into account the bet and winnings in Free Spin'):
                        total_win_sum = response["WinInfo"]['WinSum']
                        initial_balance += total_win_sum
                        logger.info(f'initial balance for {GameId}: {initial_balance}')
                        freespin_response = post_free_spin(get_game_url=get_game_url,
                                       result_id=response["ResultId"],
                                       spin_id=response["SpinResult"]["Id"])
                        while freespin_response["GameFreeSpins"]:
                            data['FreeSpinData'] = dict(WinSum=int(freespin_response["WinInfo"]['WinSum']),
                                                        Balance=int(freespin_response["WinInfo"]['Balance']),
                                                        TotalWin=int(freespin_response["WinInfo"]['TotalWin']))
                            logger.info(f'Test Free spin for {GameId}')
                            win_sum = data['FreeSpinData']['WinSum']
                            logger.info(f'Win sum for {GameId}: {win_sum}')
                            total_win_sum += win_sum
                            with allure.step(f'Total sum = {total_win_sum}, win_sum = {win_sum}, '
                                             f'Initial balance = {initial_balance}, from Free Spin'):
                                current_balance = initial_balance + win_sum
                            initial_balance = current_balance
                            with allure.step(f'Initial_balance + win_sum = Current balance({initial_balance})'):
                                logger.info(f'Current balance for {GameId}: {initial_balance}')
                            total_win = data['FreeSpinData']['TotalWin']
                            with allure.step(f'Total win from response = {total_win}'):
                                logger.info(f'Total win for {GameId} from response: {total_win}')
                            update_toml(data)
                            with allure.step('Check win sum of spin from Free spin'):
                                assert total_win == total_win_sum, 'The win sum does not match'
                            freespin_response = post_free_spin(get_game_url=get_game_url,
                                                               result_id=response["ResultId"],
                                                               spin_id=freespin_response["SpinResult"]["Id"])
                        data['FreeSpinData'] = dict(WinSum=int(freespin_response["WinInfo"]['WinSum']),
                                                    Balance=int(freespin_response["WinInfo"]['Balance']),
                                                    TotalWin=int(freespin_response["WinInfo"]['TotalWin']))
                        logger.info(f'Test Free spin for {GameId}')
                        win_sum = data['FreeSpinData']['WinSum']
                        logger.info(f'Win sum for {GameId}: {win_sum}')
                        total_win_sum += win_sum
                        with allure.step(
                                f'Total sum = {total_win_sum}, win_sum = {win_sum}, '
                                f'Initial balance = {initial_balance}, from Free Spin'):
                            current_balance = initial_balance - bet_sum + win_sum
                        initial_balance = current_balance
                        with allure.step(f'Initial_balance + win_sum = Current balance({initial_balance})'):
                            logger.info(f'Current balance for {GameId}: {initial_balance}')
                        total_win = data['FreeSpinData']['TotalWin']
                        with allure.step(f'Total win from response = {total_win}'):
                            logger.info(f'Total win for {GameId} from response: {total_win}')
                        update_toml(data)
                        with allure.step('Check win sum of spin from Free spin'):
                            assert total_win == total_win_sum, 'The win sum does not match'
                        total_balance = data['FreeSpinData']['Balance']
                        with allure.step(f'Current balance = {initial_balance} '
                                         f'and Total balance from response = {total_balance} for {GameId}'):
                            logger.info(f'Total balance for {GameId} from response: {total_balance}')
                        update_toml(data)
                        with allure.step('Check balance of spin from Free spin'):
                            assert total_balance == initial_balance, 'The balance does not match'
                else:
                    data['CreditDebitData'] = dict(WinSum=int(response["WinInfo"]['WinSum']),
                                                BetSum=int(response["BetSum"]),
                                                Balance=int(response["WinInfo"]['Balance']))
                    win_sum = data['CreditDebitData']['WinSum']
                    logger.info(f'Win sum for {GameId}: {win_sum}')
                    with allure.step(
                            f'Win_sum = {win_sum}, '
                            f'Initial balance = {initial_balance}, from CreditDebit'):
                        bet_sum = data['CreditDebitData']['BetSum']
                    logger.info(f'Bet sum for {GameId}: {bet_sum}')
                    logger.info(f'initial balance for {GameId}: {initial_balance}')
                    current_balance = initial_balance - bet_sum + win_sum
                    initial_balance = current_balance
                    with allure.step(f'Initial_balance - bet_sum + win_sum = Current balance({initial_balance}), '
                                     f'Bet sum = {bet_sum} from CreditDebit'):
                        total_balance = data['CreditDebitData']['Balance']
                    with allure.step(f'Current balance = {initial_balance} '
                                    f'and Total balance from response = {total_balance} for {GameId}'):
                        logger.info(f'Current balance = {initial_balance} '
                                        f'and Total balance from response = {total_balance} for {GameId}')
                    update_toml(data)
                    with allure.step('Check balance  of spin from CreditDebit'):
                            assert total_balance == initial_balance, 'The balance does not match'
