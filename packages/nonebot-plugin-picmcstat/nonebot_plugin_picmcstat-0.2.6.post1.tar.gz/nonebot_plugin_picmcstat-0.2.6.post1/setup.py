# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_picmcstat']

package_data = \
{'': ['*'], 'nonebot_plugin_picmcstat': ['res/*']}

install_requires = \
['mcstatus>=10.0.1,<11.0.0',
 'nonebot-adapter-onebot>=2.2.0,<3.0.0',
 'nonebot-plugin-imageutils>=0.1.13.5,<0.2.0.0',
 'nonebot2>=2.0.0rc2,<3.0.0',
 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-picmcstat',
    'version': '0.2.6.post1',
    'description': "A NoneBot2 plugin generates a pic from a Minecraft server's MOTD",
    'long_description': '<!-- markdownlint-disable MD033 MD036 MD041 -->\n\n<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="readme/picmcstat.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# NoneBot-Plugin-PicMCStat\n\n_✨ Minecraft 服务器 MOTD 查询 图片版 ✨_\n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/lgc2333/nonebot-plugin-picmcstat.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot-plugin-picmcstat">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-picmcstat.svg" alt="pypi">\n</a>\n<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n<a href="https://pypi.python.org/pypi/nonebot-plugin-picmcstat">\n    <img src="https://img.shields.io/pypi/dm/nonebot-plugin-picmcstat" alt="pypi download">\n</a>\n<a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/5bc0f141-d1ec-430a-8d21-0e312188fdae">\n  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/5bc0f141-d1ec-430a-8d21-0e312188fdae.svg" alt="wakatime">\n</a>\n\n</div>\n\n## 📖 介绍\n\n插件实际上是可以展示 **玩家列表**、**Mod 端信息 以及 Mod 列表（还未测试）** 的，这里没有找到合适的例子所以没在效果图里展示出来，如果遇到问题可以发 issue\n\n插件包体内并没有自带图片内 Unifont 字体，需要的话请参考 [这里](#字体) 安装字体\n\n因为下划线、删除线和斜体 [`nonebot-plugin-imageutils`](https://github.com/noneplugin/nonebot-plugin-imageutils) 的 bbcode 还不支持，所以还没做  \n（如果 wq 佬看到这个能不能酌情考虑一下呢 awa）\n\n<details open>\n<summary>效果图</summary>\n\n![example](readme/example.png)  \n![example](readme/example_je.png)\n\n</details>\n\n## 💿 安装\n\n### 插件\n\n<details open>\n<summary>[推荐] 使用 nb-cli 安装</summary>\n在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装\n\n    nb plugin install nonebot-plugin-picmcstat\n\n</details>\n\n<details>\n<summary>使用包管理器安装</summary>\n在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令\n\n<details>\n<summary>pip</summary>\n\n    pip install nonebot-plugin-picmcstat\n\n</details>\n<details>\n<summary>pdm</summary>\n\n    pdm add nonebot-plugin-picmcstat\n\n</details>\n<details>\n<summary>poetry</summary>\n\n    poetry add nonebot-plugin-picmcstat\n\n</details>\n<details>\n<summary>conda</summary>\n\n    conda install nonebot-plugin-picmcstat\n\n</details>\n\n打开 nonebot2 项目的 `bot.py` 文件, 在其中写入\n\n    nonebot.load_plugin(\'nonebot_plugin_picmcstat\')\n\n</details>\n\n### 字体\n\n字体文件请自行去自行去 [这里](http://ftp.gnu.org/gnu/unifont/unifont-15.0.01/unifont-15.0.01.ttf) 下载\n\n有两种方式可以安装该字体\n\n- 方式一：直接安装在系统中\n- 方式二：放在 `nonebot-plugin-imageutils` 插件的字体文件目录中并将文件重命名为 `unifont` 即可使用，该插件配置可以参考 [这里](https://github.com/noneplugin/nonebot-plugin-imageutils#%E9%85%8D%E7%BD%AE%E5%AD%97%E4%BD%93)\n\n## ⚙️ 配置\n\n### `MCSTAT_SHORTCUTS` - 快捷指令列表\n\n这个配置项能够帮助你简化一些查询指令\n\n此配置项的类型是一个列表，里面的元素需要为一个特定结构的字典  \n这个字典需要有三个元素\n\n- `regex` - 用于匹配指令的正则，例如 `^查服$`  \n  （注意，nb2 以 JSON 格式解析配置项，所以当你要在正则表达式里表示`\\`时，你需要将其转义为`\\\\`）\n- `host` - 要查询的服务器地址，格式为 `<IP>[:端口]`，  \n  例如 `hypixel.net` 或 `example.com:1919`\n- `type` - 要查询服务器的类型，`je` 表示 Java 版服，`be` 表示基岩版服\n- `whitelist` - 群聊白名单，只有里面列出的群号可以查询，可以不填来对所有群开放查询\n\n最终的配置项看起来是这样子的，当你发送 `查服` 时，机器人会把 EaseCation 服务器的状态发送出来\n\n    MCSTAT_SHORTCUTS=[{"regex":"^查服$","host":"asia.easecation.net","type":"be"}]\n\n## 🎉 使用\n\n发送 `motd` 指令 查看使用指南\n\n![usage](readme/usage.png)\n\n## 📞 联系\n\nQQ：3076823485  \nTelegram：[@lgc2333](https://t.me/lgc2333)  \n吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)  \n邮箱：<lgc2333@126.com>\n\n## 💡 鸣谢\n\n### [nonebot-plugin-imageutils](https://github.com/noneplugin/nonebot-plugin-imageutils)\n\n- 超好用的 Pillow 辅助库，快去用 awa\n\n## 💰 赞助\n\n感谢大家的赞助！你们的赞助将是我继续创作的动力！\n\n- [爱发电](https://afdian.net/@lgc2333)\n- <details>\n    <summary>赞助二维码（点击展开）</summary>\n\n  ![讨饭](https://raw.githubusercontent.com/lgc2333/ShigureBotMenu/master/src/imgs/sponsor.png)\n\n  </details>\n\n## 📝 更新日志\n\n### 0.2.6\n\n- 修复 `shortcut` 中没有 `whitelist` 项会报错的问题\n\n### 0.2.5\n\n- `shortcut` 加入 `whitelist` 项配置触发群白名单\n\n### 0.2.4\n\n- 修复玩家列表底下的多余空行\n\n### 0.2.3\n\n- 修复 JE 服务器 Motd 中粗体意外显示为蓝色的 bug\n\n### 0.2.2\n\n- 修复 motd 前后留的空去不干净的问题\n- 优化玩家列表显示效果\n\n### 0.2.1\n\n- 修复当最大人数为 0 时出错的问题\n\n### 0.2.0\n\n- 加入快捷指令，详见配置项\n- 修复某些 JE 服无法正确显示 Motd 的问题\n-\n\n### 0.1.1\n\n- 将查 JE 服时的 `游戏延迟` 字样 改为 `测试延迟`\n',
    'author': 'lgc2333',
    'author_email': 'lgc2333@126.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
