"""
Data Access Object class for handling Items.
"""

from datetime import datetime

from arguxserver.models import (
    DB_SESSION,
    ItemCategory,
    ItemName,
    ItemType,
    ItemTypeDetail,
    Item,
    TriggerSeverity
)

from arguxserver.dao.util import (
    VALUE_CLASS,
    TRIGGER_CLASS,
    ALERT_CLASS
)

from sqlalchemy.orm import (
    sessionmaker
)

class ItemDAO(object):

    def get_items_from_host(self, host):
        i = DB_SESSION.query(Item).filter(Item.host_id == host.id)
        return i

    def get_item_by_host_key(self, host, key):
        i = DB_SESSION.query(Item).filter(Item.host_id == host.id).filter(Item.key == key).first()
        return i

    def create_item(self, host, key, name, category, itemtype):
        i = Item(host_id=host.id, key=key, name=name, category=category, itemtype=itemtype)
        DB_SESSION.add(i)
        return i

    def create_trigger(self, item, name, rule, description="", severity="info"):
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)

        severity = DB_SESSION.query(TriggerSeverity).filter(TriggerSeverity.key == severity).first()
        if not severity:
            raise Exception()

        if trigger_klass.validate_rule(rule) == False:
            raise Exception()


        trigger = trigger_klass(name = name,
                                rule=rule,
                                description=description,
                                item_id=item.id,
                                severity_id=severity.id)
        DB_SESSION.add(trigger)
        return trigger


    def evaluateTrigger(self, trigger):
        item = trigger.item

        alert_klass = ALERT_CLASS.get(item.itemtype.name)

        Session = sessionmaker()
        session = Session()
        i = trigger.validate_rule(trigger.rule)
        if (i == None):
            return False

        handler = trigger.trigger_handlers.get(i[0], None)

        if handler:
            alert = session.query(alert_klass) \
                 .filter(alert_klass.trigger_id == trigger.id) \
                 .filter(alert_klass.end_time == None).first()

            (is_active, time) = handler(trigger, session, i[1], i[2], i[3])

            if is_active:
                if not alert:
                    alert = alert_klass(trigger_id = trigger.id, start_time = time, end_time=None)
                    session.add(alert)
                    session.commit()
            else:
                if alert:
                    alert.end_time = time
                    session.commit()
            session.close()
        else:
            session.close()
            return False

    def get_triggers(self, item):
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)
        triggers = DB_SESSION.query(trigger_klass) \
                .filter(trigger_klass.item_id == item.id)

        return triggers

    def get_all_triggers(self):
        triggers = []
        for name in TRIGGER_CLASS:
            klass = TRIGGER_CLASS[name]
            triggers.extend(DB_SESSION.query(klass).all())

        return triggers

    def push_value(self, item, timestamp, value):
        value_klass = VALUE_CLASS.get(item.itemtype.name, None)
        i = value_klass(item_id = item.id, timestamp=timestamp, value=value)
        DB_SESSION.add(i)
        return

    def get_last_value(self, item):
        klass = VALUE_CLASS.get(item.itemtype.name, lambda: "nothing")
        c = DB_SESSION.query(klass).filter(klass.item_id == item.id).order_by(klass.timestamp.desc()).first()
        return c

    def get_values(self, item, start_time = None, end_time = None, count = -1):
        klass = VALUE_CLASS.get(item.itemtype.name, "nothing")

        q = DB_SESSION.query(klass) \
                .filter(klass.item_id == item.id)

        if (start_time):
            q = q.filter(
                    klass.timestamp > start_time)
        if (end_time):
            q = q.filter(
                    klass.timestamp < end_time)

        values = q.order_by(klass.timestamp.asc()).all()

        return values

    def get_alerts(self, item, active=True, inactive=False):
        alert_klass = ALERT_CLASS.get(item.itemtype.name)
        alerts = []
        triggers = self.get_triggers(item)
        for trigger in triggers:
            a = DB_SESSION.query(alert_klass) \
                    .filter(alert_klass.trigger_id == trigger.id) \
                    .filter(alert_klass.end_time == None)

            alerts.extend(a)

        return alerts

    def get_itemname_by_name(self, name):
        i = DB_SESSION.query(ItemName).filter(ItemName.name == name).first()
        return i

    def create_itemName(self, name, description):
        i = ItemName(name=name, description=description)
        DB_SESSION.add(i)
        return i

    def get_itemcategory_by_name(self, name):
        cat = DB_SESSION.query(ItemCategory).filter(ItemCategory.name == name).first()
        return cat

    def create_itemCategory(self, name):
        cat = ItemCategory(name=name)
        DB_SESSION.add(cat)
        return cat

    def getItemTypeByName(self, name):
        i = DB_SESSION.query(ItemType).filter(ItemType.name == name).first()
        return i

    def add_itemtype_detail(self, item_type,name,rule):
        d = ItemTypeDetail(itemtype=item_type, name=name, rule=rule)
        DB_SESSION.add(d)
        return None

    def get_itemtype_details(self, item_type):
        return item_type.details
