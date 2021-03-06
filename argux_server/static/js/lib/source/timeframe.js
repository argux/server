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
