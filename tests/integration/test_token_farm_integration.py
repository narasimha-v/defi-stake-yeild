from brownie import network  # type: ignore
from scripts.deploy import deploy_token_farm_and_dapp_token
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)

amount_staked = 1000000000000000000  # 1 ETH in WEI


def test_stake_and_issue_correct_amounts():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    account = get_account()
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})
    starting_balance = dapp_token.balanceOf(account.address)
    price_feed_contract = get_contract("dai_usd_price_feed")
    (_, price, _, _, _) = price_feed_contract.latestRoundData()
    amount_token_to_issue = (
        price / 10 ** price_feed_contract.decimals()
    ) * amount_staked
    issue_tx = token_farm.issueTokens({"from": account})
    issue_tx.wait(1)
    assert (
        dapp_token.balanceOf(account.address)
        == amount_token_to_issue + starting_balance
    )
