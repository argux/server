"""RestView for DNSMonitorDomains."""

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

from argux_server.monitors import MONITORS

@view_defaults(renderer='json')
class RestDNSMonitorDomainViews(RestView):

    """RestMonitor View.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_dns_monitor_domain_1',
        request_method='POST',
        require_csrf=True,
        permission='view'
    )
    def dns_domain_1_view_create(self):
        host_name = self.request.matchdict['host']
        address = self.request.matchdict['address'].lower()
        domain = self.request.matchdict['domain'].lower()

        try:
            types = self.request.json_body.get('types', {})
        except ValueError:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'missing types'
                }))

        for _type in types:
            if not _type in ['A','AAAA','MX']:
                raise HTTPBadRequest(
                    body=json.dumps({
                        'error': '400 Bad Request',
                        'message': 'bad type provided'
                    }))

        self.dao.monitor_dao.set_domain(
            host_name,
            address,
            'DNS',
            domain)

        return {'ok':'ok'}

    @view_config(
        route_name='rest_dns_monitor_domain_1',
        request_method='DELETE',
        require_csrf=True,
        permission='view'
    )
    def dns_domain_1_view_delete(self):
        host_name = self.request.matchdict['host']
        address = self.request.matchdict['address'].lower()
        domain = self.request.matchdict['domain'].lower()

        self.dao.monitor_dao.remove_domain(
            host_name,
            address,
            'DNS',
            domain)

        return {'ok': 'ok'}

    @view_config(
        route_name='rest_dns_monitor_domains_1',
        request_method='GET',
        require_csrf=True,
        permission='view'
    )
    def dns_domains_1_view_get(self):
        hostname = self.request.matchdict['host']
        address = self.request.matchdict['address'].lower()
        domains = []

        d_domains = self.dao.monitor_dao.get_domains(
            hostname,
            address,
            'DNS')

        if d_domains:
            for domain in d_domains:
                domains.append({
                    'domain': domain.domain,
                    'record_a': domain.record_a,
                    'record_aaaa': domain.record_aaaa,
                    'record_mx': domain.record_mx
                })

        return {
            'domains': domains
        }
