monitors = {
    get_monitors: function (args) {
        if (args.complete_callback === undefined) {
            args.complete_callback = function(){};
        }
        rest.call({
            url : ARGUX_BASE + '/rest/1.0/monitor/' + args.type,
            success : monitors._get_monitors_success,
            complete: args.complete_callback
        });
    },
    _get_monitors_success: function(json) {
        $('#monitors').empty();
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
            $('#monitors').append(
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
                    type : rest.CallType.UPDATE,
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
                    type : rest.CallType.UPDATE,
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

    },
    remove: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        if (args.address === undefined) {
            throw "address argument missing";
        }

        rest.call({
            url : ARGUX_BASE+'/rest/1.0/monitor/'+ARGUX_MONITOR_TYPE+'/'+args.hostname+'/'+args.address,
            type : rest.CallType.DELETE
        });
    },
    create: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        if (args.address === undefined) {
            throw "address argument missing";
        }
        if (args.options === undefined) {
            args.options = {}
        }
        if (args.active === undefined) {
            args.active = true
        }

        data = {
            "options": args.options,
            "active": args.active
        };

        rest.call({
            url : ARGUX_BASE+'/rest/1.0/monitor/'+ARGUX_MONITOR_TYPE+'/'+args.hostname+'/'+args.address,
            type : rest.CallType.CREATE,
            data : data,
            success : monitors._create_success,
            error : monitors._create_error
        });
    },
    _create_error: function(json) {
    },
    _create_success: function(json) {
    }
};
