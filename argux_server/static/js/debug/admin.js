$(function() {

    function create_remove_callbacks() {
        $('.user-remove').click(function() {
            var username = $(this).parents('tr').data('username');

            $('#remove-username').val(username);
            $('#remove-user-message').text(
                'Do you want to remove the user "' +
                username + '"');
            $('#dmcm').modal('show');
        });

    }

    function get_users_success_callback(json) {
        var user_table = $('#users');
        user_table.empty();

        $.each(json.users, function(i, value) {
            if (value.protected !== true) {
                user_table.append(
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
            } else {
                user_table.append(
                    '<tr data-username="'+value.name+'"><td>' +
                    value.name +
                    '</td><td>' +
                    '-' +
                    '</td><td>' +
                    '<div class="pull-right">' +
                    '</div>' +
                    '</td></tr>'
                );
            }
        });

        create_remove_callbacks();
    }
    

    function get_users_complete_callback() {
        setTimeout(
            user.get_users,
            10000,
            {
                success : get_users_success_callback,
                complete : get_users_complete_callback
            }
        );
    }

    function create_user_error(xhr, ajaxOptions, thrownError) {
        if (xhr.status !== 201) {
            var sel = $('.modal-form-alerts');
            sel.empty();
            sel.append(
                '<div class="alert alert-danger alert-dismissible">'+
                '<strong>Problem:</strong> ' + xhr.responseJSON.message
            );
        } else {
            $('#create-user-modal').modal('hide');
            $('#create-user-modal input').val('');
            user.get_users({
                success : get_users_success_callback
            });
        }
    }

    if (ARGUX_ACTION === 'admin.users') {
        user.get_users({
            success : get_users_success_callback,
            complete : get_users_complete_callback
        });

        /* Set the input values to '', this is a workaround
         * Firefox' stupid behaviour of seeing all password
         * fields as *the* password-field. Auto-completing
         * the user's credentials in the new-user dialog.
         */
        $('#create-user-modal input').val('');
        $('#create-user-modal').on('shown.bs.modal', function() {
            $('#create-user-modal input').val('');
        });

        $('#new-user-form').submit(function(event) {
            event.preventDefault();
            user.create({
                username: $('#new-username').val(),
                password: $('#new-pass').val(),
                error : create_user_error
            })
        });
        $('#remove-user-form').submit(function(event) {
            user.remove({
                'username': $('#remove-username').val()
            });
            $('#dmcm').modal('hide');
        });
    }    
});
