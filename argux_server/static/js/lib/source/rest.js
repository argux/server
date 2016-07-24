rest = {
    CallType : {
        CREATE : "POST",
        READ : "GET",
        UPDATE : "PATCH",
        DELETE: "DELETE"
    },
    call: function (args) {
        if(args.type === undefined) {
            args.type = rest.CallType.READ;
        }
        if(args.success === undefined) {
            args.success = function(json){};
        }
        if(args.error === undefined) {
            args.error = function(json){};
        }
        if(args.complete === undefined) {
            args.complete = function(){};
        }
        if(args.data === undefined) {
            args.data = '';
        }

        $.ajax({
            url: args.url,
            type: args.type,
            headers: { 'X-CSRF-Token': CSRF_TOKEN },
            dataType: "json",
            data: JSON.stringify(args.data),
            success: function(json) {
                args.success(json);
            },
            error: function(a, b, c) {
                args.error(a, b, c);
            },
            complete: function() {
                args.complete();
            }
        });
    }
};
