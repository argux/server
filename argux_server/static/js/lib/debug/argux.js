var argux = {
    VERSION: "0.0.1"
};

rest = {
    CallType : {
        CREATE : "POST",
        READ : "GET",
        UPDATE : "PATCH",
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

var ARGUX_TIMEFRAME_START;
var ARGUX_TIMEFRAME_END;
var ARGUX_TIMEFRAME_INTERVAL = 60;

var unit = {};

var palette = [
    "#ff0000",
    "#00ff00",
    "#0000ff",
];

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
                        return ''+Math.round(value*10)/10;
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

function hex2rgba(color, opacity) {
    color = color.replace('#','');

    r = parseInt(color.substring(0,2), 16);
    g = parseInt(color.substring(2,4), 16);
    b = parseInt(color.substring(4,6), 16);

    return 'rgba('+r+','+g+','+b+','+opacity+')';
}

function get_palette_color(counter) {

    if(counter >= palette.length) {
        counter = 0;
    }

    color = palette[counter];

    counter++;

    return [color, counter];
}

$(function() {
    var auto_time = false;

    /* Use YYYY/MMM/DD HH:mm, (example: 2016/Jan/12 23:12)
     *
     * This way we won't have any confusion about those silly
     * date/time formats used in the US.
     */
    $('#timeframe-start').datetimepicker({
        format: 'YYYY/MMM/DD HH:mm',
        useCurrent: false, //Important! See issue #1075
        sideBySide: true
    });
    $('#timeframe-end').datetimepicker({
        format: 'YYYY/MMM/DD HH:mm',
        sideBySide: true
    });

    $('#timeframe-start').on("dp.change", function(e) {
        $('#timeframe-end').data("DateTimePicker").minDate(e.date);
        ARGUX_TIMEFRAME_START = e.date.format('YYYY-MM-DDTHH:mm:ss');

        $('#timeframe-window').trigger('timeframe:change');

        if(auto_time === false) {
            $('#timeframe-window').val('custom').change();
        }
    });
    $('#timeframe-end').on("dp.change", function(e) {
        $('#timeframe-start').data("DateTimePicker").maxDate(e.date);
        ARGUX_TIMEFRAME_END = e.date.format('YYYY-MM-DDTHH:mm:ss');

        $('#timeframe-window').trigger('timeframe:change');

        if(auto_time === false) {
            $('#timeframe-window').val('custom').change();
        }
    });


    $('#timeframe-window').change(function(event) {
        var real_end_time = moment();
        var end_time = moment();
        var start_time;
        switch($(this).val()) {
            case '60m':
                start_time = end_time.subtract(60, 'minutes');
                ARGUX_TIMEFRAME_INTERVAL = 60;
                break;
            case '6h':
                start_time = end_time.subtract(6, 'hours');
                ARGUX_TIMEFRAME_INTERVAL = 120;
                break;
            case '12h':
                start_time = end_time.subtract(12, 'hours');
                ARGUX_TIMEFRAME_INTERVAL = 300;
                break;
            case '24h':
                start_time = end_time.subtract(24, 'hours');
                ARGUX_TIMEFRAME_INTERVAL = 600;
                break;
            case '7d':
                start_time = end_time.subtract(7, 'days');
                ARGUX_TIMEFRAME_INTERVAL = 3600;
                break;
            case '1M':
                start_time = end_time.subtract(1, 'months');
                ARGUX_TIMEFRAME_INTERVAL = 14400;
                break;
            case 'custom':
                break;
            default:
                alert('invalid timeframe');
        }
        if($(this).val() !== 'custom') {
            auto_time = true;
            $('#timeframe-end').data("DateTimePicker").maxDate(moment());
            $('#timeframe-start').data("DateTimePicker").date(start_time);
            $('#timeframe-end').data("DateTimePicker").date(real_end_time);
            auto_time = false;
        }
        return;
    });

    // Set default value to 60 minutes
    $('#timeframe-window').val('60m').change();
});

host = {
    get_host_overview: function(args) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_host_items: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+args.hostname+'?alerts=false&items=true',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_host_alerts: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+args.hostname+'?alerts=true&items=false',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
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
        if (args.groups === undefined) {
            groups = []
        } else {
            groups = args.groups;
        }

        data = {
            "description": description,
            "groups": groups,
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
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+args.hostname+'/addr',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_groups: function(args) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/hostgroup',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_group_members: function(args) {
        if (args.group === undefined) {
            throw "group argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/hostgroup/'+args.group,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_group_alerts: function(args) {
        if (args.group === undefined) {
            throw "group argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/hostgroup/'+args.group+'/alerts',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    }
};

monitors = {
    get_monitors: function (args) {
        rest.call({
            url : ARGUX_BASE + '/rest/1.0/monitor/' + args.type,
            success : args.success,
            complete: args.complete
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
            success : args.success,
            error : args.error
        });
    }
};

user = {
    get_users: function(args) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/admin/user',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    create: function(args) {
        if (args.username === undefined) {
            throw "Username argument missing";
        }
        if (args.password === undefined) {
            throw "Password argument missing";
        }

        data = {
            "password" : args.password
        }

        rest.call({
            url : ARGUX_BASE+'/rest/1.0/admin/user/'+args.username,
            type : rest.CallType.CREATE,
            data : data,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    remove: function(args) {
        if (args.username === undefined) {
            throw "username argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/admin/user/'+args.username,
            type : rest.CallType.DELETE,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    create_bookmark: function(args) {
        if (args.bookmark === undefined) {
            throw "bookmark argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/user/bookmark/'+args.bookmark,
            type : rest.CallType.CREATE,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    delete_bookmark: function(args) {
        if (args.bookmark === undefined) {
            throw "bookmark argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/user/bookmark/'+args.bookmark,
            type : rest.CallType.DELETE,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_bookmarks: function(args) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/user/bookmark',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    set_password: function(args) {
        if (args.password === undefined) {
            throw "Password argument missing";
        }

        data = {
            "password" : args.password
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/user/profile',
            type : rest.CallType.UPDATE,
            data : data,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    }
};

$(function() {
    $('.btn-bookmark').click(function(e) {
        var bookmark = $(this).data('bookmark');
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            user.delete_bookmark({
                bookmark : bookmark
            });
        } else {
            $(this).addClass('active');
            user.create_bookmark({
                bookmark : bookmark
            });
        }
    });
});

function update_chart (obj, chart, config, repeat) {
    var chart_id = obj.data('graphid');

    rest.call({
        url: ARGUX_BASE + 
             "/rest/1.0/graph/" +
             chart_id +
             "?get_values=true"+
             "&start="+
             ARGUX_TIMEFRAME_START+
             "&end="+
             ARGUX_TIMEFRAME_END+
             "&interval="+
             ARGUX_TIMEFRAME_INTERVAL,
        dataType: "json",
        success: function(json) {
            obj.children(".heading").children(".title").text(json.name);
            config.data.datasets = [];

            counter = 0;
            // Set data for each item separately.
            $.each(json.items, function(i, item) {
                var dataset = {
                    label: item.name,
                    borderWidth: 1,
                    pointHoverRadius: 4,
                    data: [{'x': '0', 'y': '1'}]
                };
                var datapoints = [];
                datapoints.push({x: ARGUX_TIMEFRAME_START});
                var item_unit_prefix = '';
                if(item.color !== undefined && item.color !== null){
                    color = item.color;
                } else {
                    pc = get_palette_color(counter);
                    color = pc[0];
                    counter = pc[1];
                }

                dataset['borderColor'] = hex2rgba(color, 1);
                dataset['backgroundColor'] = hex2rgba(color, 0.2);

                if(item['color-fill'] === 'false') {
                    dataset['fill'] = false;
                } else {
                    dataset['fill'] = true;
                }
                

                if (item.unit) {
                    if (json.max_value < 0.1 && json.min_value > -0.1) {
                        item_unit_prefix = 'm';
                    }
                    if (json.max_value < 0.0001 && json.min_value > -0.0001) {
                        item_unit_prefix = '\u00B5';
                    }
                    if (json.max_value > 100 && json.min_value < -100) {
                        item_unit_prefix = 'k';
                    }
                    if (json.max_value > 1000000 && json.min_value < -100000) {
                        item_unit_prefix = 'M';
                    }
                    if (json.max_value > 1000000000 && json.min_value < -100000000) {
                        item_unit_prefix = 'G';
                    }
                }


                $.each(item.values, function(i, value) {
                    if(value.value != null) {
                        switch (item_unit_prefix) {
                            case '\u00B5':
                                item_value = (value.value*1000000);
                                break;
                            case 'm':
                                item_value = (value.value*1000);
                                break;
                            default:
                                item_value = value.value
                        }
                        item_value = Math.round(item_value*100)/100;
                    } else {
                        item_value = value.value;
                    }

                    datapoints.push({
                        x: value.ts,
                        y: item_value});
                });

                datapoints.push({x: ARGUX_TIMEFRAME_END});

                dataset.data = datapoints;
                config.data.datasets.push(dataset);

                var tickSymbol = '';
                if (item.unit) {
                    tickSymbol = item.unit.symbol;
                }
                config.options.scales.yAxes[0].ticks.callback =
                    function(value) {
                        if(item_unit_prefix !== ''){
                            return ''+Math.round(value*10)/10+' '+item_unit_prefix+tickSymbol;
                        } else {
                            return ''+Math.round(value*10)/10;
                        }
                    };

            });
            chart.update();
        },
        complete: function() {
            if (repeat === true) {
                setTimeout(
                    update_chart,
                    10000,
                    obj,
                    chart,
                    config);
            }
        }
    });
}

$(function() {
    $('.btn-graph-export').click(function() {
        $('#graph-export-modal').modal('show');
    });
    $('.btn-graph-full').click(function() {
        $('#graph-full-modal').modal('show');
        var graph_id = $(this).data('graphid');
        var obj  = $('#graph-full-chart-body');
        var canvas = $('<canvas/>');
        obj.empty();
        obj.append(canvas);
        obj.data('graphid', graph_id);
        var ctx = canvas[0].getContext("2d");

        // Create a copy of the history_chart_config so we can use
        // a different configuration for each chart.
        var config = $.extend(true, {}, history_chart_config);
        var chart = new Chart(ctx, config);

        update_chart (obj, chart, config, false);
    });
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

        $('#timeframe-window').on('timeframe:change', function(ev) {
            update_chart (obj, chart, config, false);
        });
        update_chart (obj, chart, config, true);
    });
});
