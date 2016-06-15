"""Data Access Object class for handling Users."""

from argux_server.models import (
    User,
    HashMethod
)

import argux_server.auth

from .BaseDAO import BaseDAO


class UserDAO(BaseDAO):

    """UserDAO Class."""

    def create_user(self, namespace, name, password, hash_method=None, protected=False):
        user = User(name=name,protected=protected)

        if password is not None:
            try:
                self.set_user_password(user, password, hash_method)
            except ValueError as err:
                raise err

        self.db_session.add(user)

    def set_user_password(self, user, password, hash_method=None):
        if hash_method:
            method = self.db_session.query(HashMethod)\
                .filter(HashMethod.name == hash_method)\
                .filter(HashMethod.allowed == True)\
                .first()
        else:
            method = self.db_session.query(HashMethod)\
                .filter(HashMethod.allowed == True)\
                .first()

        if not method:
            raise ValueError("Invalid hash_algorithm")           

        hashed = argux_server.auth.gen_hash(method.name, password)

        user.passwd_hash=hashed
        user.hashmethod=method

        self.db_session.flush()

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
            # If no hashmethod is set, can't validate user.
            if user.hashmethod is None:
                return False

            return argux_server.auth.validate(
                    user.hashmethod.name,
                    password,
                    user.passwd_hash) 
        return False

    def get_users(self):
        users = self.db_session.query(User)\
            .all()

        return users

    def delete_user(self, username):
        """
        Delete monitor object for host/address of a specific type.
        """
        user = self.get_user(username)
        if user is not None:
            self.db_session.delete(user)

        return
