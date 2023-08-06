# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flet']

package_data = \
{'': ['*']}

install_requires = \
['flet-core==0.5.0.dev1197']

setup_kwargs = {
    'name': 'flet-pyodide',
    'version': '0.5.0.dev1197',
    'description': 'Flet for Pyodide - build standalone SPA in Python with Flutter UI.',
    'long_description': '# Flet for Pyodide - build standalone Single-Page Applications (SPA) in Python with Flutter UI\n\n[Flet](https://flet.dev) is a rich User Interface (UI) framework to quickly build interactive web, desktop and mobile apps in Python without prior knowledge of web technologies like HTTP, HTML, CSS or JavaSscript. You build UI with [controls](https://flet.dev/docs/controls) based on [Flutter](https://flutter.dev/) widgets to ensure your programs look cool and professional.\n\n## Requirements\n\n* Python 3.7 or above on Windows, Linux or macOS\n\n## Installation\n\n```\npip install flet\n```\n\n## Create the app\n\nCreate `main.py` file with the following content:\n\n```python\nimport flet as ft\n\ndef main(page: ft.Page):\n    page.title = "Flet counter example"\n    page.vertical_alignment = ft.MainAxisAlignment.CENTER\n\n    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)\n\n    def minus_click(e):\n        txt_number.value = str(int(txt_number.value) - 1)\n        page.update()\n\n    def plus_click(e):\n        txt_number.value = str(int(txt_number.value) + 1)\n        page.update()\n\n    page.add(\n        ft.Row(\n            [\n                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),\n                txt_number,\n                ft.IconButton(ft.icons.ADD, on_click=plus_click),\n            ],\n            alignment=ft.MainAxisAlignment.CENTER,\n        )\n    )\n\nft.app(main)\n```\n\n## Run the app\n\n```\nflet run --web main.py\n```\n\n![Sample app in a browser](https://flet.dev/img/docs/getting-started/flet-counter-safari.png)\n\n## Publish app as a static website\n\n```\nflet publish main.py\n```\n\nA static website is published into `./dist` directory.\n\n## Test website\n\n```\npython -m http.server --directory dist\n```\n\nOpen `http://localhost:8000` in your browser to check the published website.\n\n## Deploy website\n\nDeploy a static website to any free hosting such as GitHub Pages, Cloudflare Pages or Vercel!\n\n## Learn more\n\nVisit [Flet website](https://flet.dev).\n\nContinue with [Python guide](https://flet.dev/docs/getting-started/python) to learn how to make a real app.\n\nBrowse for more [Flet examples](https://github.com/flet-dev/examples/tree/main/python).\n\nJoin to a conversation on [Flet Discord server](https://discord.gg/dzWXP8SHG8).\n',
    'author': 'Appveyor Systems Inc.',
    'author_email': 'hello@flet.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
