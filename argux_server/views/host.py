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
        self.request.matchdict['action'] = 'metrics'

        return self.host()

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
        bookmarked = False

        nav_item = self.dao.nav_dao.add_nav_item_for_request(
            'host',
            self.request,
            '[Host] ' + host + ' - ' + action)

        user = self.dao.user_dao.get_user(
            self.request.authenticated_userid)

        if nav_item in user.bookmarks:
            bookmarked = True

        host_desc = ''
        h = self.dao.host_dao.get_host_by_name(host)

        if not h:
            return Response(status="404 Not Found")

        return {
            "argux_host": host,
            "argux_host_desc": h.description,
            "addresses": h.addresses,
            "active_alerts": n_alerts,
            "bookmarked": bookmarked,
            "bookmark": nav_item.nav_hash,
            "action": action}

    @view_config(
        route_name='hostgroup_details_default',
        renderer='templates/hostgroup.pt',
        permission='view'
    )
    def hostgroup_details_default(self):
        self.request.matchdict['action'] = 'hosts'

        return self.hostgroup_details()

    @view_config(
        route_name='hostgroup_details',
        renderer='templates/hostgroup.pt',
        permission='view'
    )
    def hostgroup_details(self):
        group = self.request.matchdict['group']
        action = self.request.matchdict['action']
        bookmarked = False

        nav_item = self.dao.nav_dao.add_nav_item_for_request(
            'hostgroup_details',
            self.request,
            '[Hostgroup] ' + group + ' - ' + action)

        user = self.dao.user_dao.get_user(
            self.request.authenticated_userid)

        if nav_item in user.bookmarks:
            bookmarked = True

        if action == 'alerts':
            default_view_opts = {
                "type": "list",
                "sort": "asc",
                "buttons": {
                    "list": {
                        "state": "active",
                    },
                    "grid": {
                        "state": "disabled",
                    }
                }
            }
        if action == 'hosts':
            default_view_opts = {
                "type": "grid",
                "sort": "asc",
                "buttons": {
                    "list": {
                        "state": "",
                    },
                    "grid": {
                        "state": "active",
                    }
                }
            }

        return {
            "bookmarked": bookmarked,
            "bookmark": nav_item.nav_hash,
            "host_group": group,
            "action": action,
            "view_opts": default_view_opts
        }
