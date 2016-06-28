"""HostGroup Model."""

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

from .Host import Host

hostgroupmember_table = Table('hostgroup_member',
    BASE.metadata,
    Column('host_group.id', Integer, ForeignKey('host_group.id')),
    Column('host.id', Integer, ForeignKey('host.id'))
)


# pylint: disable=too-few-public-methods
class HostGroup(BASE):

    """HostGroup Class.

    Base object for referencing HostGroup.
    """

    __tablename__ = 'host_group'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    hosts = relationship("Host",
        secondary=lambda: hostgroupmember_table,
        backref='hostgroups')

Index('u_host_group_index', HostGroup.name, unique=True, mysql_length=255)
