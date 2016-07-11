var group_hosts;

$(function() {
    function get_group_members_success_callback(json) {
        if (VIEW_SORT === "desc") {
            group_hosts = json.hosts.sort(function(a, b) {return a.name < b.name});
        } else {
            group_hosts = json.hosts.sort(function(a, b) {return a.name >= b.name});
        }

        update_view();
    }

    function update_view() {
        var host_list = $('#host-list');
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
        });
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
            update_view();
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
            update_view();
        });
    }
});
