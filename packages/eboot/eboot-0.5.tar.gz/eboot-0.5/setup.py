# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eboot', 'eboot.gtest2html']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.6.0,<13.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['eboot = eboot.main:app']}

setup_kwargs = {
    'name': 'eboot',
    'version': '0.5',
    'description': '',
    'long_description': '# eboot-cli\n\neboot 额外提供一个命令行工具，可以简化 CodeRoot 编译流程，提高开发效率。\n\n## 特性\n\n## 安装\n\n下载 eboot 安装包，使用如下命令进行安装。\n\n```\npip install eboot-xxx.whl\n```\n\n将 eboot 的安装路径加到环境变量中，即可全局使用。\n\n## 快速上手\n\n使用如下命令编译程序\n\n```\neboot build 3 100\n```\n\n使用如下命令清理 CodeRoot\n\n```\neboot clear\n```\n',
    'author': 'qiuyeyijian',
    'author_email': 'zlw9821@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
