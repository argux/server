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

        items = []
        max_value = 0
        min_value = 0

        graph = self.dao.graph_dao.get_graph(graph_id=graph_id)
        if graph is None:
            return Response(
                status='404 Not Found',
                content_type='application/json')

        q_start = self.request.params.get('start', None)
        q_end = self.request.params.get('end', None)

        d_items = self.dao.graph_dao.graph_get_items(graph)
        for d_item in d_items:
            if (q_start != None):
                start = dateutil.parser.parse(q_start)
            else:
                start = datetime.now() - timedelta(minutes=15)

            if q_end != None:
                end = dateutil.parser.parse(q_end)
            else:
                end = datetime.now()

            try:
                interval = int(self.request.params.get('interval', '60'))
            except ValueError:
                interval = 60

            (values, max_val, min_val) = self.__get_values(d_item, start, end, interval)

            item = {
                'name': d_item.name + ' (max)',
                'key': d_item.key,
                'host': d_item.host.name,
                'color-fill': 'false',
            }

            if d_item.unit_id:
                item['unit'] = {
                    'name': d_item.unit.name,
                    'symbol': d_item.unit.symbol,
                }

            item['values'] = values['max']

            items.append(item)

            item = {
                'name': d_item.name + ' (avg)',
                'key': d_item.key,
                'host': d_item.host.name,
            }

            if d_item.color is not None:
                item['color'] = d_item.color

            if d_item.unit_id:
                item['unit'] = {
                    'name': d_item.unit.name,
                    'symbol': d_item.unit.symbol,
                }

            item['values'] = values['avg']

            items.append(item)

            item = {
                'name': d_item.name + ' (min)',
                'key': d_item.key,
                'host': d_item.host.name,
                'color-fill': 'false',
            }

            if d_item.unit_id:
                item['unit'] = {
                    'name': d_item.unit.name,
                    'symbol': d_item.unit.symbol,
                }

            item['values'] = values['min']

            items.append(item)

            if max_val > max_value:
                max_value = max_val
            if min_val < min_value:
                min_value = min_val


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

        tf_max_value = None
        tf_min_value = None
        d_values = self.dao.item_dao.get_values(
            item,
            start_time=start,
            end_time=end)

        interval_values = []
        interval_start = None
        interval_end = None

        print(interval)

        for index, value in enumerate(d_values):

            # Start interval with first value
            if interval_start is None:
                interval_start = value
                tf_max_value = value.value
                tf_min_value = value.value

            if (value.timestamp - interval_start.timestamp) < timedelta(seconds=interval):
                interval_values.append(value)
            else:
                sum_value = 0
                max_value = None
                min_value = None

                if interval_end is not None:
                    tdelta = interval_start.timestamp - interval_end.timestamp

                    # Allow for some uncertainty in timestamps,
                    # if the difference between two measurements
                    # is larger then 1.5 times the interval, add
                    # a NULL/None value.
                    if tdelta.seconds > (1.5*interval):
                        for a in range(0, int(tdelta.seconds/interval)):
                            values.append({
                                'ts': (interval_end.timestamp + timedelta(seconds=(a*interval))).strftime(DATE_FMT),
                                'value': None
                            })
                            max_values.append({
                                'ts': (interval_end.timestamp + timedelta(seconds=(a*interval))).strftime(DATE_FMT),
                                'value': None
                            })
                            min_values.append({
                                'ts': (interval_end.timestamp + timedelta(seconds=(a*interval))).strftime(DATE_FMT),
                                'value': None
                            })

                for item in interval_values:
                    if max_value is None:
                        max_value = item.value
                        min_value = item.value

                    if item.value < min_value:
                        min_value = item.value
                        if min_value > tf_min_value:
                            tf_min_value = min_value

                    if item.value > max_value:
                        max_value = item.value
                        if max_value > tf_max_value:
                            tf_max_value = max_value

                    sum_value += item.value
                    interval_end = item 

                if len(interval_values) > 0:
                    avg_value = sum_value / len(interval_values)

                    values.append({
                        'ts': interval_end.timestamp.strftime(DATE_FMT),
                        'value': str(avg_value)
                    })
                    max_values.append({
                        'ts': interval_end.timestamp.strftime(DATE_FMT),
                        'value': str(max_value)
                    })
                    min_values.append({
                        'ts': interval_end.timestamp.strftime(DATE_FMT),
                        'value': str(min_value)
                    })

                interval_start = value
                interval_values = []
                interval_values.append(value)

        return (
            {
                'avg': values,
                'max': max_values,
                'min': min_values
            },
            tf_max_value,
            tf_min_value
        )
