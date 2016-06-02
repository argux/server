"""RestView for Monitors."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.httpexceptions import (
    HTTPBadRequest
)


from pyramid.response import Response

import json

import transaction

from .. import RestView

from argux_server.monitors import MONITORS

@view_defaults(renderer='json')
class RestMonitorViews(RestView):

    """RestMonitor View.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_monitors_1',
        request_method='GET',
        require_csrf=True,
        permission='view'
    )
    def monitors_1_view_read(self):
        monitor_type = self.request.matchdict['type'].upper()
        monitors = []

        if not monitor_type in MONITORS:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'invalid type'
                }))

        d_monitors = self.dao.monitor_dao.get_all_monitors_for_type(
            monitor_type)

        for d_monitor in d_monitors:
            options = {}

            for d_option in d_monitor.options:
                options[d_option.key] = d_option.value

            monitors.append({
                'address': d_monitor.host_address.name,
                'host': d_monitor.host_address.host.name,
                'active': d_monitor.active,
                'options': options
            })

        return {
            'monitors': monitors
        }

    @view_config(
        route_name='rest_monitor_1',
        request_method='POST',
        require_csrf=True,
        permission='view'
    )
    def monitor_1_view_create(self):
        monitor_type = self.request.matchdict['type'].upper()
        host_name = self.request.matchdict['host']
        address = self.request.matchdict['address']

        try:
            active = self.request.json_body.get('active', True)
            if active=='false' or active==False:
                active = False
            else:
                active = True
        except ValueError:
            active = True

        try:
            options = self.request.json_body.get('options', None)
        except ValueError:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'missing options'
                }))

        if not monitor_type in MONITORS:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'invalid type'
                }))

        monitor = MONITORS.get(monitor_type)

        if monitor.validate_options(options) == False:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'invalid options'
                }))

        d_host = self.dao.host_dao.get_host_by_name(
            name = host_name)
        if d_host is None:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'missing host'
                }))

        d_address = self.dao.host_dao.get_address(
            host=d_host,
            address=address)
        if d_address is None:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'missing address'
                }))

        monitor = self.dao.monitor_dao.create_monitor(
            monitor_type,
            d_address,
            options,
            active=active)
        if monitor is None:
            monitor = self.dao.monitor_dao.get_monitor(
                host_name,
                address,
                monitor_type)
            if monitor is not None:
                monitor.active = active
                transaction.commit()

        # FIXME: run monitor once to create the items.
        #MONITORS[monitor_type].monitor_once(self.dao, monitor)

        return {'ok':'ok'}

    @view_config(
        route_name='rest_monitor_1',
        request_method='DELETE',
        require_csrf=True,
        permission='view'
    )
    def monitor_1_view_delete(self):
        monitor_type = self.request.matchdict['type'].upper()
        host_name = self.request.matchdict['host']
        address = self.request.matchdict['address']

        self.dao.monitor_dao.delete_monitor(
            host_name,
            address,
            monitor_type)

        return {'ok':'ok'}
