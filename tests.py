"""\
General tests on general functions in python-sisow
"""
from unittest import TestCase

import bitcoinaddress


class TestLongToBytes(TestCase):
    def test_example(self):
        n = 2491969579123783355964723219455906992268673266682165637887
        self.assertEqual(bitcoinaddress._long_to_bytes(n, 25, 'big'),
                         b'\x00e\xa1`Y\x86J/\xdb\xc7\xc9\x9aG#\xa89[\xc6\xf1\x88\xeb\xc0F\xb2\xff')


class TestBytesToLong(TestCase):
    def test_example(self):
        b = b'\x00e\xa1`Y\x86J/\xdb\xc7\xc9\x9aG#\xa89[\xc6\xf1\x88\xeb\xc0F\xb2\xff'
        self.assertEqual(bitcoinaddress._bytes_to_long(bytearray(b), 'big'),
                         2491969579123783355964723219455906992268673266682165637887)


class TestInvalidNotorious(TestCase):
    """Valid by hash calculation, not valid by format """
    def setUp(self):
        self.addresses = [
            '14oLvT2',  # padding omitted
            '111111111111111111114oLvT2',  # padding too short
#            'miwxGypTcHDXT3m4avmrMMC4co7XWqbG9r',  # invalid first character
            '31uEbMgunupShBVTewXjtqbBv5MndwfXhb',  # from https://en.bitcoin.it/wiki/Address but invalid!
            '175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W',  # from wikipedia article, but invalid
        ]
    
    def test_invalid(self):
        for bitcoin_address in self.addresses:
            self.assertFalse(bitcoinaddress.validate(bitcoin_address))


class TestInvalidLitecoin(TestCase):
    """Valid litecoin addresses should not be considered valid for bitcoins """
    def setUp(self):
        self.addresses = [
            'LRNYxwQsHpm2A1VhawrJQti3nUkPN7vtq3',
            'LRM8qA2YH5cdYDWhFMDLE7GHcW2YmXPT5m',
        ]

    def test_invalid(self):
        for bitcoin_address in self.addresses:
            self.assertFalse(bitcoinaddress.validate(bitcoin_address))


class TestValid(TestCase):
    def setUp(self):
        self.addresses = [
            '1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i',
            '1111111111111111111114oLvT2',
            '17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j',
            '1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i',
            '1Eym7pyJcaambv8FG4ZoU8A4xsiL9us2zz',
            '1cYxzmWaSsjdrfTqzJ1zTXtR7k8je9qVv',
            '12HzMcHURwmAxAkfWgtktYsF3vRTkBz4F3',
            '1GHATvgY4apPiBqmGkqfM3vWCbqtGAwKQ9',
            '3NukJ6fYZJ5Kk8bPjycAnruZkE5Q7UW7i8',
        ]
    
    def test_valid(self):
        for bitcoin_address in self.addresses:
            self.assertTrue(bitcoinaddress.validate(bitcoin_address))


class TestInvalid(TestCase):
    def setUp(self):
        valid = '1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i'
        self.addresses = [
            '',
            ' 1C9wCniTU7PP7NLhFFHhMQfhmkqdY37zuP',  # leading space
            '1C9wCniTU7PP7NLhFFHhMQfhmkqdY37zuP ',  # trailing space
            '1C9wCniTU7PP7NLhFFHhMQfhmkqdY37zu?',  # unknown base58 character
            '12HzMcHURwmAxAkfWgtktYsF3vRTkBz4F4',
            valid.replace('N', 'P', 1),
            'mpc1rKeaMSCuQnJevMViLuq8uWjHwgdjiV', # testnet invalid by default
        ]
    
    def test_invalid(self):
        for bitcoin_address in self.addresses:
            self.assertFalse(bitcoinaddress.validate(bitcoin_address))


class TestValidTestnet(TestCase):
    def test_valid(self):
        self.assertTrue(bitcoinaddress.validate(
            'mpc1rKeaMSCuQnJevMViLuq8uWjHwgdjiV', allow_testnet=True))

if __name__ == '__main__':
    from unittest import main
    main()
