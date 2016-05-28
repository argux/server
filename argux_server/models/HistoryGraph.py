"""HistoryGraph Module, containing HistoryGraph model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Text,
    ForeignKey,
    String,
    Boolean
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE

from .Item  import Item

# pylint: disable=too-few-public-methods
class HistoryGraph(BASE):

    """
    HistoryGraph class.

    Model for storing HistoryGraph details.
    """

    __tablename__ = 'history_graph'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    suggested_min = Column(Float, nullable=True, default=None)
    suggested_max = Column(Float, nullable=True, default=None)

# pylint: disable=too-few-public-methods
class HistoryGraphItem(BASE):

    """
    HistoryGraphItem class.

    Model for storing HistoryGraph - Item relationship details.
    """

    __tablename__ = 'history_graph_item'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    history_graph_id = Column(Integer, ForeignKey('history_graph.id'), nullable=False)
    history_graph = relationship(HistoryGraph, backref='items')
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship(Item, backref='history_graphs')
    color = Column(String(6), nullable=True, default=None);
