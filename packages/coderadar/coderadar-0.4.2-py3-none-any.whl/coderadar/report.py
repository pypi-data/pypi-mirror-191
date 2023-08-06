'''Reporting Module.'''
import os.path

from .pylint import PylintReport
from .pytest import CoverageReport


class Report(object):
    def __init__(self):
        pass


    def _getNum(self, num):
        if type(num) is str:
            num = num[:-1] if num[-1] == '%' else num
            return float(num) if '.' in num else int(num)

        return num


    def _getDiffTxt(self, old, new):
        if type(old) is str:
            postfix = '%' if old[-1] == '%' else ''
        else:
            postfix = ''
        old = self._getNum(old)
        new = self._getNum(new)
        if type(old) is int:
            txt = ' (%+i%s)' % (new-old, postfix)
        else:
            txt = ' (%+.2f%s)' % (new-old, postfix)
        return txt


    def _getDiffHtml(self, old, new, better=+1):
        if type(old) is str:
            postfix = '%' if old[-1] == '%' else ''
        else:
            postfix = ''
        old = self._getNum(old)
        new = self._getNum(new)
        color = {-1: 'red',
                 1: 'green',
                 0: '#666'}[-1 if (new-old)*better < 0 else (1 if (new-old)*better > 0 else 0)]
        if type(old) is int:
            html = ' (<span style="color:%s">%+i%s</span>)' % (color, new - old, postfix)
        else:
            html = ' (<span style="color:%s">%+.2f%s</span>)' % (color, new - old, postfix)
        return html


    def _getReportTemplateTxt(self):
        template = """
Code Quality Report
<package_name>
--------------------------------------------------
Pytest:
  Test coverage: <coverage><coverage_diff>
 
--------------------------------------------------
Pylint Score:  <pylint_score>/10<pylint_score_diff> 
  Missing docstrings:             <missing_docstrings><missing_docstrings_diff> 
 
  Needs Refactoring:
    Too complex:                  <too_complex_num><too_complex_num_diff> (max cyclomatic complexity=<too_complex_max><too_complex_max_diff>)
                                    <too_complex_file>: <too_complex_obj> (line <too_complex_line>)
    Function too long (LoC/func): <func_too_long_num><func_too_long_num_diff> (max LoC/func=<func_too_long_max><func_too_long_max_diff>)
                                    <func_too_long_file>: <func_too_long_obj> (line <func_too_long_line>)
    Duplicate code:               <duplicate_code> block(s)<duplicate_code_diff>
                                    <duplicate_code_lines> lines in <duplicate_code_num> modules:
                                    <duplicate_code_files>
 
  Obsolete code:
    Unused imports:             <unused_imports><unused_imports_diff>
                                  <unused_imports_file>
                                  <unused_imports_num> imports: <unused_imports_items>
    Unused variables:           <unused_variables><unused_variables_diff>
                                  <unused_variables_file>
                                  <unused_variables_num> variables: <unused_variables_items>
    Unused arguments:           <unused_arguments><unused_arguments_diff>
                                  <unused_arguments_file>
                                  <unused_arguments_num> arguments: <unused_arguments_items>
    Unreachable code:           <unreachable_code><unreachable_code_diff>
                                  <unreachable_code_file>
                                  <unreachable_code_num> block(s): <unreachable_code_items>
--------------------------------------------------
"""
        return template


    def _getReportTemplateHtml(self):
        template = """<html><body>
<head>
<style>
    td {vertical-align: top;}
    td:first-child {white-space: nowrap;}
    div.details {font-size: 90%; color: #666; margin-left:10px;}
    em.code {font-style:normal; font-family: monospace, monospace;}
    .logo {font-size:small; color:#BBB; font-style:italic;font-family:sans-serif; text-decoration: none;}
    a.logo {font-variant: small-caps;}
    a.logo:hover {color: #B33; text-decoration: underline;}
</style>
</head>
<div style='margin: 0 auto; width: 900px;'>
<div style='display: table; margin: 0 auto;'>
<h1>Code Quality Report</h1>
<package_name>
<hr>
<h2>Pytest <span style='font-weight: normal; font-size: medium;'>(<a href='<pytest_report_url>'>Report</a>)</span></h2>
<table>
<tr><td>Test coverage:</td><td><coverage><coverage_diff></td></tr>
</table>

<hr>
<h2>Pylint <span style='font-weight: normal; font-size: medium;'>(Score: <pylint_score>/10<pylint_score_diff>; <a href='<pylint_report_url>'>Report</a>)</span></h2>

<table>
<tr><td>Missing docstrings:</td><td><missing_docstrings><missing_docstrings_diff></td></tr>

<tr><td span=2>&nbsp;</td></tr>
<tr><td span=2><b>Needs Refactoring:</b></td></tr>
<tr><td style='padding: 0 10px;'>Too complex:</td><td><too_complex_num><too_complex_num_diff> (max cyclomatic complexity=<too_complex_max><too_complex_max_diff>)<br/>
  <div class='details'><em class='code'><too_complex_file></em>: <em class='code'><too_complex_obj></em> (line <too_complex_line>)</div></td></tr>
<tr><td style='padding: 0 10px;'>Function too long (LoC/func):</td><td><func_too_long_num><func_too_long_num_diff> (max LoC/func=<func_too_long_max><func_too_long_max_diff>)<br/>
  <div class='details'><em class='code'><func_too_long_file></em>: <em class='code'><func_too_long_obj></em> (line <func_too_long_line>)</div></td></tr>
<tr><td style='padding: 0 10px;'>Duplicate code:</td><td><duplicate_code> block(s)<duplicate_code_diff><br/>
  <div class='details'><duplicate_code_lines> lines in <duplicate_code_num> modules:<br/><em class='code'><duplicate_code_files></em></div></td></tr>

<tr><td span=2>&nbsp;</td></tr>
<tr><td span=2><b>Obsolete code:</b></td></tr>
<tr><td style='padding: 0 10px;'>Unused imports:</td><td><unused_imports><unused_imports_diff><br/>
  <div class='details'><em class='code'><unused_imports_file></em><br/><unused_imports_num> import(s): <em style='code'><unused_imports_items></em></div></td></tr>
<tr><td style='padding: 0 10px;'>Unused variables:</td><td><unused_variables><unused_variables_diff><br/>
  <div class='details'><em class='code'><unused_variables_file></em><br/><unused_variables_num> variable(s): <em style='code'><unused_variables_items></em></div></td></tr>
<tr><td style='padding: 0 10px;'>Unused arguments:</td><td><unused_arguments><unused_arguments_diff><br/>
  <div class='details'><em class='code'><unused_arguments_file></em><br/><unused_arguments_num> arguments(s): <em style='code'><unused_arguments_items></em></div></td></tr>
<tr><td style='padding: 0 10px;'>Unreachable code:</td><td><unreachable_code><unreachable_code_diff><br/>
  <div class='details'><em class='code'><unreachable_code_file></em><br/><unreachable_code_num> block(s): <em style='code'><unreachable_code_items></em></div></td></tr>
</table>         
<hr>
<span style='float:right;' class='logo'>generated with <a href='https://gitlab.com/ck2go/coderadar' class='logo'>CodeRadar</a></span>
</div>
</body></html>"""
        return template
      
      
    def getReportTemplate(self, report_type='txt'):
        if report_type.lower() == 'txt':
            template = self._getReportTemplateTxt()
        elif report_type.lower() == 'html':
            template = self._getReportTemplateHtml()
        return template


    def _replacePlacehlder(self, report, placeholder, actual_results, method_name, previous_results=None, arg=None, better=None):
        if arg is None:
            actual_val = getattr(actual_results, method_name)()
        else:
            actual_val = getattr(actual_results, method_name)()[arg]

        report = report.replace('<%s>' % placeholder,
                                str(actual_val))
        if previous_results:
            if arg is None:
                previous_val = getattr(previous_results, method_name)()
            else:
                previous_val = getattr(previous_results, method_name)()[arg]
            if report[1:5] == 'html':
                report = report.replace('<%s_diff>' % placeholder,
                                        self._getDiffHtml(previous_val, actual_val, better))
            else:
                report = report.replace('<%s_diff>' % placeholder,
                                        self._getDiffTxt(previous_val, actual_val))
        return report


    def _fillTemplate(self, report, package_name, coverage, pylint, previous_coverage, previous_pylint):
        report = report.replace('<package_name>', str(package_name))
        report = report.replace('<pytest_report_url>', str(coverage.getTxtUrl()))

        report = self._replacePlacehlder(report, 'coverage', coverage, 'getTotalCoverage', previous_coverage, better=+1)

        report = self._replacePlacehlder(report, 'pylint_score', pylint, 'getScore', previous_pylint, better=+1)

        report = report.replace('<pylint_report_url>', str(pylint.getTxtUrl()))
        report = self._replacePlacehlder(report, 'missing_docstrings', pylint, 'getMissingDocstrings', previous_pylint, better=-1)
        report = self._replacePlacehlder(report, 'too_complex_num', pylint, 'getTooComplex', previous_pylint, arg=0, better=-1)
        report = self._replacePlacehlder(report, 'too_complex_max', pylint, 'getTooComplex', previous_pylint, arg=1, better=-1)
        report = report.replace('<too_complex_file>', str(pylint.getTooComplex()[2]))
        report = report.replace('<too_complex_obj>', str(pylint.getTooComplex()[3]))
        report = report.replace('<too_complex_line>', str(pylint.getTooComplex()[4]))
        report = self._replacePlacehlder(report, 'func_too_long_num', pylint, 'getTooManyStatements', previous_pylint, arg=0, better=-1)
        report = self._replacePlacehlder(report, 'func_too_long_max', pylint, 'getTooManyStatements', previous_pylint, arg=1, better=-1)
        report = report.replace('<func_too_long_file>', str(pylint.getTooManyStatements()[2]))
        report = report.replace('<func_too_long_obj>', str(pylint.getTooManyStatements()[3]))
        report = report.replace('<func_too_long_line>', str(pylint.getTooManyStatements()[4]))
        report = self._replacePlacehlder(report, 'duplicate_code', pylint, 'getDuplicateCode', previous_pylint, arg=0, better=-1)
        report = report.replace('<duplicate_code_num>', str(pylint.getDuplicateCode()[1]))
        report = report.replace('<duplicate_code_files>', ', '.join(pylint.getDuplicateCode()[2]))
        report = report.replace('<duplicate_code_lines>', str(pylint.getDuplicateCode()[3]))
        report = self._replacePlacehlder(report, 'unused_imports', pylint, 'getUnusedImports', previous_pylint, arg=0, better=-1)
        report = report.replace('<unused_imports_file>', str(pylint.getUnusedImports()[1]))
        report = report.replace('<unused_imports_num>', str(pylint.getUnusedImports()[2]))
        report = report.replace('<unused_imports_items>', ', '.join(pylint.getUnusedImports()[3]))
        report = self._replacePlacehlder(report, 'unused_variables', pylint, 'getUnusedVariables', previous_pylint, arg=0, better=-1)
        report = report.replace('<unused_variables_file>', str(pylint.getUnusedVariables()[1]))
        report = report.replace('<unused_variables_num>', str(pylint.getUnusedVariables()[2]))
        report = report.replace('<unused_variables_items>', ', '.join(pylint.getUnusedVariables()[3]))
        report = self._replacePlacehlder(report, 'unused_arguments', pylint, 'getUnusedArguments', previous_pylint, arg=0, better=-1)
        report = report.replace('<unused_arguments_file>', str(pylint.getUnusedArguments()[1]))
        report = report.replace('<unused_arguments_num>', str(pylint.getUnusedArguments()[2]))
        report = report.replace('<unused_arguments_items>', ', '.join(pylint.getUnusedArguments()[3]))
        report = self._replacePlacehlder(report, 'unreachable_code', pylint, 'getUnreachableCode', previous_pylint, arg=0, better=-1)
        report = report.replace('<unreachable_code_file>', str(pylint.getUnreachableCode()[1]))
        report = report.replace('<unreachable_code_num>', str(pylint.getUnreachableCode()[2]))
        report = report.replace('<unreachable_code_items>', ', '.join(pylint.getUnreachableCode()[3]))
        return report
    
    
    def summarizeCodeQuality(self, package_name):
        coverage = CoverageReport()
        previous_coverage_file = 'last_run/coverage'
        if os.path.exists(previous_coverage_file+'.txt'):
            previous_coverage = CoverageReport(txt=previous_coverage_file+'.txt', xml=previous_coverage_file+'.xml')
        else:
            previous_coverage = None

        pylint = PylintReport()
        previous_pylint_file = 'last_run/pylint'
        if os.path.exists(previous_pylint_file+'.txt'):
            previous_pylint = PylintReport(txt=previous_pylint_file+'.txt', json=previous_pylint_file+'.json')
        else:
            previous_pylint = None

        report_txt = self.getReportTemplate(report_type='txt')
        report_txt = self._fillTemplate(report_txt, package_name, coverage, pylint, previous_coverage, previous_pylint)
        print(report_txt)
        with open('code_quality_report.txt', 'w') as f:
            f.write(report_txt)
        
        report_html = self.getReportTemplate(report_type='html')
        report_html = self._fillTemplate(report_html, package_name, coverage, pylint, previous_coverage, previous_pylint)
        with open('code_quality_report.html', 'w') as f:
            f.write(report_html)
            