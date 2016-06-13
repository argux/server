"""ArguxServer Module."""

from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.config import Configurator

from pyramid.renderers import JSON

from pyramid.session import SignedCookieSessionFactory

from pyramid.security import (
    ALL_PERMISSIONS,
    Everyone,
    Authenticated,
    Allow
)

from sqlalchemy import engine_from_config

from .models import (
    DB_SESSION,
    BASE,
)

import transaction

from argux_server import dao

from argux_server.auth import user, gen_password

from argux_server.trigger import TriggerWorker

from argux_server.monitors import (
    start_monitors
)


# MAP GROUPS TO PERMISSIONS
class RootFactory(object):

    """ RootFactory:

    __acl__: base ACL
    """

    __acl__ = [
        (Allow, 'group:admin', ALL_PERMISSIONS),
        (Allow, 'group:admin', 'admin'),
        (Allow, Authenticated, 'view'),
        (Allow, Everyone, 'koffie')
    ]

    def __init__(self, request):
        """Initialize RootFactory."""
        self.request = request


# pylint: disable=unused-argument
def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    DB_SESSION.configure(bind=engine)
    BASE.metadata.bind = engine
    settings['dao'] = dao.DAO(DB_SESSION)

    if settings['session.secure_cookie'] == 'true':
        secure_cookie=True
    else:
        secure_cookie=False

    factory = SignedCookieSessionFactory(
        'SEECREET',
        cookie_name='argux_server',
        secure=secure_cookie,
        httponly=True,
        reissue_time=0,
        timeout=1800)

    authentication_policy = SessionAuthenticationPolicy(
        callback=user.get_principals
    )
    authorization_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        root_factory=RootFactory
    )
    config.set_session_factory(factory)
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)

    config.include('pyramid_chameleon')
    config.include('pyramid_tm')

    config.add_static_view(
        'static',
        'argux_server:static/',
        cache_max_age=3600)

    config.add_route('home',
                     '/')
    config.add_route('host_overview_default',
                     '/hosts')
    config.add_route('host_overview',
                     '/hosts/{action}')
    config.add_route('host_default',
                     '/host/{host}')
    config.add_route('host',
                     '/host/{host}/{action}')
    config.add_route('item',
                     '/host/{host}/item/{item}')
    config.add_route('item_details',
                     '/host/{host}/item/{item}/{action}')
    config.add_route('monitor_default',
                     '/monitor')
    config.add_route('monitor',
                     '/monitor/{action}')
    config.add_route('monitor_edit',
                     '/monitor/{action}/{host}/{address}/edit')
    config.add_route('login',
                     '/login')
    config.add_route('logout',
                     '/logout')
    config.add_route('profile',
                     '/profile')
    config.add_route('reports_default',
                     '/reports')

    config.add_route('admin',
                     '/admin')
    config.add_route('admin_users',
                     '/admin/users')

    config.add_route('dashboards',
                     '/dashboard')

    # REST 1.0 API
    config.add_route('rest_login_1',
                     '/rest/1.0/login')
    config.add_route('rest_logout_1',
                     '/rest/1.0/logout')
    config.add_route('rest_hosts_1',
                     '/rest/1.0/host')
    config.add_route('rest_host_1',
                     '/rest/1.0/host/{host}')
    config.add_route('rest_host_details_1',
                     '/rest/1.0/host/{host}/details')

    config.add_route('rest_item_1',
                     '/rest/1.0/host/{host}/item/{item}')
    config.add_route('rest_item_details_1',
                     '/rest/1.0/host/{host}/item/{item}/details')
    config.add_route('rest_item_values_1',
                     '/rest/1.0/host/{host}/item/{item}/values')
    config.add_route('rest_triggers_1',
                     '/rest/1.0/host/{host}/item/{item}/trigger')
    config.add_route('rest_trigger_validate_1',
                     '/rest/1.0/host/{host}/item/{item}/trigger/validate')
    config.add_route('rest_trigger_1',
                     '/rest/1.0/host/{host}/item/{item}/trigger/{id}')
    config.add_route('rest_host_addresses_1',
                     '/rest/1.0/host/{host}/addr')
    config.add_route('rest_host_address_1',
                     '/rest/1.0/host/{host}/addr/{address}')

    config.add_route('rest_note_1',
                     '/rest/1.0/note')

    config.add_route('rest_graph_1',
                     '/rest/1.0/graph/{id}')
    config.add_route('rest_graphs_1',
                     '/rest/1.0/graph')

    config.add_route('rest_itemtype_details_1',
                     '/rest/1.0/itemtype/{itemtype}/detail')
    config.add_route('rest_itemtype_detail_1',
                     '/rest/1.0/itemtype/{itemtype}/detail/{id}')

    config.add_route('rest_monitors_1',
                     '/rest/1.0/monitor/{type}')
    config.add_route('rest_monitor_1',
                     '/rest/1.0/monitor/{type}/{host}/{address}')
    config.add_route('rest_dns_monitor_domains_1',
                     '/rest/1.0/monitor/dns/{host}/{address}/domain')
    config.add_route('rest_dns_monitor_domain_1',
                     '/rest/1.0/monitor/dns/{host}/{address}/domain/{domain}')

    config.add_route('rest_admin_user_1',
                     '/rest/1.0/admin/user/{username}')
    config.add_route('rest_admin_users_1',
                     '/rest/1.0/admin/user')

    # Pretty-print JSON, useful for development.
    if settings['rest.pretty_json'] == 'true':
        config.add_renderer('json', JSON(indent=4))

    config.scan('.views')
    config.scan('.rest.views')

    transaction.begin()

    monitor_user = settings['dao'].user_dao.get_user(name='__monitor__')
    monitor_pass = gen_password()
    settings['dao'].user_dao.set_user_password(
        monitor_user,
        monitor_pass)

    settings['monitor_pass'] = monitor_pass

    transaction.commit()

    worker = TriggerWorker()
    worker.start()

    start_monitors(settings=settings)

    return config.make_wsgi_app()
