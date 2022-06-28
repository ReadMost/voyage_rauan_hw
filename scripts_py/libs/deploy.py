import json
import os

from web3 import Web3


def deploy_contract(w3: Web3, artifact: json, constructor_kwargs: dict):
    tx_hash = w3.eth.contract(
        abi=artifact['abi'],
        bytecode=artifact['bytecode']).constructor(
        **constructor_kwargs
    ).transact()

    address = w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
    return address


def get_file_path(relative_file_path: str) -> str:
    """
    :param relative_file_path: must be relevant path from deploy.py in project
    :return: absolute path of file
    """
    parent_abs_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(parent_abs_path, relative_file_path)


def get_event_response(contract, event_name, key):
    event_filter = getattr(contract.events, event_name).createFilter(fromBlock='latest')
    log = event_filter.get_new_entries()
    if log:
        return log[0]["args"][key]
    return None
