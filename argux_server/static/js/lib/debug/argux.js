var argux = {
    VERSION: "0.0.1"
};

rest = {
    CallType : {
        CREATE : "POST",
        READ : "GET",
        UPDATE : "POST",
        DELETE: "DELETE"
    },
    call: function (args) {
        if(args.type === undefined) {
            args.type = rest.CallType.READ;
        }
        if(args.success === undefined) {
            args.success = function(json){};
        }
        if(args.error === undefined) {
            args.error = function(json){};
        }
        if(args.complete === undefined) {
            args.complete = function(){};
        }
        if(args.data === undefined) {
            args.data = '';
        }

        $.ajax({
            url: args.url,
            type: args.type,
            headers: { 'X-CSRF-Token': CSRF_TOKEN },
            dataType: "json",
            data: JSON.stringify(args.data),
            success: function(json) {
                args.success(json);
            },
            error: function(a, b, c) {
                args.error(a, b, c);
            },
            complete: function() {
                args.complete();
            }
        });
    }
};


var unit = {};

var history_chart_config = {
    type: 'line',
    data: {
        datasets: [
        ]
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
                type: "time",
                display: true,
                time: {
                    format: 'YYYY-MM-DDTHH:mm:SS',
                    displayFormats: {
                        'millisecond': 'SSS [ms]',
                        'second': 'HH:mm:ss', // 23:20:01
                        'minute': 'MM/DD HH:mm', // 23:20:01
                        'hour': 'YY/MM/DD HH:00', // 2015/12/22 23:00
                        'day': 'YY/MM/DD', // 2015/12/22
                        'month': 'MMM YYYY', // Sept 2015
                        'quarter': '[Q]Q - YYYY', // Q3 - 2015
                        'year': 'YYYY' // 2015
                    }
                },
                scaleLabel: {
                    show: true,
                    labelString: 'Date/Time'
                }
            }],
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,
                    suggestedMin: 0.0,
                    suggestedMax: 1.0,
                    callback: function(value) {
                        if(unit.symbol){
                            return ''+Math.round(value*10)/10+' '+item_unit_prefix+unit.symbol;
                        } else {
                            return ''+Math.round(value*10)/10;
                        }
                    }
                },
                scaleLabel: {
                    show: true
                }
            }]
        },
        elements: {
            line: {
                tension: 0.0
            },
            point: {
                radius: 1
            }
        }
    }
};

var host_overview_chart_config = {
    type: 'doughnut',
    data: {
        datasets: [
            {
                data: [
                    0,
                    0,
                    0,
                    1 ],
                backgroundColor: [
                    "#419641",
                    "#f0ad4e",
                    "#c12e2a",
                    "#e0e0e0"]
            }
        ],
        labels: [
            "Okay",
            "Warning",
            "Critical",
            "Unknown"
            ]
    },
    options: {
        responsive: true,
        legend: {
            display: false
        }
    }
};

host = {
    get_host_overview: function(args) {
        if (args.complete_callback === undefined) {
            args.complete_callback = function(){};
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host',
            success : host._get_host_overview_success,
            error : host._get_host_overview_error,
            complete : args.complete_callback
        });
    },
    _get_host_overview_success: function(json) {
        var total_active_alerts = 0;
        var graph_data = [0,0,0,0];

        $('#hosts').empty();

        // Sort by name - this is done here because we can't
        // trust that the order of the elements remains unaltered
        // throughout the AJAX chain.
        json.hosts = json.hosts.sort(function(a, b) {return a.name >= b.name});
        $.each(json.hosts, function(i, value) {
            $('#hosts').append(
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
    },
    _get_host_overview_error: function(json) {
    },
    create: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        if (args.description === undefined) {
            description = '';
        } else {
            description = args.description;
        }
        if (args.addresses === undefined) {
            addresses = []
        } else {
            addresses = args.addresses;
        }

        data = {
            "description": description,
            "address": addresses
        };

        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+args.hostname,
            type : rest.CallType.CREATE,
            data : data,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_addresses: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        if (args.callback_success === undefined) {
            throw "callback_success missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+args.hostname+'/addr',
            success: args.callback_success
        });
    }
};

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

user = {

};

function update_chart (obj, chart, config) {
    var chart_id = obj.data('graphid');

    rest.call({
        url: ARGUX_BASE + 
             "/rest/1.0/graph/" +
             chart_id +
             "?get_values=true",
        dataType: "json",
        success: function(json) {
            obj.children(".heading").children(".title").text(json.name);
            config.data.datasets = [];

            // Set data for each item separately.
            $.each(json.items, function(i, item) {
                var dataset = {
                    label: item.name,
                    borderWidth: 1,
                    borderColor: "rgba(10,145,115,1)",
                    backgroundColor: "rgba(10,200,160,0.2)",
                    pointHoverRadius: 4,
                    data: [{'x': '0', 'y': '1'}]
                };
                var datapoints = [];

                $.each(item.values.avg, function(i, value) {
                    datapoints.push({
                        x: value.ts,
                        y: value.value});
                });

                dataset.data = datapoints;

                config.data.datasets.push(dataset)
            });
            chart.update();
        },
        complete: function() {
            setTimeout(
                update_chart,
                10000,
                obj,
                chart,
                config);
        }
    });
}

$(function() {
    $('.argux-chart').each(function (index) {
        var obj = $(this);

        var chart_obj  = obj.children('.chart-body');
        var canvas = $('<canvas/>');
        chart_obj.append(canvas);
        var ctx = canvas[0].getContext("2d");

        // Create a copy of the history_chart_config so we can use
        // a different configuration for each chart.
        var config = $.extend(true, {}, history_chart_config);
        var chart = new Chart(ctx, config);

        update_chart (obj, chart, config);
    });
});
