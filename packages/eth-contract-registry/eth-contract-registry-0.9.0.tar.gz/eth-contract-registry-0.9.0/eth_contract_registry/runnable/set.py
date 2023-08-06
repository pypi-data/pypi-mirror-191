"""Set identifier value on contract registry

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import sys
import os
import logging
import hashlib

# external imports
import chainlib.eth.cli
from chainlib.chain import ChainSpec
from chainlib.eth.connection import EthHTTPConnection
from chainlib.eth.tx import receipt
from chainlib.eth.constant import ZERO_CONTENT
from chainlib.eth.address import to_checksum_address
from hexathon import (
        add_0x,
        strip_0x,
        )
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
from eth_contract_registry.registry import ContractRegistry

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()


def process_config_local(config, arg, args, flags):
    #hsh = strip_0x(args.chain_hash)
    #if len(hsh) != 64:
    #    raise ValueError('chain hash must be 32 bytes')
    #config.add(hsh, '_CHAIN_HASH')
    if len(config.get('_POSARG')) > 32:
        raise ValueError('identifier must be max 32 characters')
    config.add(config.get('_POSARG'), '_IDENTIFIER')
    return config


arg_flags = ArgFlag()
arg = Arg(arg_flags)
flags = arg_flags.STD_WRITE | arg_flags.EXEC | arg_flags.WALLET

argparser = chainlib.eth.cli.ArgumentParser()
argparser = process_args(argparser, arg, flags)
#argparser.add_argument('--chain-hash', type=str, default=ZERO_CONTENT, help='Chain config hash to use for entry')
argparser.add_argument('identifier', type=str, help='Contract identifier to set')
args = argparser.parse_args()

logg = process_log(args, logg)

config = Config()
config = process_config(config, arg, args, flags, positional_name='identifier')
config = process_config_local(config, arg, args, flags)
logg.debug('config loaded:\n{}'.format(config))

settings = ChainSettings()
settings = process_settings(settings, config)
logg.debug('settings loaded:\n{}'.format(settings))


def main():
    conn = settings.get('CONN')
    c = ContractRegistry(
            settings.get('CHAIN_SPEC'),
            signer=settings.get('SIGNER'),
            gas_oracle=settings.get('FEE_ORACLE'),
            nonce_oracle=settings.get('NONCE_ORACLE'),
            )

    (tx_hash_hex, o) = c.set(
            settings.get('EXEC'),
            settings.get('SENDER_ADDRESS'),
            config.get('_IDENTIFIER'),
            settings.get('RECIPIENT'),
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
