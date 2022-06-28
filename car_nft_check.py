from plt_transfer_check import w3, plt, first_eoa, second_eoa
from scripts_py.libs.car_nft import CarNFTHandler

car_nft = CarNFTHandler(plt)

print("Balance Before", plt.balanceOf(first_eoa.address))
r = car_nft.create_car(first_eoa, "https://images.unsplash.com/")
r = car_nft.create_car(first_eoa, "https://images.unsplash.com/")
print("Balance after", plt.balanceOf(first_eoa.address))
print("-----------------Other case ------------------------")
print("Balance Before", plt.balanceOf(second_eoa.address))
car_nft.create_car(second_eoa, "https://images.unsplash.com/")
print("Balance after", plt.balanceOf(second_eoa.address))

print("First_user cars", car_nft.get_all_cars(first_eoa))
print("Second_user cars", car_nft.get_all_cars(second_eoa))