# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flet',
 'flet.__pyinstaller',
 'flet.__pyinstaller.rthooks',
 'flet.auth',
 'flet.auth.providers',
 'flet.cli',
 'flet.cli.commands']

package_data = \
{'': ['*'],
 'flet': ['web/*',
          'web/assets/*',
          'web/assets/fonts/*',
          'web/assets/packages/window_manager/images/*',
          'web/icons/*']}

install_requires = \
['flet-core==0.5.0.dev1197',
 'httpx>=0.23.3,<0.24.0',
 'oauthlib>=3.2.2,<4.0.0',
 'packaging>=23.0,<24.0',
 'watchdog>=2.2.1,<3.0.0',
 'websocket-client>=1.4.2,<2.0.0',
 'websockets>=10.4,<11.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.4.0,<5.0.0']}

entry_points = \
{'console_scripts': ['flet = flet.cli.cli:main'],
 'pyinstaller40': ['hook-dirs = flet.__pyinstaller:get_hook_dirs']}

setup_kwargs = {
    'name': 'flet',
    'version': '0.5.0.dev1197',
    'description': 'Flet for Python - easily build interactive multi-platform apps in Python',
    'long_description': '# Flet - quickly build interactive apps for web, desktop and mobile in Python\n\n[Flet](https://flet.dev) is a rich User Interface (UI) framework to quickly build interactive web, desktop and mobile apps in Python without prior knowledge of web technologies like HTTP, HTML, CSS or JavaSscript. You build UI with [controls](https://flet.dev/docs/controls) based on [Flutter](https://flutter.dev/) widgets to ensure your programs look cool and professional.\n\n## Requirements\n\n* Python 3.7 or above on Windows, Linux or macOS\n\n## Installation\n\n```\npip install flet\n```\n\n## Create the app\n\nCreate `main.py` file with the following content:\n\n```python\nimport flet as ft\n\ndef main(page: ft.Page):\n    page.title = "Flet counter example"\n    page.vertical_alignment = ft.MainAxisAlignment.CENTER\n\n    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)\n\n    def minus_click(e):\n        txt_number.value = str(int(txt_number.value) - 1)\n        page.update()\n\n    def plus_click(e):\n        txt_number.value = str(int(txt_number.value) + 1)\n        page.update()\n\n    page.add(\n        ft.Row(\n            [\n                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),\n                txt_number,\n                ft.IconButton(ft.icons.ADD, on_click=plus_click),\n            ],\n            alignment=ft.MainAxisAlignment.CENTER,\n        )\n    )\n\nft.app(main)\n```\n\n## Run as a desktop app\n\nThe following command will start the app in a native OS window:\n\n```\nflet run main.py\n```\n\n![Sample app in a native window](https://flet.dev/img/docs/getting-started/flet-counter-macos.png)\n\n## Run as a web app\n\nThe following command will start the app as a web app:\n\n```\nflet run --web main.py\n```\n\n![Sample app in a browser](https://flet.dev/img/docs/getting-started/flet-counter-safari.png)\n\n## Learn more\n\nVisit [Flet website](https://flet.dev).\n\nContinue with [Python guide](https://flet.dev/docs/getting-started/python) to learn how to make a real app.\n\nBrowse for more [Flet examples](https://github.com/flet-dev/examples/tree/main/python).\n\nJoin to a conversation on [Flet Discord server](https://discord.gg/dzWXP8SHG8).\n',
    'author': 'Appveyor Systems Inc.',
    'author_email': 'hello@flet.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
