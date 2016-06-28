from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPNotFound,
    HTTPFound
)

from argux_server.util import (
    TIMESPAN_EXPR,
)

import json

from . import BaseView


@view_defaults(renderer='templates/host_overview.pt')
class MainViews(BaseView):

    # pylint: disable=no-self-use
    @view_config(
        route_name='home',
        permission='view'
    )
    def home(self):
        return self.host_overview_default()

    # pylint: disable=no-self-use
    @view_config(
        route_name='host_overview_default',
        renderer='templates/host_overview.pt',
        permission='view',
    )
    def host_overview_default(self):
        return {
            "action": 'overview'}

    # pylint: disable=no-self-use
    @view_config(
        route_name='host_overview',
        renderer='templates/host_overview.pt',
        permission='view'
    )
    def host_overview(self):
        action = self.request.matchdict['action']
        return {
            "action": action}

    @view_config(
        route_name='host_default',
        renderer='templates/host.pt',
        permission='view'
    )
    def host_default(self):
        host_name = self.request.matchdict['host']
        host_desc = ''
        n_alerts = 0
        host = self.dao.host_dao.get_host_by_name(host_name)

        if host:
            host_desc = host.description

        has_summary = False

        if has_summary is True:
            action = 'summary'
        else:
            action = 'metrics'

        return {
            "argux_host": host_name,
            "argux_host_desc": host_desc,
            "active_alerts": n_alerts,
            "action": action}

    @view_config(
        route_name='host',
        renderer='templates/host.pt',
        permission='view'
    )
    def host(self):
        host = self.request.matchdict['host']
        action = self.request.matchdict['action']
        n_alerts = 0
        addresses = []

        host_desc = ''
        h = self.dao.host_dao.get_host_by_name(host)

        if h:
            host_desc = h.description
            addresses = h.addresses

        return {
            "argux_host": host,
            "argux_host_desc": host_desc,
            "addresses": addresses,
            "active_alerts": n_alerts,
            "action": action}

    # pylint: disable=no-self-use
    @view_config(
        route_name='hostgroup_details',
        renderer='templates/hostgroup.pt',
        permission='view'
    )
    def home(self):
        group = self.request.matchdict['group']

        return {
            "hostgroup": group
            }
