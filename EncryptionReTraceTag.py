#!/usr/bin/python
from ReTraceWorker import RetraceWorker
from EncryptionNameBuilder import EncryptionNameBuilder

class EncryptionRetraceWorker(RetraceWorker):

    def __init__(self, retrace_file):
        RetraceWorker.__init__(self, retrace_file)
        self.decrypt = EncryptionNameBuilder()

    def get_original_value(self, key):
        return self.decrypt.decrypt_tag(key)
