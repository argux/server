"""RestView for Users."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.httpexceptions import (
    HTTPBadRequest
)


from pyramid.response import Response
from pyramid.request import Request

import json

from . import RestView

from argux_server.monitors import MONITORS

@view_defaults(renderer='json')
class RestUserViews(RestView):

    """RestMonitor View.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_user_bookmark_1',
        request_method='POST',
        require_csrf=True,
        permission='view'
    )
    def user_bookmark_1_view_create(self):
        bookmark = self.request.matchdict['bookmark'].lower()

        item = self.dao.nav_dao.lookup_nav_item(bookmark)
        if item is None:
            # Return Conflict (Item doesn't exist)
            return None

        user = self.dao.user_dao.get_user(
            self.request.authenticated_userid)

        user.bookmarks.append(item)

        return {'ok':'ok'}

    @view_config(
        route_name='rest_user_bookmark_1',
        request_method='DELETE',
        require_csrf=True,
        permission='view'
    )
    def user_bookmark_1_view_delete(self):
        bookmark = self.request.matchdict['bookmark'].lower()

        item = self.dao.nav_dao.lookup_nav_item(bookmark)
        if item is None:
            # Return Conflict (Item doesn't exist)
            return None

        user = self.dao.user_dao.get_user(
            self.request.authenticated_userid)

        user.bookmarks.remove(item)

        return {'ok':'ok'}

    @view_config(
        route_name='rest_user_bookmark_1',
        request_method='GET',
        require_csrf=True,
        permission='view'
    )
    def user_bookmark_1_view_get(self):
        bookmark = self.request.matchdict['bookmark'].lower()

        item = self.dao.nav_dao.lookup_nav_item(bookmark)
        if item is not None:
            matched = json.loads(item.route_matched)
            params = json.loads(item.route_params)

            a = {'route_name': item.route_name}
            a.update(matched)
            print(type(matched))

            url = self.request.route_url(route_name=item.route_name, **matched)

            print(url)

        return {'ok':'ok'}
