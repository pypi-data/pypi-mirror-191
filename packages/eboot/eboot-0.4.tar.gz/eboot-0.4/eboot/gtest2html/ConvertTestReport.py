#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import xml.etree.ElementTree as ElementTree
from eboot.PlatformEnvirConfigs import configs


class CTestReportTemplate(object):
    """
        html Template Report
    """
    TEST_HTML_TEMP = r"""
        <!DOCTYPE html>
        <html lang="zh-cn">
        <head>
            <meta charset="UTF-8">
            <title>Test Report</title>
            <link href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css" rel="stylesheet">
            <script src="https://cdn.bootcss.com/echarts/3.8.5/echarts.common.min.js"></script>
            <style media="screen" type="text/css">%(css)s</style>
        </head>
        <body>
        <div class="container-fluid">
            <div class="row"><div class="col col-lg-12"><h1 style="text-align:center">Test Report Detail</h1></div></div>
            <div class="row">
            <div class="col col-lg-8">
                    <h3 class='attribute'><strong>Test Run Time:&#8194</strong>%(test_time)s</h3>
                    <h3 class='attribute'><strong>Test Target Platform:&#8194</strong>%(platform)s</h3>
                    <h3 class='attribute'><strong>Total Test Time:&#8194</strong>%(all_time)ss</h3>
                    <h3 class='attribute'><strong>Total Number of Test Cases:&#8194</strong>%(all_count)s</h3>
                </div>
                <div class="col col-lg-4">
                    <div id="chart" style="margin-top:20px;width:100%%;height:300px;float:left;"></div>
                </div>
            </div>
        <div class="row">
            <div class="col col-lg-12">
            <table class="bordered">
                <colgroup>
                    <col align="left"/>
                    <col align="right"/>
                    <col align="right"/>
                    <col align="right"/>
                    <col align="right"/>
                    <col align="right"/>
                </colgroup>
                <tr class="title_style"><th>Test Group/Test case</th>
                    <th>Time</th>
                    <th>Count</th>
                    <th>Pass</th>
                    <th>Fail</th>
                    <th>Error</th>
                    <th>View</th></tr>
                %(table_tr)s</table></div>
        </div>
        %(chart)s
        </body>
        </html>"""

    SUITE_TEMP = """
        <tr class="list_style"><td align="left">%(SuiteName)s</td>
            <td align="center"><font color="696969">%(BarTime)ss</font></td>
            <td align="center"><font color="#4672C4">%(Count)s</font></td>
            <td align="center"><font color="green">%(Pass)s</font></td>
            <td align="center"><font color="red">%(Fail)s</font></td>
            <td align="center"><font color="red">%(Error)s</font></td>
            <td align="center"><font color="green"><a href="%(link)s">detail</a></font></td>
        </tr>"""

    TEST_PASS_TEMP = """
        <tr><td class="passCase">%(TestName)s</td>
            <td align="center"><span class="label passCase">%(SamTime)ss</span></td>
            <td colspan="5" align="center"><span class="label passCase">pass</span></td>
        </tr>"""

    TEST_DISABLED_TEMP = """
        <tr><td class="disabledCase">%(TestName)s</td>
            <td align="center"><span class="label disabledCase">%(SamTime)ss</span></td>
            <td colspan="5" align="center"><span class="label disabledCase">not run</span></td>
        </tr>"""

    TEST_FAILED_TEMP = """
        <tr><td class="failCase">%(TestName)s</td>
            <td align="center"><span class="label failCase">%(SamTime)ss</span></td>
            <td colspan="5" align="center">
                <span class="label failCase">fail</span>
                <div id="div_ft1_2" class="collapse in">
                    <pre>%(info)s</pre>
                </div></td>
        </tr>"""

    ECHARTS_SCRIPT = """
        <script type="text/javascript">
            var myChart = echarts.init(document.getElementById('chart'));
            var option = {
                title : {
                    text: 'Test Execution',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%%)"
                },
                color: ['#64B012', '#F6DA3E', '#DE3A3A', '#B0C4DE'],
                legend: {
                    orient: 'vertical',
                    left: 'left',
                    data: ['Pass','Fail','Error','Not Run'],
                    "textStyle": {
                        "fontSize": 16
                    }
                },
                series : [
                    {
                        name: 'Test Execution',
                        type: 'pie',
                        radius : '60%%',
                        center: ['50%%', '60%%'],
                        data:[
                            {value:%(passed)s, name:'Pass'},
                            {value:%(fail)s, name:'Fail'},
                            {value:%(error)s, name:'Error'},
                            {value:%(not_run)s, name:'Not Run'}
                        ],
                        "label": {
                            "normal": {
                                "textStyle": {
                                    "fontSize": 16
                                }
                            },
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }       
                        }
                    }
                ]
            };
            myChart.setOption(option);
    </script>
    """


def ConvertTestReport(file_path, file):
    # check file
    str_file = os.path.join(file_path, file)
    if not os.access(str_file, os.F_OK):
        return

    try:
        name, ext = os.path.splitext(str_file)
        parse = ElementTree.parse(str_file)
        root_node = parse.getroot()

        test_info = {}
        for item in root_node.attrib:
            test_info[item] = root_node.get(item)

        html = CTestReportTemplate()
        table_tr = ''
        all_time = 0
        all_count = 0
        for suite in root_node:
            suite_name = suite.get('name')
            bar_time = suite.get('time')
            tests = suite.get('tests')
            failures = suite.get('failures')
            disabled = suite.get('disabled')
            errors = suite.get('errors')
            all_time = all_time + float(bar_time)
            all_count = all_count + int(tests)

            # generate suite table
            passed = int(tests) - int(failures) - int(disabled) - int(errors)
            suite_td = html.SUITE_TEMP % dict(SuiteName=suite_name,
                                              BarTime=str(bar_time),
                                              Count=str(tests),
                                              Pass=str(passed),
                                              Fail=str(failures),
                                              Error=str(errors),
                                              link=file)

            for test in suite:
                test_name = test.get('name')
                status = test.get('status')
                sam_time = test.get('time')
                status = status if status == 'run' else 'not run'
                test_td = html.TEST_DISABLED_TEMP % dict(TestName=test_name,
                                                         SamTime=str(sam_time))
                if status == 'run':
                    test_td = html.TEST_PASS_TEMP % dict(TestName=test_name,
                                                         SamTime=str(sam_time))
                    child_node = test.findall('failure')
                    if child_node:
                        message = child_node[0].get('message')

                        # generate test table
                        test_td = html.TEST_FAILED_TEMP % dict(TestName=test_name,
                                                               SamTime=str(
                                                                   sam_time),
                                                               info=message)
                suite_td += test_td

            table_tr += suite_td
        func = html.ECHARTS_SCRIPT % dict(passed=int(passed),
                                          fail=int(failures),
                                          error=int(errors),
                                          not_run=int(disabled))
        plat = configs.get('PLATFORM')
        with open('./script/css/report.css', 'r') as css_file:
            data = css_file.read()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        report = html.TEST_HTML_TEMP % dict(test_time=now_time,
                                            css=data,
                                            platform=plat,
                                            all_time=all_time,
                                            all_count=all_count,
                                            table_tr=table_tr,
                                            chart=func)
        file_name = name + '.html'
        with open(file_name, 'w') as fp:
            fp.write(report)

        return test_info
    except IOError as e:
        print('raise error %s ' % e.message)
