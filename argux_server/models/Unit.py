"""Unit Module, containing Unit model."""

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
class Unit(BASE):

    """
    Unit class.

    Model for storing Units.

    It has indicators to determine which
    """

    __tablename__ = 'unit'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    symbol = Column(Text, nullable=False)
    metric_prefix_id = Column(Integer, ForeignKey('metric_prefix.id'))
    metric_prefix = relationship("MetricPrefix", uselist=False, back_populates="unit")

Index('u_unit_name_index', Unit.name, unique=True)
