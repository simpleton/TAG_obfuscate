#!/usr/bin/python

from NameBuilder import *
from pyDes import *
import base64
import os

class EncryptionNameBuilder(NameBuilder):
    def __init__(self):
        NameBuilder.__init__(self)
        folder = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(folder, "skey.key"), "r") as fd:
            self.skey_string = fd.read().strip()
        self.skey = des(self.skey_string, CBC, "manifest", pad=None, padmode=PAD_PKCS5)
        self.cache = {}

    def _create_tag(self, key):
        encrypt_key = self.skey.encrypt(key)
        new_key = base64.b64encode(encrypt_key)
        new_key = "!{}@{}".format(len(new_key), new_key)
        return new_key

    def decrypt_tag(self, encrypted_tag):
        # hit cache
        key = encrypted_tag
        if key in self.cache:
            return self.cache[key]
        result = None
        if (encrypted_tag.startswith('!')):
            encrypted_tag = encrypted_tag[1:]
            _str_list = encrypted_tag.split("@")
            if (len(_str_list) > 1):
                estr_len = int(_str_list[0])
                _estr = encrypted_tag[len(_str_list[0]) + 1:len(_str_list[0]) + 1 + estr_len]
                _left_str = encrypted_tag[len(_str_list[0]) + 1 + estr_len:]

                encrypt_key = base64.b64decode(_estr)
                original_tag = self.skey.decrypt(encrypt_key)

                result = original_tag + _left_str
            else:
                result = encrypted_tag
        else:
            # didn't encrypt
            result = encrypted_tag
        self.cache[key] = result
        return result


if __name__ == "__main__":
    builder = EncryptionNameBuilder()
    print builder.decrypt_tag("!32@/B4Tb64lLpLv0CLSQhWm+q66vaS28Ftd")
    print builder.decrypt_tag("!44@/B4Tb64lLpJuhu2/ESJkabMJfH3i9t/DwyFrIHZgO+g=")
