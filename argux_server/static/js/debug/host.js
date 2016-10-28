$(function() {

    function get_items_success_callback(json) {
        var categories = {};
        var alerts     = {};
        var collapsed  = {};
        var item_table = $('#objects');
        item_table.empty();

        // Build the panel contents.
        json.items.sort(function(a,b) {
            if (a.name < b.name) return -1;
            if (a.name > b.name) return 1;
            return 0;
        });

        $.each(json.items, function(i, item) {

            var category = 'global';
            var item_name = item.key;
            var item_value = 'unknown';
            var item_time = '-';
            var item_unit = '';
            var item_unit_prefix = '';

            // Pick a category
            if (item.category !== null) {
                category = item.category;
            }

            // If name exists, don't use the key.
            if (item.name !== null) {
                item_name = item.name;
            }

            // Get the unit
            if (item.unit !== null) {
                item_unit = item.unit.symbol
            }

            //
            if (item.last_ts !== undefined) {
                item_time = item.last_ts;
            }

            if (item.last_val !== undefined) {
                item_value = item.last_val;
                if (item_unit !== '') {
                    if (item_value < 0.1) {
                        item_unit_prefix = 'm';
                    }
                    if (item_value < 0.0001) {
                        item_unit_prefix = '&micro;';
                    }
                    if (item_value > 100) {
                        item_unit_prefix = 'k';
                    }
                    if (item_value > 100000) {
                        item_unit_prefix = 'M';
                    }
                    if (item_value > 100000000) {
                        item_unit_prefix = 'G';
                    }

                    switch (item_unit_prefix) {
                        case '&micro;':
                            item_value = (item_value*1000000);
                            break;
                        case 'm':
                            item_value = (item_value*1000);
                            break;
                    }
                    item_value = Math.round(item_value*100)/100;
                }
            }

            /* Initialise alerts to '' */
            if (alerts.hasOwnProperty(category) === false) {
                alerts[category] = '';
            }
            var item_base_url = 
                ARGUX_BASE +
                '/host/' +
                ARGUX_HOST +
                '/item/' +
                item.key;

            categories[category]+='<tr>' +
              '<td>' +
              '<a href="'+item_base_url+'">' +
              '<span ' +
              ' data-toggle="tooltip"' +
              ' title="'+item.key+'">' +
              item_name +
              '</span>' +
              '</a>' +
              '</td>' +
              '<td>' + item_value + ' ' + item_unit_prefix + item_unit + '</td>' +
              '<td class="hidden-xs" data-toggle="tooltip" title="'+item_time+'">' +
              moment(item_time).fromNow() +
              '</td>' +
              '<td class="item-details">' +
              '<a href="'+item_base_url+'/bookmark" aria-label="Bookmark">' +
              '<span class="glyphicon glyphicon-bookmark" aria-hidden="true"></span>' +
              '</a>' +
              '</td>' +
              '</tr>';
        });

        // Determine if a panel was collapsed before the refresh.
        $('#objects div.collapse').each(function(i, item) {
            var id = item.id.substring(12);
            collapsed[id] = $(this).hasClass('in');
        });

        // Remove all panels and build the page again.
        $('#objects').empty();

        for (var key in categories) {
            if (categories.hasOwnProperty(key)) {
                $('#objects').append(
                    '<div class="panel panel-default">' +
                    '<div class="panel-heading metric-category">' +
                    '<a data-toggle="collapse" data-target="#table-items-'+key+'">' +
                    key +
                    ' <span class="badge">'+alerts[key]+'</span>' +
                    '</a>' +
                    '</div>' +
                    '<div class="collapse in" id="table-items-'+key+'">' +
                    '<table class="table table-striped table-condensed">' +
                    '<thead>' +
                    '<tr>' + 
                    '<th>Name</th>' +
                    '<th class="col-xs-2">Value</th>' +
                    '<th class="col-sm-3 hidden-xs">Timestamp</th>' +
                    '<th class="col-xs-2 col-sm-1"></th>' +
                    '</tr>' +
                    '</thead>' +
                    '<tbody>' +
                    '<tbody id="items-'+key+'">' +
                    '</tbody>' +
                    '</table>' +
                    '</div>' +
                    '</div>');

                // Collapse panels that were collapsed before the refresh.
                if (collapsed[key] === false) {
                    $('#table-items-'+key).removeClass('in');
                }

                // Add the panel-content.
                $('#items-'+key).append(
                    categories[key]
                    );
            }
        }
    }

    function get_items_complete_callback() {
        setTimeout(
            host.get_host_items,
            10000,
            {
                hostname : ARGUX_HOST,
                success : get_items_success_callback,
                complete : get_items_complete_callback
            }
        );
    }

    if (ARGUX_ACTION === "host.metrics") {
        host.get_host_items({
            hostname : ARGUX_HOST,
            success : get_items_success_callback,
            complete : get_items_complete_callback
        });
    }
});

