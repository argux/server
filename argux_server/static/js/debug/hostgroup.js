var group_hosts;

$(function() {

    function get_group_alerts_success_callback(json) {
        if (VIEW_SORT === "desc") {
            group_hosts = json.hosts.sort(function(a, b) {return a.name < b.name});
        } else {
            group_hosts = json.hosts.sort(function(a, b) {return a.name >= b.name});
        }

        update_alerts_view();
    }

    function update_alerts_view() {
        active_alert_count = 0;
        var alert_list = $('#alert-list');
        alert_list.empty();
        alert_list.append(
            '<div class="col-xs-12">' +
            '<div class="panel panel-default">' +
            '<table class="table table-striped">' +
            '<thead>' +
            '<tr><th>Host</th><th>Alert</th><th>Duration</th><th>Acknowledged</th></tr>' +
            '</thead>' +
            '<tbody id="alert-list-body">' +
            '</tbody>' +
            '</table>' +
            '</div>' +
            '</div>'
        );

        alert_list = $('#alert-list-body');

        $.each(group_hosts, function(i, host) {
            active_alert_count+=host.active_alerts;
            $.each(host.alerts, function (i, host_alert) {
                if(host_alert.severity === 'info') {
                    icon = 'glyphicon-none';
                    severity = 'info';
                } else {
                    if (host_alert.severity === "crit") {
                        severity = "danger";
                    }
                    if (host_alert.severity === "warn") {
                        severity = "warning";
                    }
                    icon = 'glyphicon-exclamation-sign';
                }
                if(host_alert.acknowledgement === null) {
                    ack = 'No (<a href="#">Acknowledge</a>)';
                } else {
                    ack = 'Yes (<a href="#">Show Ack</a>)';
                }
                alert_list.append(
                    '<tr class="'+severity+'">' +
                    '<td>'+
                    host.name +
                    '</td>' +
                    '<td>'+host_alert.name+'</td>' +
                    '<td>'+
                    moment(host_alert.start_time).fromNow(true) +
                    '</td><td>' +
                    ack +
                    '</td>' +
                    '</tr>'
                );
            });
        });

        if (active_alert_count > 0) {
            $("#alert_count").text(active_alert_count);
        } else {
            $("#alert_count").text('');
        }

    }

    function get_group_members_success_callback(json) {
        if (VIEW_SORT === "desc") {
            group_hosts = json.hosts.sort(function(a, b) {return a.name < b.name});
        } else {
            group_hosts = json.hosts.sort(function(a, b) {return a.name >= b.name});
        }

        update_hosts_view();
    }

    function update_hosts_view() {
        var host_list = $('#host-list');
        var active_alert_count = 0;

        host_list.empty();
        if (VIEW_TYPE === 'list') {
            host_list.append(
                '<div class="col-xs-12">' +
                '<div class="panel panel-default">' +
                '<table class="table table-striped">' +
                '<thead>' +
                '<tr><th>Host</th><th>Items</th><th>Alerts</th></tr>' +
                '</thead>' +
                '<tbody id="host-list-body">' +
                '</tbody>' +
                '</table>' +
                '</div>' +
                '</div>'
            );
            host_list = $('#host-list-body');
        }

        $.each(group_hosts, function(i, value) {
            var panel_class;
            var severity;
            switch(value.severity) {
                case 'warn':
                    panel_class = 'panel panel-warning'; 
                    severity = 'warning';
                    break;
                case 'crit':
                    panel_class = 'panel panel-danger'; 
                    severity = 'danger';
                    break;
                default:
                    panel_class = 'panel panel-default'; 
                    severity = '';
                    break;
            }
            switch(VIEW_TYPE) {
                case 'grid':
                    host_list.append(
                        '<div class="col-xs-12 col-sm-4 col-md-3 col-lg-2">' +
                        '<a class="host" href="/host/'+value.name+'">' +
                        '<div class="'+panel_class+'">' +
                        '<div class="panel-heading active">' + value.name + '</div>' +
                        '<div class="panel-body">' +
                        '<ul>' +
                        '<li>Items: '+value.n_items+'</li>' +
                        '<li>Alerts: '+value.active_alerts+'</li>' +
                        '</ul>' +
                        '</div>' +
                        '</div>' +
                        '</a>' +
                        '</div>'
                    );
                    break;
                case 'list':
                    host_list.append(
                        '<tr class="'+severity+'">' +
                        '<td>'+
                        '<a class="host" href="/host/'+value.name+'">' +
                        value.name +
                        '</a>' +
                        '</td>' +
                        '<td>'+value.n_items+'</td>' +
                        '<td>'+value.active_alerts+'</td>' +
                        '</tr>'
                    );
                    break;
            }
            active_alert_count+=value.active_alerts;
        });

        if (active_alert_count > 0) {
            $("#alert_count").text(active_alert_count);
        } else {
            $("#alert_count").text('');
        }

    }

    if (ACTION === "hosts") {
        host.get_group_members({
            group : HOST_GROUP,
            success : get_group_members_success_callback
        });

        $('.hostlist-view').click(function(e) {
            VIEW_TYPE = $(this).data('view');
            if (VIEW_TYPE === "list") {
                $('.hostlist-view-list').addClass('active');
                $('.hostlist-view-grid').removeClass('active');
            } else {
                $('.hostlist-view-grid').addClass('active');
                $('.hostlist-view-list').removeClass('active');
            }
            update_hosts_view();
        });

        $('.hostlist-sort').click(function(e) {
            VIEW_SORT = $(this).data('direction');
            if (VIEW_SORT === "desc") {
                group_hosts = group_hosts.sort(function(a, b) {return a.name < b.name});
                $('.hostlist-sort-desc').addClass('active');
                $('.hostlist-sort-asc').removeClass('active');
            } else {
                group_hosts = group_hosts.sort(function(a, b) {return a.name >= b.name});
                $('.hostlist-sort-asc').addClass('active');
                $('.hostlist-sort-desc').removeClass('active');
            }
            update_hosts_view();
        });
    }
    if (ACTION === "alerts") {
        host.get_group_alerts({
            group : HOST_GROUP,
            success : get_group_alerts_success_callback
        });
    }
});
