"""RestView for Host Groups."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

from . import RestView


@view_defaults(
    renderer='json',
    require_csrf=True,
)
class RestHostGroupViews(RestView):

    """RestHostGroupView.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_host_group_1',
        request_method='POST',
        permission='view'
    )
    def host_group_1_view_create(self):
        group_name = self.request.matchdict['group']

        try:
            description = self.request.json_body.get('description', '')
        except ValueError:
            description = ""

        group = self.dao.host_dao.create_hostgroup(name=group_name, description=description)

        return Response(
            status='201 Created',
            content_type='application/json')

    @view_config(
        route_name='rest_host_group_1',
        request_method='GET',
        permission='view'
    )
    def host_group_1_view_get(self):
        group_name = self.request.matchdict['group']
        hosts = []

        group = self.dao.host_dao.get_hostgroup_by_name(name=group_name)
        if group is None:
            return 'host-not-found'

        for host in group.hosts:
            hosts.append(host.name)

        return {
            "name": group_name,
            "hosts": hosts
        }

    @view_config(
        route_name='rest_host_groups_1',
        request_method='GET',
        permission='view'
    )
    def host_groups_1_view_get(self):

        d_groups = self.dao.host_dao.get_all_hostgroups()

        groups = []
        for group in d_groups:
            groups.append({
                "name": group.name
            })

        return {"groups": groups}
