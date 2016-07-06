"""User Module, containing User model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Table,
    DateTime,
    ForeignKey,
    Boolean,
    Binary
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE


# pylint: disable=too-few-public-methods
class HashMethod(BASE):

    """Hashmethod object.

    The hashmethod can be 'allowed' or 'disallowed'. If it is disallowed,
    the user must be forced to change his password after login. This way
    it is possible to force an update of the encryption algorithm used
    when this is appropriate.
    """

    __tablename__ = 'hashmethod'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    allowed = Column(Boolean, default=True, nullable=False)

Index('u_hashmethod_name', HashMethod.name, unique=True)

user_bookmark_table = Table('user_bookmark',
    BASE.metadata,
    Column(
        'navitem_id',
        Integer,
        ForeignKey('nav_item.id')),
    Column(
        'user_id',
        Integer,
        ForeignKey('user.id'))
)

user_history_table = Table('user_history',
    BASE.metadata,
    Column(
        'navitem_id',
        Integer,
        ForeignKey('nav_item.id')),
    Column(
        'user_id',
        Integer,
        ForeignKey('user.id')),
    Column(
        'timestamp',
        DateTime,
        nullable=False)
)


# pylint: disable=too-few-public-methods
class User(BASE):

    """User class.

    Store user (and it's credentials) in the database.

    local: If a user is only allowed to connect from localhost
    locked: a locked account cannot login
    protected: a protected account cannot be deleted
    """

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    passwd_hash = Column(Binary, default=None, nullable=True)
    hashmethod_id = Column(Integer, ForeignKey('hashmethod.id'), nullable=True, default=None)
    hashmethod = relationship(HashMethod, backref='users')
    local = Column(Boolean, default=False, nullable=False)
    locked = Column(Boolean, default=False, nullable=False)
    protected = Column(Boolean, default=False, nullable=False)
    bookmarks = relationship("NavItem",
        secondary=lambda: user_bookmark_table)
    history = relationship("NavItem",
        secondary=lambda: user_history_table)

Index('u_user_name', User.name, unique=True)
Index('i_user_hashmethod_id', User.hashmethod_id)
