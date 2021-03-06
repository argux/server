var ctx = null;
var overviewChart = null;

$(function() {

    function get_host_groups_success_callback(json) {
        $('#objects').empty();
        $('#source-groups').empty();

        json.groups = json.groups.sort(function(a, b) {
            return a.name >= b.name
        });

        $.each(json.groups, function(i, value) {
            var okay = (value.total - value.warning - value.critical);

            if (value.total === 0) {
                okay_class = '';
                warning_class = '';
                critical_class = '';
            } else {
                if (okay > 0) {
                    okay_class = 'success';
                } else {
                    okay_class = '';
                }

                if (value.warning > 0) {
                    warning_class = 'warning';
                } else {
                    warning_class = 'success';
                }

                if (value.critical > 0) {
                    critical_class = 'danger';
                } else {
                    critical_class = 'success';
                }
            }

            $('#objects').append(
                '<tr><td>' +
                '<a href="'+ARGUX_BASE+'/hosts/groups/' + value.name + '">' +
                value.name +
                '</a></td>' + 
                '<td class="'+okay_class+'">' +
                okay +
                '</td><td class="'+warning_class+'">' +
                value.warning +
                '</td><td class="'+critical_class+'">' +
                value.critical +
                '</td></tr>'
            );

            /* Add all groups not named 'All' to the hostgroup list
             * for the new-host dialog.
             *
             * Hosts get added to 'All' automatically.
             */
            if (value.name !== 'All') {
                $('#source-groups').append(
                    $('<option></option>')
                        .attr('value', value.name)
                        .text(value.name));
            }
        });
    }

    function get_host_group_members_success_callback(json) {
        $('#source-hosts').empty();
        json.hosts = json.hosts.sort(function(a, b) {
            return a.name >= b.name
        });
        $.each(json.hosts, function(i, value) {
            $('#source-hosts').append(
                $('<option></option>')
                    .attr('value', value.name)
                    .text(value.name));
        });
    }

    function get_host_overview_success_callback(json) {
        var total_active_alerts = 0;
        var graph_data = [0,0,0,0];

        $('#objects').empty();

        // Sort by name - this is done here because we can't
        // trust that the order of the elements remains unaltered
        // throughout the AJAX chain.
        json.hosts = json.hosts.sort(function(a, b) {return a.name >= b.name});
        $.each(json.hosts, function(i, value) {
            $('#objects').append(
                '<tr><td>' +
                '<a href="'+ARGUX_BASE+'/host/' + value.name + '">' +
                value.name +
                '</a></td><td>' +
                '<a href="'+ARGUX_BASE+'/host/' + value.name + '/metrics">' +
                value.n_items +
                '</a></td><td>' +
                '<a href="'+ARGUX_BASE+'/host/' + value.name + '/alerts">' +
                value.active_alerts+
                '</a></td></tr>'
            );

            if (value.severity === 'crit') {
                graph_data[2] += 1;
            } else if (value.severity === 'warn') {
                graph_data[1] += 1;
            } else if (value.severity === 'info') {
                graph_data[3] += 1;
            } else {
                graph_data[0] += 1;
            }

            total_active_alerts+=value.active_alerts;
        });

        host_overview_chart_config.data.datasets[0].data = graph_data;

        // Set the label on the alert tab
        if (total_active_alerts > 0) {
            $("#alert_count").text(total_active_alerts);
        } else {
            $("#alert_count").text('');
        }

        overviewChart.update();
    };

    function create_host_error(xhr, ajaxOptions, thrownError) {
        if (xhr.status !== 201) {
            var sel = $('.modal-form-alerts');
            sel.empty();
            sel.append(
                '<div class="alert alert-danger alert-dismissible">'+
                '<strong>Problem:</strong> ' + xhr.responseJSON.message
            );
        } else {
            $('#create-host-modal').modal('hide');
            $('#create-hostgroup-modal').modal('hide');
            host.get_groups({
                success : get_host_groups_success_callback
            });
        }
    }

    function get_host_overview_complete_callback() {
        setTimeout(
            host.get_host_overview,
            10000, {
                success : get_host_overview_success_callback,
                complete : get_host_overview_complete_callback
            }
        );
    }

    if (ARGUX_ACTION==='overview') {
        ctx = document.getElementById("overview").getContext("2d");
        overviewChart = new Chart(ctx, host_overview_chart_config);

        host.get_host_overview({
            success : get_host_overview_success_callback,
            complete : get_host_overview_complete_callback
        });
    }

    if (ARGUX_ACTION==='groups') {
        host.get_groups({
            success : get_host_groups_success_callback
        });
        host.get_group_members({
            group: 'All',
            success: get_host_group_members_success_callback
        });

        /* Host dialog */
        $('#add-group').click(function(event) {
            event.preventDefault();
            $('#source-groups option:selected').each(function() {
                $('#dst-groups').append(this);
            });
        });
        $('#remove-group').click(function(event) {
            event.preventDefault();
            $('#dst-groups option:selected').each(function() {
                $('#source-groups').append(this);
            });
        });

        $('#new-host-form').submit(function(event) {
            event.preventDefault();
            groups = []
            $('#dst-groups option:selected').each(function() {
                groups.push(this.value)

            });
            host.create_host({
                hostname : $('#host-name').val(),
                description : $('#host-description').val(),
                groups : groups,
                error : create_host_error
            })
        });

        /* Hostgroup dialog */
        $('#add-host').click(function(event) {
            event.preventDefault();
            $('#source-hosts option:selected').each(function() {
                $('#dst-hosts').append(this);
            });
        });
        $('#remove-host').click(function(event) {
            event.preventDefault();
            $('#dst-hosts option:selected').each(function() {
                $('#source-hosts').append(this);
            });
        });

        $('#new-hostgroup-form').submit(function(event) {
            event.preventDefault();
            hosts = []
            $('#dst-hosts option:selected').each(function() {
                hosts.push(this.value)
            });

            host.create_group({
                group : $('#hostgroup-name').val(),
                hosts : hosts,
                error : create_host_error
            })
        });

    }
});
