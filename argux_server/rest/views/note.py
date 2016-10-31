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
        permission='view'
    )
    def note_1_view(self):
        """Return notes or create note."""
        # Fallback response
        ret = Response(
            status='400 Bad Request',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "400 Bad Request", "message": "dunno"}')

        if self.request.method == "GET":
            ret = self.note_1_view_read()

        if self.request.method == "POST":
            ret = self.note_1_view_create()

        return ret

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



    def note_1_view_read(self):
        """Return list of notes for host"""
        host_name = self.request.params.get('host', None)
        if host_name is None:
            raise ValueError("Hostname not provided.")

        host = self.dao.host_dao.get_host_by_name(host_name)
        if host is None:
            raise ValueError("Host does not exist.")

        page = self.request.params.get('page', 0)
        pagesize = self.request.params.get('pagesize', 10)

        d_notes = self.dao.note_dao.get_notes_for_host(host, page=page, pagesize=pagesize)
        note_count = self.dao.note_dao.get_note_count_for_host(host)

        notes = []

        if d_notes:
            for d_note in d_notes:
                notes.append({
                    "subject": d_note.subject,
                    "message": d_note.message,
                    "timestamp": d_note\
                        .timestamp.strftime("%Y-%m-%dT%H:%M:%S")
                })

        return {
            'host' : host_name,
            'notes' : notes,
            'note_count' : note_count,
            'page' : page,
            'page_size' : page_size,
            'active_alerts': 0
        }
