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
            sev_label = 'unknown'
            n_items = self.dao.item_dao.get_item_count_from_host(host)
            severity = self.dao.get_host_severity(host)
            if (severity):
                sev_label = severity.key

            hosts.append({
                "name": host.name,
                "n_items": n_items,
                "severity": sev_label,
                "active_alerts": self.dao.get_active_alert_count(host)
            })

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
            critical = 0
            warning = 0
            for host in group.hosts:
                severity = self.dao.get_host_severity(host)
                if severity:
                    if severity.key == 'warn':
                        warning=warning+1
                    if severity.key == 'crit':
                        critical=critical+1

            groups.append({
                "name": group.name,
                "critical": critical,
                "warning": warning,
                "total": len(group.hosts)
            })

        return {"groups": groups}
