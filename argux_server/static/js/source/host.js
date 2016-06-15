$(function() {

    function get_items_success_callback(json) {
        var item_table = $('#objects');
        item_table.empty();

        $.each(json.users, function(i, value) {
            item_table.append(
                '<tr data-username="'+value.name+'"><td>' +
                value.name +
                '</td><td>' +
                '-' +
                '</td><td>' +
                '<div class="pull-right">' +
                '<a href="#" class="user-remove"><span class="glyphicon glyphicon-trash"></span></a>' +
                '</div>' +
                '</td></tr>'
            );
        });

        create_remove_callbacks();
    }

    function get_items_complete_callback() {
        setTimeout(
            host.get_host_items,
            10000,
            {
                success : get_items_success_callback,
                complete : get_items_complete_callback
            }
        );
    }

    if (ARGUX_ACTION === 'host.metrics') {
        host.get_host_items({
            success : get_items_success_callback,
            complete : get_items_complete_callback
        })
    }
});

