"""RestView for Graphs."""

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
class RestGraphViews(RestView):

    """RestItemViews class.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_graph_1',
        request_method='GET',
        require_csrf=True,
        permission='view'
    )
    def graph_1_view_read(self):
        graph_id = self.request.matchdict['id']
        get_values = self.request.params.get('get_values', 'false')

        items = []
        max_value = 0
        min_value = 0

        graph = self.dao.graph_dao.get_graph(graph_id=graph_id)
        if graph is None:
            return Response(
                status='404 Not Found',
                content_type='application/json')

        d_items = self.dao.graph_dao.graph_get_items(graph)
        for d_item in d_items:
            item = {
                'name': d_item.name,
                'key': d_item.key,
                'host': d_item.host.name,
            }

            if d_item.color is not None:
                item['color'] = d_item.color

            if get_values == 'true':
                q_start = self.request.params.get('start', None)
                q_end = self.request.params.get('end', None)

                try:
                    interval = int(self.request.params.get('interval', '60'))
                except ValueError:
                    interval = 60

                if (q_start != None):
                    start = dateutil.parser.parse(q_start)
                else:
                    start = datetime.now() - timedelta(minutes=15)

                if q_end != None:
                    end = dateutil.parser.parse(q_end)
                else:
                    end = datetime.now()

                (values, max_val, min_val) = self.__get_values(d_item, start, end, interval)

                item['values'] = values

                if max_val > max_value:
                    max_value = max_val
                if min_val < min_value:
                    min_value = min_val

                if d_item.unit_id:
                    item['unit'] = {
                        'name': d_item.unit.name,
                        'symbol': d_item.unit.symbol,
                    }

            items.append(item)

        return {
            'id': graph.id,
            'name': graph.name,
            'items': items,
            'max_value': max_value,
            'min_value': min_value
        }

    @view_config(
        route_name='rest_graph_1',
        request_method='PATCH',
        require_csrf=True,
        permission='view'
    )
    def graph_1_view_update(self):
        graph_id = self.request.matchdict['id']

        try:
            json_body = self.request.json_body
        except ValueError as err:
            return Response(
                status='400 Bad Request',
                content_type='application/json')

        try:
            items = json_body.get('items', [])
        except ValueError:
            item = []

        try:
            graph_name = json_body.get('name', None)
        except ValueError as err:
            return Response(
                status='400 Bad Request',
                content_type='application/json')
        if graph_name is None:
            return Response(
                status='400 Bad Request',
                content_type='application/json')

        if items.count == 0:
            return Response(
                status='400 Bad Request',
                content_type='application/json')

        return {} 

    @view_config(
        route_name='rest_graph_1',
        request_method='DELETE',
        require_csrf=True,
        permission='view'
    )
    def graph_1_view_delete(self):
        graph_id = self.request.matchdict['id']

        return {}

    @view_config(
        route_name='rest_graphs_1',
        request_method='GET',
        require_csrf=True,
        permission='view'
    )
    def graphs_1_view_read(self):
        return {}

    @view_config(
        route_name='rest_graphs_1',
        request_method='POST',
        require_csrf=True,
        permission='view'
    )
    def graphs_1_view_create(self):

        try:
            json_body = self.request.json_body
        except ValueError as err:
            return Response(
                status='400 Bad Request',
                content_type='application/json')

        try:
            items = json_body.get('items', [])
        except ValueError:
            item = []

        try:
            graph_name = json_body.get('name', None)
        except ValueError as err:
            return Response(
                status='400 Bad Request',
                content_type='application/json')
        if graph_name is None:
            return Response(
                status='400 Bad Request',
                content_type='application/json')


        if items.count == 0:
            return Response(
                status='400 Bad Request',
                content_type='application/json')

        d_items = []

        # Add items to graph
        ####################
        for item in items:
            d_host = self.dao.host_dao.get_host_by_name(item['host'])
            if d_host is None:
                return Response(
                    status='400 Bad Request',
                    content_type='application/json')

            d_item = self.dao.item_dao.get_item_by_host_key(
                host=d_host,
                key=item['name'])
            if d_item is None:
                return Response(
                    status='400 Bad Request',
                    content_type='application/json')

            if 'color' in item:
                d_items.append([d_item, item['color']])
            else:
                d_items.append([d_item, None])

        graph = self.dao.graph_dao.create_graph(name=graph_name)

        for d_item in d_items:
            self.dao.graph_dao.graph_add_item(graph, d_item[0], color=d_item[1])

        return {
            'id': graph.id,
            'name': graph.name,
            'items': items
        }

    def __get_values(self, item, start, end, interval=60):
        """Return array of timestamp+value objects within a timeframe.

        timestamp is formatted according to argux_server.util.DATE_FMT

        This format should be in ISO8601 (YYYY/MM/DDTmm:hh:ssZ)
        """
        values = []
        max_values = []
        min_values = []
        max_value = None
        min_value = None
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
                if tdelta.seconds > (1.5*interval):
                    for a in range(0, int(tdelta.seconds/interval)):
                        values.append({
                            'ts': (old_value.timestamp + timedelta(minutes=a)).strftime(DATE_FMT),
                            'value': None
                        })

            if max_value is None:
                max_value = value.value
                min_value = value.value

            if value.value < min_value:
                min_value = value.value

            if value.value > max_value:
                max_value = value.value

            values.append({
                'ts': value.timestamp.strftime(DATE_FMT),
                'value': str(value.value)
            })

            old_value = value

        # Make sure we do not return None
        if max_value is None:
            max_value = 0
            min_value = 0

        return (
            {
                'avg': values,
                'max': max_values,
                'min': min_values
            },
            max_value,
            min_value
        )
