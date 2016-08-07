"""Event Module, containing Event model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Boolean,
    DateTime,
    Text,
    Table,
    ForeignKey
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE


eventsubscriber_table = Table('event_subscriber',
    BASE.metadata,
    Column(
        'event_type_id',
        Integer,
        ForeignKey('eventtype.id')),
    Column(
        'user_id',
        Integer,
        ForeignKey('user.id'))
)

# pylint: disable=too-few-public-methods
class EventType(BASE):

    """
    EventType class.

    Model for storing Event-Types.
    """

    __tablename__ = 'eventtype'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    key = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    subscribers = relationship("User",
        secondary=lambda: eventsubscriber_table)

Index('u_eventtype_key_index', EventType.key, unique=True)
Index('i_eventtype_id_index', EventType.id, unique=True)

# pylint: disable=too-few-public-methods
class Event(BASE):

    """
    Event class.

    Model for storing Events.
    """

    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    type_id = Column(
        Integer,
        ForeignKey('eventtype.id'),
        nullable=False)
    timestamp = Column(DateTime, nullable=False)
    published = Column(Boolean, default=False)

Index('u_event_eventtype_id_index', Event.type_id, unique=True)
Index('i_event_id_index', Event.id, unique=True)
