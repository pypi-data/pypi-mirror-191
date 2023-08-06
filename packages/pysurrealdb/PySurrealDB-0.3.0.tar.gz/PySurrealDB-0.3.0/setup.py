# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysurrealdb', 'pysurrealdb.clients', 'pysurrealdb.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests']

setup_kwargs = {
    'name': 'pysurrealdb',
    'version': '0.3.0',
    'description': 'A library to connect to SurrealDB.',
    'long_description': '# PySurrealDB\n\n[![Join the chat at https://gitter.im/pysurrealdb/community](https://badges.gitter.im/pysurrealdb/community.svg)](https://gitter.im/pysurrealdb/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\nAn unofficial library to connect to SurrealDB.\n\nMinimal dependencies, easy to use.\n\n---\n## Getting Started\n\nIf you don\'t already have it, install [SurrealDB](https://surrealdb.com/docs/start/installation)\n\nLinux: \n``` bash\n$ curl -sSf https://install.surrealdb.com | sh\n# then\n$ surreal start --user test --pass test\n```\n\n\n### Install PySurrealDB\n```\npip install pysurrealdb\n```\n\n\n### Examples\n\n```python\nimport pysurrealdb as surreal\n\nconn = surreal.connect(user=\'test\', password=\'test\')\n\nconn.create(\'person\', {\'name\': \'Mike\'})\nconn.query(\'select * from person\')\n```\n\nYou can specify additional connection info either in the connect call, or in a config file.\n\n```python\nimport pysurrealdb as surreal\nconn = surreal.connect(host=\'surreal.com\', port=8000, user=\'user\', password=\'pass\', database=\'db\', namespace=\'ns\')\n```\n\nBoth http and websocket are supported. Specify which to use with the client keyword.\n```python\nconn = surreal.connect(client=\'websocket\')\n# Websocket was added and made the default as of version 0.3. Try http if you run into issues, and please report any bugs you find!\n```\n\nOptional Config file:\n```python\n# use a configured connection. \nconn = surreal.connection(\'default\')\n# Requires pysurrealdb.json file. Place it in your root directory, or specify the file location with the env variable \'PYSURREALDB_CONFIG\'.\n\nExample pysurrealdb.json:\n{\n    "connections": {\n        "default": {\n            "host": "localhost",\n            "port": 8000,\n            "user": "test",\n            "password": "test"\n            "database": "test",\n            "namespace": "test",\n            "client": "http",\n        }\n    }\n}\n\n# when using a config file, you do not even need to connect, you can access most functions directly:\nimport pysurrealdb as surreal\n\nsurreal.query(\'select * from test\') # uses the last connection from connect() or the default connection if connect() has not been called.\n```\n\n\n## Query Builder\n\nYou can write queries using Laravel and Orator style syntax:\n```python\nimport pysurrealdb as surreal\nconn = surreal.connection()\n\n# setup data\nconn.drop(\'person\')\nconn.insert(\'person\', [{\'name\': \'Mike\', \'age\': 31}, {\'name\':\'Mr P\'}])\n\n# query builder examples\nfirst_person = conn.table(\'person\').where(\'name\', \'Mike\').first()\n\nadults = conn.table(\'person\').where(\'age\', \'>=\', 18).order_by(\'age\', \'desc\').limit(10).get()\n```\n\n## Methods\nSome of the basic methods available:\n```python\nquery(sql)\nget(table, id=\'\')\ninsert(table, data)\ncreate(table, data)\nupdate(table, data)\nupsert(table, data)\ndelete(table, id)\ndrop(table)\nrelate(noun, verb, noun2, data={})\n\n# Most methods accept a table or table:id as the main arguement. The data is also checked for an ID when relevant.\n```\n\n\nThis project is a work in progress. Questions and feedback are welcome! Please create an issue or use the gitter chat link at the top. Thanks!\n',
    'author': 'Aurelion314',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
