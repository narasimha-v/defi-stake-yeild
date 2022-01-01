import json
import os
import shutil

import yaml
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


def deploy_token_farm_and_dapp_token(should_update_front_end=False):
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
    if should_update_front_end:
        update_front_end()
    return token_farm, dapp_token


def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def update_front_end():
    # Send the build folder
    copy_folders_to_front_end("./build", "./front_end/src/chain-info")

    # Sending the front end our config in JSON format
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print("Front end updated!")


def main():
    deploy_token_farm_and_dapp_token(should_update_front_end=True)
