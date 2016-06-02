$(function() {
    function get_users_success_callback(json) {

    }

    function get_users_complete_callback() {

    }
    if (ARGUX_ACTION === 'admin.users') {
        user.get_users({
            success : get_users_success_callback,
            complete : get_users_complete_callback
        });
    }    
});
