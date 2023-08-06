from __future__ import absolute_import

import pytest
from coderadar.pytest import CoverageReport


def test_CoverageReport():
    my_report = CoverageReport()
    assert isinstance(my_report, CoverageReport)
def test_coverage_file_empty(mocker):
    mocked_data = mocker.mock_open(read_data='')
    mocker.patch('builtins.open', mocked_data)

    my_report = CoverageReport()
    with pytest.raises(RuntimeError) as e:
        my_report.getTotalCoverage()
    assert 'empty' in str(e)

def test_coverage_file_no_data(mocker):
    mocked_data = mocker.mock_open(read_data='blah')
    mocker.patch('builtins.open', mocked_data)

    my_report = CoverageReport()
    with pytest.raises(RuntimeError) as e:
        my_report.getTotalCoverage()
    assert 'coverage' in str(e)