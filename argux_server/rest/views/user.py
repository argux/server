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
        route_name='rest_user_bookmarks_1',
        request_method='GET',
        require_csrf=True,
        permission='view'
    )
    def user_bookmarks_1_view_get(self):
        bookmarks = []

        user = self.dao.user_dao.get_user(
            self.request.authenticated_userid)

        for bookmark in user.bookmarks:
            matched = json.loads(bookmark.route_matched)

            url = self.request.route_url(
                route_name=bookmark.route_name,
                **matched)

            bookmarks.append({
                'id': bookmark.nav_hash,
                'url': url,
                'title': bookmark.title
            })

        return {
            'bookmarks' : bookmarks
        }

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
        return Response(
            status='400 Bad Request',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "400 Bad Request", "message": "Not implemented"}')

    @view_config(
        route_name='rest_user_profile_1',
        request_method='PATCH',
        require_csrf=True,
        permission='view'
    )
    def user_profile_1_view_patch(self):
        try:
            json_body = self.request.json_body
        except ValueError as err:
            return Response(
                status='400 Bad Request',
                content_type='application/json')

        user = self.dao.user_dao.get_user(
            self.request.authenticated_userid)

        try:
            password = json_body.get('password', None)
            if password is not None:
                self.dao.user_dao.set_user_password(
                    user,
                    password)
                return {'password reset':'ok'}
        except ValueError as err:
            return Response(
                status='400 Bad Request',
                content_type='application/json')


        return Response(
            status='400 Bad Request',
            content_type='application/json')
