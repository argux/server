"""Authentication Module."""

import inspect

import string
import random

from . import auth_bcrypt

__VALIDATE_METHODS = {}
__GEN_HASH_METHODS = {}


def __verify_validate_function(func):
    """
    Verify function to validate a hash.

    Should have two parameters, one for the password
    and one for the hashed representation of the
    password.
    """
    sig = inspect.signature(func)
    if len(sig.parameters) != 2:
        raise ValueError(
            "Function has {} arguments, expected 2"
            .format(len(sig.parameters)))

    if "password" not in sig.parameters:
        raise ValueError("Function has no 'password' argument")
    if "hashed" not in sig.parameters:
        raise ValueError("Function has no 'hashed' argument")
    return


def __verify_gen_hash_function(func):
    """
    Verify function to generate a hash.

    Should have only one parameter called 'password'.
    """
    sig = inspect.signature(func)
    if len(sig.parameters) != 1:
        raise ValueError(
            "Function has {} arguments, expected 1"
            .format(len(sig.parameters)))

    if "password" not in sig.parameters:
        raise ValueError("Function has no 'password' argument")
    return


def register_auth_functions(name, validate_func, gen_hash_func):
    """Register auth and passwd func."""
    __verify_validate_function(validate_func)
    __verify_gen_hash_function(gen_hash_func)

    if name in __VALIDATE_METHODS:
        raise ValueError(
            "Function name '{}' already exists"
            .format(name))

    __VALIDATE_METHODS[name] = validate_func
    __GEN_HASH_METHODS[name] = gen_hash_func


def validate(name, password, hashed):
    """
    Validate hash 'hashed' of type 'name' against password

    Returns True if the hash can be validated.
    """
    if name in __VALIDATE_METHODS:
        return __VALIDATE_METHODS[name](password, hashed)
    else:
        return False


def gen_hash(name, password):
    """
    Generate a hash of type 'name' from password.

    Raises a ValueError if Hash-method of type 'name'
    does not exist.
    """
    if name in __GEN_HASH_METHODS:
        return __GEN_HASH_METHODS[name](password)
    else:
        raise ValueError(
            "Hash-method '{}' does not exists"
            .format(name))


def gen_password(size=12, chars=string.ascii_uppercase + string.digits):
    """Generate a random password-string of 'size' characters long."""
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

# Register functions.
register_auth_functions(
    'bcrypt',
    auth_bcrypt.validate,
    auth_bcrypt.gen_hash)
