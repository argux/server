$(function() {

    function update_success_callback (json) {
        $('#objects').empty();
        $.each(json.monitors, function(i, monitor) { options = '';
            $.each(monitor.options, function(key, value) {
                options+= '<li><span style="font-weight: bold">'+key+':</span> '+value+'</li>';
            });
            if (monitor.active) {
                button = '<span class="glyphicon glyphicon-pause"></span>';
                state = 'running';
                klass = '';
            } else {
                button = '<span class="glyphicon glyphicon-play"></span>';
                state = 'paused';
                klass = 'pause';
            }
            $('#objects').append(
                '<tr class="'+klass+'" ' +
                'data-hostname="' + monitor.host +'" ' +
                'data-address="' + monitor.address +'" ' +
                '>' +
                '<td>' +
                '<a href="#" class="monitor-play-btn">' +
                button +
                '</a>' +
                '<a href="'+ARGUX_BASE+'/monitor/'+ARGUX_MONITOR_TYPE+'/'+monitor.host+'/'+monitor.address+'/edit">' +
                monitor.host +
                ' (' + monitor.address + ')' +
                '</a>' +
                '</td><td>' +
                '<ul>' +
                options + 
                '</ul>' +
                '</td>' +
                '<td class="state">' +
                state +
                '</td>' + 
                '<td>' +
                '<div class="pull-right">' +
                '<a href="#" class="monitor-remove"><span class="glyphicon glyphicon-trash"></span></a>' +
                '</div>' +
                '</td>' +
                '</tr>'
            );
        });

        $('.monitor-play-btn').click(function() {
            var button = $(this);
            var par = button.parents('tr');
            var hostname = par.data('hostname');
            var address = par.data('address');
            var state = par.children('td.state');
            var paused = par.hasClass('pause');

            data = {
                "options" : {"interval": 60}
            };

            if (paused === true) {
                data['active'] = "true";
                rest.call({
                    url : ARGUX_BASE+'/rest/1.0/monitor/'+ARGUX_MONITOR_TYPE+'/'+hostname+'/'+address,
                    type : rest.CallType.CREATE, /* Replace */
                    data : data,
                    success : function() {
                        par.removeClass('pause');
                        button.children().removeClass('glyphicon-play');
                        button.children().addClass('glyphicon-pause');
                        state.text('running');
                    }
                });
            } else {
                data['active'] = "false";
                rest.call({
                    url : ARGUX_BASE+'/rest/1.0/monitor/'+ARGUX_MONITOR_TYPE+'/'+hostname+'/'+address,
                    type : rest.CallType.CREATE, /* Replace */
                    data : data,
                    success : function() {
                        par.addClass('pause');
                        button.children().addClass('glyphicon-play');
                        button.children().removeClass('glyphicon-pause');
                        state.text('paused');
                    }
                });
            }

        });

        $('.monitor-remove').click(function() {
            var hostname = $(this).parents('tr').data('hostname');
            var address = $(this).parents('tr').data('address');

            $('#dmcm-hostname').val(hostname);
            $('#dmcm-address').val(address);
            $('#dmcm-message').text(
                'Do you want to remove the ' +
                ARGUX_MONITOR_TYPE +
                ' monitor for ' +
                hostname + 
                ' on ' +
                address);
            $('#dmcm').modal('show');

        });

    }

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
        complete : update_complete_callback,
        success : update_success_callback,
        type : ARGUX_MONITOR_TYPE
    });

    host.get_addresses({
        hostname : hostname,
        success : get_address_success_callback
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
            hostname : this.value,
            success : get_address_success_callback
        });
    });
});
