$(function() {
    /* Use YYYY/MMM/DD HH:mm, (example: 2016/Jan/12 23:12)
     *
     * This way we won't have any confusion about those silly
     * date/time formats used in the US.
     */
    $('#timeframe-start').datetimepicker({
        format: 'YYYY/MMM/DD HH:mm'
    });
    $('#timeframe-end').datetimepicker({
        format: 'YYYY/MMM/DD HH:mm',
        useCurrent: false //Important! See issue #1075
    });
});
