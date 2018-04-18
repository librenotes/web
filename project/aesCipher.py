from Crypto.Cipher import AES
from Crypto import Random
import base64
# from werkzeug import

BS = 16
# pad = lambda s: "{}{}".format(s, (BS - len(s) % BS) * chr(BS - len(s) % BS))


def pad(s):
    remainder = (BS - len(s) % BS)
    padded_s = s + (chr(remainder)*remainder).encode('utf-8')
    return padded_s


unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[AES.block_size:]))
