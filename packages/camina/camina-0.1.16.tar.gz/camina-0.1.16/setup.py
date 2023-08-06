# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camina']

package_data = \
{'': ['*']}

install_requires = \
['miller>=0.1.7,<0.2.0']

setup_kwargs = {
    'name': 'camina',
    'version': '0.1.16',
    'description': 'Your Python project companion',
    'long_description': "[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Documentation Status](https://readthedocs.org/projects/camina/badge/?version=latest)](http://camina.readthedocs.io/?badge=latest)\n\n\nThis package adds functionality to core Python container classes and provides functions for common tasks.\n\n## Mappings\n* `Dictionary`: drop-in replacement for a python dict with an `add` method for a default mechanism of adding data, a `delete` method for a default mechanism of deleting data, and a `subset` method for returning a subset of the key/value pairs in a new `Dictionary`.\n* `Catalog`: wildcard-accepting dict which is intended for storing different options and strategies. It also returns lists of matches if a list of keys is provided.\n* `Library`: a dictionary that automatically supplies key names for stored items. The 'overwrite' argument determines if a unique key should always be created or whether entries may be overwritten.\n\n## Sequences\n* `Listing`: drop-in replacement for a python list with an `add` method for a default mechanism of adding data, a `delete` method for a default mechanism of deleting data, and a `subset` method for returning a subset of the key/value pairs in a new `Listing`.\n* `Hybrid`: iterable with both dict and list interfaces. Stored items must be hashable or have a `name` attribute.\n\n## Passthrough\n* `Proxy`: transparently wraps an object and directs access methods to access the wrapped object when appropriate (under construction for edge cases).\n\n## Converters\n\n* `instancify`: converts a class to an instance or adds kwargs to a passed instance as attributes.\n* `listify`: converts passed item to a list.\n* `namify`: returns hashable name for passed item.\n* `numify`: attempts to convert passed item to a numerical type.\n* `pathlibify`: converts a str to a pathlib object or leaves it as a pathlib object.\n* `stringify`:\n* `tuplify`: converts a passed item to a tuple.\n* `typify`: converts a str type to other common types, if possible.\n*  `windowify`:\n* `to_dict`:\n* `to_index`:\n* `str_to_index`:\n* `to_int`:\n* `str_to_int`:\n* `float_to_int`:\n* `to_list`:\n* `str_to_list`:\n* `to_float`:\n* `int_to_float`:\n* `str_to_float`:\n* `to_path`:\n* `str_to_path`:\n* `to_str`:\n* `int_to_str`:\n* `float_to_str`:\n* `list_to_str`:\n* `none_to_str`:\n* `path_to_str`:\n* `datetime_to_str`:\n\n## Modifiers\n* Adders:\n    * `add_prefix`: adds a str prefix to item.\n    * `add_slots`: adds `__slots__` to a dataclass.\n    * `add_suffix`: adds a str suffix to item.\n* Dividers:\n    * `cleave`: divides an item into 2 parts based on `divider` argument.\n    * `separate`: divides an item into n+1 parts based on `divider` argument.\n* Subtractors:\n    * `deduplicate`: removes duplicate data from an item.\n    * `drop_dunders`: drops strings from a list if they start and end with double underscores.\n    * `drop_prefix`: removes a str prefix from an item.\n    * `drop_prefix_from_dict`\n    * `drop_prefix_from_list`\n    * `drop_prefix_from_set`\n    * `drop_prefix_from_str`\n    * `drop_prefix_from_tuple`\n    * `drop_privates`\n    * `drop_substring`: removes a substring from an item.\n    * `drop_suffix`: removes a str suffix from an item.\n    * `drop_suffix_from_dict`\n    * `drop_suffix_from_list`\n    * `drop_suffix_from_set`\n    * `drop_suffix_from_str`\n    * `drop_suffix_from_tuple`\n* Other: \n    * `capitalify`: converts a snake case str to capital case.\n    * `snakify`: converts a capital case str to snake case.\n    * `uniquify`: returns a unique key for a dict.\n\ncamina supports a wide range of coding styles. You can create complex multiple inheritance structures with mixins galore or simpler, compositional objects. Even though the data structures are necessarily object-oriented, all of the tools to modify them are also available as functions, for those who prefer a more funcitonal approaching to programming. \n\nThe project is also highly internally documented so that users and developers can easily make camina work with their projects. It is designed for Python coders at all levels. Beginners should be able to follow the readable code and internal documentation to understand how it works. More advanced users should find complex and tricky problems addressed through efficient code.",
    'author': 'corey rayburn yung',
    'author_email': 'coreyrayburnyung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WithPrecedent/camina',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
