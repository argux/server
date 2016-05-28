"""Data Access Object class for handling Graphs."""

from argux_server.models import (
    HistoryGraph,
    HistoryGraphItem
)

import argux_server.auth

from sqlalchemy.orm import (
    joinedload
)

from .BaseDAO import BaseDAO


class GraphDAO(BaseDAO):

    """GraphDAO Class."""

    def create_graph(self, name):

        graph = HistoryGraph(
            name=name)

        self.db_session.add(graph)

        self.db_session.flush()

        return graph

    def get_graph(self, graph_id):
        graph = self.db_session.query(HistoryGraph)\
            .options(joinedload('items'))\
            .filter(HistoryGraph.id==graph_id)\
            .first()

        return graph

    def graph_add_item(self, graph, item, color=None):
        d_graph_item = self.db_session.query(HistoryGraphItem)\
            .filter(HistoryGraphItem.history_graph_id == graph.id)\
            .filter(HistoryGraphItem.item_id == item.id)\
            .first()

        if d_graph_item is None:
            d_graph_item = HistoryGraphItem(
                history_graph_id=graph.id,
                item_id=item.id,
                color=color)
            self.db_session.add(d_graph_item)
            self.db_session.flush()

        return d_graph_item

    def graph_get_items(self, graph):
        items = []

        for item in graph.items:
            i = item.item
            i.color = item.color
            items.append(i)

        return items
