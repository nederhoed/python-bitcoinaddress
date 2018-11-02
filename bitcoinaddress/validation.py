"""Validate bitcoin/altcoin addresses

Copied from:
http://rosettacode.org/wiki/Bitcoin/address_validation#Python
"""

import string
from hashlib import sha256

digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def _bytes_to_long(bytestring, byteorder):
    """Convert a bytestring to a long

    For use in python version prior to 3.2
    """
    result = []
    if byteorder == 'little':
        result = (v << i * 8 for (i, v) in enumerate(bytestring))
    else:
        result = (v << i * 8 for (i, v) in enumerate(reversed(bytestring)))
    return sum(result)

def _long_to_bytes(n, length, byteorder):
    """Convert a long to a bytestring

    For use in python version prior to 3.2
    Source:
    http://bugs.python.org/issue16580#msg177208
    """
    if byteorder == 'little':
        indexes = range(length)
    else:
        indexes = reversed(range(length))
    return bytearray((n >> i * 8) & 0xff for i in indexes)

def decode_base58(bitcoin_address, length):
    """Decode a base58 encoded address

    This form of base58 decoding is bitcoind specific. Be careful outside of
    bitcoind context.
    """
    n = 0
    for char in bitcoin_address:
        try:
            n = n * 58 + digits58.index(char)
        except:
            msg = u"Character not part of Bitcoin's base58: '%s'"
            raise ValueError(msg % (char,))
    try:
        return n.to_bytes(length, 'big')
    except AttributeError:
        # Python version < 3.2
        return _long_to_bytes(n, length, 'big')

def encode_base58(bytestring):
    """Encode a bytestring to a base58 encoded string
    """
    # Count zero's
    zeros = 0
    for i in range(len(bytestring)):
        if bytestring[i] == 0:
            zeros += 1
        else:
            break
    try:
        n = int.from_bytes(bytestring, 'big')
    except AttributeError:
        # Python version < 3.2
        n = _bytes_to_long(bytestring, 'big')
    result = ''
    (n, rest) = divmod(n, 58)
    while n or rest:
        result += digits58[rest]
        (n, rest) = divmod(n, 58)
    return zeros * '1' + result[::-1]  # reverse string

def validate(bitcoin_address, decimal_prefixes=(0, 5)):
    """Check the integrity of a bitcoin address

    Returns True if the address is valid, False if not.

    >>> validate('1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i')
    True
    >>> validate('')
    False

    Arguments are the address (as a string) and the allowed decimal prefixes
    (the decimal 'version byte' or 'magic byte' that forms the first character
    of an address). The value of decimal_prefixes can be a single integer if
    only a single prefix should match (e.g. 0 to allow only P2PKH Bitcoin
    addresses), a tuple of integers for multiple prefixes (e.g.  (0, 5) for
    Bitcoin P2PKH and P2SH addresses) or None to allow any prefix. Default is
    (0, 5).

    For a list of prefixes, see (e.g.):

        https://github.com/libbitcoin/libbitcoin/wiki/Altcoin-Version-Mappings
    """
    if isinstance(decimal_prefixes, int):
        decimal_prefixes = (decimal_prefixes,)
    clen = len(bitcoin_address)
    if clen < 27 or clen > 35: # XXX or 34?
        return False
    allowed_first = tuple(string.digits)
    try:
        bcbytes = decode_base58(bitcoin_address, 25)
    except ValueError:
        return False
    # Allow None (or empty tuple, False, etc.) as value for decimal_prefixes to
    # skip version byte verification - suggestion by neonknight on GitHub
    if decimal_prefixes:
        # Check magic byte, by making this variable we support Bitcoin clones,
        # too - fix by Frederico Reiven
        for dp in decimal_prefixes:
            if bcbytes.startswith(chr(int(dp))):
                break
        else:
            return False
    # Compare checksum
    checksum = sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    if bcbytes[-4:] != checksum:
        return False
    # Encoded bytestring should be equal to the original address,
    # for example '14oLvT2' has a valid checksum, but is not a valid btc
    # address
    return bitcoin_address == encode_base58(bcbytes)
