#!/usr/bin/env python
from DictNameBuilder import DictNameBuilder
from EncryptionNameBuilder import EncryptionNameBuilder

if __name__ == "__main__":
    name_builder = DictNameBuilder()
    print name_builder.create_tag("test")

    name_builder = EncryptionNameBuilder()
    print name_builder.create_tag("test")
