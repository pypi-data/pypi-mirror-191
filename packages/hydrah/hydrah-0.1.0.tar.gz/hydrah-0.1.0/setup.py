# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hydrah']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hydrah',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Hydra Validator Library\n\nHydrah is a validation library for Python that provides a simple and easy way to validate inputs in your applications. With Hydrah, you can validate user inputs, command-line arguments, or configuration files with just a few lines of code.\n\n## Features\n- Simple and easy to use\n- Supports multiple data types (strings, integers, lists, objects, booleans, datetime)\n- Can validate inputs and provide detailed error messages\n- Provides a `coerce` method to automatically convert inputs to the desired data type\n\n## Installation\nh can be installed using pip:\n\n```shell\npip install hydrah\n```\n\n\n## Usage\nTo validate an input, you need to first create a validator instance for the desired data type. For example, to validate a string input:\n\n```python\nfrom hydrah import h\n\nvalidator = h.string()\n\nif validator.is_valid("hello"):\n    print("Valid input")\nelse:\n    print(validator.get_error_message("hello"))\n```\n\nTo validate a list of strings:\n\n```python\nfrom hydrah import h\n\nlist_validator = h.list()string()\n\nif list_validator.is_valid(["hello", "world"]):\n    print("Valid input")\nelse:\n    print(list_validator.get_error_message(["hello", 1]))\n```\n\nTo validate an object:\n\n```python\nfrom hydrah import h\n\nobject_validator = h.object({\n    "name": h.string(),\n    "age": h.integer()\n})\n\nif object_validator.is_valid({"name": "John", "age": 30}):\n    print("Valid input")\nelse:\n    print(object_validator.get_error_message({"name": "John", "age": "30"}))\n```\n\n## Custom Validators\n\nHydrah can also be extended to support custom data types. To create a custom validator, you need to inherit from the Validator class and implement the is_valid and get_error_message methods.\n\nFor example, to create a validator for boolean inputs:\n\n```python\nfrom hydrah import Validator\n\nclass BooleanValidator(Validator):\n    def is_valid(self, value):\n        return isinstance(value, bool)\n\n    def get_error_message(self, value):\n        return f"Expected boolean, but got {type(value).__name__}"\n```\n\n## Coercion\n\nHydrah also provides a coerce method to automatically convert inputs to the desired data type. For example:\n\n```python\nfrom hydrah import h\n\nvalidator = h.integer()\n\nvalue = validator.coerce("10")\n\nprint(value) # 10\nprint(type(value)) # <class \'int\'>\n```\n\n## Creating Objects with Optional Schemas\n\nIn some cases, you may want to define a schema that is optional, meaning that it can either be present or absent in the data. To define an optional schema in Hydrah, you can either use `hydrah.h.string().optional()` or `hydrah.h.optional(hydrah.h.string())`.\n\nHere\'s an example of how you could define an object with an optional string field using both methods:\n\n```python\nfrom hydrah import h\n# Using string().optional()\noptional_string_validator = h.object({\n    "optional_field": h.string().optional()\n})\n\n# Using optional(hydrah.h.string())\noptional_string_validator = h.object({\n    "optional_field": h.optional(hydrah.string())\n})\n\n# Both of these validators will accept the following data:\ndata = {\n    "optional_field": "Hello, world!"\n}\n\nassert optional_string_validator.is_valid(data)\n\n# And also this data:\ndata = {}\n\nassert optional_string_validator.is_valid(data)\n```',
    'author': 'Marco Maier',
    'author_email': 'mm.maiermarco@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
