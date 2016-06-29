"""RestView for Users."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.httpexceptions import (
    HTTPBadRequest
)


from pyramid.response import Response

import json

from .. import RestView

from argux_server.monitors import MONITORS

@view_defaults(renderer='json')
class RestUserViews(RestView):

    """RestMonitor View.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_admin_user_1',
        request_method='POST',
        require_csrf=True,
        permission='admin'
    )
    def admin_user_1_view_create(self):
        username = self.request.matchdict['username'].lower()

        if len(self.request.body) > 0:
            try:
                json_body = self.request.json_body
            except ValueError as err:
                return Response(
                    status='400 Bad Request',
                    content_type='application/json')

            try:
                password = json_body.get('password', None)
            except ValueError:
                return Response(
                    status='400 Bad Request',
                    content_type='application/json')

            user = self.dao.user_dao.create_user (
                username,
                password,
                hash_method='bcrypt');

        return {'ok':'ok'}

    @view_config(
        route_name='rest_admin_user_1',
        request_method='GET',
        require_csrf=True,
        permission='admin'
    )
    def admin_user_1_view_read(self):
        return {'ok': 'ok'}

    @view_config(
        route_name='rest_admin_user_1',
        request_method='DELETE',
        require_csrf=True,
        permission='admin'
    )
    def admin_user_1_view_delete(self):
        username = self.request.matchdict['username'].lower()

        # Make sure we don't remove the userid of the currently logged in user
        if username == self.request.authenticated_userid:
            return Response(
                status='409 Conflict',
                content_type='application/json',
                body=json.dumps({
                    "error": "409 Conflict",
                    "message" : "Cannot remove userid of session-owner."
                }))
        user = self.dao.user_dao.get_user(username)
        if user.protected:
            return Response(
                status='409 Conflict',
                content_type='application/json',
                body=json.dumps({
                    "error": "409 Conflict",
                    "message" : "User is protected."
                }))

        self.dao.user_dao.delete_user(username)
        return {'ok': 'ok'}

    @view_config(
        route_name='rest_admin_users_1',
        request_method='GET',
        require_csrf=True,
        permission='admin'
    )
    def admin_users_1_view_get(self):
        d_users = self.dao.user_dao.get_users()

        users = []
        for user in d_users:
            users.append({
                "name": user.name,  
                "protected": user.protected
            })

        return {
            'users':users
        }
