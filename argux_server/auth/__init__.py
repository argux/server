"""Authentication Module."""

import inspect

import string
import random

from . import auth_bcrypt

__VALIDATE_METHODS = {}
__GEN_HASH_METHODS = {}

def __verify_validate_function(func):
    sig = inspect.signature(func)
    if len(sig.parameters) != 2:
        raise ValueError(
            "Function has {} arguments, expected 2"\
            .format(len(sig.parameters)))
    if "password" not in sig.parameters:
        raise ValueError("Function has no 'password' argument")
    if "hashed" not in sig.parameters:
        raise ValueError("Function has no 'hashed' argument")
    return

def __verify_gen_hash_function(func):
    sig = inspect.signature(func)
    if len(sig.parameters) != 1:
        raise ValueError(
            "Function has {} arguments, expected 1"\
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
            "Function name '{}' already exists"\
            .format(name))

    __VALIDATE_METHODS[name] = validate_func
    __GEN_HASH_METHODS[name] = gen_hash_func

def validate(name, password, hashed):
    if name in __VALIDATE_METHODS:
        return __VALIDATE_METHODS[name](password, hashed)
    else:
        return False

def gen_hash(name, password):
    if name in __GEN_HASH_METHODS:
        return __GEN_HASH_METHODS[name](password)
    else:
        return None

def gen_password(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

# Register functions.
register_auth_functions(
    'bcrypt',
    auth_bcrypt.validate,
    auth_bcrypt.gen_hash)
