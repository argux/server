"""Data Access Object class for handling Triggers."""

import logging

from argux_server.models import (
    TriggerSeverity
)

from argux_server.dao.util import (
    TRIGGER_CLASS,
    ALERT_CLASS
)

from .BaseDAO import BaseDAO


class TriggerDAO(BaseDAO):

    """Trigger DAO.

    Data Access Object for handling Triggers.
    """

    logger = logging.getLogger(__name__)

    def create_trigger(self, properties):
        """Create trigger."""

        severity_key = properties.get('severity', 'info')
        rule = properties['rule']

        trigger_klass = TRIGGER_CLASS.get(properties['item'].itemtype.name)

        severity = self.db_session.query(TriggerSeverity)\
            .filter(TriggerSeverity.key == severity_key).first()

        if not severity:
            raise ValueError('Severity "' + severity + '" is invalid')

        if not trigger_klass.validate_rule(rule):
            raise ValueError('Rule "' + rule + '" can\'t be validated')

        trigger = trigger_klass(
            name=properties['name'],
            rule=properties['rule'],
            description=properties.get('description', ""),
            item_id=properties['item'].id,
            severity_id=severity.id)

        self.db_session.add(trigger)
        return trigger

    def delete_trigger_by_id(self, item, trigger_id):
        """Delete Trigger for Item."""
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)

        trigger = self.db_session.query(trigger_klass)\
            .filter(trigger_klass.id == trigger_id)\
            .filter(trigger_klass.item_id == item.id)\
            .first()

        if trigger:
            self.db_session.query(trigger_klass)\
                .filter(trigger_klass.id == trigger_id)\
                .filter(trigger_klass.item_id == item.id)\
                .delete()
        else:
            raise ValueError("trigger_id not valid for item")

        return

    def evaluate_trigger(self, trigger):
        """Evaluate Trigger."""
        item = trigger.item

        alert_klass = ALERT_CLASS.get(item.itemtype.name)

        i = trigger.validate_rule(trigger.rule)
        if i is None:
            return False

        handler = trigger.trigger_handlers.get(i[0], None)

        if handler:
            try:
                alert = self.db_session.query(alert_klass)\
                    .filter(alert_klass.trigger_id == trigger.id)\
                    .filter(alert_klass.end_time.is_(None)).first()

                # Execute trigger-handler
                (is_active, time) = handler(
                    trigger,
                    self.db_session,
                    i[1],
                    i[2],
                    i[3])

                if is_active:
                    if not alert:
                        trigger.active_alert = True
                        alert = alert_klass(trigger_id=trigger.id,
                                            start_time=time,
                                            end_time=None)
                        self.db_session.add(alert)
                else:
                    if alert:
                        trigger.active_alert = False
                        alert.end_time = time
            except ValueError as e:
                self.logger.debug(str(e))
        else:
            print("Handler not found")
            return False

    # pylint: disable=no-self-use
    def validate_trigger_rule(self, item, rule):
        """Return True if Trigger-rule is valid."""
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)

        ret = trigger_klass.validate_rule(rule)
        if ret is None:
            return False

        return True

    def get_all_triggers(self):
        """Return all triggers."""
        triggers = []
        for name in TRIGGER_CLASS:
            klass = TRIGGER_CLASS[name]
            triggers.extend(self.db_session.query(klass).all())

        return triggers

    def get_last_alert_for_trigger(self, trigger):
        """Return last alert for a trigger.

        This function is used for every trigger individually...
        It makes more sense if we could query it for all triggers at once.
        """
        alert_klass = ALERT_CLASS.get(trigger.item.itemtype.name)

        alert = self.db_session.query(alert_klass)\
            .filter(alert_klass.trigger_id == trigger.id)\
            .order_by(alert_klass.start_time.desc())\
            .first()

        return alert
