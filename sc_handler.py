import functools
import time
from typing import Union

from scripts_py.libs.car_nft import CarNFTHandler
from scripts_py.libs.parking_lot import ParkingLotHandler
from scripts_py.libs.plt import PLTHandler
from scripts_py.libs.w3_basic import W3Obj


def set_signer(func):
    @functools.wraps(func)
    def wrapper(self=None, *args, **kwargs):
        if kwargs.get("key", None):
            self.w3_handler.set_signer(kwargs.pop("key"))
        return func(self, *args, **kwargs)

    return wrapper


class SCHandler:
    _initial_supply = 20000000

    def __init__(self):
        # Deploy SCs
        self.w3_handler = W3Obj()
        self.plt_handler = PLTHandler(self.w3_handler, self._initial_supply)
        self.car_nft_handler = CarNFTHandler(self.plt_handler)
        self.parking_handler = ParkingLotHandler(self.plt_handler, self.car_nft_handler)
        self._distribute_plts()

    def _distribute_plts(self):
        accounts = self.w3_handler.accounts_handler.accounts
        for i in range(1, len(accounts)):
            self.plt_handler.transfer(
                self.w3_handler.get_eoa(accounts[i]).address,
                (self._initial_supply // len(accounts)),
                signer=self.w3_handler.get_eoa(accounts[0])
            )
        for i in range(len(accounts)):
            print(f"{i} Balance: {self.plt_handler.balanceOf(self.w3_handler.get_eoa(accounts[i]).address)}")


    @set_signer
    def create_car(self, url: str) -> Union[id, None]:
        car_id = self.car_nft_handler.create_car(img_url=url)
        return car_id

    def _cars_status(self) -> str:
        all_cars = self.car_nft_handler.get_all_cars()
        parked_cars = self.parking_handler.get_parked_cars()
        parked_cars_dict = {car_id: fee for car_id, fee in parked_cars}
        non_parked_cars = all_cars.difference(set(parked_cars_dict.keys()))
        result = []
        total_fee = 0
        for car_id in parked_cars_dict:
            car_fee = self.plt_handler.toPLT(parked_cars_dict[car_id])
            result.append(
                f"{car_id} (status: Parked, fees: {car_fee})"
            )
            total_fee += car_fee
        for car_id in non_parked_cars:
            result.append(f"{str(car_id)} (status: Unparked)")

        return ", ".join(result) + f"\nTotal fee: {total_fee}"

    def _my_balance(self) -> int:
        return self.plt_handler.balanceOf(self.w3_handler.signer.address)

    @set_signer
    def status(self) -> str:
        cars_status = self._cars_status()
        my_balance = self._my_balance()
        return f"PLT Balance: {my_balance} \nCars owned: {cars_status}"

    @set_signer
    def deposit(self, car_id: int):
        return self.parking_handler.park(car_id)

    @set_signer
    def retrieve(self, car_id: int):
        return self.parking_handler.retrieve(car_id)

    def free_lots(self):
        return self.parking_handler.available_lots()

    @set_signer
    def parked_car_ids(self):
        parked_cars = self.parking_handler.get_parked_cars()
        parked_cars_dict = {car_id: fee for car_id, fee in parked_cars}
        return list(parked_cars_dict.keys())



if __name__ == "__main__":
    s = SCHandler()
    key_1 = "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"
    car_1 = s.create_car(key=key_1, url="11")
    car_2 = s.create_car(key=key_1, url="22")
    car_3 = s.create_car(key=key_1, url="33")
    print(s.status(key=key_1))
    s.deposit(key=key_1, car_id=car_1)
    s.deposit(key=key_1, car_id=car_2)
    print("---------------")
    print(s.status(key=key_1))
    print("---------------")
    time.sleep(70)
    print("---------------")
    print(s.status(key=key_1))
    print("---------------")
    print(s.status(key=key_1))
    s.retrieve(key=key_1, car_id=car_1)
    print(s.status(key=key_1))

