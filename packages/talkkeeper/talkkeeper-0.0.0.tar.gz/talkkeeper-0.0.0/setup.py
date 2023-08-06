# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['talkkeeper', 'talkkeeper.cli']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['gdshoplib = talkkeeper:application']}

setup_kwargs = {
    'name': 'talkkeeper',
    'version': '0.0.0',
    'description': 'Библиотека Python talkkeeper для загрузки в хранилище / предобработки / разметки / ...',
    'long_description': '# Обработчик Media файлов\n\n- Создание meta заголовка\n- Разбивка на фреймы\n- Загрузка фреймов в очередь\n\n',
    'author': 'Nikolay Baryshnikov',
    'author_email': 'root@k0d.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/p141592',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
