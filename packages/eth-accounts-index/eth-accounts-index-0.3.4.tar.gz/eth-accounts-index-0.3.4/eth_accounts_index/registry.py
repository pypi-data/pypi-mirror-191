# standard imports
import os
import json

import pathlib
# external imports
from chainlib.eth.tx import (
    TxFormat,
)
from chainlib.eth.contract import (
    ABIContractEncoder,
    ABIContractType,
)

# local imports
from .interface import AccountsIndex

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, 'data')


class AccountRegistry(AccountsIndex):
    __abi = None
    __bytecode = None

    @staticmethod
    def abi():
        if AccountRegistry.__abi is None:
            with open(os.path.join(datadir, 'AccountsIndex.json'), 'r') as f:
                AccountRegistry.__abi = json.load(f)
        return AccountRegistry.__abi

    @staticmethod
    def bytecode():
        if AccountRegistry.__bytecode is None:
            AccountRegistry.__bytecode = pathlib.Path(
                os.path.join(datadir, 'AccountsIndex.bin')
            ).read_text()
        return AccountRegistry.__bytecode

    @staticmethod
    def gas(code=None):
        return 1200000

    def constructor(self, sender_address):
        code = AccountRegistry.bytecode()
        tx = self.template(sender_address, None, use_nonce=True)
        tx = self.set_code(tx, code)
        return self.build(tx)

    def __single_address_method(self, method, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method(method)
        enc.typ(ABIContractType.ADDRESS)
        enc.address(address)
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)
        return tx

    def add_writer(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        return self.__single_address_method('addWriter', contract_address, sender_address, address, tx_format)

    def delete_writer(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        return self.__single_address_method('deleteWriter', contract_address, sender_address, address, tx_format)
