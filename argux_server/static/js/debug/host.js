$(function() {

    var PAGE=0;
    var refresh_timer = null;

    function get_host_complete_callback() {
        refresh_timer = setTimeout(
            host.get_host_items,
            10000,
            {
                hostname : ARGUX_HOST,
                page : PAGE,
                success : get_host_success_callback,
                complete : get_host_complete_callback
            }
        );
    }

    function get_host_success_callback(json) {
        var object_table = $('#objects');
        object_table.empty();

        if (ARGUX_ACTION === 'host.metrics') {
            set_items(json);
        }
        if (ARGUX_ACTION === 'host.notes') {
            set_notes(json);
        }

    }

    function set_items(json) {
        var categories = {};
        var alerts     = {};
        var collapsed  = {};
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

    function set_notes(json) {
        var last_page = (json.note_count / json.page_size)-1;

        if (json.note_count > json.page_size) {
            $('#pager').removeClass('hidden');
            $('#pager').children('.page').remove();
            for (i = 0; i < (json.note_count / json.page_size); ++i) {
                if (i == json.page) {
                    $('#pager').children('.next').before(
                        '<li class="page disabled active"><a href="#" class="page">'+(i+1)+'</a></li>');
                } else {
                    $('#pager').children('.next').before(
                        '<li class="page"><a href="#" class="page">'+(i+1)+'</a></li>');
                }
            }
            if (parseInt(json.page) === 0) {
                $('#pager').children('.previous').addClass('disabled');
            } else {
                $('#pager').children('.previous').removeClass('disabled');
            }
            if (parseInt(json.page) === last_page) {
                $('#pager').children('.next').addClass('disabled');
            } else {
                $('#pager').children('.next').removeClass('disabled');
            }

            $('a.page').click(function() {

                PAGE = $(this).text()-1;

                if (refresh_timer) {
                    clearTimeout(refresh_timer);
                }
                host.get_notes({
                    hostname : ARGUX_HOST,
                    page : PAGE,
                    success : get_notes_success_callback,
                    complete : get_notes_complete_callback
                })
            });
        } else {
            $('#pager').addClass('hidden');
        }

        // Build the panel contents.
        $.each(json.notes, function(i, note) {

            // Note timestamp is in ISO format.
            var ts = moment(note.timestamp);


            $('#objects').append(
                '<div class="panel panel-default">' +
                '<div class="panel-heading">' +
                note.subject +
                '</div>' +
                '<div class="panel-body">' +
                '<p>' +
                note.message +
                '</p>' +
                '<div class="xs" data-toggle="tooltip" title="'+
                ts.toLocaleString() +
                '">' +
                '<span class="small pull-right">' +
                ts.fromNow() +
                '</span>' +
                '</div>' +
                '</div>' +
                '</div>');
        });
    }

    if (ARGUX_ACTION === "host.metrics") {
        host.get_host({
            hostname : ARGUX_HOST,
            items : 'true',
            page : PAGE,
            success : get_host_success_callback,
            complete : get_host_complete_callback
        });
    }
    if (ARGUX_ACTION === "host.notes") {
        $('#notes-form').submit(function(event) {
            event.preventDefault();

            var subject = $('#note-subject').val();
            var message = $('#note-body').val();

            if (( subject !== "") &&
                ( message !== "")) {
                
                host.create_note({
                    hostname : ARGUX_HOST,
                    message : message,
                    subject : subject,
                    error: function(json) {
                        $('#alerts').empty();
                        $('#alerts').append(
                            '<div class="alert alert-danger alert-dismissible">'+
                            '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                            '<strong>Problem:</strong> Creating new Note failed.'+
                            '</div>');
                    },
                    complete: function(json) {
                        $('#new-note-modal').modal('hide');
                    }
                });
            }
        });
        host.get_host({
            hostname : ARGUX_HOST,
            notes : 'true',
            page : PAGE,
            success : get_host_success_callback,
            complete : get_host_complete_callback
        })
    }


    // Show/hide details below host header.
    $("#host_detail_btn").click(function(e) {
        var span = $('#host_detail_btn > span');
        $('#host_detail').toggleClass('hidden');
        if ($('#host_detail').is('.hidden')) {
            span.addClass('glyphicon-chevron-up');
            span.removeClass('glyphicon-chevron-down');
        } else {
            span.addClass('glyphicon-chevron-down');
            span.removeClass('glyphicon-chevron-up');
        }
    });
});

