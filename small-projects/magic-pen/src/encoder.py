# -*- coding: utf8 -*-

import logging as l

from src.utils import get_boundary_limits


def decoder(higher_byte, lower_byte):
    """
    Converts encoded hex value back into the original signed integer.

    Argument:
        higher_byte {string} -- higher byter hex input to be decoded.
        lower_byte {string} -- lower byter hex input to be decoded.

    Returns:
        Decoded value string in decimal base.
    """
    min_lim, _ = get_boundary_limits('enc')

    # Left shift 7 to get higher byte.
    higher_byte <<= 7

    # 'OR' byte withing the decimal lower limit.
    encoding_range = get_boundary_limits
    return (lower_byte | higher_byte) + min_lim


def encoder(value):
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
    _, max_lim = get_boundary_limits('enc')
    sign_int = int(value)
    unsign_int = sign_int + max_lim + 1

    # 'AND' with 0b0000000001111111 for lower byte and
    # 'AND' with 0b0011111110000000 for higher byter
    lower_byte = unsign_int & 0x007F
    higher_byte = ((unsign_int & 0x3F80) << 1)

    # Return hex encoding of the sum of the two bytes
    return hex(lower_byte + higher_byte)


def extract_two_bytes(value):
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


def run_decoder(input_hex):
    """
    Verifies if an input is valid 2-byte hexadecimal,
    returning its decoded value.

    Arguments:
        value {string} -- hexadecimal input value.

    Returns:
        Decoded byte or -1 (if error).
    """
    min_lim, max_lim = get_boundary_limits('dec')

    # Convert to hexadecimal.
    try:
        l.debug('Converting {} to decimal...'.format(input_hex))
        input_dec = int(input_hex, 16)
    except ValueError as e:
        l.error('Could not convert {0} decimal: {1}'.format(input_hex, e))
        return -1
        
    # Verify whether the input is within the range,
    # and then decode it.
    if min_lim <= input_dec <= max_lim:
        dec_byte = decoder(*extract_two_bytes(input_dec))
        l.debug('{0} decodes as {1}'.format(input_dec, dec_byte))
        return dec_byte

    else:
        l.debug('{0} is out of range of [{1}, {2}].'.format(input_dec,
                    hex(min_lim), hex(max_lim)))
        
        return -1


def run_encoder(value):
    """
    Verifies whether a byte input is a valid 14-bit integer, 
    returning its encoded value.

    Arguments:
        value {byte} -- 14-bit signed integer.

    Returns:
        Encoded byte or -1 (if error).
    """
    int_value = int.from_bytes(value, byteorder='big', signed=True)
    min_lim, max_lim = get_boundary_limits('enc')

    if min_lim <= int_value <= max_lim:
        enc_byte = encoder(int_value)
        l.debug('Value {0} encodes as {1}'.format(value, enc_byte))
        return enc_byte

    else:
        l.error(int('Value {0} out of range: {1}'.format(value, enc_byte)))
        return -1
