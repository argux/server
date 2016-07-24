user = {
    get_users: function(args) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/admin/user',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    create: function(args) {
        if (args.username === undefined) {
            throw "Username argument missing";
        }
        if (args.password === undefined) {
            throw "Password argument missing";
        }

        data = {
            "password" : args.password
        }

        rest.call({
            url : ARGUX_BASE+'/rest/1.0/admin/user/'+args.username,
            type : rest.CallType.CREATE,
            data : data,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    remove: function(args) {
        if (args.username === undefined) {
            throw "username argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/admin/user/'+args.username,
            type : rest.CallType.DELETE,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    create_bookmark: function(args) {
        if (args.bookmark === undefined) {
            throw "bookmark argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/user/bookmark/'+args.bookmark,
            type : rest.CallType.CREATE,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    delete_bookmark: function(args) {
        if (args.bookmark === undefined) {
            throw "bookmark argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/user/bookmark/'+args.bookmark,
            type : rest.CallType.DELETE,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_bookmarks: function(args) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/user/bookmark',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    set_password: function(args) {
        if (args.password === undefined) {
            throw "Password argument missing";
        }

        data = {
            "password" : args.password
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/user/profile',
            type : rest.CallType.UPDATE,
            data : data,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    }
};

$(function() {
    $('.btn-bookmark').click(function(e) {
        var bookmark = $(this).data('bookmark');
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            user.delete_bookmark({
                bookmark : bookmark
            });
        } else {
            $(this).addClass('active');
            user.create_bookmark({
                bookmark : bookmark
            });
        }
    });
});
