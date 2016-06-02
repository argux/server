"""UserGroupMember Model."""

from sqlalchemy import (
    Column,
    Index,
    Boolean,
    Integer,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE

from .User import User
from .UserGroup import UserGroup


# pylint: disable=too-few-public-methods
class UserGroupMember(BASE):

    """UserGroupMember Class.

    Base object for referencing members of a UserGroup.
    """

    __tablename__ = 'user_group_member'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    user_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False)
    user = relationship(User, backref='groups')
    user_group_id = Column(
        Integer,
        ForeignKey('user_group.id'),
        nullable=False)
    user_group = relationship(UserGroup, backref='members')

Index('i_user_group_member_index', UserGroupMember.user_id)
Index('i_user_group_group_index', UserGroupMember.user_group_id)
Index('u_user_group_index', UserGroupMember.id)
