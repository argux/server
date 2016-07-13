"""Concrete classes for Triggers and Values of Floating-point items."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    ForeignKey
)

from sqlalchemy.orm import (
    relationship
)

from .. import BASE

from .AbstractValue import (
    AbstractValue,
    AbstractSimpleTrigger,
    AbstractSimpleAlert
)


# pylint: disable=too-few-public-methods
class FloatValue(AbstractValue, BASE):

    """FloatValue class.

    Subclass of AbstractValue and BASE.
    """

    __tablename__ = 'history_float'
    value = Column(Float, nullable=True)

Index('floatvalue_ts_index', FloatValue.timestamp, mysql_length=255)


# pylint: disable=too-few-public-methods
class FloatSimpleTrigger(AbstractSimpleTrigger, BASE):

    """FloatSimpleTrigger class.

    Subclass of AbstractSimpleTrigger and BASE.
    """

    __tablename__ = 'simple_trigger_float'

    @staticmethod
    def validate_rule(rule):
        """Validate FloatSimpleTriger rules."""
        ret = AbstractSimpleTrigger.validate_rule(rule)
        if ret is None:
            return None

        operators = ['!=', '==', '>', '<', '>=', '<=']
        if ret[2] not in operators:
            return None

        return ret

    # pylint: disable=unused-argument
    def __handle_last(self, session, selector, operator, value):

        item = self.item
        val = session.query(FloatValue)\
            .filter(FloatValue.item_id == item.id)\
            .order_by(FloatValue.timestamp.desc()).first()

        # Should be custom error
        if val is None:
            raise ValueError("No Values")

        if ((operator == '>' and val.value > float(value)) or
                (operator == '<' and val.value < float(value)) or
                (operator == '>=' and val.value >= float(value)) or
                (operator == '<=' and val.value <= float(value)) or
                (operator == '==' and val.value == float(value)) or
                (operator == '!=' and val.value != float(value))):
            return (True, val.timestamp)
        else:
            return (False, val.timestamp)

    trigger_handlers = {
        "last": __handle_last
    }


# pylint: disable=too-few-public-methods
class FloatSimpleAlert(AbstractSimpleAlert, BASE):

    """FloatSimpleAlert class.

    Subclass of AbstractSimpleAlert and BASE.
    """

    __tablename__ = 'simple_alert_float'
    trigger_id = Column(
        Integer,
        ForeignKey('simple_trigger_float.id'),
        nullable=False)
    trigger = relationship(FloatSimpleTrigger)

Index(
    'floatsimple_alert_start_ts',
    FloatSimpleAlert.start_time,
    mysql_length=255)
Index(
    'floatsimple_alert_end_ts',
    FloatSimpleAlert.end_time,
    mysql_length=255)
