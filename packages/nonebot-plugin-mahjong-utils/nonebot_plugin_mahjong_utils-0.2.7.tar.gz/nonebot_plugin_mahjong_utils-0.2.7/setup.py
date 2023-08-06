# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_mahjong_utils',
 'nonebot_plugin_mahjong_utils.interceptors',
 'nonebot_plugin_mahjong_utils.mapper',
 'nonebot_plugin_mahjong_utils.matchers',
 'nonebot_plugin_mahjong_utils.utils']

package_data = \
{'': ['*']}

install_requires = \
['mahjong-utils>=0.4.0,<0.5.0', 'nonebot2>=2.0.0rc1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-mahjong-utils',
    'version': '0.2.7',
    'description': '',
    'long_description': 'nonebot-plugin-mahjong-utils\n========\n\n## 功能\n\n### 手牌分析\n\n- 输入手牌代码，根据输入手牌输出向听数（未摸牌状态）、牌理（已摸牌、未和牌状态）、副露分析（未摸牌状态+他家打出的牌）或和牌分析（已摸牌、已和牌状态）。\n\n#### 向听数分析（未摸牌状态）\n\n输入的手牌为3k+1张时。\n\n计算向听数与进张。一向听的手牌还会计算好型与愚型进张数。\n\n![shanten_without_got](img/shanten_without_got.png)\n\n#### 牌理（已摸牌状态）\n\n输入的手牌为3k+2张，且未和牌（向听数大于-1）时。\n\n对每种打法（包括打出与暗杠）计算向听数与进张。一向听的手牌还会计算好型与愚型进张数。\n\n![shanten_with_got_1](img/shanten_with_got_1.png)\n\n![shanten_with_got_2](img/shanten_with_got_2.png)\n\n#### 副露分析（未摸牌状态+他家打出的牌）\n\n格式：`手牌代码<上家打出的牌`、`手牌代码^对家打出的牌`或`手牌代码>下家打出的牌`，其中输入的手牌为3k+1张。\n\n~~实际上对家打出和下家打出是一样的（不能吃），这里区分是为了命令的工整性~~\n\n对每种打法（包括吃、碰、大明杠与PASS）计算向听数与进张。一向听的手牌还会计算好型与愚型进张数。\n\n![furo_shanten_1](img/furo_shanten_1.png)\n\n![furo_shanten_2](img/furo_shanten_2.png)\n\n![furo_shanten_3](img/furo_shanten_3.png)\n\n#### 和牌分析\n\n输入的手牌为3k+2张，且已和牌（向听数等于-1）时。\n\n手牌代码的最后一张牌作为所和的牌，手牌代码后可通过空格分割输入副露、自风、场风、dora、额外役。暗杠通过0990m的格式输入。\n\n![hora_1](img/hora_1.png)\n\n![hora_2](img/hora_2.png)\n\n![hora_3](img/hora_3.png)\n\n![hora_4](img/hora_4.png)\n\n### 番符点数查询\n\n- 输入x番y符，输出亲家/子家的自摸/荣和得点\n\n## Special Thanks\n\n-  [nonebot/nonebot2](https://github.com/nonebot/nonebot2)\n-  [ssttkkl/mahjong-utils](https://github.com/ssttkkl/mahjong-utils) ~~我谢我自己~~\n\n## 在线乞讨\n\n<details><summary>点击请我打两把maimai</summary>\n\n![](https://github.com/ssttkkl/ssttkkl/blob/main/afdian-ssttkkl.jfif)\n\n</details>\n\n## LICENSE\n\n> MIT License\n> \n> Copyright (c) 2022 ssttkkl\n> \n> Permission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n> \n> The above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n> \n> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ssttkkl/nonebot-plugin-mahjong-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
