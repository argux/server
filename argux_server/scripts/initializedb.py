"""Initialisation script for Argux DB."""
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models import (
    DB_SESSION,
    BASE,
    ItemType,
    TriggerSeverity,
    HashMethod,
    MonitorType,
    Unit,
    MetricPrefix,
    HostGroup
)

from ..dao.UserDAO import UserDAO


def usage(argv):
    """Print usage string."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def initialise_itemtypes():
    model = ItemType(name='int', description='Integer field')
    DB_SESSION.add(model)
    model = ItemType(name='float', description='Floating point')
    DB_SESSION.add(model)
    model = ItemType(name='text', description='Text')
    DB_SESSION.add(model)
    model = ItemType(name='boolean', description='Boolean')
    DB_SESSION.add(model)
    model = ItemType(name='decimal', description='Decimal')
    DB_SESSION.add(model)

def initialise_triggerseverity():
    model = TriggerSeverity(level=1, key="info", name="Information")
    DB_SESSION.add(model)
    model = TriggerSeverity(level=2, key="warn", name="Warning")
    DB_SESSION.add(model)
    model = TriggerSeverity(level=3, key="crit", name="Critical")
    DB_SESSION.add(model)

def initialise_hashmethods():
    model = HashMethod(name='bcrypt', allowed=True)
    DB_SESSION.add(model)

def initialise_monitortypes():
    model = MonitorType(name='ICMP')
    DB_SESSION.add(model)
    model = MonitorType(name='DNS')
    DB_SESSION.add(model)
    model = MonitorType(name='SNMP')
    DB_SESSION.add(model)

def initialise_units():
    prefix = MetricPrefix(milli=True,micro=True,nano=True)
    DB_SESSION.add(prefix)
    model = Unit(name='Seconds', symbol='s', metric_prefix=prefix)
    DB_SESSION.add(model)
    prefix = MetricPrefix(kilo=True,mega=True,giga=True,tera=True,peta=True,exa=True)
    DB_SESSION.add(prefix)
    model = Unit(name='Bytes', symbol='B', metric_prefix=prefix)
    DB_SESSION.add(model)
    prefix = MetricPrefix(kilo=True,mega=True,giga=True,tera=True,peta=True,exa=True)
    DB_SESSION.add(prefix)
    model = Unit(name='Bits', symbol='b', metric_prefix=prefix)
    DB_SESSION.add(model)

def initialise_hostgroups():
    hostgroup_all = HostGroup(name='All', description='All hosts')
    DB_SESSION.add(hostgroup_all)

def initdb(settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DB_SESSION.configure(bind=engine)
    BASE.metadata.create_all(engine)
    with transaction.manager:
        initialise_itemtypes()
        initialise_triggerseverity()
        initialise_hashmethods()
        initialise_monitortypes()
        initialise_units()
        initialise_hostgroups()

        user_dao = UserDAO(DB_SESSION)
        user_dao.create_user('admin', 'admin', hash_method='bcrypt')
        user_dao.create_user('__monitor__', None, hash_method='bcrypt',protected=True)


def main():
    """Main function for Initialisation script."""
    if len(sys.argv) < 2:
        usage(sys.argv)
    config_uri = sys.argv[1]
    options = parse_vars(sys.argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    initdb(settings)
