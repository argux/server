"""Data Access Object class for handling Items."""

from sqlalchemy.orm import joinedload

from argux_server.models import (
    Host,
    Item,
    ItemType,
    ItemCategory,
    Unit
)

from argux_server.dao.util import (
    VALUE_CLASS,
    TRIGGER_CLASS,
    ALERT_CLASS,
)

from .BaseDAO import BaseDAO


class ItemDAO(BaseDAO):

    """
    Item DAO.
    """

    def get_items_from_host(self, host):
        """Get all items registered on a host."""
        item = self.db_session.query(Item)\
            .filter(Item.host_id == host.id)
        return item

    def get_item_count_from_host(self, host):
        """Get number of items registered on a host."""
        n_items = self.db_session.query(Item)\
            .filter(Item.host_id == host.id)\
            .count()
        return n_items

    def get_item_by_host_key(self, host, key):
        """Get item registered on a host."""
        item = self.db_session.query(Item)\
            .filter(Item.host_id == host.id)\
            .filter(Item.key == key).first()
        return item

    def create_item(self, properties):
        """Create new Item."""
        category = self.db_session.query(ItemCategory)\
            .filter(ItemCategory.name == properties['category'])\
            .first()
        if category is None and 'category' in properties:
            if properties['category'] is not None:
                category = ItemCategory(name=properties['category'])

                self.db_session.add(category)
                self.db_session.flush()

        category_id = None
        if category is not None:
            category_id = category.id

        unit = None
        if 'unit' in properties:
            if properties['unit'] is not None:
                unit = self.db_session.query(Unit)\
                    .filter(Unit.name == properties['unit'])\
                    .first()

        item = self.db_session.query(Item)\
            .filter(Item.host_id == properties['host'].id)\
            .filter(Item.key == properties['key'])\
            .filter(Item.category_id == category_id)\
            .first()

        if item is not None:
            raise ValueError("Item already exists")

        item = Item(
            host_id=properties['host'].id,
            name=properties['name'],
            key=properties['key'],
            category_id=category_id,
            itemtype=properties['itemtype'],
            unit=unit)

        self.db_session.add(item)
        self.db_session.flush()

        return item

    def push_value(self, item, timestamp, value):
        """Push new value to an item."""
        value_klass = VALUE_CLASS.get(item.itemtype.name, None)

        val = value_klass(item_id=item.id, timestamp=timestamp, value=value)
        self.db_session.add(val)
        return val

    def get_last_value(self, item):
        """Return last value published on an item."""
        klass = VALUE_CLASS.get(item.itemtype.name, lambda: "nothing")

        val = self.db_session.query(klass)\
            .filter(klass.item_id == item.id)\
            .order_by(klass.timestamp.desc())\
            .first()

        return val

    # pylint: disable=unused-argument
    def get_values(self, item, start_time=None, end_time=None, count=-1):
        """Query values."""
        klass = VALUE_CLASS.get(item.itemtype.name, "nothing")

        query = self.db_session.query(klass)\
            .filter(klass.item_id == item.id)

        if start_time:
            query = query.filter(
                klass.timestamp > start_time)

        if end_time:
            query = query.filter(
                klass.timestamp < end_time)

        values = query.order_by(klass.timestamp.asc()).all()

        return values

    def get_alerts(self, item, active=True, inactive=False):
        """Query Alerts."""
        alert_klass = ALERT_CLASS.get(item.itemtype.name)
        alerts = []
        triggers = self.get_triggers(item)

        for trigger in triggers:
            active_alert = self.db_session.query(alert_klass)\
                .filter(alert_klass.trigger_id == trigger.id)\
                .filter(alert_klass.end_time.is_(None))

            alerts.extend(active_alert)

        return alerts

    def get_active_alert_count(self, item):
        """Get number of active alerts."""
        alert_klass = ALERT_CLASS.get(item.itemtype.name)
        triggers = self.get_triggers(item)

        n_alerts = 0

        for trigger in triggers:
            n_alerts += self.db_session.query(alert_klass)\
                .filter(alert_klass.trigger_id == trigger.id)\
                .filter(alert_klass.end_time.is_(None))\
                .count()

        return n_alerts

    def get_triggers(self, item):
        """Return all triggers on an item."""
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)
        triggers = self.db_session.query(trigger_klass)\
            .options(joinedload(trigger_klass.item))\
            .filter(trigger_klass.item_id == item.id)

        return triggers

    def get_itemcategory_by_name(self, name):
        """Return ItemCategory object or None."""
        cat = self.db_session.query(ItemCategory)\
            .filter(ItemCategory.name == name).first()
        return cat

    def create_itemcategory(self, name):
        """Create ItemCategory object."""
        cat = ItemCategory(name=name)
        self.db_session.add(cat)
        return cat

    def get_itemtype_by_name(self, name):
        """Return ItemType object or None."""
        item_type = self.db_session.query(ItemType)\
            .filter(ItemType.name == name).first()
        return item_type

    def get_item_exists(self, itemname, hostname):
        item = self.db_session.query(Item)\
            .filter(Item.host_id == (
                self.db_session.query(Host.id)\
                    .filter(Host.name == hostname)
                )
            )\
            .first()

        if item is None:
            return False

        return True
