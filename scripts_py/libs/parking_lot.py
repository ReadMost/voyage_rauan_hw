import json

from scripts_py.libs.car_nft import CarNFTHandler
from scripts_py.libs.deploy import deploy_contract, get_file_path, get_event_response
from scripts_py.libs.plt import PLTHandler
from scripts_py.libs.singleton_meta import SingletonMeta


class ParkingLotHandler(metaclass=SingletonMeta):
    artifact_path = get_file_path("../../packages/hardhat/artifacts/contracts/ParkingLot.sol/ParkingLot.json")

    def __init__(self, plt_handler: PLTHandler, car_nft_handler: CarNFTHandler):
        self.artifact = json.load(open(self.artifact_path))
        self._abi = self.artifact["abi"]
        self.w3_handler = plt_handler.w3_handler
        self.w3 = plt_handler.w3
        self.plt_handler = plt_handler
        self.car_nft_handler = car_nft_handler
        self.contract_address = deploy_contract(
            w3=self.w3,
            artifact=self.artifact,
            constructor_kwargs={
                "_plt": plt_handler.contract_address,
                "_car": car_nft_handler.contract_address,
            }
        )
        self.contract = self.w3.eth.contract(
            address=self.contract_address, abi=self._abi
        )

    def get_contract_address(self):
        return self.contract_address

    def park(self, car_id: int):
        # if ParkingLot does not have access to assets isApprovedForAll=False, then give perm
        if not self.car_nft_handler.contract.functions.isApprovedForAll(
                self.w3_handler.signer.address,
                self.contract_address
        ).call():
            self.w3_handler.send_transaction(
                self.car_nft_handler.contract.functions.setApprovalForAll,
                [self.contract_address, True]
            )

        # call parking logic
        self.w3_handler.send_transaction(
            self.contract.functions.park,
            [car_id]
        )
        # check logs
        car_id = get_event_response(self.contract, "Parked", "carId")
        if not car_id:
            print("Car is not Parked!")
            return None
        response = f"Car was parked! with id = {car_id}"
        print(response)
        return response

    def retrieve(self, car_id: int):
        self.plt_handler.w3_handler.send_transaction(
            self.plt_handler.contract.functions.approve,
            [self.contract_address, self.plt_handler.fromPLT(100)]
        )

        self.w3_handler.send_transaction(
            self.contract.functions.retrieve,
            [car_id]
        )
        feeCharged = get_event_response(self.contract, "Retrieved", "feeCharged")
        if feeCharged is None:
            print("Car is not Retrieved!")
            return None
        print(f"Car was Retrieved! feeCharged = {self.plt_handler.toPLT(feeCharged)}")

    def get_parked_cars_legacy(self, eoa):
        return self.contract.functions.parkedCars(eoa.address).call()

    def available_lots(self):
        self.plt_handler.w3_handler.send_transaction(
            self.contract.functions.ping,
            []
        )
        return self.contract.functions.availableLots().call()

    def get_parked_cars(self):
        self.plt_handler.w3_handler.send_transaction(
            self.contract.functions.ping,
            []
        )
        eoa = self.w3_handler.signer
        parked_cars_number = self.contract.functions.parkedCarsCount(
            eoa.address
        ).call()
        result = []
        for i in range(parked_cars_number):
            result.append(
                self.contract.functions.parkedCarOfOwnerByIndex(eoa.address, i).call()
            )
        return result
