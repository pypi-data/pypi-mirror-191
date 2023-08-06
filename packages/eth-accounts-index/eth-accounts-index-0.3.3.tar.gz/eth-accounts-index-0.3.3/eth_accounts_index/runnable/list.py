"""Query account index state

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import sys
import os
import json
import argparse
import logging

# external imports
import chainlib.eth.cli
from chainlib.chain import ChainSpec
from chainlib.eth.connection import EthHTTPConnection
from chainlib.eth.tx import receipt
from chainlib.eth.constant import ZERO_CONTENT
from chainlib.error import JSONRPCException

# local imports
from eth_accounts_index import AccountsIndex
from eth_accounts_index.registry import AccountRegistry

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

arg_flags = chainlib.eth.cli.argflag_std_write | chainlib.eth.cli.Flag.EXEC
argparser = chainlib.eth.cli.ArgumentParser(arg_flags)
argparser.add_positional('address', required=False, type=str, help='Check only whether given address is in registry')
args = argparser.parse_args()

extra_args = {
    'address': None,
        }
config = chainlib.eth.cli.Config.from_args(args, arg_flags, extra_args=extra_args, default_fee_limit=AccountRegistry.gas())

wallet = chainlib.eth.cli.Wallet()
wallet.from_config(config)

rpc = chainlib.eth.cli.Rpc(wallet=wallet)
conn = rpc.connect_by_config(config)

chain_spec = ChainSpec.from_chain_str(config.get('CHAIN_SPEC'))


def out_element(e, w=sys.stdout):
    w.write(str(e[1]) + '\n')


def element(ifc, conn, contract_address, address, w=sys.stdout):
    o = ifc.have(contract_address, address)
    r =  conn.do(o)
    have = ifc.parse_have(r)
    out_element((0, address), w)


def ls(ifc, conn, contract_address, w=sys.stdout):
    i = 0
    while True:
        o = ifc.entry(contract_address, i)
        try:
            r = conn.do(o)
            account = ifc.parse_account(r)
            out_element((i, account), w)
            i += 1
        except JSONRPCException as e:
            break


def main():
    address = config.get('_ADDRESS')
    contract_address = config.get('_EXEC_ADDRESS')
    c = AccountsIndex(chain_spec)
    if address != None:
        element(c, conn, contract_address, address, w=sys.stdout)
    else:
        ls(c, conn, contract_address, w=sys.stdout)


if __name__ == '__main__':
    main()
