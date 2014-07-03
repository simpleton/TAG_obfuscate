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

    def _create_tag(self, key):
        encrypt_key = self.skey.encrypt(key)
        new_key = base64.b64encode(encrypt_key)
        return new_key

    def decrypt_tag(self, encrypted_tag):
        encrypt_key = base64.b64decode(encrypted_tag)
        original_tag = self.skey.decrypt(encrypt_key)
        return original_tag
