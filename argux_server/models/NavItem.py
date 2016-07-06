"""Tag Module, containing Tag model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from . import BASE

# pylint: disable=too-few-public-methods
class NavItem(BASE):

    """
    NavItem class.

    Model for storing NavigationItems, these are used
    as storage-model for Bookmarks and NavigationHistory.

    Attributes:
      nav_hash       SHA1 Hash of
        route_name +
        route_matched +
        route_params
      route_name     The name of the pyramid route
      route_matched  JSON-encoded string of matched dict
      route_params   JSON-encoded string of parameters.

    """

    __tablename__ = 'nav_item'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    nav_hash = Column(Text, nullable=False)
    route_name = Column(Text, nullable=False)
    route_matched = Column(Text, nullable=False)
    route_params = Column(Text, nullable=False)

Index('u_nav_item_index',
    NavItem.nav_hash,
    NavItem.route_name,
    NavItem.route_matched,
    NavItem.route_params,
    unique=True)
