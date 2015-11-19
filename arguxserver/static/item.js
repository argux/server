/* globals Chart: false */
/* globals ARGUX_BASE: false */
/* globals ARGUX_HOST: false */
/* globals ARGUX_ITEM: false */
/* globals ARGUX_ITEM_ACTION: false */

var config = {
    type: 'line',
    data: {
        datasets: [
            {
                label: ARGUX_ITEM,
                fillColor: "rgba(220,220,220,0.2)",
                strokeColor: "rgba(110,110,220,1)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: [{x:'0',y:'1'}]
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
                type: "time",
                display: true,
                time: {
                    format: 'MM/DD/YYYY HH:mm:SS',
                    //round: 'min'
                },
                scaleLabel: {
                    show: true,
                    labelString: 'Date/Time'
                }
            }, ],
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,
                    suggestedMin: 0.0,
                    suggestedMax: 1.0,
                },
                scaleLabel: {
                    show: true,
                    labelString: ARGUX_ITEM
                }
            }]
        },
        elements: {
            line: {
                tension: 0.3
            }
        },
    }
};

function pollItemValues(chart, start, end) {
    $.ajax({
        url: ARGUX_BASE+
             "/rest/1.0/host/"+
             ARGUX_HOST+
             "/item/"+
             ARGUX_ITEM+
             "/values?end="+end+"&start="+start,
        type: "GET",
        dataType: "json",
        success: function(json) {

            var datapoints = [];

            if (json.values.count > 0) {
                $.each(json.values, function(i, value) {
                    datapoints.push({
                        x: value.ts,
                        y: value.value});
                });
            } else {
                datapoints.push({
                        x: '01/01/1970 00:00:01',
                        y: 0.1
                        });
                datapoints.push({
                        x: '01/01/1970 00:30:01',
                        y: 0.1
                        });
            }

            config.data.datasets[0].data = datapoints;

            chart.update();

            setTimeout(pollItemValues, 3000);
        }
    });
}

$(function() {
    if (ARGUX_ITEM_ACTION==="details") {
        // Get the context of the canvas element we want to select
        var ctx = document.getElementById("item-timechart").getContext("2d");
        var chart = new Chart(ctx, config);

        pollItemValues(chart, '-30m', 'now');

    }
});
