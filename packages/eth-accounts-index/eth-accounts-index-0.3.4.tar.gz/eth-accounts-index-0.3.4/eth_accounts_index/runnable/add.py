"""Adds account entries to accounts index

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import os
import json
import argparse
import logging
import sys

# external imports
import chainlib.eth.cli
from chainlib.chain import ChainSpec
from chainlib.eth.connection import EthHTTPConnection
from chainlib.eth.tx import receipt
from chainlib.eth.address import to_checksum_address
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

# local imports
from eth_accounts_index.registry import AccountRegistry

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()


def process_config_local(config, arg, args, flags):
    address = to_checksum_address(config.get('_POSARG'))
    config.add(address, '_ADDRESS')
    return config


arg_flags = ArgFlag()
arg = Arg(arg_flags)
flags = arg_flags.STD_WRITE | arg_flags.EXEC 

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


def main():
    conn = settings.get('CONN')
    c = AccountRegistry(
            settings.get('CHAIN_SPEC'),
            signer=settings.get('SIGNER'),
            gas_oracle=settings.get('FEE_ORACLE'),
            nonce_oracle=settings.get('NONCE_ORACLE'),
            )

    (tx_hash_hex, o) = c.add(
            settings.get('EXEC'),
            settings.get('SENDER_ADDRESS'),
            config.get('_ADDRESS'),
            )

    if settings.get('RPC_SEND'):
        conn.do(o)
        if config.true('_WAIT'):
            r = conn.wait(tx_hash_hex)
            if r['status'] == 0:
                sys.stderr.write('EVM revert while deploying contract. Wish I had more to tell you')
                sys.exit(1)

        print(tx_hash_hex)
    else:
        print(o)


if __name__ == '__main__':
    main()
