"""UserGroup Model."""

from sqlalchemy import (
    Column,
    Index,
    Boolean,
    Integer,
    Text,
    ForeignKey,
)

from sqlalchemy.schema import (
    Table
)


from sqlalchemy.orm import (
    relationship
)

from . import BASE

from .User import User

usergroupmember_table = Table('usergroup_member',
    BASE.metadata,
    Column(
        'usergroup_id',
        Integer,
        ForeignKey('user_group.id')),
    Column(
        'user_id',
        Integer,
        ForeignKey('user.id'))
)


# pylint: disable=too-few-public-methods
class UserGroup(BASE):

    """UserGroup Class.

    Base object for referencing HostGroup.
    """

    __tablename__ = 'user_group'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    users = relationship("User",
        secondary=lambda: usergroupmember_table,
        backref='usergroups')

Index('u_user_group_index', UserGroup.name, unique=True, mysql_length=255)
