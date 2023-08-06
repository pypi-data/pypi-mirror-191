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
from chainlib.eth.cli.arg import (
        Arg,
        ArgFlag,
        process_args,
        )
from chainlib.eth.cli.config import (
        Config,
        process_config,
        )
from chainlib.eth.cli.log import process_log
from chainlib.eth.settings import process_settings
from chainlib.settings import ChainSettings
from chainlib.eth.address import to_checksum_address

# local imports
from eth_accounts_index import AccountsIndex
from eth_accounts_index.registry import AccountRegistry

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()


def process_config_local(config, arg, args, flags):
    address = config.get('_POSARG')
    if address != None:
        address = to_checksum_address(address)
    config.add(address, '_ADDRESS')
    return config


arg_flags = ArgFlag()
arg = Arg(arg_flags)
flags = arg_flags.STD_READ | arg_flags.EXEC

argparser = chainlib.eth.cli.ArgumentParser()
argparser = process_args(argparser, arg, flags)
argparser.add_argument('address', type=str, help='Address to add to registry')
args = argparser.parse_args()

logg = process_log(args, logg)

config = Config()
config = process_config(config, arg, args, flags, positional_name='address')
config = process_config_local(config, arg, args, flags)
logg.debug('config loaded:\n{}'.format(config))

settings = ChainSettings()
settings = process_settings(settings, config)
logg.debug('settings loaded:\n{}'.format(settings))


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
    conn = settings.get('CONN')
    address = config.get('_ADDRESS')
    c = AccountsIndex(
            settings.get('CHAIN_SPEC')
            )
    if address != None:
        element(
                c,
                conn,
                settings.get('EXEC'),
                address,
                w=sys.stdout,
                )
    else:
        ls(
                c,
                conn,
                settings.get('EXEC'),
                w=sys.stdout,
                )


if __name__ == '__main__':
    main()
