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
                button = 
                '<a class="monitor-play-btn pause">' +
                '<span class="glyphicon glyphicon-pause"></span>' +
                '</a> ';
                status = 'running';
            } else {
                button =
                '<a href="#" class="monitor-play-btn">' +
                '<span class="glyphicon glyphicon-play"></span>' +
                '</a> ';
                status = 'paused';
            }
            $('#monitors').append(
                '<tr class="" ' +
                'data-hostname="' + monitor.host +'" ' +
                'data-address="' + monitor.address +'" ' +
                '>' +
                '<td>' +
                button +
                '<a href="'+ARGUX_BASE+'/monitor/'+ARGUX_MONITOR_TYPE+'/'+monitor.host+'/'+monitor.address+'/edit">' +
                monitor.host +
                ' (' + monitor.address + ')' +
                '</a>' +
                '</td><td>' +
                '<ul>' +
                options + 
                '</ul>' +
                '</td>' +
                '<td>' +
                '<div class="pull-right">' +
                '<a href="#" class="monitor-remove"><span class="glyphicon glyphicon-trash"></span></a>' +
                '</div>' +
                '</td>' +
                '<td>' +
                status +
                '</td>' + 
                '</tr>'
            );
        });

        $('.monitor-play-btn').click(function() {
            var hostname = $(this).parents('tr').data('hostname');
            var address = $(this).parents('tr').data('address');
            var button = $(this);

            data = {
                "active": "true",
                "options" : {"interval": 60}
            };

            rest.call({
                url : ARGUX_BASE+'/rest/1.0/monitor/'+ARGUX_MONITOR_TYPE+'/'+hostname+'/'+address,
                type : rest.CallType.UPDATE,
                data : data,
                success : function() {
                    button.addClass('pause');
                    button.children().removeClass('glyphicon-play');
                    button.children().addClass('glyphicon-pause');
                }
            });
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

        $('.monitor-play-btn.pause').click(function() {
            var hostname = $(this).parents('tr').data('hostname');
            var address = $(this).parents('tr').data('address');
            var button = $(this);

            data = {
                "active": "false",
                "options" : {"interval": 60}
            };

            rest.call({
                url : ARGUX_BASE+'/rest/1.0/monitor/'+ARGUX_MONITOR_TYPE+'/'+hostname+'/'+address,
                type : rest.CallType.UPDATE,
                data : data,
                success : function() {
                    button.removeClass('pause');
                    button.children().removeClass('glyphicon-pause');
                    button.children().addClass('glyphicon-play');
                }
            });
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

        data = {
            "options": args.options
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
