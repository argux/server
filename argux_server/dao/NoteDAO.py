"""Data Access Object class for handling Notes."""

from argux_server.models import (
    Note
)

from .BaseDAO import BaseDAO


class NoteDAO(BaseDAO):

    """Note DAO.

    Data Access Object for handling Notes.
    """

    def get_notes_for_host(self, host):
        """Get notes for host."""
        note = self.db_session.query(Note)\
            .filter(Note.host == host)\
            .order_by(Note.timestamp.desc())\
            .all()

        return note

    def create_note_for_host(self, host, subject, message, timestamp):
        """Create new note for host."""
        note = Note(
            host=host,
            subject=subject,
            message=message,
            timestamp=timestamp)

        self.db_session.add(note)
        return note
