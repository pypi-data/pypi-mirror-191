from __future__ import absolute_import

from coderadar.report import Report


def test_Report():
    my_report = Report()
    assert isinstance(my_report, Report)