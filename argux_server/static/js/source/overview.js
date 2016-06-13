var ctx = null;
var overviewChart = null;

$(function() {
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
            host.get_host_overview({'complete_callback': get_host_complete_callback});
        }
    }

    function get_host_complete_callback() {
        overviewChart.update();
    }

    function poll_hosts_callback() {
        get_host_complete_callback();
        setTimeout(host.get_host_overview, 10000, {'complete_callback' : poll_hosts_callback});
    }

    if (ARGUX_ACTION==='overview') {
        ctx = document.getElementById("overview").getContext("2d");
        overviewChart = new Chart(ctx, host_overview_chart_config);

        host.get_host_overview({'complete_callback': poll_hosts_callback});

        $('#host-form').submit(function(event) {
            event.preventDefault();
            host.create({
                hostname : $('#host-name').val(),
                description : $('#host-description').val(),
                error : create_host_error
            })
        });
    }
});
