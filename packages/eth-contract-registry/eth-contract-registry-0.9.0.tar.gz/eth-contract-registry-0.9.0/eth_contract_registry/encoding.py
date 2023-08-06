# standard imports
import logging

# external imports
from hexathon import strip_0x

logg = logging.getLogger(__name__)


def to_text(b):
        b = b[:b.find(0)]
        # TODO: why was this part of this method previously?
        # if len(b) % 2 > 0:
        #     b = b'\x00' + b
        return b.decode('utf-8')


def from_text(txt):
    return '0x{:0<64s}'.format(txt.encode('utf-8').hex())


def from_identifier(b):
    return to_text(b)


def from_identifier_hex(hx):
    b = bytes.fromhex(strip_0x(hx))
    return from_identifier(b)


def to_identifier(txt):
    return from_text(txt)
