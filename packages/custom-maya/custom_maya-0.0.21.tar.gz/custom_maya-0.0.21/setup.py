# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['custom_maya',
 'custom_maya.customclass',
 'custom_maya.tools',
 'custom_maya.tools.get_scene_infos']

package_data = \
{'': ['*'], 'custom_maya': ['templates/*', 'templates/base/*']}

install_requires = \
['Jinja2', 'custom_maya', 'openpyxl', 'pandas']

setup_kwargs = {
    'name': 'custom-maya',
    'version': '0.0.21',
    'description': 'Maya的便利工具',
    'long_description': '# 项目说明\n\n此工具内含各种实用工具。**仅为测试用！！！**\n\n仅支持Maya2023及以上版本。\n\n\n参照\n* [如何使用mayapy运行venv](https://knowledge.autodesk.com/zh-hans/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2023/CHS/Maya-Scripting/files/GUID-6AF99E9C-1473-481E-A144-357577A53717-htm.html)\n* [Maya Python 解释器 mayapy](https://knowledge.autodesk.com/zh-hans/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2023/CHS/Maya-Scripting/files/GUID-D64ACA64-2566-42B3-BE0F-BCE843A1702F-htm.html)\n\n\n## 安装并获取更新\n\n使用 pip 安装\n```shell\npip install custom-maya\n```\n\n需要使用 mayapy 环境安装。\n\n测试用\n```shell\nXcopy custom_maya "C:\\Program Files\\Autodesk\\Maya2023\\Python\\Lib\\site-packages\\custom_maya" /E/H/C/I\n```\n\n\n## 如何设置IDE\n\n\n### 制作从名为 python 的命令创建指向 mayapy 的软链接\n\n```shell\ncd "C:\\Program Files\\Autodesk\\Maya2023\\bin"\nmklink python.exe mayapy.exe\n```\n\n### 将IDE的解释器设置为\n```\n"C:\\Program Files\\Autodesk\\Maya2023\\bin\\python.exe"\n```\n\n\n\n\n## 例子\n\n### 获取某根目录下所有Maya文件的信息\n\n```python\n\n```\n\n\n\n\n\n## 打包上传到pipy\n\n升级\n```shell\npython.exe -m pip install --upgrade build\npython.exe -m pip install --upgrade pip\n```\n\n```shell\npython -m build\n```\n\n上传测试包\n```shell\npython -m twine upload --repository testpypi dist/*\n```\n\n\n上传正式版本包\n```shell\npython -m twine upload dist/*\n```\n\n',
    'author': 'Yuanzhen Qiao',
    'author_email': 'narutozbjp@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
