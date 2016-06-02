"""Authentication REST Interface."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.security import (
    remember,
    forget,
)

from pyramid.response import Response

from pyramid.httpexceptions import (
    HTTPBadRequest
)

import json

from . import RestView


@view_defaults(renderer='json')
class RestAuthenticationViews(RestView):

    """AuthenticationViews, login/logout...

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_login_1',
        request_method='POST',
    )
    def login_1_view(self):
        username = self.request.json_body.get('username', None)
        password = self.request.json_body.get('password', None)

        if self.dao.user_dao.validate_user(username, password):
            self.request.session['username'] = username

            headers = remember(self.request, username)

            response = Response(
                content_type="application/json",
                body=json.dumps(
                    {
                        'status': 'success'
                    }))
            response.headerlist.extend(headers)
            response.headerlist.extend(
                [(
                    'X-CSRF-Token',
                    self.request.session.get_csrf_token()
                )])

            return response

        return HTTPBadRequest()

    @view_config(
        route_name='rest_logout_1',
        request_method='POST',
        require_csrf=True,
        permission='logout'
    )
    def logout_1_view(self):
        self.request.session.invalidate()

        headers = forget(self.request)

        response = Response(
            content_type="application/json",
            body=json.dumps(
                {
                    'status': 'success'
                }))
        response.headerlist.extend(headers)

        return response
