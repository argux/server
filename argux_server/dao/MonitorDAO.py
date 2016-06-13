"""Data Access Object class for handling Servers."""

from argux_server.models.Monitor import Monitor
from argux_server.models.MonitorType import MonitorType
from argux_server.models.MonitorOption import MonitorOption
from argux_server.models.DNSMonitorDomain import DNSMonitorDomain
from argux_server.models.Host import Host
from argux_server.models.HostAddress import HostAddress

import transaction

from .BaseDAO import BaseDAO


class MonitorDAO(BaseDAO):

    """MonitorDAO class.

    Object for accessing Monitor objects.
    """

    def create_monitor(self, monitor_type, host_address, options, active=True):
        d_type = self.db_session.query(MonitorType)\
            .filter(MonitorType.name == monitor_type.upper())\
            .first()
        if d_type is None:
            raise KeyError

        monitor = Monitor(
            host_address=host_address,
            monitor_type=d_type,
            active=active)

        self.db_session.add(monitor)

        for key, value in options.items():
            option = MonitorOption(key=key, value=value, monitor=monitor)
            self.db_session.add(option)

        try:
            transaction.commit()
        except:
            transaction.abort()
            monitor = None

        return monitor

    def add_monitor_type(self, name):
        """Add a new monitor-type if it does not already exist."""
        monitor_type = self.db_session.query(MonitorType)\
            .filter(MonitorType.name == name)\
            .first()
        if monitor_type is None:
            monitor_type = MonitorType(
                name=name.upper())
            self.db_session.add(monitor_type)

    def get_all_monitors_for_type(self, monitor_type):
        """Query all monitors for a type."""
        monitors = self.db_session.query(Monitor)\
            .filter(Monitor.monitor_type_id == (
                self.db_session.query(MonitorType.id)
                    .filter(MonitorType.name == monitor_type)
            ))\
            .all()

        return monitors

    def get_monitor(self, hostname, address, monitor_type):
        """
        Get monitor object for host/address of a specific type.
        """
        monitor = self.db_session.query(Monitor)\
            .filter(Monitor.monitor_type_id == (
                self.db_session.query(MonitorType.id)
                    .filter(MonitorType.name == monitor_type)
            ))\
            .filter(Monitor.host_address_id == (
                self.db_session.query(HostAddress.id)
                    .filter(HostAddress.name == address)
                    .filter(HostAddress.host_id == (
                        self.db_session.query(Host.id)
                            .filter(Host.name == hostname)
                    ))
            ))\
            .first()

        return monitor

    def delete_monitor(self, hostname, address, monitor_type):
        """
        Delete monitor object for host/address of a specific type.
        """
        monitor = self.get_monitor(hostname, address, monitor_type)
        if monitor is not None:
            self.db_session.delete(monitor)

        return

    def set_domain(self, hostname, address, monitor_type, domain):
        if monitor_type != 'DNS':
            raise ValueError("cannot add domain to monitor of type" + monitor_type)

        monitor = self.get_monitor(hostname, address, monitor_type)

        if monitor is not None:
            domain = DNSMonitorDomain(
                monitor_id=monitor.id,
                domain=domain,
                record_a=True,
                record_aaaa=False,
                record_mx=True)

            self.db_session.add(domain)

    def remove_domain(self, hostname, address, monitor_type, domain):

        monitor = self.get_monitor(hostname, address, monitor_type)

        if monitor is not None:
            self.db_session.query(DNSMonitorDomain)\
                .filter(DNSMonitorDomain.monitor_id == monitor.id)\
                .filter(DNSMonitorDomain.domain == domain)\
                .delete()

    def get_domains(self, hostname, address, monitor_type):

        domains = []
        monitor = self.get_monitor(hostname, address, monitor_type)

        if monitor is not None:
            domains = self.db_session.query(DNSMonitorDomain)\
                .filter(DNSMonitorDomain.monitor_id == monitor.id)\
                .all()

        return domains
