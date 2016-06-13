"""Monitors module."""

from .ICMPMonitor import ICMPMonitor
from .DNSMonitor import DNSMonitor
from .SNMPMonitor import SNMPMonitor
from .TriggerMonitor import TriggerMonitor

MONITORS = {}

def start_monitors(settings):
    MONITORS['ICMP'] = ICMPMonitor(settings)
    MONITORS['DNS'] = DNSMonitor(settings)
    MONITORS['SNMP'] = SNMPMonitor(settings)
    MONITORS['Trigger'] = TriggerMonitor(settings)

    for monitor in MONITORS:
        MONITORS[monitor].start()
