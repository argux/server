$(function() {

    function get_users_success_callback(json) {
        var user_table = $('#users');
        user_table.empty();

        $.each(json.users, function(i, value) {
            user_table.append(
                '<tr><td>' +
                value.name +
                '</td><td>' +
                '-' +
                '</td></tr>'
            );
        });
    }
    

    function get_users_complete_callback() {

    }

    function create_user_error(xhr, ajaxOptions, thrownError) {
        if (xhr.status != 201) {
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
                success : get_users_success_callback,
            });
        }
    }

    if (ARGUX_ACTION === 'admin.users') {
        user.get_users({
            success : get_users_success_callback,
            complete : get_users_complete_callback
        });
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
        $('#create-user-modal input').val('');
    }    
});
