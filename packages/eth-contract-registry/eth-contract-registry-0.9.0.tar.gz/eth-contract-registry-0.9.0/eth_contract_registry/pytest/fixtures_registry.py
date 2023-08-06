# standard imports
import json
import logging
import hashlib

# external imports
from hexathon import add_0x
import pytest
from chainlib.connection import RPCConnection
from chainlib.eth.tx import receipt
from chainlib.eth.nonce import RPCNonceOracle

# local imports
from eth_contract_registry.registry import ContractRegistry
from eth_contract_registry.encoding import to_identifier

#logg = logging.getLogger(__name__)
logg = logging.getLogger()

valid_identifiers = [
        'ContractRegistry',
        ]


@pytest.fixture(scope='function')
def roles(
    eth_accounts,
    ):
    return {
        'DEFAULT': eth_accounts[0],
        'CONTRACT_DEPLOYER': eth_accounts[1],
        }


@pytest.fixture(scope='function')
def registry(
    default_chain_spec,
    default_chain_config,
    init_eth_tester,
    eth_rpc,
    eth_accounts,
    eth_signer,
    roles,
        ):
  
    nonce_oracle = RPCNonceOracle(roles['CONTRACT_DEPLOYER'], eth_rpc)

    builder = ContractRegistry(default_chain_spec, signer=eth_signer, nonce_oracle=nonce_oracle)
    logg.info('registering identifiers {} in contract registry'.format(valid_identifiers))
    (tx_hash_hex, o) = builder.constructor(roles['CONTRACT_DEPLOYER'], valid_identifiers)
    r = eth_rpc.do(o)
    
    o = receipt(r)
    rcpt = eth_rpc.do(o)
    assert rcpt['status'] == 1

    registry_address = rcpt['contract_address'] 

    c = ContractRegistry(default_chain_spec, signer=eth_signer, nonce_oracle=nonce_oracle)

    chain_spec_identifier = to_identifier(str(default_chain_spec))

    h = hashlib.new('sha256')
    j = json.dumps(default_chain_config)
    h.update(j.encode('utf-8'))
    z = h.digest()
    chain_config_digest = add_0x(z.hex())
    (tx_hash_hex, o) = c.set(registry_address, roles['CONTRACT_DEPLOYER'], 'ContractRegistry', registry_address)
    r = eth_rpc.do(o)
    o = receipt(tx_hash_hex)
    r = eth_rpc.do(o)
    assert r['status'] == 1

    return registry_address
