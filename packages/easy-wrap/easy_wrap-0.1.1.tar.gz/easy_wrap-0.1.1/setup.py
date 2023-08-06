# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easy_wrap']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=9.4.0,<10.0.0']

setup_kwargs = {
    'name': 'easy-wrap',
    'version': '0.1.1',
    'description': '',
    'long_description': '## 基于pillow的简单文本转图片渲染工具\n\n示例代码：\n\n```py\nfrom easy_wrap import Drawer\n\ntext = "... the text you want to render ....测试自动换行"\n\nfont_path = "msyh.ttc"\nfont_size = 30\ndrawer = Drawer(font_path, font_size)\n\nimage_width = 180\ncanvas = drawer.draw_text(text, image_width)\n\n# save the image\ncanvas.save(open("test.png", "wb")) \n```\n\n特性：\n\n- 快速，800字平均渲染时长为0.04s（i7 cpu 2.7GHz）\n- 遵循如下换行规则（与css word-break: normal 稍有差异）\n  - 纯中文：自动换行，一个汉字看做一个单词；\n  - 纯英文：看做一个单词，不换行；\n  - 遇到英文空格或者换行符：会换行；\n\n## 更新日志\n\n### 0.1.0\n\n- 第一个可用版本\n\n### 0.1.1\n\n- 修复BUG：修复3.10以下python环境调用easy_wrap发生`TypeError: \'type\' object is not subscriptable`的问题\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/easy_wrap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
