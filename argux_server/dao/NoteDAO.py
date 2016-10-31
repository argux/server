"""Data Access Object class for handling Notes."""

from argux_server.models import (
    Note
)

from .BaseDAO import BaseDAO


class NoteDAO(BaseDAO):

    """Note DAO.

    Data Access Object for handling Notes.
    """

    def get_notes_for_host(self, host, page=0, pagesize=20):
        """Get notes for host."""
        note = self.db_session.query(Note)\
            .filter(Note.host == host)\
            .order_by(Note.timestamp.desc())\
            .slice(int(pagesize)*int(page), int(pagesize)*(int(page)+1))\
            .all()
        return note

    def get_note_count_for_host(self, host):
        note_count = self.db_session.query(Note)\
            .filter(Note.host == host)\
            .count()

        return note_count

    def create_note_for_host(self, host, subject, message, timestamp):
        """Create new note for host."""
        note = Note(
            host=host,
            subject=subject,
            message=message,
            timestamp=timestamp)

        self.db_session.add(note)
        return note
