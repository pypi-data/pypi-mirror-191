# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_txt2img']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot2[fastapi]>=2.0.0rc1,<3.0.0',
 'pillow>=9.0.0,<10.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-txt2img',
    'version': '0.3.0',
    'description': '轻量文字转图片插件',
    'long_description': '<!-- markdownlint-disable MD033 MD036 MD041-->\n<p align="center">\n  <img src="https://github.com/mobyw/images/raw/main/Screenshots/nonebot-plugin-txt2img.png" width="400px"/>\n</p>\n\n<div align="center">\n\n# nonebot-plugin-txt2img\n\n_✨ 轻量文字转图片插件 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/mobyw/nonebot-plugin-txt2img/master/LICENSE">\n    <img src="https://img.shields.io/github/license/mobyw/nonebot-plugin-txt2img.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-txt2img">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-txt2img.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">\n</p>\n\n## 简介\n\n本插件由使用 `PIL(Pillow)` 库将纯文字消息转为图片，启动时会检测所需资源是否存在，若不存在会自动下载到对应位置。生成的图片以 `base64` 格式发送，不保存到磁盘。\n\n## 安装步骤\n\n### 安装 NoneBot2\n\n完整文档可以在 [这里](https://v2.nonebot.dev/) 查看。\n\n请在创建项目时选用 `onebot v11` 适配器，并且按照文档完成最小实例的创建。\n\n### 安装 nonebot-plugin-txt2img\n\n#### 使用 `nb-cli` 安装（推荐）\n\n```bash\nnb plugin install nonebot-plugin-txt2img\n```\n\n#### 使用 `pip` 安装\n\n```bash\npip install nonebot-plugin-txt2img\n```\n\n需要在 `bot.py` 文件添加以下代码加载插件：\n\n```python\nnonebot.load_plugin("nonebot_plugin_txt2img")\n```\n\n## 指令说明\n\n指令匹配方式添加了 `to_me()` 规则，在群聊中使用时需要在命令首部或尾部添加 @机器人 (`@{bot_self_id}`) 或 机器人昵称 (`{bot_nickname}`)。\n\n**使用指令**：txt2img\n\n发送指令后根据提示输入标题、内容与字体大小，即可完成图片生成。\n\n* 标题：以 `1.5` 倍字体大小排版在首行居中位置。\n* 内容：以 `1` 倍字体大小左对齐排版。\n* 字体大小：位于 `20~120` 之间的数字。\n\n若内容不满一行，或每行都是较短的内容，会根据内容文本宽度调节图片宽度。\n\n## 跨插件使用\n\n如需在其他插件中使用文本转图片功能，可以从本插件导入。\n\n导入方式：\n\n```python\nfrom nonebot.adapters.onebot.v11 import MessageSegment\nfrom nonebot_plugin_txt2img import Txt2Img\n```\n\n基本使用方式：\n\n```python\n# 标题设置为 \'\' 或 \' \' 可以去除标题行\ntitle = \'标题\'\ntext = \'正文内容\'\nfont_size = 32\n\ntxt2img = Txt2Img()\n\n# 设置字体大小\ntxt2img.set_font_size(font_size)\n\n# # 同时设置内容与标题字体大小\n# title_font_size = 48\n# txt2img.set_font_size(font_size, title_font_size)\n\n# # 设置固定宽度\n# # 设置后不会在内容较窄时自动调整宽度\n# width = 1080\n# txt2img.set_width(1080)\n\n# # 绘制 PIL.Image.Image 图片\n# pic = txt2img.draw_img(title, text)\n\n# 绘制 base64 图片并发送\npic = txt2img.draw(title, text)\nmsg = MessageSegment.image(pic)\n```\n\n使用模板：\n\n插件内置 `["mi", "simple"]` 两个模板，分别是小米便笺以及黑底白字简单风格。默认模板是 `"mi"`，可使用以下代码修改使用的模板：\n\n```python\n...\n# 使用简约模板\npic = txt2img.draw(title, text, "simple")\nmsg = MessageSegment.image(pic)\n```\n\n也可以传入一个 `dict` 以实现自定义模板，示例如下：\n\n```python\ntemplate = {\n    {\n        # 必填项\n        "font": "arial.ttf",                # 字体文件路径字符串，必填\n        "text": {\n            "color": (0, 0, 0),             # 正文颜色 RGB，必填\n        },\n        "title": {\n            "color": (0, 0, 0),             # 标题颜色 RGB，必填\n        },\n        "margin": 80,                       # 边距，必填\n        "background": {\n            "type": "image",                # 背景类型，"image" 或 "color"，必填\n            "image": "/path/to/img.png",    # 背景图片路径，类型为 "image" 时必填\n            "color": (255, 255, 255),       # 背景颜色 RGB，类型为 "color" 时必填\n        },\n        # 可选项\n        "border": {\n            "color": (255, 255, 0),         # 边框颜色 RGB，必填\n            "width": 2,                     # 边框宽度，必填\n            "margin": 30,                   # 边框边距，小于顶层 "margin" 项，必填\n        },\n    }\n}\n...\n# 使用自定义模板\npic = txt2img.draw(title, text, template)\nmsg = MessageSegment.image(pic)\n```\n\n## 项目致谢\n\n本项目基于以下项目或服务实现，排名不分先后。\n\n* [nonebot2](https://github.com/nonebot/nonebot2)\n* [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)\n* [txt2img](https://github.com/taseikyo/txt2img)\n',
    'author': 'mobyw',
    'author_email': 'mobyw66@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mobyw/nonebot-plugin-txt2img',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
