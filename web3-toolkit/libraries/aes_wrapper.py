# -*- encoding: utf-8 -*-
# aes_cipher.py
# This class implements methods for AES cipher standard.


from Crypto import Random
from Crypto.Cipher import AES

from math_utils import str_to_bytes, b64encode, b64decode, hash256


class AESWrapper():

    def __init__(self, key: str, block_size=32) -> None:

        self.block_size = block_size

        # AES encryption needs a strong key. The stronger the key, the
        # stronger the encryption (meaning not easily guessable and with
        # enough entropy). The key is a string of 16, 24 or 32 bytes.
        self.key = hash256(key)

    #################
    # Private methods
    #################\

    def _create_iv(self) -> str:
        """
            AES needs an initialization vector (IV), which is generated
            with every encryption, with the purpose to disallow cryptanalysis
            of the ciphertext. The IV does not need  to be kept secret.
        """
        return Random.new().read(AES.block_size)

    def _pad(self, data: str) -> str:
        """
            AES is a block cipher, meaning that it encrypts data in blocks,
            and the data must be padded to fit the block size. The padding
            is done by adding bytes to the end of the data, with the value
            of the number of bytes added.
        """
        padding = (self.block_size - len(data) % self.block_size) * \
                    str_to_bytes(chr(self.block_size - len(data) % self.block_size))
        return data + padding

    def _unpad(self, data: str) -> str:
        """
            Unpadding is done by removing the number of bytes at the 
            end of the data, with the value of the last byte.
        """
        return data[:-ord(data[len(data) - 1:])]

    #################
    # Public methods
    #################
    def encrypt(self, raw: str) -> str:
        """Encrypt data."""
        data = self._pad(str_to_bytes(raw))
        iv = self._create_iv()
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(data))

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data."""
        data = b64decode(encrypted_data)
        iv = data[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(data[AES.block_size:])).decode('utf-8')


if __name__ == '__main__':

    key = '12345678901234567890123456789012'
    aes = AESWrapper(key)

    data = 'hello world'
    encrypted = aes.encrypt(data)
    print('Encrypted:', encrypted)

    decrypted = aes.decrypt(encrypted)
    print('Decrypted:', decrypted)
