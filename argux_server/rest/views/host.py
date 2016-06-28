"""RestView for Hosts."""

from pyramid.view import (
    view_config,
    view_defaults,
)

import transaction

import json

from pyramid.response import Response

from . import RestView

from argux_server.util import (
    TIME_OFFSET_EXPR,
    DATE_FMT
)


@view_defaults(renderer='json')
class RestHostViews(RestView):

    """RestHosts View.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_hosts_1',
        require_csrf=True,
        permission='view'
    )
    def hosts_1_view(self):
        """Return array of all hosts."""
        d_hosts = self.dao.host_dao.get_all_hosts()

        hosts = []
        for host in d_hosts:
            sev_label = 'unknown'
            n_items = self.dao.item_dao.get_item_count_from_host(host)
            severity = self.dao.host_dao.get_host_severity(host)
            if (severity):
                sev_label = severity.key
            hosts.append({
                "name": host.name,
                "n_items": n_items,
                "severity": sev_label,
                "active_alerts": self.__get_active_alert_count(host)
            })

        return {'hosts': hosts}

    @view_config(
        route_name='rest_host_1',
        require_csrf=True,
        permission='view'
    )
    def host_1_view(self):
        """Create host or return host.

        POST creates a host.
        GET  returns Host details.
        """
        host_name = self.request.matchdict['host']

        ret = Response(
            status='400 Bad Request',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "400 Bad Request", "message": "dunno"}')

        if self.request.method == "DELETE":
            ret = self.host_1_view_delete(host_name)

        if self.request.method == "POST":
            ret = self.host_1_view_post(host_name)

        if self.request.method == "GET":
            ret = self.host_1_view_get(host_name)

        return ret

    def host_1_view_post(self, host_name):
        """Create new host."""
        description = None
        addresses = []
        groups = []

        if len(self.request.body) > 0:
            try:
                json_body = self.request.json_body
            except ValueError as err:
                return Response(
                    status='400 Bad Request',
                    content_type='application/json')

            # Optional (Description)
            try:
                description = json_body.get('description', None)
            except ValueError:
                description = None

            # Optional (Host-Addresses)
            try:
                addresses = json_body.get('address', [])
            except ValueError:
                addresses = []

            # Optional (Host-Groups)
            try:
                groups = json_body.get('groups', [])
            except ValueError:
                groups = []

        for group in groups:
            g = self.dao.host_dao.get_hostgroup_by_name(group)
            if g is None:
                return Response(
                    status='409 Conflict',
                    content_type='application/json',
                    charset='UTF-8',
                    body=json.dumps({
                        'hostgroup': group,
                        'conflict': 'Does not exists'
                    }))
                

        host = self.dao.host_dao.create_host(
            name=host_name,
            description=description)

        for address in addresses:
            address_description = ""
            if 'description' in address:
                address_description = address['description']
            if 'address' in address:
                try:
                    self.dao.host_dao.add_address(
                        host,
                        address['address'],
                        address_description)
                except Exception as e:
                    transaction.abort()
                    return str(e)

        self.dao.host_dao.add_host_to_group('All', host)
        for group in groups:
            self.dao.host_dao.add_host_to_group(group, host)

        try:
            transaction.commit()
        except Exception as err:
            transaction.abort()
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body=json.dumps({
                    "error": "400 Bad Request",
                    "message": str(err)
                }))

        return Response(
            status='201 Created',
            content_type='application/json')

    def host_1_view_delete(self, host_name):
        """Delete a host."""

        self.dao.host_dao.delete_host(
            name=host_name)

        return Response(
            status='200 Ok',
            content_type='application/json')

    def host_1_view_get(self, host_name):
        """Return host details."""
        host_get_details = self.request.params.get('details', 'false')
        host_get_items = self.request.params.get('items', 'false')
        host_get_alerts = self.request.params.get('alerts', 'false')

        host = self.dao.host_dao.get_host_by_name(host_name)

        items = []
        details = []
        active_alerts = []
        active_alert_count = 0 
        if host is None:
            return Response(
                status="404 Not Found",
                content_type='application/json',
                charset='utf-8',
                body='{"error":"NOT FOUND"}')


        if host_get_alerts == 'true':
            active_alerts = self.__get_active_alerts(host)
            active_alert_count = len(active_alerts)

        if host_get_items == 'true':
            items = self._get_items(host)
            if host_get_alerts != 'true':
                active_alert_count = self.__get_active_alert_count(host)

        if host_get_details == 'true':
            details = []
            if (host_get_alerts != 'true'):
                active_alert_count = self.__get_active_alert_count(host)


        return {
            'name' : host.name,
            'items': items,
            'details': details,
            'alerts': active_alerts,
            'active_alerts': active_alert_count,
        }

    def __get_active_alert_count(self, host):
        d_items = self.dao.item_dao.get_items_from_host(host)
        if (d_items == None):
            return 0

        n_total_alerts = 0

        for item in d_items:
            n_alerts = self.dao.item_dao.get_active_alert_count(item)
            n_total_alerts += n_alerts

        return n_total_alerts

    def __get_active_alerts(self, host):
        d_items = self.dao.item_dao.get_items_from_host(host)
        if (d_items == None):
            return []

        alerts = []
        for item in d_items:
            d_alerts = self.dao.item_dao.get_alerts(item)
            for alert in d_alerts:
                alerts.append({
                    'start_time': alert.start_time.strftime(DATE_FMT),
                    'severity': alert.trigger.severity.key,
                    'acknowledgement': alert.acknowledgement,
                    'name': alert.trigger.name,
                    'item': {
                        'key': alert.trigger.item.key,
                        'name': alert.trigger.item.name
                    }
                })

        return alerts

    def _get_items(self, host):
        """Get list of items for host."""
        d_items = self.dao.item_dao.get_items_from_host(host)
        if (d_items == None):
            return []

        items = []
        for item in d_items:
            if item.name:
                name = item.name
            else:
                name = None

            if item.category:
                category = item.category.name
            else:
                category = None

            unit = None
            if item.unit_id:
                unit = {
                    'name': item.unit.name,
                    'symbol': item.unit.symbol,
                }

            value = self.dao.item_dao.get_last_value(item)

            if value:
                items.append({
                    "category": category,
                    "name": name,
                    "key": item.key,
                    "unit": unit,
                    "last_val": str(value.value),
                    "last_ts": value.timestamp.strftime("%Y-%m-%dT%H:%M:%S")})
            else:
                items.append({
                    "category": category,
                    "name": name,
                    "unit": unit,
                    "key": item.key})
        return items

