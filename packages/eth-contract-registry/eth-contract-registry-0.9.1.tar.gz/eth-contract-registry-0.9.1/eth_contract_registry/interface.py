# standard imports
import logging

# external imports
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractType,
        abi_decode_single,
        )
from chainlib.eth.tx import TxFactory
from hexathon import (
        add_0x,
        )
from chainlib.eth.constant import (
        ZERO_ADDRESS,
        )

# local imports
from .encoding import (
        to_identifier,
    )

logg = logging.getLogger(__name__)

class Registry(TxFactory):

    def address_of(self, contract_address, identifier_string, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('addressOf')
        enc.typ(ABIContractType.BYTES32)
        identifier = to_identifier(identifier_string)
        logg.debug('identifier {} {}'.format(identifier, identifier_string))
        enc.bytes32(identifier)
        data = add_0x(enc.encode())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    @classmethod
    def parse_address_of(self, v):
        return abi_decode_single(ABIContractType.ADDRESS, v)
