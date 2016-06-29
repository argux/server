"""MetricPrefix Module, containing MetricPrefix preferences of a Unit."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Boolean
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE

# pylint: disable=too-few-public-methods
class MetricPrefix(BASE):

    """
    MetricPrefix class.

    Model for storing MetricPrefixes.

    It has indicators to determine which prefixes are to be used for a unit.
    """

    __tablename__ = 'metric_prefix'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    unit = relationship("Unit", uselist=False, back_populates="metric_prefix")
    exa = Column(Boolean, default=False, nullable=False)    # 1e18
    peta = Column(Boolean, default=False, nullable=False)   # 1e15
    tera = Column(Boolean, default=False, nullable=False)   # 1e12
    giga = Column(Boolean, default=False, nullable=False)   # 1e9
    mega = Column(Boolean, default=False, nullable=False)   # 1e6
    kilo = Column(Boolean, default=False, nullable=False)   # 1e3
    hecto = Column(Boolean, default=False, nullable=False)  # 1e2
    deca = Column(Boolean, default=False, nullable=False)   # 1e1
    ####
    deci = Column(Boolean, default=False, nullable=False)   # 0e-1
    centi = Column(Boolean, default=False, nullable=False)  # 0e-2
    milli = Column(Boolean, default=False, nullable=False)  # 0e-3
    micro = Column(Boolean, default=False, nullable=False)  # 0e-6
    nano = Column(Boolean, default=False, nullable=False)   # 0e-9
    pico = Column(Boolean, default=False, nullable=False)   # 0e-12
    femto = Column(Boolean, default=False, nullable=False)  # 0e-15
    atto = Column(Boolean, default=False, nullable=False)   # 0e-18
