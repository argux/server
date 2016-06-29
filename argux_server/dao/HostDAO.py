"""Data Access Object class for handling Hosts."""

import transaction

from argux_server.models import (
    Host,
    HostAddress,
    HostGroup,
    Item,
    TriggerSeverity
)

from argux_server.dao.util import (
    TRIGGER_CLASS,
    ALERT_CLASS
)

from .BaseDAO import BaseDAO



class HostDAO(BaseDAO):

    """
    HostDAO Class.
    """

    def get_host_by_name(self, name):
        """Return host-object based on name."""
        host = self.db_session.query(Host)\
            .filter(Host.name == name)\
            .first()
        return host

    def create_host(self, name, description=""):
        """Create host."""
        host = Host(name=name, description=description)

        self.db_session.add(host)
        return host

    def get_all_hosts(self):
        """Return all hosts."""
        hosts = self.db_session.query(Host).all()

        return hosts

    def get_host_severity(self, host):
        """Return highest severity of active triggers for this host."""
        float_trigger_klass = TRIGGER_CLASS.get('float')
        float_alert_klass = ALERT_CLASS.get('float')

        severity = self.db_session.query(TriggerSeverity)\
            .filter(TriggerSeverity.id.in_(
                self.db_session.query(float_trigger_klass.severity_id)
                .filter(float_trigger_klass.item_id.in_(
                    self.db_session.query(Item.id)
                    .filter(Item.host_id == host.id)
                ))
                .filter(float_trigger_klass.id.in_(
                    self.db_session.query(float_alert_klass.trigger_id)
                    .filter(float_alert_klass.end_time.is_(None))
                ))
            ))\
            .order_by(TriggerSeverity.level.desc())\
            .first()

        return severity

    def delete_host(self, name):
        """Delete host."""

        host = self.get_host_by_name(name=name)

        self.db_session.delete(host)

        return

    def add_address(self, host, address, description=''):
        """Add address."""
        d_address = HostAddress(
            host=host,
            name=address,
            description=description)
        self.db_session.add(d_address)
        transaction.commit()
        return

    def get_address(self, host, address):
        d_address = self.db_session.query(HostAddress)\
            .filter(HostAddress.host == host)\
            .filter(HostAddress.name == address)\
            .first()
        return d_address

    def get_addresses(self, host):
        """Return associated addresses."""
        d_addresses = self.db_session.query(HostAddress)\
            .filter(HostAddress.host == host)\
            .all()
        return d_addresses

    def create_hostgroup(self, name, description=None, hosts=[]):
        """Create hostgroup."""
        group = HostGroup(name=name, description=description)

        self.db_session.add(group)

        return group

    def get_hostgroup_by_name(self, name):
        """Return hostgroup-object based on name."""
        group = self.db_session.query(HostGroup)\
            .filter(HostGroup.name == name)\
            .first()
        return group

    def get_all_hostgroups(self):
        """Return all hostgroups."""
        groups= self.db_session.query(HostGroup).all()

        return groups

    def add_host_to_group(self, name, host):
        """Add host to hostgroup."""
        group = self.get_hostgroup_by_name(name)
        group.hosts.append(host)
        transaction.commit()
