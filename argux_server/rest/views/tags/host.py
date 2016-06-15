"""RestViews for Tags."""

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

@view_defaults(renderer='json')
class RestTagsViews(RestView):

    def tags_host_1_view_create(self):
        return {}
