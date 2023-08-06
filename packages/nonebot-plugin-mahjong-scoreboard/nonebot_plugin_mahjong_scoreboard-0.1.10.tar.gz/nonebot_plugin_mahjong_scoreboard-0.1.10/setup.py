# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_mahjong_scoreboard',
 'nonebot_plugin_mahjong_scoreboard.controller',
 'nonebot_plugin_mahjong_scoreboard.controller.interceptor',
 'nonebot_plugin_mahjong_scoreboard.controller.mapper',
 'nonebot_plugin_mahjong_scoreboard.model',
 'nonebot_plugin_mahjong_scoreboard.model.orm',
 'nonebot_plugin_mahjong_scoreboard.service',
 'nonebot_plugin_mahjong_scoreboard.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.17,<0.19',
 'cachetools>=5.2.0,<6.0.0',
 'nonebot-adapter-onebot>=2.1.5,<3.0.0',
 'nonebot-plugin-gocqhttp-cross-machine-upload-file>=0.1.0,<0.2.0',
 'nonebot-plugin-sqlalchemy>=0.1.4,<0.2.0',
 'nonebot2>=2.0.0rc1,<3.0.0',
 'nonebot_plugin_apscheduler>=0.2.0,<0.3.0',
 'tzlocal>=4.2,<5.0']

setup_kwargs = {
    'name': 'nonebot-plugin-mahjong-scoreboard',
    'version': '0.1.10',
    'description': '日麻寄分器（NoneBot插件）',
    'long_description': '<!-- markdownlint-disable MD033 MD036 MD041 -->\n\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\nnonebot-plugin-mahjong-scoreboard\n============\n\n_✨ NoneBot 日麻记分器插件 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/ssttkkl/nonebot-plugin-mahjong-scoreboard/master/LICENSE">\n    <img src="https://img.shields.io/github/license/ssttkkl/nonebot-plugin-mahjong-scoreboard.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-mahjong-scoreboard">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-mahjong-scoreboard.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">\n</p>\n\n支持适配器：[OneBot V11](https://onebot.adapters.nonebot.dev/)\n\n支持驱动器：[FastAPI](https://v2.nonebot.dev/docs/tutorial/choose-driver)\n\n## 功能\n\n为群友提供日麻对局分数记录。根据马点进行PT精算，统计PT增减，支持对局与榜单查询与导出。\n\nPT精算算法为（点数-返点+马点）/1000，返点和马点在创建赛季时进行设置。\n\n## 指令\n\n### 对局\n\n- `/新建对局 [四人南|四人东]`\n    - 别名：`/新对局`\n- `/结算对局 <成绩> [对局<编号>] [@<用户>] [<自风>]`\n    - 别名：`/结算`\n- `/撤销结算对局 [对局<编号>] [@<用户>]`\n    - 别名：`/撤销结算`\n- `/设置对局PT <PT> [对局<编号>] [@<用户>]`\n    - 别名：`/对局PT`\n- `/删除对局 [对局<编号>]`\n- `/设置对局进度 <进度> [对局<编号>]`\n    - 别名：`/对局进度`\n- `/设置对局备注 [对局<编号>] <对局备注>`\n    - 别名：`/对局备注`\n\n与对局相关的指令可以省略对局编号，省略时默认对最近新建的对局进行操作。也可以通过回复Bot发出的对局消息来代替指定对局编号。\n\n对局相关指令在对局完成超过24小时后需要拥有群主或管理员身份才能使用。（`/删除对局`除外，该指令需要拥有群主或管理员身份才能使用）\n\n未完成且未设置进度的对局会在创建24小时后自动删除。赛季结束后，未完成对局会自动删除，所有已完成对局均无法再进行修改。\n\n### 对局查询\n\n- `/查询对局 [<编号>]`\n    - 别名：`/对局`\n- `/个人最近对局 [@<用户>]`\n    - 别名：`/最近对局`\n- `/群最近对局`\n- `/个人未完成对局 [@<用户>]`\n    - 别名：`/未完成对局`\n- `/群未完成对局`\n- `/导出赛季对局 [<代号>]`\n    - 别名：`/导出对局`\n- `/导出所有对局`\n\n### 赛季\n\n- `/查询赛季 [<代号>]`\n    - 别名：`/赛季`，`/当前赛季`\n- `/查询所有赛季`\n    - 别名：`/所有赛季`\n- `/新建赛季`\n    - 别名：`/新赛季`\n- `/开启赛季 [<代号>]`\n- `/结束赛季`\n- `/删除赛季 [<代号>]`\n\n### 赛季PT\n\n- `/设置赛季PT <PT> [@<用户>]`\n    - 别名：`/设置PT`，`/设置赛季pt`，`/设置pt`\n- `/查询PT [@<用户>]`\n    - 别名：`/PT`\n- `/查询榜单`\n    - 别名：`/榜单`\n- `/导出榜单`\n\n与赛季/赛季PT相关的指令均可通过私聊/群聊两种方式使用。当未指定参数时进入问答模式，回复`/q`可退出问答模式。\n\n与赛季/赛季PT相关的指令（查询、导出除外）需要拥有群主或管理员身份才能使用。\n\n## 配置\n\n### mahjong_scoreboard_database_conn_url\n\n数据库连接URL，必须使用异步SQLAlchemy驱动器。\n\n默认值：sqlite+aiosqlite:///mahjong_scoreboard.db\n\n### callback_host\n\n回调HOST，若为非容器环境部署（go-cqhttp与nonebot均运行在同一环境）则保持默认值。若为Docker环境部署则设置为Docker容器名。用于上传文件时让go-cqhttp下载本机文件。\n\n默认值：127.0.0.1\n\n### callback_port\n\n回调端口，保持默认值即可。\n\n默认值：与PORT保持一致即可\n\n## 在线乞讨\n\n<details><summary>点击请我打两把maimai</summary>\n\n![](https://github.com/ssttkkl/ssttkkl/blob/main/afdian-ssttkkl.jfif)\n\n</details>\n\n## LICENSE\n\n> MIT License\n>\n> Copyright (c) 2022 ssttkkl\n>\n> Permission is hereby granted, free of charge, to any person obtaining a copy\n> of this software and associated documentation files (the "Software"), to deal\n> in the Software without restriction, including without limitation the rights\n> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n> copies of the Software, and to permit persons to whom the Software is\n> furnished to do so, subject to the following conditions:\n>\n> The above copyright notice and this permission notice shall be included in all\n> copies or substantial portions of the Software.\n>\n> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n> SOFTWARE.\n> \n',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ssttkkl/nonebot-plugin-mahjong-scoreboard',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
