from scripts_py.libs.w3_basic import W3Obj
from scripts_py.libs.accounts import AccountsHandler

w3_obj = W3Obj()
w3 = w3_obj.get_w3()

all_accounts = w3_obj.accounts_handler.accounts
first_eoa = w3.eth.account.privateKeyToAccount(all_accounts[0])
second_eoa = w3.eth.account.privateKeyToAccount(all_accounts[1])
third_eoa = w3.eth.account.privateKeyToAccount(all_accounts[2])
