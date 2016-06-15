var ctx = null;
var overviewChart = null;

$(function() {

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
            $('#create-object-modal').modal('hide');
            host.get_host_overview({'complete_callback': get_host_complete_callback});
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

        $('#new-object-form').submit(function(event) {
            event.preventDefault();
            host.create({
                hostname : $('#host-name').val(),
                description : $('#host-description').val(),
                error : create_host_error
            })
        });
    }
});
