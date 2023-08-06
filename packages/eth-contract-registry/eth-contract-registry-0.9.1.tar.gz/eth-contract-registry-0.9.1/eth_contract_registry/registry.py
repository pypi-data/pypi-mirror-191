# standard imports
import os
import logging
import json
import hashlib

# third-party imports
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractType,
        abi_decode_single,
        )
from chainlib.chain import ChainSpec
from chainlib.eth.constant import (
        ZERO_ADDRESS,
        )
from chainlib.jsonrpc import JSONRPCRequest
from hexathon import (
        even,
        add_0x,
        )
from chainlib.eth.tx import TxFactory

# local imports
from .encoding import (
        to_identifier,
        from_identifier_hex,
        )
from .interface import Registry

logg = logging.getLogger(__name__)

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, 'data')


class ContractRegistry(Registry):

    default_chain_spec = None
    __chains_registry = {}

    __abi = None
    __bytecode = None

    @staticmethod
    def abi():
        if ContractRegistry.__abi == None:
            f = open(os.path.join(datadir, 'Registry.json'), 'r')
            ContractRegistry.__abi = json.load(f)
            f.close()
        return ContractRegistry.__abi


    @staticmethod
    def bytecode():
        if ContractRegistry.__bytecode == None:
            f = open(os.path.join(datadir, 'Registry.bin'))
            ContractRegistry.__bytecode = f.read()
            f.close()
        return ContractRegistry.__bytecode


    @staticmethod
    def gas(code=None):
        return 1500000


    def constructor(self, sender_address, identifier_strings=[]):
        # TODO: handle arrays in chainlib encode instead
        enc = ABIContractEncoder()
        enc.uint256(32)
        enc.uint256(len(identifier_strings))
        for s in identifier_strings:
            enc.bytes32(to_identifier(s))
        data = enc.get_contents()

        tx = self.template(sender_address, None, use_nonce=True)
        tx = self.set_code(tx, ContractRegistry.bytecode() + data)
        logg.debug('bytecode {}\ndata {}\ntx {}'.format(ContractRegistry.bytecode(), data, tx))
        return self.build(tx)


    @staticmethod
    def address(address=None):
        if address != None:
            ContractRegistry.__address = address
        return Registry.__address
        

    @staticmethod
    def load_for(chain_spec):
        chain_str = str(chain_spec)
        raise NotImplementedError()


    def set(self, contract_address, sender_address, identifier_string, address):
        enc = ABIContractEncoder()
        enc.method('set')
        enc.typ(ABIContractType.BYTES32)
        enc.typ(ABIContractType.ADDRESS)
        identifier = to_identifier(identifier_string)
        enc.bytes32(identifier)
        enc.address(address)
        data = enc.encode()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        return self.build(tx)


    def identifier(self, contract_address, idx, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('identifiers')
        enc.typ(ABIContractType.UINT256)
        enc.uint256(idx)
        data = add_0x(enc.encode())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    @classmethod
    def parse_identifier(self, v):
        return from_identifier_hex(v)
