import unittest


from argux_server.auth import register_auth_functions

def gen_hash_valid(password):
    """Function with a signature of a valid gen_hash function."""
    return

def gen_hash_missing_password(wrong):
    """Gen_hash function with a missing password argument."""
    return

def gen_hash_too_many_args(password, wrong):
    """Gen_hash function with too many arguments."""
    return

def validate_valid(password, hashed):
    """Function with a signature of a valid validate function."""
    return

def validate_missing_password(wrong, hashed):
    """Validate function with a missing password argument."""
    return

def validate_missing_hashed(password, wrong):
    """Validate function with a missing hashed argument."""
    return

def validate_too_many_args(password, hashed, too_many):
    """Validate function with too many arguments"""
    return


class AuthenticationTests(unittest.TestCase):

    def test_register_auth_validate_missing_password(self):
        """Test register_auth_func error with missing hashed argument.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password).
        It raises a ValueError if a function does not follow this
        format.

        This Test validates the error-message when the function
        is missing a 'username' argument.
        """
        with self.assertRaises(ValueError) as cm:
            register_auth_functions(
                'validate_missing_password',
                validate_missing_password,
                gen_hash_valid)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function has no 'password' argument")

    def test_register_auth_validate_missing_hashed(self):
        """Test register_auth_func error with missing hashed argument.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password).
        It raises a ValueError if a function does not follow this
        format.

        This Test validates the error-message when the function
        is missing a 'password' argument.
        """
        with self.assertRaises(ValueError) as cm:
            register_auth_functions(
                'validate_missing_hashed',
                validate_missing_hashed,
                gen_hash_valid)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function has no 'hashed' argument")

    def test_register_auth_validate_too_many_args(self):
        """Test register_auth_func error with too many arguments.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password).
        It raises a ValueError if a function does not follow this
        format.

        This Test validates the error-message when the function does
        not have the right number of arguments.
        """
        with self.assertRaises(ValueError) as cm:
            register_auth_functions(
                'validate_too_many_args',
                validate_too_many_args,
                gen_hash_valid)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function has 3 arguments, expected 2")

    def test_register_auth_gen_hash_missing_password(self):
        """Test register_auth_func error with missing hashed argument.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password).
        It raises a ValueError if a function does not follow this
        format.

        This Test validates the error-message when the function
        is missing a 'username' argument.
        """
        with self.assertRaises(ValueError) as cm:
            register_auth_functions(
                'gen_hash_missing_password',
                validate_valid,
                gen_hash_missing_password)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function has no 'password' argument")

    def test_register_auth_gen_hash_too_many_args(self):
        """Test register_auth_func error with too many arguments.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password).
        It raises a ValueError if a function does not follow this
        format.

        This Test validates the error-message when the function does
        not have the right number of arguments.
        """
        with self.assertRaises(ValueError) as cm:
            register_auth_functions(
                'gen_hash_too_many_args',
                validate_valid,
                gen_hash_too_many_args)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function has 2 arguments, expected 1")

    def test_register_valid_func(self):
        """Test behaviour if a valid auth_func is registered."""

        register_auth_functions(
            'valid_func',
            validate_valid,
            gen_hash_valid)

    def test_register_duplicates(self):
        """Test register_auth_func error with duplicate names.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password)
        and a name argument.
.
        It raises a ValueError if a function with a simmilar
        name is already registered.

        This Test validates the error-message when a duplicate
        name already exists.
        """

        register_auth_functions(
            'duplicate',
            validate_valid,
            gen_hash_valid)

        with self.assertRaises(ValueError) as cm:
            register_auth_functions(
                'duplicate',
                validate_valid,
                gen_hash_valid)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function name 'duplicate' already exists")
