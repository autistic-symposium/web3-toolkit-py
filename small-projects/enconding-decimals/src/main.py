#!/usr/bin/env python

import argparse


class Efun(object):

    def __init__(self):
        self.enc_byte = None
        self.dec_byte = None
        self.enc_range = [-8192, 8191]
        self.dec_range = [0x0000, 0x7F7F]

    def _decode(self, higher_byte, lower_byte):
        """
        Converts encoded hex value back into the original signed integer.

        Argument:
            higher_byte {string} -- higher byter hex input to be decoded.
            lower_byte {string} -- lower byter hex input to be decoded.

        Returns:
            Decoded value string in decimal base.
        """

        # Left shift 7 to get higher byte.
        higher_byte <<= 7

        # 'OR' byte withing the decimal lower limit.
        self.dec_byte = (lower_byte | higher_byte) + self.enc_range[0]

    def _encode(self, value):
        """
        Gets a signed integer and return a 4 character string,
        such that after the encoding is complete, the most
        significant bit of each byte has been cleared.

        Argument:
            value {string} -- integer input value to be encoded.

        Returns:
            Encoded 2-byte string.
        """

        # Add 8192 for unsigned
        sign_int = int(value)
        unsign_int = sign_int + 8192

        # 'AND' with 0b0000000001111111 for lower byte and
        # 'AND' with 0b0011111110000000 for higher byter
        lower_byte = unsign_int & 0x007F
        higher_byte = ((unsign_int & 0x3F80) << 1)

        # Return hex enconding of sum of the two bytes
        self.enc_byte = hex(lower_byte + higher_byte)

    def _extract_two_bytes(self, value):
        """
        Extract two bytes from a hexadecimal string.

        Arguments:
            value {hex} -- hexadecimal between 0x0000 and 0x7F7F.

        Returns:
            higher_byte, lower_byte -- byte strings.
        """

        # 'And' with 0b0000000001111111 for lower byte
        lower_byte = value & 0x00FF

        # Left shift 8 positions for higher byte
        higher_byte = value >> 8

        return higher_byte, lower_byte

    def run_decode(self, value):
        """
        Verifies if an input is valid 2-byte hexadecimal,
        returning its decoded value.

        Arguments:
            value {string} -- hexadecimal input value.

        Returns:
            None.
        """

        # Convert to hexadecimal.
        try:
            value = int(value, 16)

        except ValueError as e:
            print('Could not convert value to hexadecimal: {}.'.fomart(e))
            return -1

        # Verify whether the value is within the range,
        # and then decode it.
        if self.dec_range[0] <= value <= self.dec_range[1]:
            self._decode(*self._extract_two_bytes(value))
            print('{0} decodes as {1}'.format(hex(value), self.dec_byte))

        else:
            print('Value {0} is out of range of [{1}, {2}]'.format(hex(value),
                  hex(self.dec_range[0], hex(self.dec_range[1]))))

    def run_encode(self, value):
        """
        Verifies whether an input is valid 14-bit integer,
        returning its encoded value.

        Arguments:
            value {byte} -- 14-bit signed integer.

        Returns:
            None.
        """
        int_value = int.from_bytes(value, byteorder='big', signed=True)

        if self.enc_range[0] <= int_value <= self.enc_range[1]:
            self._encode(int_value)
            print('Value {0} encodes as {1}'.format(int_value, self.enc_byte))

        else:
            print('Value {0} out of range: {1}'.format(int_value, self.enc_byte))


def main():

    # Creater an instance of Efun().
    e = Efun()

    # Set strings for Argparse.
    description = 'Efun is an Art + Logic Enconding + Decoding application.'
    encode_help = 'Enter an INT value in the range {}.'.format(e.enc_range)
    decode_help = 'Enter an HEX value in the range {}.'.format(e.dec_range)

    # Run CLI menu.
    parser = argparse.ArgumentParser(description=description)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encode', type=int, help=encode_help)
    group.add_argument('-d', '--decode', help=decode_help)
    args = parser.parse_args()

    # Get the 14-byte input, enconde/decode it, and print results.
    bit_range = 14
    if args.encode:
        sig_bytes = args.encode.to_bytes(bit_range, byteorder='big', signed=True)
        e.run_encode(sig_bytes)
    else:
        e.run_decode(args.decode)


if __name__ == "__main__":
    main()
