import json

from web3 import Web3

from .deploy import deploy_contract, get_file_path
from .singleton_meta import SingletonMeta
from .w3_basic import W3Obj


class PLTHandler(metaclass=SingletonMeta):
    artifact_path = get_file_path("../../packages/hardhat/artifacts/contracts/PLTToken.sol/PLTToken.json")

    def __init__(self, w3_handler: W3Obj, initial_supply=20000000):
        self.artifact = json.load(open(self.artifact_path))
        self._abi = self.artifact["abi"]
        self.w3_handler = w3_handler
        self.w3 = w3_handler.w3
        self.contract_address = deploy_contract(
            w3=self.w3,
            artifact=self.artifact,
            constructor_kwargs={"_initialSupply": initial_supply*(10**18)} # 10mln
        )
        self.contract = self.w3.eth.contract(
            address=self.contract_address, abi=self._abi
        )
        self.DECIMALS = 10 ** self.contract.functions.decimals().call()

    def get_contract_address(self):
        return self.contract_address

    def fromPLT(self, value: int):
        """returns system PLT by * 10**decimal"""
        return value * self.DECIMALS

    def toPLT(self, value: int):
        """returns normal PLT by // 10**decimal"""
        return value // self.DECIMALS

    def balanceOf(self, address: str) -> int:
        return self.toPLT(self.contract.functions.balanceOf(address).call())

    def transfer(self, to_address, amount: int, signer=None):
        self.w3_handler.send_transaction(
            self.contract.functions.transfer,
            [to_address, self.fromPLT(amount)],
            signer=signer
        )

