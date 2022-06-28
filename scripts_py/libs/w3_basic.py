import json
from typing import Callable

from eth_account.signers.local import (
    LocalAccount,
)
from web3 import Web3, HTTPProvider

from scripts_py.libs.accounts import AccountsHandler


class W3Obj:

    def __init__(self, url: str = "http://localhost:8545", *args, **kwargs):
        self.w3 = Web3(HTTPProvider(url))
        self.accounts_handler = AccountsHandler()
        self.set_signer(self.accounts_handler.accounts[0])
        print("Connected? ", self.w3.isConnected())

    def get_w3(self) -> Web3:
        return self.w3

    def get_eoa(self, key: str) -> LocalAccount:
        if not self.accounts_handler.check_pk(key):
            raise ValueError(f"{key} does not exist")
        eoa = self.w3.eth.account.privateKeyToAccount(key)
        return eoa

    def set_signer(self, key):
        eoa = self.get_eoa(key)
        self.signer = eoa

    def _get_nonce(self, signer):
        return self.w3.eth.get_transaction_count(signer.address)

    def send_transaction(self, function: Callable, tx_kwargs: list, signer=None):
        signer = signer or self.signer
        try:
            tx = function(*tx_kwargs).buildTransaction({
                'from': signer.address,
                'gas': 30000000,
                'maxFeePerGas': self.w3.toWei('2', 'gwei'),
                'maxPriorityFeePerGas': self.w3.toWei('1', 'gwei'),
                'nonce': self._get_nonce(signer),
            })
            signed_tx = signer.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return tx_receipt
        except Exception as e:
            try:
                print("Error:", e.args[0]["data"]["message"])
            except:
                print("Error: ", str(e))
            return None




