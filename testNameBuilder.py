#!/usr/bin/env python
from DictNameBuilder import DictNameBuilder
from EncryptionNameBuilder import EncryptionNameBuilder

if __name__ == "__main__":
    name_builder = DictNameBuilder()
    print name_builder.create_tag("test")

    name_builder = EncryptionNameBuilder()
    encrypted_key = name_builder.create_tag("test")
    print encrypted_key
    print name_builder.decrypt_tag(encrypted_key)
