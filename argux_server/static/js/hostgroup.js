var group_hosts;$(function(){function s(s){group_hosts="desc"===VIEW_SORT?s.hosts.sort(function(s,t){return s.name<t.name}):s.hosts.sort(function(s,t){return s.name>=t.name}),t()}function t(){var s=$("#host-list");s.empty(),"list"===VIEW_TYPE&&(s.append('<div class="col-xs-12"><div class="panel panel-default"><table class="table table-striped"><thead><tr><th>Host</th><th>Items</th><th>Alerts</th></tr></thead><tbody id="host-list-body"></tbody></table></div></div>'),s=$("#host-list-body")),$.each(group_hosts,function(t,e){var a,i;switch(e.severity){case"warn":a="panel panel-warning",i="warning";break;case"crit":a="panel panel-danger",i="danger";break;default:a="panel panel-default",i=""}switch(VIEW_TYPE){case"grid":s.append('<div class="col-xs-12 col-sm-4 col-md-3 col-lg-2"><a class="host" href="/host/'+e.name+'"><div class="'+a+'"><div class="panel-heading active">'+e.name+'</div><div class="panel-body"><ul><li>Items: '+e.n_items+"</li><li>Alerts: "+e.active_alerts+"</li></ul></div></div></a></div>");break;case"list":s.append('<tr class="'+i+'"><td><a class="host" href="/host/'+e.name+'">'+e.name+"</a></td><td>"+e.n_items+"</td><td>"+e.active_alerts+"</td></tr>")}})}host.get_group_members({group:HOST_GROUP,success:s}),$(".hostlist-view").click(function(s){VIEW_TYPE=$(this).data("view"),"list"===VIEW_TYPE?($(".hostlist-view-list").addClass("active"),$(".hostlist-view-grid").removeClass("active")):($(".hostlist-view-grid").addClass("active"),$(".hostlist-view-list").removeClass("active")),t()}),$(".hostlist-sort").click(function(s){VIEW_SORT=$(this).data("direction"),"desc"===VIEW_SORT?(group_hosts=group_hosts.sort(function(s,t){return s.name<t.name}),$(".hostlist-sort-desc").addClass("active"),$(".hostlist-sort-asc").removeClass("active")):(group_hosts=group_hosts.sort(function(s,t){return s.name>=t.name}),$(".hostlist-sort-asc").addClass("active"),$(".hostlist-sort-desc").removeClass("active")),t()})});
