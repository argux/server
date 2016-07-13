"""Data Access Object class for handling Graphs."""

import hashlib
import json
import transaction

from binascii import hexlify

from sqlalchemy.exc import IntegrityError

from argux_server.models import (
    NavItem,
)

from sqlalchemy.orm import (
    joinedload
)

from .BaseDAO import BaseDAO


class NavDAO(BaseDAO):

    """NavDAO Class."""

    def add_nav_item_for_request(self, route_name, request, title):
        serialised_route_name = route_name

        serialised_matched_dict = \
            json.dumps(
                request.matchdict
            )

        nav_hash = hashlib.sha1()
        nav_hash.update(serialised_route_name.encode('utf-8'))
        nav_hash.update(serialised_matched_dict.encode('utf-8'))
        nav_hash.update(''.encode('utf-8'))

        hex_nav_hash = str(
            hexlify(nav_hash.digest()),
            'utf-8')

        try:
            item = NavItem(
                nav_hash=hex_nav_hash,
                route_name=serialised_route_name,
                route_matched=serialised_matched_dict,
                route_params='{}',
                title=title)

            self.db_session.add(item)
            self.db_session.flush()

        except IntegrityError as err:
            self.db_session.rollback()
            item = self.db_session.query(NavItem)\
                .filter(NavItem.route_name == serialised_route_name)\
                .filter(NavItem.route_matched == serialised_matched_dict)\
                .filter(NavItem.route_params == '{}')\
                .first()

        return item

    def lookup_nav_item(self, nav_hash):
        item = self.db_session.query(NavItem)\
            .filter(NavItem.nav_hash == nav_hash)\
            .first()

        return item
