# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_gsabyss', 'nonebot_plugin_gsabyss.models']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0',
 'httpx>=0.20.0,<1.0.0',
 'nonebot-adapter-onebot>=2.0.0b1',
 'nonebot-plugin-apscheduler>=0.2.0',
 'nonebot2>=2.0.0b3']

setup_kwargs = {
    'name': 'nonebot-plugin-gsabyss',
    'version': '0.1.1',
    'description': 'Genshin spiral abyss plugin for NoneBot2',
    'long_description': '<h1 align="center">NoneBot Plugin GsAbyss</h1></br>\n\n\n<p align="center">🤖 用于展示原神深境螺旋数据的 NoneBot2 插件</p></br>\n\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/monsterxcn/nonebot-plugin-gsabyss/master/LICENSE"><img src="https://img.shields.io/github/license/monsterxcn/nonebot-plugin-gsabyss" alt="license" /></a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-gsabyss"><img src="https://img.shields.io/pypi/v/nonebot-plugin-gsabyss" alt="pypi" /></a>\n  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.8+-blue" alt="python" /></a>\n  <a href="https://jq.qq.com/?_wv=1027&k=GF2vqPgf"><img src="https://img.shields.io/badge/QQ%E7%BE%A4-662597191-orange" alt="QQ Chat Group" /></a><br />\n  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" /></a>\n  <a href="https://pycqa.github.io/isort"><img src="https://img.shields.io/badge/%20imports-isort-%231674b1?&labelColor=ef8336" alt="Imports: isort" /></a>\n  <a href="https://flake8.pycqa.org/"><img src="https://img.shields.io/badge/lint-flake8-&labelColor=4c9c39" alt="Lint: flake8" /></a>\n  <a href="https://results.pre-commit.ci/latest/github/monsterxcn/nonebot-plugin-gsabyss/main"><img src="https://results.pre-commit.ci/badge/github/monsterxcn/nonebot-plugin-gsabyss/main.svg" alt="pre-commit" /></a>\n</p></br>\n\n\n| ![全层](https://user-images.githubusercontent.com/22407052/217551477-a0a252a9-31b4-4bb0-8b08-41cfe26679d6.jpg) | ![单间](https://user-images.githubusercontent.com/22407052/217551559-4f75ad13-1a74-42e1-adfc-06c6b0521263.jpg) | ![统计](https://user-images.githubusercontent.com/22407052/218297626-463b5ab3-8500-4337-980f-000bb4289439.png) |\n|:--:|:--:|:--:|\n\n\n## 安装方法\n\n\n如果你正在使用 2.0.0.beta1 以上版本 NoneBot2，推荐使用以下命令安装：\n\n\n```bash\n# 从 nb_cli 安装\nnb plugin install nonebot-plugin-gsabyss\n```\n\n\n## 插件配置\n\n\n一般来说，此插件安装后无需任何配置即可使用。你也可以根据需要配置以下环境变量：\n\n\n| 环境变量 | 必需 | 默认 | 说明 |\n|:-------|:----:|:-----|:----|\n| `gsabyss_dir` | 否 | `data/gsabyss` | 插件数据缓存目录 |\n| `gsabyss_priority` | 否 | 10 | 插件响应优先级。触发本插件功能的消息无法被优先级低于此配置的其他插件处理 |\n| `hhw_mirror` | 否 | `https://genshin.honeyhunterworld.com/img/` | 素材图片下载镜像，**暂不可用** |\n\n\n## 命令说明\n\n\n### 深渊速览\n\n\n插件响应以 `速览` / `深渊速览` 开头的消息，并且阻止事件继续向下传播。默认返回 **本期** **12** 层 **全层** 的深渊速览图片。\n\n你也可以通过合理搭配下面格式的参数限定查找的内容。各参数按空格分开即可，顺序随意。\n\n\n| 可选附带参数 | 说明 |\n|:--------|:-----|\n| `12` / `十二` / `十二层` / `第12层` / ... | 查询指定层全层的深渊速览 |\n| `12-3` / `12—3` / `12－3` / `12_3` / ... | 查询指定层指定间的深渊速览 |\n| `上期` / `下期` | 查询上期或下期的深渊速览 |\n| `三月上` / `22年3月上` / `2022年三月上` / ... | 查询指定时间的深渊速览 |\n\n\n### 深渊统计\n\n\n插件 **仅响应**  `深渊统计` 消息，不可附带任何参数，并且阻止事件继续向下传播。默认返回虚空数据库（Akasha Database）最新的深渊统计图片。\n\n\n## 特别鸣谢\n\n\n[@nonebot/nonebot2](https://github.com/nonebot/nonebot2/) | [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) | [Honey Hunter World](https://genshin.honeyhunterworld.com/d_1001/) | [Akasha Database](https://akashadata.com/)\n',
    'author': 'monsterxcn',
    'author_email': 'monsterxcn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/monsterxcn/nonebot-plugin-gsabyss',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
