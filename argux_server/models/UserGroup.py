"""User Module, containing User model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    Boolean,
    Binary
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE


# pylint: disable=too-few-public-methods
class UserGroup(BASE):

    """UserGroup class.

    Store user (and it's credentials) in the database.
    """

    __tablename__ = 'user_group'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)

Index('u_usergroup_name', UserGroup.name, unique=True)
