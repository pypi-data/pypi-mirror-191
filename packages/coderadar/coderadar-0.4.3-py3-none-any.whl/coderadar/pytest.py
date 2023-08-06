'''Module for PyTest functionality.'''

from __future__ import absolute_import

import os
from ._functions import executeShell

    
def runPytest(package_name):
    print('Running PyTest...')
    
    cmd = ['python',
           '-m',
           'pytest',
           '-v',
           '--cov=%s' % package_name,
           '--cov-report=term',
           '--cov-report=xml',
           '--cov-branch']
    if os.path.exists('./tests'):
        test_dir = 'tests'
    elif os.path.exists('%s/tests' % package_name):
        test_dir = '%s/tests' % package_name
    
    coveragerc_path = '%s/.coveragerc' % test_dir
    if os.path.exists(coveragerc_path):
        cmd += ['--cov-config=%s' % coveragerc_path]
    
    cmd += [test_dir]
    print(' '.join(cmd))
    
    executeShell(cmd, save_output_as='coverage.txt')
        

class CoverageReport(object):
    def __init__(self, txt=None, xml=None):
        if txt is None:
            txt = 'coverage.txt'
        if xml is None:
            xml = 'coverage.xml'
            
        self._txt = txt 
        self._xml = xml 
        
        
    def getTxtUrl(self):
        return self._txt
    
    
    def getTotalCoverage(self):
        with open(self._txt) as f:
            lines = f.readlines()

        if len(lines) == 0:
            raise RuntimeError("File '%s' is empty!" % self._txt)

        # find the correct line in the coverage report and extract the total coverage
        in_coverage = False
        for line in lines:
            if '-- coverage:' in line:
                in_coverage = True
            if in_coverage and line[:5] == 'TOTAL':
                coverage = line.split()[-1]
                break
        if 'coverage' not in locals():
            raise RuntimeError("File '%s' does not contain Pytest coverage report!" % self._txt)
        return coverage
