from scripts_py.libs.plt import PLTHandler
from base_check import *

plt = PLTHandler(w3_obj)
plt_contract = plt.contract

# print("Balance Before", plt.balanceOf(first_eoa.address))
r = plt.transfer(second_eoa.address, 100, signer=first_eoa)
# print("Balance after", plt.balanceOf(first_eoa.address))
# print("Balance after", plt.balanceOf(second_eoa.address))
# plt.transfer(third_eoa.address, 100, second_eoa)
# print("Balance after", plt.balanceOf(second_eoa.address))
# print("Balance after", plt.balanceOf(third_eoa.address))