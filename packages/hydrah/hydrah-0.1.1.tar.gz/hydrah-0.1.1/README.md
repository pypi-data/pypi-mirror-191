![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydrah?style=plastic)

# Hydra Validator Library

Hydrah is a validation library for Python that provides a simple and easy way to validate inputs in your applications. With Hydrah, you can validate user inputs, command-line arguments, or configuration files with just a few lines of code.

## Features
- Simple and easy to use
- Supports multiple data types (strings, integers, lists, objects, booleans, datetime)
- Can validate inputs and provide detailed error messages
- Provides a `coerce` method to automatically convert inputs to the desired data type

## Installation
h can be installed using pip:

```shell
pip install hydrah
```


## Usage
To validate an input, you need to first create a validator instance for the desired data type. For example, to validate a string input:

```python
from hydrah import h

validator = h.string()

if validator.is_valid("hello"):
    print("Valid input")
else:
    print(validator.get_error_message("hello"))
```

To validate a list of strings:

```python
from hydrah import h

list_validator = h.list()string()

if list_validator.is_valid(["hello", "world"]):
    print("Valid input")
else:
    print(list_validator.get_error_message(["hello", 1]))
```

To validate an object:

```python
from hydrah import h

object_validator = h.object({
    "name": h.string(),
    "age": h.integer()
})

if object_validator.is_valid({"name": "John", "age": 30}):
    print("Valid input")
else:
    print(object_validator.get_error_message({"name": "John", "age": "30"}))
```

## Custom Validators

Hydrah can also be extended to support custom data types. To create a custom validator, you need to inherit from the Validator class and implement the is_valid and get_error_message methods.

For example, to create a validator for boolean inputs:

```python
from hydrah import Validator

class BooleanValidator(Validator):
    def is_valid(self, value):
        return isinstance(value, bool)

    def get_error_message(self, value):
        return f"Expected boolean, but got {type(value).__name__}"
```

## Coercion

Hydrah also provides a coerce method to automatically convert inputs to the desired data type. For example:

```python
from hydrah import h

validator = h.integer()

value = validator.coerce("10")

print(value) # 10
print(type(value)) # <class 'int'>
```

## Creating Objects with Optional Schemas

In some cases, you may want to define a schema that is optional, meaning that it can either be present or absent in the data. To define an optional schema in Hydrah, you can either use `hydrah.h.string().optional()` or `hydrah.h.optional(hydrah.h.string())`.

Here's an example of how you could define an object with an optional string field using both methods:

```python
from hydrah import h
# Using string().optional()
optional_string_validator = h.object({
    "optional_field": h.string().optional()
})

# Using optional(hydrah.h.string())
optional_string_validator = h.object({
    "optional_field": h.optional(hydrah.string())
})

# Both of these validators will accept the following data:
data = {
    "optional_field": "Hello, world!"
}

assert optional_string_validator.is_valid(data)

# And also this data:
data = {}

assert optional_string_validator.is_valid(data)
```