"""RestView for Host Addresses."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

from . import RestView


@view_defaults(renderer='json')
class RestHostAddressViews(RestView):

    """RestHostAddress View.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_host_address_1',
        request_method='POST',
        require_csrf=True,
        permission='view'
    )
    def host_address_1_view_create(self):
        host_name = self.request.matchdict['host']
        address = self.request.matchdict['address']

        description = ""
        try:
            description = self.request.json_body.get('description', '')
        except ValueError:
            description = ""

        host = self.dao.host_dao.get_host_by_name(name=host_name)
        if host is None:
            return 'host-not-found'

        try:
            self.dao.host_dao.add_address(host, address, description)
            return {}
        except Exception as e:
            return str(e)

    @view_config(
        route_name='rest_host_addresses_1',
        request_method='GET',
        require_csrf=True,
        permission='view'
    )
    def host_addresses_1_view_get(self):
        host_name = self.request.matchdict['host']
        addresses = []

        host = self.dao.host_dao.get_host_by_name(name=host_name)
        if host is None:
            return 'host-not-found'

        d_addr = self.dao.host_dao.get_addresses(host)
        for addr in d_addr:
            addresses.append({'name': addr.name, 'description': addr.description})

        return {
            "addresses": addresses
        }
