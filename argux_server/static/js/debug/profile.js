var bookmarks;

$(function() {

    /*
     * Create callback hooks for removing users.
     */
    function create_remove_callbacks(obj) {
        $('.bookmark-remove').click(function() {
            var bookmark_id = $(this).parents('tr').data('bookmark');

            $('#remove-bookmark').val(bookmark_id);
            $('#remove-bookmark-message').text(
                'Do you want to remove the bookmark "' +
                bookmark_id + '"');
            $('#remove-bookmark-modal').modal('show');
        });
    }

    function get_bookmarks_success_callback(json) {
        if (VIEW_SORT === "desc") {
            bookmarks = json.bookmarks.sort(function(a, b) {return a.title < b.title});
        } else {
            bookmarks = json.bookmarks.sort(function(a, b) {return a.title >= b.title});
        }

        update_view();
    }

    function update_view() {
        list = $('#bookmark-list-body');
        list.empty();

        if(bookmarks.length > 0) {
            $.each(bookmarks, function(i, value) {
                list.append(
                    '<tr data-bookmark="'+value.id+'">' +
                    '<td>'+
                    '<a class="host" href="'+value.url+'">' +
                    '<span class="glyphicon glyphicon-bookmark"></span> '+
                    value.title +
                    '</a>' +
                    '<div class="pull-right">' +
                    '<a href="#" class="bookmark-remove">'+
                    '<span class="glyphicon glyphicon-remove"></span>'+
                    '</a>'+
                    '</div>' +
                    '</td>' +
                    '</tr>'
                );
            });
        } else {
            list.append(
                '<tr><td><em>Empty</em></tr>'
            );
        }

        create_remove_callbacks();
    }

    if (ACTION === 'bookmarks') {
        user.get_bookmarks({
            success : get_bookmarks_success_callback
        });

        $('.bookmarks-sort').click(function(e) {
            VIEW_SORT = $(this).data('direction');
            if (VIEW_SORT === "desc") {
                bookmarks = bookmarks.sort(function(a, b) {return a.title < b.title});
                $('.bookmarks-sort-desc').addClass('active');
                $('.bookmarks-sort-asc').removeClass('active');
            } else {
                bookmarks = bookmarks.sort(function(a, b) {return a.title >= b.title});
                $('.bookmarks-sort-asc').addClass('active');
                $('.bookmarks-sort-desc').removeClass('active');
            }

            update_view();
        });
    }

    $('#remove-bookmark-form').submit(function(event) {
        user.delete_bookmark({
            'bookmark': $('#remove-bookmark').val()
        });
        $('#remove-bookmark-modal').modal('hide');

        user.get_bookmarks({
            success : get_bookmarks_success_callback
        });
    });
});

