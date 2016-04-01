"""RestView for Items."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

import dateutil.parser

from datetime import datetime, timedelta

import json

import math

from . import RestView

from argux_server.util import (
    TIME_OFFSET_EXPR,
    DATE_FMT
)


@view_defaults(renderer='json')
class RestItemViews(RestView):

    """RestItemViews class.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_item_1',
        check_csrf=True,
        permission='view'
    )
    def item_1_view(self):
        """Create Item or Return item.

        POST creates an Item.
        GET  returns Item Details.
        """
        # Fallback response
        ret = Response(
            status='400 Bad Request',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "400 Bad Request", "message": "dunno"}')

        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']

        if self.request.method == "POST":
            ret = self.item_1_view_create(host_name, item_key)

        if self.request.method == "GET":
            ret = Response(
                status='404 Not Found',
                content_type='application/json',
                charset='UTF-8',
                body=json.dumps(
                    {
                        'error': 'Not Found',
                        'host': host_name,
                        'item': item_key
                    }))

            host = self.dao.host_dao.get_host_by_name(host_name)
            if host is not None:
                item = self.dao.item_dao.get_item_by_host_key(
                    host,
                    item_key)

                if item is not None:
                    ret = self.item_details_1_view_read(host, item)

        return ret

    def item_1_view_create(self, host_name, item_key):
        dao = self.dao

        category = None

        try:
            item_name = self.request.json_body.get('name', None)
            item_desc = self.request.json_body.get('description', None)
            item_category = self.request.json_body.get('category', None)
            item_type_key = self.request.json_body.get('type', None)
            item_unit = self.request.json_body.get('unit', None)
        except ValueError:
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "type not specified"}')

        if item_type_key is None:
            return Response(
                status='400 Bad Request',
                content_type='application/json; charset=UTF-8',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "type not specified"}')

        host = dao.host_dao.get_host_by_name(host_name)

        item_type = dao.item_dao.get_itemtype_by_name(item_type_key)

        item = dao.item_dao.create_item({
            'key': item_key,
            'host': host,
            'name': item_name,
            'category': item_category,
            'itemtype': item_type,
            'unit': item_unit})

        return Response(
            status='201 Created',
            content_type='application/json',
            charset='UTF-8',
            body=json.dumps({'name': item.key}))

    @view_config(
        route_name='rest_item_values_1',
        request_method='POST',
        check_csrf=True,
        permission='view'
    )
    def item_values_1_view(self):
        """Return values for an item."""
        dao = self.dao

        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']

        try:
            value = self.request.json_body.get('value', None)
            ts = self.request.json_body.get('timestamp', None)
        except ValueError:
            value = None
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "value not specified"}')

        host = dao.host_dao.get_host_by_name(host_name)
        item = dao.item_dao.get_item_by_host_key(host, item_key)

        t = dateutil.parser.parse(ts)

        dao.item_dao.push_value(item, t, value)

        return Response(
            status='201 Created',
            content_type='application/json; charset=UTF-8')

    @view_config(
        route_name='rest_item_details_1',
        check_csrf=True,
        permission='view'
    )
    def item_details_1_view(self):
        """Return details (summary) for an item."""

        # Fallback response
        ret = Response(
            status='400 Bad Request',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "400 Bad Request", "message": "don\'t do that"}')

        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']

        if self.request.method == "GET":
            ret = Response(
                status='404 Not Found',
                content_type='application/json',
                charset='UTF-8',
                body=json.dumps(
                    {
                        'error': 'Not Found',
                        'host': host_name,
                        'item': item_key
                    }))

            host = self.dao.host_dao.get_host_by_name(host_name)
            if host is not None:
                item = self.dao.item_dao.get_item_by_host_key(
                    host,
                    item_key)

                if item is not None:
                    ret = self.item_details_1_view_read(host, item)

        return ret

    def item_details_1_view_read(self, host, item):
        values = []
        active_alerts = []

        q_start = self.request.params.get('start', None)
        q_end = self.request.params.get('end', 'now')

        get_values = self.request.params.get('get_values', 'true')
        get_alerts = self.request.params.get('get_alerts', 'false')

        try:
            interval = int(self.request.params.get('interval', '60'))
        except ValueError:
            interval = 60


        if (q_start != None):
            start = dateutil.parser.parse(q_start)

        if q_end != 'now':
            end = dateutil.parser.parse(q_end)
        else:
            end = datetime.now()

        if get_values == 'true':
            values = self.__get_values(item, start, end, interval)
            active_alerts = self.__get_active_alerts(item)

        if get_alerts == 'true':
            active_alerts = self.__get_active_alerts(item)

        unit = None
        if item.unit_id:
            unit = {
                'name': item.unit.name,
                'symbol': item.unit.symbol,
            }

        return {
            'host': host.name,
            'item': item.key,
            'active_alerts': len(active_alerts),
            'start_time': start.strftime(DATE_FMT),
            'end_time': end.strftime(DATE_FMT),
            'unit': unit,
            'values': values,
            'alerts': active_alerts
        }

    def __get_active_alerts(self, item):
        """Return active alermetric_prefix:
                unit['metric]ts on an item."""
        alerts = []
        d_alerts = self.dao.item_dao.get_alerts(item)

        for alert in d_alerts:
            alerts.append({
                'start_time': alert.start_time.strftime(DATE_FMT),
                'severity': alert.trigger.severity.key,
                'acknowledgement': alert.acknowledgement,
                'name': alert.trigger.name
            })

        return alerts

    def __get_values(self, item, start, end, interval=60):
        """Return array of timestamp+value objects within a timeframe.

        timestamp is formatted according to argux_server.util.DATE_FMT

        This format should be in ISO8601 (YYYY/MM/DDTmm:hh:ssZ)
        """
        values = []
        max_values = []
        min_values = []
        d_values = self.dao.item_dao.get_values(
            item,
            start_time=start,
            end_time=end)

        old_value = None

        for index, value in enumerate(d_values):
            # Fill in the gaps between values.
            # This section of the code assumes 1 minute gaps, which is silly.
            # The interval should be known somehow (maybe configurable in the item?).
            # Also, it should calculate min/max/avg values.
            if old_value:
                tdelta = value.timestamp - old_value.timestamp
                if tdelta.seconds > interval:
                    for a in range(0, int(tdelta.seconds/interval)):
                        values.append({
                            'ts': (old_value.timestamp + timedelta(minutes=a)).strftime(DATE_FMT),
                            'value': None
                        })

            values.append({
                'ts': value.timestamp.strftime(DATE_FMT),
                'value': str(value.value)
            })

            old_value = value

        return {
            'avg': values,
            'max': max_values,
            'min': min_values
        }
