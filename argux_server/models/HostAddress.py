"""HostAddress Model."""

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


# pylint: disable=too-few-public-methods
class HostAddress(BASE):

    """HostAddress Class.

    Base object for referencing Monitors.
    """

    __tablename__ = 'host_address'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    host_id = Column(
        Integer,
        ForeignKey('host.id'),
        nullable=False)
    host = relationship(Host, backref='addresses')

Index('u_host_address_index', HostAddress.name, unique=True, mysql_length=255)
