import json

from scripts_py.libs.deploy import deploy_contract, get_file_path, get_event_response
from scripts_py.libs.plt import PLTHandler
from scripts_py.libs.singleton_meta import SingletonMeta
from scripts_py.libs.w3_basic import W3Obj


class CarNFTHandler(metaclass=SingletonMeta):
    artifact_path = get_file_path("../../packages/hardhat/artifacts/contracts/CarNFT.sol/CarNFT.json")

    def __init__(self, plt_handler: PLTHandler):
        self.artifact = json.load(open(self.artifact_path))
        self._abi = self.artifact["abi"]
        self.w3 = plt_handler.w3
        self.plt_handler = plt_handler
        self.contract_address = deploy_contract(
            w3=self.w3,
            artifact=self.artifact,
            constructor_kwargs={"_plt": plt_handler.contract_address}
        )
        self.contract = self.w3.eth.contract(
            address=self.contract_address, abi=self._abi
        )

    def get_contract_address(self):
        return self.contract_address

    def create_car(self, img_url: str):
        self.plt_handler.w3_handler.send_transaction(
            self.plt_handler.contract.functions.approve,
            [self.contract_address, self.plt_handler.fromPLT(100)],
        )

        self.plt_handler.w3_handler.send_transaction(
            self.contract.functions.createCar,
            [img_url],
        )
        car_id = get_event_response(self.contract, "Created", "carId")
        if not car_id:
            print("Car does not created!")
            return None
        else:
            print(f"Car was created! id = {car_id}")
            return car_id

    def get_all_cars(self) -> set:
        eoa = self.plt_handler.w3_handler.signer
        total_car_number = self.contract.functions.balanceOf(eoa.address).call()
        eoa_cars = set()
        for i in range(total_car_number):
            eoa_cars.add(
                self.contract.functions.tokenOfOwnerByIndex(eoa.address, i).call()
            )
        return eoa_cars
