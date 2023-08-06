# standard imports
import logging
import json
import os

# external imports
from chainlib.eth.tx import (
    TxFactory,
    TxFormat,
)
from chainlib.eth.contract import (
    ABIContractEncoder,
    ABIContractDecoder,
    ABIContractType,
    abi_decode_single,
)
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.eth.error import RequestMismatchException
from hexathon import (
    add_0x,
    strip_0x,
)

logg = logging.getLogger()


class AccountsIndex(TxFactory):

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

    def add(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        return self.__single_address_method('add', contract_address, sender_address, address, tx_format)

    def remove(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        return self.__single_address_method('remove', contract_address, sender_address, address, tx_format)

    def activate(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        return self.__single_address_method('activate', contract_address, sender_address, address, tx_format)

    def deactivate(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        return self.__single_address_method('deactivate', contract_address, sender_address, address, tx_format)


    def time(self, contract_address, address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('time')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(address)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o



    def have(self, contract_address, address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('have')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(address)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o

    def is_active(self, contract_address, address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('isActive')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(address)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o


    def entry_count(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('entryCount')
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o

    def count(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        return self.entry_count(contract_address, sender_address=sender_address, id_generator=id_generator)
    
    def entry(self, contract_address, idx, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('entry')
        enc.typ(ABIContractType.UINT256)
        enc.uint256(idx)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o

    @classmethod
    def parse_account(self, v):
        return abi_decode_single(ABIContractType.ADDRESS, v)

    @classmethod
    def parse_entry_count(self, v):
        return abi_decode_single(ABIContractType.UINT256, v)

    @classmethod
    def parse_have(self, v):
        return abi_decode_single(ABIContractType.BOOLEAN, v)

    @classmethod
    def parse_add_request(self, v):
        v = strip_0x(v)
        cursor = 0
        enc = ABIContractEncoder()
        enc.method('add')
        enc.typ(ABIContractType.ADDRESS)
        r = enc.get()
        l = len(r)
        m = v[:l]
        if m != r:
            raise RequestMismatchException(v)
        cursor += l

        dec = ABIContractDecoder()
        dec.typ(ABIContractType.ADDRESS)
        dec.val(v[cursor:cursor + 64])
        r = dec.decode()
        return r
