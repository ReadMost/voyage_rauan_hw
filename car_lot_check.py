import time

from car_nft_check import plt, first_eoa, second_eoa, car_nft
from scripts_py.libs.parking_lot import ParkingLotHandler

parking_handler = ParkingLotHandler(plt, car_nft)
# cars = []
# for i in range(3):
#     car = car_nft.create_car(first_eoa, f"https://images.unsplash.com/{i}")
#     cars.append(car)
#
# print("Balance Before", plt.balanceOf(first_eoa.address))
# parking_handler.park(cars[0])
# print("Balance After 1", plt.balanceOf(first_eoa.address))
# time.sleep(60)
# parking_handler.retrieve(cars[0])
# print("Balance After 2", plt.balanceOf(first_eoa.address))
parking_handler.plt_handler.transfer(second_eoa.address, 100)
parking_handler.w3_handler.set_signer("0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d")
print("Balance 1", plt.balanceOf(second_eoa.address))
car = car_nft.create_car(second_eoa, f"https://images.unsplash.com/")
parking_handler.park(car)
print(parking_handler.get_parked_cars(second_eoa))
# print("Balance 2", plt.balanceOf(second_eoa.address))
# time.sleep(60)
# parking_handler.retrieve(car)
# print("Balance After 2", plt.balanceOf(second_eoa.address))