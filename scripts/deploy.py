from brownie import DappToken, TokenFarm, config, network  # type: ignore

from scripts.helpful_scripts import get_account, get_contract

KEPT_BALANCE = 100000000000000000000  # 100 ether in wei


# dapp_token, weth_token, fau_token/dai
def add_allowed_tokens(token_farm, allowed_tokens_dict, account):
    for token in allowed_tokens_dict:
        add_tx = token_farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(
            token.address, allowed_tokens_dict[token]
        )
        set_tx.wait(1)
    return token_farm


def deploy_token_farm_and_dapp_token():
    account = get_account()
    dapp_token = DappToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    allowed_tokens_dict = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }
    add_allowed_tokens(token_farm, allowed_tokens_dict, account)
    return token_farm, dapp_token


def main():
    deploy_token_farm_and_dapp_token()
