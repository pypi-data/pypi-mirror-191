# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_localstore']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-rc.1,<3.0.0', 'typing-extensions>=4.0.0']

entry_points = \
{'nb_scripts': ['localstore = nonebot_plugin_localstore.script:main']}

setup_kwargs = {
    'name': 'nonebot-plugin-localstore',
    'version': '0.4.1',
    'description': 'Local Storage Support for NoneBot2',
    'long_description': '<!-- markdownlint-disable MD041 -->\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# NoneBot Plugin LocalStore\n\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable-next-line MD036 -->\n_✨ NoneBot 本地数据存储插件 ✨_\n<!-- prettier-ignore-end -->\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/nonebot/plugin-localstore/master/LICENSE">\n    <img src="https://img.shields.io/github/license/nonebot/plugin-localstore.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-localstore">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-localstore.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n</p>\n\n## 使用方式\n\n加载插件后使用 `require` 声明插件依赖，直接使用 `localstore` 插件提供的函数即可。\n\n```python\nfrom pathlib import Path\nfrom nonebot import require\n\nrequire("nonebot_plugin_localstore")\n\nimport nonebot_plugin_localstore as store\n\nplugin_cache_dir: Path = store.get_cache_dir("plugin_name")\nplugin_cache_file: Path = store.get_cache_file("plugin_name", "filename")\nplugin_config_dir: Path = store.get_config_dir("plugin_name", "filename")\nplugin_config_file: Path = store.get_config_file("plugin_name", "filename")\nplugin_data_dir: Path = store.get_data_dir("plugin_name")\nplugin_data_file: Path = store.get_data_file("plugin_name", "filename")\n```\n\n## 存储路径\n\n在项目安装插件后，可以使用 `nb-cli` 查看具体的存储路径：\n\n```bash\nnb localstore\n```\n\n参考路径如下：\n\n### cache path\n\n- macOS: `~/Library/Caches/<AppName>`\n- Unix: `~/.cache/<AppName>` (XDG default)\n- Windows: `C:\\Users\\<username>\\AppData\\Local\\<AppName>\\Cache`\n\n### data path\n\n- macOS: `~/Library/Application Support/<AppName>`\n- Unix: `~/.local/share/<AppName>` or in $XDG_DATA_HOME, if defined\n- Win XP (not roaming): `C:\\Documents and Settings\\<username>\\Application Data\\<AppName>`\n- Win 7 (not roaming): `C:\\Users\\<username>\\AppData\\Local\\<AppName>`\n\n### config path\n\n- macOS: same as user_data_dir\n- Unix: `~/.config/<AppName>`\n- Win XP (roaming): `C:\\Documents and Settings\\<username>\\Local Settings\\Application Data\\<AppName>`\n- Win 7 (roaming): `C:\\Users\\<username>\\AppData\\Roaming\\<AppName>`\n',
    'author': 'yanyongyu',
    'author_email': 'yyy@nonebot.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nonebot/plugin-localstore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
