"""Host Model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from . import BASE


# pylint: disable=too-few-public-methods
class Host(BASE):

    """Host Class.

    Base object for monitored hosts.
    """

    __tablename__ = 'host'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")

Index('u_host_index', Host.name, unique=True, mysql_length=255)
