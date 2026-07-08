import os

class BlockCipher:
    """
    A wrapper class that extends AES (or other compatible block ciphers) to support
    different block cipher modes of operation: ECB, CBC, CFB, and OFB.

    Parameters:
    - key (bytes): 16-byte encryption key
    - iv (bytes, optional): Initialization vector (IV) for applicable modes
    - algorithm (class, optional): AES-like class with encrypt/decrypt methods
    - mode (str): One of 'ECB', 'CBC', 'CFB', 'OFB'
    """
    def __init__(self, key, iv=None, algorithm=None, mode='ECB'):
        """
        Initialize BlockCipher with a key, mode, and optional IV and algorithm.
        """
        if len(key) != 16:
            raise ValueError("This teaching implementation expects a 16-byte AES-128 key.")

        if algorithm is None:
            from aes import AES
            algorithm = AES

        self.key = key
        self.mode = mode.upper()

        if self.mode == 'ECB':
            self.iv = None
        else:
            self.iv = iv if iv is not None else self.generate_iv()
            if len(self.iv) != 16:
                raise ValueError("IV must be 16 bytes for AES block modes.")

        self.algorithm = algorithm(key)

    def generate_iv(self):
        """
        Generate a cryptographically random 16-byte initialization vector (IV).
        """
        return os.urandom(16)

    def pad(self, data):
        """
        Apply PKCS#7 padding to the data to ensure it is a multiple of 16 bytes.
        """
        pad_len = 16 - (len(data) % 16)
        return data + bytes([pad_len] * pad_len)

    def unpad(self, data):
        """
        Remove PKCS#7 padding from the data.
        """
        if not data:
            raise ValueError("Invalid padding: empty plaintext")
        pad_len = data[-1]
        if pad_len < 1 or pad_len > 16 or data[-pad_len:] != bytes([pad_len] * pad_len):
            raise ValueError("Invalid padding")
        return data[:-pad_len]

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using the selected mode of operation.
        Supports ECB, CBC, CFB, and OFB.

        Returns:
        - ciphertext (bytes)
        """
        plaintext = self.pad(plaintext)
        ciphertext = b''
        iv = self.iv

        if self.mode == 'ECB':
            for i in range(0, len(plaintext), 16):
                block = plaintext[i:i+16]
                ciphertext += self.algorithm.encrypt(block)

        elif self.mode == 'CBC':
            for i in range(0, len(plaintext), 16):
                block = bytes(a ^ b for a, b in zip(plaintext[i:i+16], iv))
                block = self.algorithm.encrypt(block)
                ciphertext += block
                iv = block

        elif self.mode == 'CFB':
            for i in range(0, len(plaintext), 16):
                keystream = self.algorithm.encrypt(iv)
                block = bytes(a ^ b for a, b in zip(plaintext[i:i+16], keystream))
                ciphertext += block
                iv = block

        elif self.mode == 'OFB':
            for i in range(0, len(plaintext), 16):
                iv = self.algorithm.encrypt(iv)
                block = bytes(a ^ b for a, b in zip(plaintext[i:i+16], iv))
                ciphertext += block

        else:
            raise ValueError("Unsupported mode")

        return ciphertext

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using the selected mode of operation.
        Supports ECB, CBC, CFB, and OFB.

        Returns:
        - plaintext (bytes): Decrypted and unpadded original message
        """
        plaintext = b''
        iv = self.iv

        if self.mode == 'ECB':
            for i in range(0, len(ciphertext), 16):
                block = ciphertext[i:i+16]
                plaintext += self.algorithm.decrypt(block)

        elif self.mode == 'CBC':
            for i in range(0, len(ciphertext), 16):
                block = ciphertext[i:i+16]
                dec_block = self.algorithm.decrypt(block)
                plaintext += bytes(a ^ b for a, b in zip(dec_block, iv))
                iv = block

        elif self.mode == 'CFB':
            for i in range(0, len(ciphertext), 16):
                keystream = self.algorithm.encrypt(iv)
                block = ciphertext[i:i+16]
                plaintext += bytes(a ^ b for a, b in zip(block, keystream))
                iv = block

        elif self.mode == 'OFB':
            for i in range(0, len(ciphertext), 16):
                iv = self.algorithm.encrypt(iv)
                block = ciphertext[i:i+16]
                plaintext += bytes(a ^ b for a, b in zip(block, iv))

        else:
            raise ValueError("Unsupported mode")

        return self.unpad(plaintext)
