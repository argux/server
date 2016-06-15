$(function() {
    function update_complete_callback() {
        setTimeout(
            monitors.get_monitors,
            60000,
            {
                'complete_callback' : update_complete_callback,
                'type': ARGUX_MONITOR_TYPE
            }
        );
    }

    function get_address_success_callback(json) {
        $('#monitor-address').empty();
        if(json.addresses.length == 0) {
            $('#monitor-address').append(
                '<option disabled>No addresses</option>');
        } else {
            $.each(json.addresses, function(i, address) {
                if (address.description != '') {
                    $('#monitor-address').append(
                        '<option value="'+address.name+'">'+
                        address.name+' ('+address.description+')'+
                        '</option>');
                } else {
                    $('#monitor-address').append(
                        '<option value="'+address.name+'">'+
                        address.name +
                        '</option>');
                }
            });
        }

    }

    var hostname = $('#monitor-host').val();

// Initialisation
    monitors.get_monitors({
        'complete_callback': update_complete_callback,
        'type': ARGUX_MONITOR_TYPE
    });

    host.get_addresses({
        'hostname': hostname,
        'callback_success': get_address_success_callback
    });

// Forms
    $('#new-object-form').submit(function(event) {
        var running = $('#monitor-running').is(':checked');
        monitors.create({
            'hostname': $('#monitor-host').val(),
            'address': $('#monitor-address').val(),
            'active': running,
            'options': {
                'interval': $('#monitor-interval').val(),
            }
        })
        $('#create-monitor-modal').modal('hide');
        monitors.get_monitors({'type': ARGUX_MONITOR_TYPE});
    });
    $('#monitor-delete-form').submit(function(event) {
        monitors.remove({
            'hostname': $('#dmcm-hostname').val(),
            'address': $('#dmcm-address').val()
        });
        $('#dmcm').modal('hide');
        monitors.get_monitors({'type': ARGUX_MONITOR_TYPE});
    });

    $('#monitor-host').on('change', function(e) {
        host.get_addresses({
            'hostname': this.value,
            'callback_success': get_address_success_callback
        });
    });
});
