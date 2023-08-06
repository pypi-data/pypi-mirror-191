from __future__ import absolute_import

from coderadar.pylint import PylintReport
import pytest


class TestPylintReport():
    

    def setup_class(self):
        pass

    def teardown_class(self):
        pass
        
    def setup_method(self, test_method):
        pass
    
    def teardown_method(self, test_method):
        pass


    def test_init(self, mocker):
        mock_load_report = mocker.patch('coderadar.pylint.PylintReport._loadJsonReport')
        my_report = PylintReport()
        assert isinstance(my_report, PylintReport)

    def test_json_empty(self, mocker):
        mock_open_report_file = mocker.patch('builtins.open')
        mock_open_report_file.return_value.read.return_value = ''
        mock_getsize = mocker.patch('os.path.getsize')
        mock_getsize.return_value = 0

        with pytest.raises(RuntimeError) as e:
            my_report = PylintReport()
        assert 'empty' in str(e)


    def test_json_invalid(self, mocker):
        mock_open_report_file = mocker.patch('builtins.open')
        mock_open_report_file.return_value.read.return_value = 'blah'
        mock_getsize = mocker.patch('os.path.getsize')
        mock_getsize.return_value = 5

        with pytest.raises(RuntimeError) as e:
            my_report = PylintReport()
        assert 'decode' in str(e)

    def test_loadJsonReport(self, mocker):
        mocked_data = mocker.mock_open(read_data='[\n{"test": 1},\n{"testb": 2}\n]')
        mocker.patch('builtins.open', mocked_data)

        my_report = PylintReport()
        assert isinstance(my_report._report, list)
