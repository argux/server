from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPNotFound,
    HTTPFound
)

from pyramid.security import (
    remember,
    forget,
)

from argux_server.util import (
    TIMESPAN_EXPR,
)

import json

from . import BaseView

class ItemViews(BaseView):

    @view_config(
        route_name='item',
        renderer='templates/item.pt',
        permission='view'
    )
    def item(self):
        self.request.matchdict['action'] = 'details'

        return self.item_details()

    @view_config(
        route_name='item_details',
        renderer='templates/item.pt',
        permission='view'
    )
    def item_details(self):
        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']
        action = self.request.matchdict['action']

        timespan = self.request.params.get('timespan', '30m')

        # Validate timespan input and default to 30 minutes
        # if it fails.
        i = TIMESPAN_EXPR.match(timespan)
        if i is None:
            timespan = '30m'

        has_details = False

        host = self.dao.host_dao.get_host_by_name(host_name)
        item = self.dao.item_dao.get_item_by_host_key(host, item_key)

        if item.itemtype.name == 'float':
            has_details = True

        alerts = self.dao.item_dao.get_alerts(item)

        return {
            "argux_host": host_name,
            "argux_item": item,
            "userid": self.request.authenticated_userid,
            "timespan": timespan,
            "action": action,
            'active_alerts': len(alerts),
            "has_details": has_details}
