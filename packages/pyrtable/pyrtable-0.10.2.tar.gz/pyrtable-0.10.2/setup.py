# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyrtable', 'pyrtable.context', 'pyrtable.fields', 'pyrtable.filters']

package_data = \
{'': ['*']}

install_requires = \
['deprecated',
 'pyyaml>=5.1,<7',
 'requests>=2.22.0,<3.0.0',
 'simplejson>=3.16.0,<4.0.0']

setup_kwargs = {
    'name': 'pyrtable',
    'version': '0.10.2',
    'description': 'Django-inspired library to interface with Airtable',
    'long_description': '# Pyrtable: Python framework for interfacing with Airtable\n\nPyrtable is a Python 3 library to interface with [Airtable](https://airtable.com)\'s REST API.\n\nThere are other Python projects to deal with Airtable. However, most of them basically offer a thin layer to ease authentication and filtering – at the end, the programmer still has to manually deal with JSON encoding/decoding, pagination, request rate limits, and so on.\n\nPyrtable is a high-level, ORM-like library that hides all these details. It performs automatic mapping between Airtable records and Python objects, allowing CRUD operations while aiming to be intuitive and fun. Programmers used to [Django](https://www.djangoproject.com) will find many similarities and will (hopefully) be able to interface with Airtable bases in just a couple of minutes.\n\n## What does it look like?\n\nOk, let\'s have a taste of how one can define a class that maps onto records of a table:\n\n````python\nimport enum\nfrom pyrtable.record import BaseRecord\nfrom pyrtable.fields import StringField, DateField, SingleSelectionField, \\\n        SingleRecordLinkField, MultipleRecordLinkField\n\nclass Role(enum.Enum):\n    DEVELOPER = \'Developer\'\n    MANAGER = \'Manager\'\n    CEO = \'C.E.O.\'\n\nclass EmployeeRecord(BaseRecord):\n    class Meta:\n        # Open “Help > API documentation” in Airtable and search for a line\n        # starting with “The ID of this base is XXX”.\n        base_id = \'appABCDE12345\'\n        table_id = \'Employees\'\n\n    @classmethod\n    def get_api_key(cls):\n        # The API Key can be generated in you Airtable Account page.\n        # DO NOT COMMIT THIS STRING!\n        return \'keyABCDE12345\'\n\n    name = StringField(\'Name\')\n    birth_date = DateField(\'Birth date\')\n    office = SingleRecordLinkField(\'Office\', linked_class=\'OfficeRecord\')\n    projects = MultipleRecordLinkField(\n            \'Allocated in projects\', linked_class=\'ProjectRecord\')\n    role = SingleSelectionField(\'Role\', choices=Role)\n````\n\nAfter that, common operations are pretty simple:\n\n````python\n# Iterating over all records\nfor employee in EmployeeRecord.objects.all():\n    print("%s is currently working on %d project(s)" % (\n        employee.name, len(employee.projects)))\n\n# Filtering\nfor employee in EmployeeRecord.objects.filter(\n        birth_date__gte=datetime.datetime(2001, 1, 1)):\n    print("%s was born in this century!" % employee.name)\n\n# Creating, updating and deleting a record\nnew_employee = EmployeeRecord(\n    name=\'John Doe\',\n    birth_date=datetime.date(1980, 5, 10),\n    role=Role.DEVELOPER)\nnew_employee.save()\n\nnew_employee.role = Role.MANAGER\nnew_employee.save()\n\nnew_employee.delete()\n````\n\nNotice that we don\'t deal with Airtable column or table names once record classes are defined.\n\n## Beyond the basics\n\nKeep in mind that Airtable is *not* a database system and is not really designed for tasks that need changing tons of data. In fact, only fetch (list) operations are batched – insert/update/delete operations are limited to a single record per request, and Airtable imposes a 5 requests per second limit even for paid accounts. You will need a full minute to update 300 records!\n\nThat said, Pyrtable will respect that limit. In fact, it will track dirty fields to avoid unnecessary server requests and will render `.save()` calls as no-ops for unchanged objects. That also works with multiple threads, so the following pattern can be used to update and/or create several records:\n\n```python\nfrom concurrent.futures.thread import ThreadPoolExecutor\n\nall_records = list(EmployeeRecord.objects.all())\n\n# Do operations that change some records here\n# No need to keep track of which records were changed\n\nwith ThreadPoolExecutor(max_workers=10) as executor:\n    for record in all_records:\n        executor.submit(record.save)\n```\n\nOr, if you want a really nice [tqdm](https://tqdm.github.io) progress bar:\n\n```python\nfrom tqdm import tqdm\n\nwith ThreadPoolExecutor(max_workers=10) as executor:\n    for _ in tqdm(executor.map(lambda record: record.save(), all_records),\n                  total=len(all_records), dynamic_ncols=True, unit=\'\',\n                  desc=\'Updating Airtable records\'):\n        pass\n```\n\nPyrtable also has some extra tools to cache data and to store authentication keys in JSON/YAML files or in an environment variable. Remember to never commit sensitive data to your repository, as Airtable authentication allows **full R/W access to all your bases** with a single API Key!\n\n## Compatibility\n\nPyrtable is compatible with Python 3.8 and above. Python 2.x is not supported at all.\n\n## Documentation\n\nTechnical documentation is available at https://pyrtable.readthedocs.io.\n\n## Questions, bug reports, improvements\n\nWant to try it out, contribute, suggest, offer a hand? Great! The project is available at https://github.com/vilarneto/pyrtable.\n\n## License\n\nPyrtable is released under [MIT license](https://opensource.org/licenses/MIT).\n\nCopyright (c) 2020,2021,2022 by Vilar Fiuza da Camara Neto\n',
    'author': 'Vilar da Camara Neto',
    'author_email': 'vilarneto@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vilarneto/pyrtable',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
