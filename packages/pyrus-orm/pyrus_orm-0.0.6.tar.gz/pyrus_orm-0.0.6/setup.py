# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrus_orm']

package_data = \
{'': ['*']}

install_requires = \
['pyrus-api>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'pyrus-orm',
    'version': '0.0.6',
    'description': "Radically simple ORM for Pyrus's tasks",
    'long_description': 'pyrus-orm\n=========\n\nRadically simple, django/peewee-like, easy and incomplete ORM for [Pyrus](https://pyrus.com).\n\nWith pyrus-orm, you can read, create and modify [tasks](https://pyrus.com/en/help/api/models#form-registry-task).\n\nWorks with [pyrus-api](https://github.com/simplygoodsoftware/pyrusapi-python) under the hood.\n\n### This is an early development version\n\n### Features:\n\n- Define models with:\n    - [x] simple fields (text, number, dates, ...)\n    - [x] catalog fields, single item\n    - [ ] catalog fields, multiple items\n    - [ ] "title" fields\n    - [x] multiple choice fields (without nested fields at this moment)\n- Operations with models:\n    - [x] Create and save\n    - [x] Read from registry by ID\n    - [x] Modify and save changes\n- Filtering:\n    - [x] by include_archived and steps fields\n    - [x] by value of simple or catalog fields\n    - [ ] less than, greater than\n    - [ ] value in a list\n    - [ ] ranges\n\nInstallation\n-----------\n\n```shell\npip install pyrus-orm\n```\n\nExamples\n-------\n\n\n### Define model and initialize\n\n```python\n\nclass Book(PyrusModel):\n    title = TextField(1)  # 1 is a field ID in pyrus\'s form\n    time = TimeField(2)\n    date = DateField(3)\n    number = NumericField(4)\n    round_number = IntegerField(5)\n    author = CatalogField(6, catalog=<catalog id>)\n\n    class Meta:\n        form_id = <form_id>\n\n\npyrus_api = PyrusAPI(...)\nsession = PyrusORMSession(pyrus_api)\n\nset_session_global(session)\n```\n\n\n### Create item\n\n```python\nbook = Book(\n    title=\'Don Quixote\',\n    date=\'1605-01-01\',\n    author=Book.author.find({\'Name\': \'Alonso Fernández de Avellaneda\'})\n)\n\nbook.save()\n\nbook.id\n>>> <task_id>\n```\n\n\n### Read and modify item\n\n```python\nbook = Book.objects.get(id=...)\n\n# simple field\nbook.title\n>>> \'Don Quixote\'\nbook.title = \'Don Quixote, Part Two\'\nbook.save(\'title changed\')\n\n# catalog field\nbook.author\n>>> CatalogItem(item_id=..., values={\'Name\': \'Alonso Fernández de Avellaneda\'})  # values comes from the catalog definition\n\nbook.author.find_and_set({\'Name\': \'Miguel de Cervantes\'})  # may raise ValueError if no value found\nbook.save(\'changed an author to the real one\')\n```\n\n### Catalog Enum fields\n\nEnums can be mapped to catalog items by ID or by custom property name.\n\n#### Enums mapped to specific catalog items ID\n\nNo catalog lookups are preformed on reading or writing of such fields.\n\n```python\nclass Genre(Enum):\n    fiction = 100001\n    nonfiction = 100002\n\n\nclass Book(PyrusModel):\n    genre = CatalogEnumField(<field_id>, catalog_id=<catalog_id>, enum=Genre, id_field=\'item_id\')\n\nbook = Book.objects.get(id=...)\n\nbook.genre\n>>> Genre.fiction\n\nbook.genre = Genre.nonfiction\nbook.save()\n\nbook.genre\n>>> Genre.nonfiction\n```\n\n\n#### Enums mapped to catalog item properties\n\n(imagine book has a property \'media\' with field \'Name\')\n\n```python\nclass Media(Enum):\n    paper = \'paper\'\n    papirus = \'papirus\'\n    pdf = \'pdf\'\n\nclass Book(PyrusModel):\n    media = CatalogEnumField(<field_id>, catalog_id=<catalog_id>, enum=Genre, id_field=\'Name\')\n```\n\n### Filtering\n\nOnly basic filtering is supported:\n\n```python\n\nBook.objects.get_filtered(\n    title=\'Don Quixote\',\n)\n>>> [Book(...), ...]\n\n\nBook.objects.get_filtered(\n    genre=Book.genre.find({\'Name\': \'Fiction\'})\n)\n>>> [Book(...), ...]\n\nBook.objects.get_filtered(\n    ...\n    include_archived=True,\n    steps=[1, 2],\n)\n>>> [Book(...), ...]\n```\n\n\n### Catalog fields, all the API\n```python\n# Read values\n\n# Non-empty value\nbook.author\n>>> CatalogItem(item_id=..., values={<your custom values here>})\n\nassert bool(book.author) == True\n\n# Empty value\nbook.author\n>>> CatalogEmptyValue()\n\nassert bool(book.author) == False\n\n\n# Get all possible values (works for empty fields as well)\nbook.author.catalog()\n>>> [CatalogItem(...), CatalogItem(...), ...]\n\n\n# Find a value in a catalog\nnew_author = book.author.catalog().find({\'Name\': \'Miguel de Cervantes\'})\nnew_author\n>>> CatalogItem(item_id=..., values={\'Name\': \'Miguel de Cervantes\'})  # or None\n\nbook.author = new_author\nbook.save()\n\n\n# Find and set shortcut\nbook.author.catalog().find_and_set({\'Name\': \'William Shakespeare\'})\n\nbook.author.find_and_set({\'Name\': \'NonExistent\'})\n>>> ValueError raised\n\n\n# Set value to a specific item_id\nbook.author = CatalogItem(item_id=123456)\n```',
    'author': 'Alexey Sveshnikov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
