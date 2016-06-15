"""HostGroupMember Model."""

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

from .Host import Host
from .Tag import Tag


# pylint: disable=too-few-public-methods
class HostTag(BASE):

    """HostTag Class.

    Base object for referencing tags and hosts.
    """

    __tablename__ = 'host_tag'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    host_id = Column(
        Integer,
        ForeignKey('host.id'),
        nullable=False)
    host = relationship(Host, backref='tags')
    tag_id = Column(
        Integer,
        ForeignKey('tag.id'),
        nullable=False)
    tag = relationship(Tag)

Index('i_host_tag_index', HostTag.id)
Index('u_host_tag_index', HostTag.host_id, HostTag.tag_id, unique=True)
