"""Data Access Object class for handling Hosts."""

import transaction

from argux_server.models import (
    Host,
    HostAddress,
    HostGroup,
    Item,
    TriggerSeverity
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

