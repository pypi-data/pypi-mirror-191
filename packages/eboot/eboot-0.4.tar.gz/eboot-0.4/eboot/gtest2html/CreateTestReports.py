#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from eboot.PlatformEnvirConfigs import configs
from eboot.gtest2html import ConvertTestReport


class CTestsTemplate(object):
    """
        html Template Report
    """
    HTML_TEMP = r"""
        <!DOCTYPE html>
        <html lang="zh-cn">
        <head>
            <meta charset="UTF-8">
            <title>Test Report</title>
            <link type="text/css" href="./script/css/report.css" rel="stylesheet">
        </head>
        <body>
            <table class="gridtable">
                <colgroup>
                    <col align="left"/>
                    <col align="right"/>
                    <col align="right"/>
                    <col align="right"/>
                    <col align="right"/>
                    <col align="right"/>
                    <col align="right"/>
                </colgroup>
                <tr><th>Module Name</th>
                    <th>Total</th>
                    <th>Pass</th>
                    <th>Fail</th>
                    <th>Error</th>
                    <th>Disabled</th>
                    <th>View</th></tr>
                %(table_tr)s</table>
        </body>
        </html>"""

    TABLE_TEMP = """
        <tr><td align="center">%(module)s</td>
            <td align="center"><font color="blue">%(total)s</font></td>
            <td align="center"><font color="green">%(passed)s</font></td>
            <td align="center"><font color="red">%(fail)s</font></td>
            <td align="center"><font color="red">%(error)s</font></td>
            <td align="center"><font color="blue">%(disabled)s</font></td>
            <td align="center"><font color="green"><a href="%(project_url)sws/test_reports/%(link)s">detail</a></font>
        </td></tr>"""


def CreateTestReports(dirName):
    try:
        root_path = configs.get('ROOT_PATH')

        html = CTestsTemplate()
        table_tr = ''

        reports_path = os.path.join(root_path, dirName)
        if not os.path.exists(reports_path):
            os.mkdir(reports_path)

        for file in os.listdir(reports_path):
            file_path = os.path.join(reports_path, file)
            if os.path.isdir(file_path):
                continue

            name, ext = os.path.splitext(file)
            if ext == '.xml' and name.startswith('test_'):
                test_info = ConvertTestReport.ConvertTestReport(
                    reports_path, file)

                error_count = int(test_info.get('tests')) - int(test_info.get('failures')) - \
                    int(test_info.get('disabled')) - \
                    int(test_info.get('errors'))
                # generate html table
                table_td = html.TABLE_TEMP % dict(module=name,
                                                  total=str(
                                                      test_info.get('tests')),
                                                  passed=str(error_count),
                                                  fail=str(
                                                      test_info.get('failures')),
                                                  error=str(
                                                      test_info.get('errors')),
                                                  disabled=str(
                                                      test_info.get('disabled')),
                                                  project_url=os.getenv(
                                                      'JOB_URL'),
                                                  link=name+'.html')
                table_tr += table_td
        if len(table_tr) > 0:
            report = html.HTML_TEMP % dict(table_tr=table_tr)
            file_name = os.path.join(reports_path, 'test_reports.html')
            with open(file_name, 'w') as fp:
                fp.write(report)
    except IOError as e:
        print('raise error %s ' % str(e))
