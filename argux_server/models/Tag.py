"""Tag Module, containing Tag model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE

# pylint: disable=too-few-public-methods
class Tag(BASE):

    """
    Tag class.

    Model for storing Tags.

    It has indicators to determine which 
    """

    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)

Index('u_tag_name_index', Tag.name, unique=True)
