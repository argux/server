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

    function create_user_error() {

    }

    if (ARGUX_ACTION === 'admin.users') {
        user.get_users({
            success : get_users_success_callback,
            complete : get_users_complete_callback
        });

        $('#user-form').submit(function(event) {
            event.preventDefault();
            user.create({
                username: $('#user-name').val(),
                error : create_user_error
            })
        });
    }    
});
