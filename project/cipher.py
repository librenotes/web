from Crypto.Cipher import AES
from Crypto import Random
import base64


class AESCipher:

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[AES.block_size:]))

    def pad(self, s):
        BS = 16
        if type(s) == str:
            s = s.encode('utf-8')
        remainder = (BS - len(s) % BS)
        pad = (chr(remainder) * remainder).encode('utf-8')
        padded_s = s + pad
        return padded_s

    def unpad(self, s):
        s = s[:-ord(s[len(s) - 1:])]
        return s
