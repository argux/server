"""Item Module, containing Item model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
)

from sqlalchemy.orm import (
    relationship
)

from .ItemType import ItemType
from .ItemCategory import ItemCategory
from .Unit import Unit
from .Host import Host

from . import BASE


# pylint: disable=too-few-public-methods
class Item(BASE):

    """
    Item class.

    Model for storing measurement Items.
    """

    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    key = Column(Text, nullable=False)
    host_id = Column(
        Integer,
        ForeignKey('host.id'),
        nullable=False)
    host = relationship(Host, backref='items')

    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default='')
    category_id = Column(
        Integer,
        ForeignKey('item_category.id'),
        nullable=True,
        default=None)
    category = relationship(ItemCategory, backref='item_category')

    itemtype_id = Column(
        Integer,
        ForeignKey('itemtype.id'),
        nullable=False)
    itemtype = relationship(ItemType, backref='items')

    unit_id = Column(
        Integer,
        ForeignKey('unit.id'))
    unit = relationship(Unit)

    default_graph_id = Column(
        Integer,
        ForeignKey('history_graph.id'),
        nullable=True,
        default=None)

Index('u_item_key_host_id_index', Item.key, Item.host_id, unique=True)
Index('i_item_host_id_index', Item.host_id)
Index('i_item_category_id_index', Item.category_id)
