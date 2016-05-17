"""Data Access Object class for handling Graphs."""

from argux_server.models import (
    HistoryGraph
)

import argux_server.auth

from .BaseDAO import BaseDAO


class GraphDAO(BaseDAO):

    """GraphDAO Class."""

    def create_graph(self):

        graph = HistoryGraph(
            name=name)

        self.db_session.add(graph)
