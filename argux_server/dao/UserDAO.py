"""Data Access Object class for handling Users."""

from argux_server.models import (
    User,
    HashMethod
)

import argux_server.auth

from .BaseDAO import BaseDAO


class UserDAO(BaseDAO):

    """UserDAO Class."""

    def create_user(self, namespace, name, password, hash_method=None):
        if hash_method:
            method = self.db_session.query(HashMethod)\
                .filter(HashMethod.name == hash_method)\
                .first()
        else:
            method = self.db_session.query(HashMethod)\
                .filter(HashMethod.allowed == True)\
                .first()

        if not method:
            raise ValueError("Invalid hash_algorithm")           

        hashed = argux_server.auth.gen_hash(method.name, password)

        user = User(
            name=name,
            passwd_hash=hashed,
            hashmethod=method)

        self.db_session.add(user)

    def get_user(self, name):
        user = self.db_session.query(User)\
            .filter(User.name == name)\
            .first()
        return user

    def validate_user(self, name, password):
        user = self.db_session.query(User)\
            .filter(User.name == name)\
            .first()

        if user:
            return argux_server.auth.validate(
                    user.hashmethod.name,
                    password,
                    user.passwd_hash) 
        return False

    def get_users(self):
        users = self.db_session.query(User)\
            .all()

        return users
