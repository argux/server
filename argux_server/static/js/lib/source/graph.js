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
                if(item.color !== undefined && item.color !== null){
                    color = item.color;
                } else {
                    pc = get_palette_color(counter);
                    color = pc[0];
                    counter = pc[1];
                }

                dataset['borderColor'] = hex2rgba(color, 1);
                dataset['backgroundColor'] = hex2rgba(color, 0.2);

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


                $.each(item.values.avg, function(i, value) {
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

                dataset.data = datapoints;
                config.data.datasets.push(dataset);

                var tickSymbol = item.unit.symbol;
                config.options.scales.yAxes.ticks = {};
                config.options.scales.yAxes.ticks.callback =
                    function(tickValue) {
                        alert(tickSymbol);
                        return tickValue+'>'+tickSymbol;
                    };

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
