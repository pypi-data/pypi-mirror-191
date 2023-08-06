# Copyright (c) 2017 Pieter Wuille
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Based on this specification from Pieter Wuille:
# https://github.com/sipa/bips/blob/bip-bech32m/bip-bech32m.mediawiki

# Based on this specification from chia-blockchain:
# https://github.com/Chia-Network/chia-blockchain/blob/main/chia/util/bech32m.py

"""Reference implementation for Bech32m and segwit addresses."""

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def bech32_polymod(values) -> int:
    """Internal function that computes the Bech32 checksum."""
    generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk


def bech32_hrp_expand(hrp: str):
    """Expand the HRP into values for checksum computation."""
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


M = 0x2BC830A3


def bech32_verify_checksum(hrp: str, data) -> bool:
    return bech32_polymod(bech32_hrp_expand(hrp) + data) == M


def bech32_create_checksum(hrp: str, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ M
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def bech32_encode(hrp: str, data) -> str:
    """Compute a Bech32 string given HRP and data values."""
    hrp=hrp.lower() if hrp else "xch"
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + "1" + "".join([CHARSET[d] for d in combined])


def bech32_decode(bech: str, max_length: int = 90):
    """Validate a Bech32 string, and determine HRP and data."""
    bech = bech.strip()
    if (any(ord(x) < 33 or ord(x) > 126 for x in bech)) or (bech.lower() != bech and bech.upper() != bech):
        return (None, None)
    bech = bech.lower()
    pos = bech.rfind("1")
    if pos < 1 or pos + 7 > len(bech) or len(bech) > max_length:
        return (None, None)
    if not all(x in CHARSET for x in bech[pos + 1 :]):
        return (None, None)
    hrp = bech[:pos]
    data = [CHARSET.find(x) for x in bech[pos + 1 :]]
    if not bech32_verify_checksum(hrp, data):
        return (None, None)
    return hrp, data[:-6]


def convertbits(data, frombits: int, tobits: int, pad: bool = True):
    """General power-of-2 base conversion."""
    if pad:
        data=bytes.fromhex(data.lower()) if data[0:2].lower()!="0x" else bytes.fromhex(data[2:].lower())
    else:
        data=data
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            raise ValueError("Invalid Value")
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        raise ValueError("Invalid bits")
    return ret


def encode_puzzle_hash(puzzle_hash, prefix: str) -> str:
    encoded = bech32_encode(prefix, convertbits(puzzle_hash, 8, 5))
    return encoded


def decode_puzzle_hash(address: str):
    hrpgot, data = bech32_decode(address)
    if data is None:
        raise ValueError("Invalid Address")
    decoded = convertbits(data, 5, 8, False)
    _decoded="".join([ "0"+str(hex(i))[2:] if len(str(hex(i))[2:])==1 else str(hex(i))[2:] for i in decoded ])
    return _decoded

def encode(puzzle_hash, prefix: str):
    return encode_puzzle_hash(puzzle_hash, prefix)

def decode(address: str):
    return decode_puzzle_hash(address)