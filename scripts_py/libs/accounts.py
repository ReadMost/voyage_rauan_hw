import json
from collections import OrderedDict

from .deploy import get_file_path


class AccountsHandler:
    def __init__(self, file_path="../data/.keystore.json"):
        self.file_path = file_path
        self.accounts = self.get_accounts_list()

    def _read_all_accounts(self) -> dict:
        fp = open(get_file_path(self.file_path), "r")
        return json.load(fp)

    def get_accounts_list(self) -> list:
        all_accounts = self._read_all_accounts()
        result = [i["private_key"] for _, i in all_accounts.items()]
        return result

    def check_pk(self, pk) -> bool:
        return str(pk) in self.accounts
