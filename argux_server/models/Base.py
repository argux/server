# Package

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension

Session = sessionmaker(extension=ZopeTransactionExtension())  # pylint: disable=invalid-name

DB_SESSION = scoped_session(Session)
BASE = declarative_base()
