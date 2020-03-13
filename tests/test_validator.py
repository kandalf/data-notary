import unittest

from notary.validator import Validator

class UserValidator(Validator):
    def validate(self):
        self.assert_present("email")
        self.assert_present("name", message = "Name is not present")

        self.assert_list("phone_numbers")
        self.assert_list("addresses", message = "Addresses is not a list")

        self.assert_not_present("middle_name")
        self.assert_not_present("age", message = "Age is not allowed")

        self.assert_in("identifications", "Passport")

class TestValidator(unittest.TestCase):
    def test_presence(self):
        attrs = { "last_name": "Staley" }

        validator = UserValidator(**attrs)

        self.assertFalse(validator.is_valid())
        self.assertEqual(validator.errors["email"], ["not_present"])
        self.assertEqual(validator.errors["name"], ["Name is not present"])

    def test_no_presence(self):
        attrs = {
            "first_name": "Layne",
            "middle_name": "Thomas",
            "last_name": "Staley",
            "email": "layne@aic.com",
            "phone_numbers": "(555) 555-5555, (222) 222-2222",
            "addresses": "123 Some St",
            "age": 34
        }

        validator = UserValidator(**attrs)

        self.assertFalse(validator.is_valid())
        self.assertEqual(validator.errors["middle_name"], ["not_allowed"])
        self.assertEqual(validator.errors["age"], ["Age is not allowed"])

    def test_list(self):
        attrs = {
            "first_name": "Layne",
            "last_name": "Staley",
            "email": "layne@aic.com",
            "phone_numbers": "(555) 555-5555, (222) 222-2222",
            "addresses": "123 Some St"
        }

        validator = UserValidator(**attrs)

        self.assertFalse(validator.is_valid())
        self.assertEqual(validator.errors["phone_numbers"], ["not_valid"])
        self.assertEqual(validator.errors["addresses"], ["Addresses is not a list"])

    def test_in_list(self):
        attrs = {
            "first_name": "Layne",
            "last_name": "Staley",
            "email": "layne@aic.com",
            "phone_numbers": "(555) 555-5555, (222) 222-2222",
            "addresses": "123 Some St",
            "identifications": ["Driver's License", "Government ID"]
        }

        validator = UserValidator(**attrs)

        self.assertFalse(validator.is_valid())
        self.assertEqual(validator.errors["identifications"], ["Passport_not_in_list"])

if __name__ == '__main__':
    unittest.main()
