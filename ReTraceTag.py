#!/usr/bin/python
import os
import fileinput
import re
import util
from Replacement import Replacement
from DictReTraceTag import DictRetraceWorker
from EncryptionReTraceTag import EncryptionRetraceWorker

class Retrace(object):
    def __init__(self, worker, root_folder):
        self.worker = worker
        self.root_folder = root_folder
        self.suffix_list = ['*.log', '*.savelog.txt']
        return;

    def run(self):
        log_files = []
        for suffix in self.suffix_list:
            log_files.extend(util.find_all_files_with_suffix(self.root_folder, suffix))
            log_files.extend(util.find_all_files_with_suffix(self.root_folder, suffix))

        for log_file in log_files:
            retrace.retrace(log_file)
        return;

if __name__ == "__main__":
#    worker = EncryptionRetraceWorker(retrace_file = "TagMapping.txt")
    worker = DictRetraceWorker(retrace_file = "TagMapping.txt")
    retracer = Retrace(worker, "./")
    retracer.run()
