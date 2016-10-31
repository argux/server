host = {
    get_host_overview: function(args) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host',
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    },
    get_host: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        if (args.items === undefined) {
            args.items = 'false';
        }
        if (args.alerts === undefined) {
            args.alerts = 'false';
        }
        if (args.notes === undefined) {
            args.notes = 'false';
        }
        if (args.page=== undefined) {
            args.page = 0;
        }
        rest.call({
            url : ARGUX_BASE+
                    '/rest/1.0/host/'+
                    args.hostname+
                    '?alerts='+args.alerts+
                    '&items='+args.items+
                    '&notes='+args.notes+
                    '&page='+args.page,
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
    },
    create_note: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        if (args.message === undefined) {
            throw "Message argument missing";
        }
        if (args.subject === undefined) {
            throw "Subject argument missing";
        }

        data = {
            "host": args.hostname,
            "message" : args.message,
            "subject" : args.subject
        };

        rest.call({
            url : ARGUX_BASE+'/rest/1.0/note',
            type : rest.CallType.CREATE,
            data : data,
            success : args.success,
            error : args.error,
            complete : args.complete
        });
    }
};
