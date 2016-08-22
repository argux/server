"""Monitors module."""

from .ICMPMonitor import ICMPMonitor
from .DNSMonitor import DNSMonitor
from .SNMPMonitor import SNMPMonitor
from .TriggerMonitor import TriggerMonitor
from .EventMonitor import EventMonitor

MONITORS = {}

def start_monitors(settings):
    MONITORS['ICMP'] = ICMPMonitor(settings)
    MONITORS['DNS'] = DNSMonitor(settings)
    MONITORS['SNMP'] = SNMPMonitor(settings)
    MONITORS['Trigger'] = TriggerMonitor(settings)
    MONITORS['Event'] = EventMonitor(settings)

    for monitor in MONITORS:
        MONITORS[monitor].start()
