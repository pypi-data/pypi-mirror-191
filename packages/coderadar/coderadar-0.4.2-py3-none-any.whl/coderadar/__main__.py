'''Module to run Code Radar.'''

from __future__ import absolute_import

import sys
import os

from .report import Report

from .pylint import runPylint
from .pytest import runPytest
# from .flake8 import runFlake8
# from .gitlab import Gitlab
  

class CodeRadar(object):
    def __init__(self, package_name):
        self._package_name = package_name

    
    def analyze(self):
        runPytest(self._package_name)
        runPylint(self._package_name)
        
    def report(self):
        myReport = Report()
        myReport.summarizeCodeQuality(self._package_name)
        
    

def main():
    package_name = os.path.relpath(sys.argv[1])
    cr = CodeRadar(package_name)
    cr.analyze()
    cr.report()
    
    
# if __name__ == '__main__':
#     main()
    
