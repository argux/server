"""RestView for Notes."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

from datetime import datetime

import json

from . import RestView


@view_defaults(renderer='json')
class RestNoteViews(RestView):

    """RestNote views.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_note_1',
        require_csrf=True,
        permission='view',
        method='POST'
    )
    def note_1_view_create(self):
        """Create new note."""
        dao = self.dao
        try:
            host_name = self.request.json_body.get("host", None)
            subject = self.request.json_body.get("subject", None)
            msg = self.request.json_body.get("message", None)
        except ValueError:
            print(self.request.body)
            return "AA"

        if msg is None:
            raise ValueError("Message is missing.")
        if subject is None:
            raise ValueError("Subject is missing.")
        if host_name is None:
            raise ValueError("Hostname is missing.")

        host = dao.host_dao.get_host_by_name(host_name)

        if host is None:
            raise ValueError("Host is missing.")

        note = dao.note_dao.create_note_for_host(
            host,
            subject,
            msg,
            datetime.now())

        return Response(
            status='201 Created',
            content_type='application/json',
            body=json.dumps(
                {
                    'subject': note.subject
                }))
