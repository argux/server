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
    create_host: function(args) {
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
        if (args.groups === undefined) {
            groups = []
        } else {
            groups = args.groups;
        }

        data = {
            "description": description,
            "groups": groups,
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
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+args.hostname+'/addr',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    create_group: function(args) {
        if (args.group === undefined) {
            throw "group argument missing";
        }
        if (args.description === undefined) {
            description = '';
        } else {
            description = args.description;
        }
        if (args.hosts === undefined) {
            hosts = []
        } else {
            hosts = args.hosts;
        }

        data = {
            "description": description,
            "hosts" : hosts
        };

        rest.call({
            url : ARGUX_BASE+'/rest/1.0/hostgroup/'+args.group,
            type : rest.CallType.CREATE,
            data : data,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_groups: function(args) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/hostgroup',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_group_members: function(args) {
        if (args.group === undefined) {
            throw "group argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/hostgroup/'+args.group,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_group_alerts: function(args) {
        if (args.group === undefined) {
            throw "group argument missing";
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/hostgroup/'+args.group+'/alerts',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    }
};
