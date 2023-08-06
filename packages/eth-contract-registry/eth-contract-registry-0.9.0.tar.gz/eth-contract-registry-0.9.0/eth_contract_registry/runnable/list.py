"""Set identifier value on contract registry

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import sys
import os
import logging

# external imports
import chainlib.eth.cli
from chainlib.chain import ChainSpec
from chainlib.eth.tx import receipt
from chainlib.eth.constant import ZERO_CONTENT
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.error import JSONRPCException
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
    config.add(config.get('_POSARG'), '_IDENTIFIER')
    return config


arg_flags = ArgFlag()
arg = Arg(arg_flags)
flags = arg_flags.STD_READ | arg_flags.EXEC

argparser = chainlib.eth.cli.ArgumentParser()
argparser = process_args(argparser, arg, flags)
argparser.add_argument('identifier', type=str, help='Contract identifier to look up')
args = argparser.parse_args()

logg = process_log(args, logg)

config = Config()
config = process_config(config, arg, args, flags, positional_name='identifier')
config = process_config_local(config, arg, args, flags)
logg.debug('config loaded:\n{}'.format(config))

settings = ChainSettings()
settings = process_settings(settings, config)
logg.debug('settings loaded:\n{}'.format(settings))


def out_element(e, w=sys.stdout):
    if config.get('_RAW'):
        w.write(e[1] + '\n')
    else:
        w.write(e[0] + '\t' + e[1] + '\n')


def element(ifc, conn, registry_address, identifier, w=sys.stdout):
    o = ifc.address_of(registry_address, identifier, sender_address=ZERO_ADDRESS)
    r =  conn.do(o)
    address = ifc.parse_address_of(r)
    out_element((identifier, address), w)


def ls(ifc, conn, registry_address, w=sys.stdout):
    i = 0
    while True:
        o = ifc.identifier(registry_address, i)
        try:
            r =  conn.do(o)
            identifier = ifc.parse_identifier(r)
            element(ifc, conn, registry_address, identifier, w)
            i += 1
        except JSONRPCException:
            break


def main():
    c = ContractRegistry(
            settings.get('CHAIN_SPEC')
            )

    identifier = config.get('_IDENTIFIER')

    registry_address = to_checksum_address(config.get('_EXEC_ADDRESS'))
    if not config.true('_UNSAFE') and strip_0x(registry_address) != strip_0x(config.get('_EXEC_ADDRESS')):
        raise ValueError('invalid checksum address for contract')

    if identifier != None:
        element(
            c,
            settings.get('CONN'),
            settings.get('EXEC'),
            config.get('_IDENTIFIER'),
            w=sys.stdout,
            )
    else:
        ls(
            c,
            settings.get('CONN'),
            settings.get('EXEC'),
            w=sys.stdout,
            )


if __name__ == '__main__':
    main()
