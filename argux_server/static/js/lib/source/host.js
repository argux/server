host = {
    get_host_overview: function(args) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_host_items: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+args.hostname+'?alerts=false&items=true',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_host_alerts: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+args.hostname+'?alerts=true&items=false',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    create: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        if (args.description === undefined) {
            description = '';
        } else {
            description = args.description;
        }
        if (args.addresses === undefined) {
            addresses = []
        } else {
            addresses = args.addresses;
        }

        data = {
            "description": description,
            "address": addresses
        };

        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+args.hostname,
            type : rest.CallType.CREATE,
            data : data,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_addresses: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        if (args.callback_success === undefined) {
            throw "callback_success missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+args.hostname+'/addr',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    }
};
