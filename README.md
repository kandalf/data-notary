# Data Notary

Or simply _notary_ is a simple data validation for Python objects. "Inspired on" (actually stolen from) [Scrivener](https://github.com/soveran/scrivener) for Ruby.

## Install

```
pip install data-notary
```

## Usage

You need to subclass `notary.validator.Validator` and override the `validate` instance method.

For example, a class to validate user data could be like:

```Python
from notary.validator import Validator

class UserValidator(Validator):
  def validate(self):
    self.assert_present("first_name")

    self.assert_not_present("middle_name")

    self.assert_present("email")

    self.assert_list("phone_numbers")

    self.assert_in("identifications", "Passport")

```

The validator has 4 basic assertions as shown in the example. Once defined, you can use it like the following example:

```Python
from .validators import UserValidator
from .models import User

attrs = {
    "first_name": "Layne",
    "middle_name": "Thomas",
    "last_name": "Staley",
    "email": "layne@aic.com",
    "phone_numbers": "(555) 555-5555, (222) 222-2222",
    "addresses": "123 Some St",
    "identification_methods": ["Driver's License", "Government ID"]
}

validator = UserValidator(**attrs)

if validator.is_valid():
  user = User(
    first_name = validator.first_name,
    last_name  = validator.last_name,
    email = validator.email,
    phone_numbers = validator.phone_numbers,
    addresses = validator.addresses,
    identification_methods = validator.identification_methods
  )
else:
  print("Error!")
  print(validator.errors)
```

In this case, you should see an output like the following

```
Error!
{'middle_name': ['not_allowed'], 'phone_numbers': ['not_valid'], 'identifications': ['Passport_not_in_list']}
```

You could also specify your own error messages, for example, a validator like the following

```Python
class UserValidator(Validator):
  def validate(self):
    self.assert_present("first_name")

    self.assert_not_present("middle_name", message = "Sorry, mate, I don't like middle names")

    self.assert_present("email")

    self.assert_list("phone_numbers")

    self.assert_in("identifications", "Passport")

```

would produce the following output

```
Error!
{'middle_name': ["Sorry, mate, I don't like middle names"], 'phone_numbers': ['not_valid'], 'identifications': ['Passport_not_in_list']}
```

In case you need to validate something that goes beyond the basic assertion methods provided, the `notary.validator.Validator` class provides the `_add_error` method. For example

```Python
class UserValidator(Validator):
  def validate(self):
    self.assert_present("first_name")

    if self.last_name and len(self.last_name) >= 5:
      self._add_error("last_name", "Last name must be shorter than 5 characters")

    self.assert_not_present("middle_name")

    self.assert_present("email")

    self.assert_list("phone_numbers")

    self.assert_in("identifications", "Passport")
```

Using the same example, this would produce the following output

```
Error!
{'last_name': ['Last name must be shorter than 5 characters'], 'middle_name': ["Sorry, mate, I don't like middle names"], 'phone_numbers': ['not_valid'], 'identifications': ['Passport_not_in_list']
```

And last but not least, you can have more than one validation per attribute, modifying a bit the example above, we could have the following:

```Python
class UserValidator(Validator):
  def validate(self):
    self.assert_present("first_name")

    if self.assert_present("password"):
      if len(self.password) <= 5:
        self._add_error("password", "Password must be longer than 5 characters")

      if not "#" in self.password:
        self._add_error("password", "Password must include the # character")

    self.assert_not_present("middle_name")

    self.assert_present("email")

    self.assert_list("phone_numbers")

    self.assert_in("identifications", "Passport")
```

Which would produce the follwing output:

```Python
Error!
{'password': ['Password must be longer than 5 characters', 'Password must include the # character'], 'middle_name': ["Sorry, mate, I don't like middle names"], 'phone_numbers': ['not_valid'], 'identifications': ['Passport_not_in_list']}
```
