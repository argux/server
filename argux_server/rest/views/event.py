"""RestView for Events."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.httpexceptions import (
    HTTPBadRequest
)

from pyramid.response import Response

import json

from . import RestView

from argux_server.util import (
    DATE_FMT
)


@view_defaults(renderer='json')
class RestEventViews(RestView):

    """Views for REST interface of Events.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_events_1',
        request_method='GET',
        require_csrf=True,
        permission='view'
    )
    def events_1_view_read(self):
        """Get all events."""
        return {'a':'n'}

    @view_config(
        route_name='rest_event_1',
        request_method='GET',
        require_csrf=True,
        permission='view'
    )
    def event_1_view_read(self):
        """Get all events."""
        return {'a':'n'}

    @view_config(
        route_name='rest_event_1',
        request_method='PUT',
        require_csrf=True,
        permission='view'
    )
    def event_1_view_update(self):
        """Get all events."""
        return {'a':'n'}
