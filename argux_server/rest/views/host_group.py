"""RestView for Host Groups."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

import html

from . import RestView

from argux_server.util import (
    TIME_OFFSET_EXPR,
    DATE_FMT
)


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
        route_name='rest_host_group_default_1',
        request_method='POST',
        permission='view'
    )
    def host_group_1_view_create(self):
        group_name = self.request.matchdict['group']

        try:
            description = self.request.json_body.get('description', '')
        except ValueError:
            description = ""

        try:
            hosts = self.request.json_body.get('hosts', [])
        except ValueError:
            hosts = ""

        # Escape HTML
        group_name = html.escape(group_name)
        description = html.escape(description)

        group = self.dao.host_dao.create_hostgroup(
            name=group_name,
            description=description)

        for host_name in hosts:
            host = self.dao.host_dao.get_host_by_name(name=host_name)
            if host:
                self.dao.host_dao.add_host_to_group(group_name, host)

        return Response(
            status='201 Created',
            content_type='application/json')

    @view_config(
        route_name='rest_host_group_default_1',
        request_method='GET',
        permission='view'
    )
    def host_group_default_1_view_get(self):
        self.request.matchdict['action'] = 'hosts'

        return self.host_group_1_view_get()

    @view_config(
        route_name='rest_host_group_1',
        request_method='GET',
        permission='view'
    )
    def host_group_1_view_get(self):
        group_name = self.request.matchdict['group']
        action = self.request.matchdict['action']
        hosts = []
        n_alerts = 0

        group = self.dao.host_dao.get_hostgroup_by_name(name=group_name)
        if group is None:
            return 'group-not-found'

        for host in group.hosts:
            host_alerts = []
            sev_label = 'unknown'
            n_items = self.dao.item_dao.get_item_count_from_host(host)
            n_alerts += self.dao.get_active_alert_count(host)
            severity = self.dao.get_host_severity(host)
            if (severity):
                sev_label = severity.key

            if action == 'alerts':
                for item in host.items:
                    alerts = self.dao.item_dao.get_alerts(item)
                    for alert in alerts:
                        host_alerts.append({
                            'start_time': alert.start_time.strftime(DATE_FMT),
                            'severity': alert.trigger.severity.key,
                            'acknowledgement': alert.acknowledgement,
                            'name': alert.trigger.name,
                            'item': {
                                'key': alert.trigger.item.key,
                                'name': alert.trigger.item.name
                            }
                        })

            hosts.append({
                "name": host.name,
                "n_items": n_items,
                "severity": sev_label,
                "alerts": host_alerts,
                "active_alerts": self.dao.get_active_alert_count(host)
            })

        return {
            "name": group_name,
            "hosts": hosts,
            "active_alerts": n_alerts
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
