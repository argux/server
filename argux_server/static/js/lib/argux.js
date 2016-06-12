function hex2rgba(e,t){return e=e.replace("#",""),r=parseInt(e.substring(0,2),16),g=parseInt(e.substring(2,4),16),b=parseInt(e.substring(4,6),16),"rgba("+r+","+g+","+b+","+t+")"}function get_palette_color(e){return e>=palette.length&&(e=0),color=palette[e],e++,[color,e]}function update_chart(e,t,a,s){var r=e.data("graphid");rest.call({url:ARGUX_BASE+"/rest/1.0/graph/"+r+"?get_values=true&start="+ARGUX_TIMEFRAME_START+"&end="+ARGUX_TIMEFRAME_END+"&interval="+ARGUX_TIMEFRAME_INTERVAL,dataType:"json",success:function(s){e.children(".heading").children(".title").text(s.name),a.data.datasets=[],counter=0,$.each(s.items,function(e,t){var r={label:t.name,borderWidth:1,pointHoverRadius:4,data:[{x:"0",y:"1"}]},o=[];o.push({x:ARGUX_TIMEFRAME_START});var n="";void 0!==t.color&&null!==t.color?color=t.color:(pc=get_palette_color(counter),color=pc[0],counter=pc[1]),r.borderColor=hex2rgba(color,1),r.backgroundColor=hex2rgba(color,.2),t["color-fill"]===!1?(r.fill=!1,r.backgroundColor=null):r.fill=!0,t.unit&&(s.max_value<.1&&s.min_value>-.1&&(n="m"),s.max_value<1e-4&&s.min_value>-1e-4&&(n="µ"),s.max_value>100&&s.min_value<-100&&(n="k"),s.max_value>1e6&&s.min_value<-1e5&&(n="M"),s.max_value>1e9&&s.min_value<-1e8&&(n="G")),$.each(t.values,function(e,t){if(null!=t.value){switch(n){case"µ":item_value=1e6*t.value;break;case"m":item_value=1e3*t.value;break;default:item_value=t.value}item_value=Math.round(100*item_value)/100}else item_value=t.value;o.push({x:t.ts,y:item_value})}),o.push({x:ARGUX_TIMEFRAME_END}),r.data=o,a.data.datasets.push(r);var i="";t.unit&&(i=t.unit.symbol),a.options.scales.yAxes[0].ticks.callback=function(e){return""!==n?""+Math.round(10*e)/10+" "+n+i:""+Math.round(10*e)/10}}),t.update()},complete:function(){s===!0&&setTimeout(update_chart,1e4,e,t,a)}})}var argux={VERSION:"0.0.1"};rest={CallType:{CREATE:"POST",READ:"GET",UPDATE:"POST",DELETE:"DELETE"},call:function(e){void 0===e.type&&(e.type=rest.CallType.READ),void 0===e.success&&(e.success=function(e){}),void 0===e.error&&(e.error=function(e){}),void 0===e.complete&&(e.complete=function(){}),void 0===e.data&&(e.data=""),$.ajax({url:e.url,type:e.type,headers:{"X-CSRF-Token":CSRF_TOKEN},dataType:"json",data:JSON.stringify(e.data),success:function(t){e.success(t)},error:function(t,a,s){e.error(t,a,s)},complete:function(){e.complete()}})}};var ARGUX_TIMEFRAME_START,ARGUX_TIMEFRAME_END,ARGUX_TIMEFRAME_INTERVAL=60,unit={},palette=["#ff0000","#00ff00","#0000ff"],history_chart_config={type:"line",data:{datasets:[]},options:{responsive:!0,scales:{xAxes:[{type:"time",display:!0,time:{format:"YYYY-MM-DDTHH:mm:SS",displayFormats:{millisecond:"SSS [ms]",second:"HH:mm:ss",minute:"MM/DD HH:mm",hour:"YY/MM/DD HH:00",day:"YY/MM/DD",month:"MMM YYYY",quarter:"[Q]Q - YYYY",year:"YYYY"}},scaleLabel:{show:!0,labelString:"Date/Time"}}],yAxes:[{display:!0,ticks:{beginAtZero:!0,suggestedMin:0,suggestedMax:1,callback:function(e){return""+Math.round(10*e)/10}},scaleLabel:{show:!0}}]},elements:{line:{tension:0},point:{radius:1}}}},host_overview_chart_config={type:"doughnut",data:{datasets:[{data:[0,0,0,1],backgroundColor:["#419641","#f0ad4e","#c12e2a","#e0e0e0"]}],labels:["Okay","Warning","Critical","Unknown"]},options:{responsive:!0,legend:{display:!1}}};$(function(){var e=!1;$("#timeframe-start").datetimepicker({format:"YYYY/MMM/DD HH:mm",useCurrent:!1,sideBySide:!0}),$("#timeframe-end").datetimepicker({format:"YYYY/MMM/DD HH:mm",sideBySide:!0}),$("#timeframe-start").on("dp.change",function(t){$("#timeframe-end").data("DateTimePicker").minDate(t.date),ARGUX_TIMEFRAME_START=t.date.format("YYYY-MM-DDTHH:mm:ss"),$("#timeframe-window").trigger("timeframe:change"),e===!1&&$("#timeframe-window").val("custom").change()}),$("#timeframe-end").on("dp.change",function(t){$("#timeframe-start").data("DateTimePicker").maxDate(t.date),ARGUX_TIMEFRAME_END=t.date.format("YYYY-MM-DDTHH:mm:ss"),$("#timeframe-window").trigger("timeframe:change"),e===!1&&$("#timeframe-window").val("custom").change()}),$("#timeframe-window").change(function(t){var a,s=moment(),r=moment();switch($(this).val()){case"60m":a=r.subtract(60,"minutes"),ARGUX_TIMEFRAME_INTERVAL=60;break;case"6h":a=r.subtract(6,"hours"),ARGUX_TIMEFRAME_INTERVAL=120;break;case"12h":a=r.subtract(12,"hours"),ARGUX_TIMEFRAME_INTERVAL=300;break;case"24h":a=r.subtract(24,"hours"),ARGUX_TIMEFRAME_INTERVAL=600;break;case"7d":a=r.subtract(7,"days"),ARGUX_TIMEFRAME_INTERVAL=3600;break;case"1M":a=r.subtract(1,"months"),ARGUX_TIMEFRAME_INTERVAL=14400;break;case"custom":break;default:alert("invalid timeframe")}"custom"!==$(this).val()&&(e=!0,$("#timeframe-end").data("DateTimePicker").maxDate(moment()),$("#timeframe-start").data("DateTimePicker").date(a),$("#timeframe-end").data("DateTimePicker").date(s),e=!1)}),$("#timeframe-window").val("60m").change()}),host={get_host_overview:function(e){void 0===e.complete_callback&&(e.complete_callback=function(){}),rest.call({url:ARGUX_BASE+"/rest/1.0/host",success:host._get_host_overview_success,error:host._get_host_overview_error,complete:e.complete_callback})},_get_host_overview_success:function(e){var t=0,a=[0,0,0,0];$("#hosts").empty(),e.hosts=e.hosts.sort(function(e,t){return e.name>=t.name}),$.each(e.hosts,function(e,s){$("#hosts").append('<tr><td><a href="'+ARGUX_BASE+"/host/"+s.name+'">'+s.name+'</a></td><td><a href="'+ARGUX_BASE+"/host/"+s.name+'/metrics">'+s.n_items+'</a></td><td><a href="'+ARGUX_BASE+"/host/"+s.name+'/alerts">'+s.active_alerts+"</a></td></tr>"),"crit"===s.severity?a[2]+=1:"warn"===s.severity?a[1]+=1:"info"===s.severity?a[3]+=1:a[0]+=1,t+=s.active_alerts}),host_overview_chart_config.data.datasets[0].data=a,t>0?$("#alert_count").text(t):$("#alert_count").text("")},_get_host_overview_error:function(e){},create:function(e){if(void 0===e.hostname)throw"Hostname argument missing";void 0===e.description?description="":description=e.description,void 0===e.addresses?addresses=[]:addresses=e.addresses,data={description:description,address:addresses},rest.call({url:ARGUX_BASE+"/rest/1.0/host/"+e.hostname,type:rest.CallType.CREATE,data:data,success:e.success,error:e.error,complete:e.complete})},get_addresses:function(e){if(void 0===e.hostname)throw"Hostname argument missing";if(void 0===e.callback_success)throw"callback_success missing";rest.call({url:ARGUX_BASE+"/rest/1.0/host/"+e.hostname+"/addr",success:e.callback_success})}},monitors={get_monitors:function(e){void 0===e.complete_callback&&(e.complete_callback=function(){}),rest.call({url:ARGUX_BASE+"/rest/1.0/monitor/"+e.type,success:monitors._get_monitors_success,complete:e.complete_callback})},_get_monitors_success:function(e){$("#monitors").empty(),$.each(e.monitors,function(e,t){options="",$.each(t.options,function(e,t){options+='<li><span style="font-weight: bold">'+e+":</span> "+t+"</li>"}),t.active?(button='<span class="glyphicon glyphicon-pause"></span>',state="running",klass=""):(button='<span class="glyphicon glyphicon-play"></span>',state="paused",klass="pause"),$("#monitors").append('<tr class="'+klass+'" data-hostname="'+t.host+'" data-address="'+t.address+'" ><td><a href="#" class="monitor-play-btn">'+button+'</a><a href="'+ARGUX_BASE+"/monitor/"+ARGUX_MONITOR_TYPE+"/"+t.host+"/"+t.address+'/edit">'+t.host+" ("+t.address+")</a></td><td><ul>"+options+'</ul></td><td class="state">'+state+'</td><td><div class="pull-right"><a href="#" class="monitor-remove"><span class="glyphicon glyphicon-trash"></span></a></div></td></tr>')}),$(".monitor-play-btn").click(function(){var e=$(this),t=e.parents("tr"),a=t.data("hostname"),s=t.data("address"),r=t.children("td.state"),o=t.hasClass("pause");data={options:{interval:60}},o===!0?(data.active="true",rest.call({url:ARGUX_BASE+"/rest/1.0/monitor/"+ARGUX_MONITOR_TYPE+"/"+a+"/"+s,type:rest.CallType.UPDATE,data:data,success:function(){t.removeClass("pause"),e.children().removeClass("glyphicon-play"),e.children().addClass("glyphicon-pause"),r.text("running")}})):(data.active="false",rest.call({url:ARGUX_BASE+"/rest/1.0/monitor/"+ARGUX_MONITOR_TYPE+"/"+a+"/"+s,type:rest.CallType.UPDATE,data:data,success:function(){t.addClass("pause"),e.children().addClass("glyphicon-play"),e.children().removeClass("glyphicon-pause"),r.text("paused")}}))}),$(".monitor-remove").click(function(){var e=$(this).parents("tr").data("hostname"),t=$(this).parents("tr").data("address");$("#dmcm-hostname").val(e),$("#dmcm-address").val(t),$("#dmcm-message").text("Do you want to remove the "+ARGUX_MONITOR_TYPE+" monitor for "+e+" on "+t),$("#dmcm").modal("show")})},remove:function(e){if(void 0===e.hostname)throw"Hostname argument missing";if(void 0===e.address)throw"address argument missing";rest.call({url:ARGUX_BASE+"/rest/1.0/monitor/"+ARGUX_MONITOR_TYPE+"/"+e.hostname+"/"+e.address,type:rest.CallType.DELETE})},create:function(e){if(void 0===e.hostname)throw"Hostname argument missing";if(void 0===e.address)throw"address argument missing";void 0===e.options&&(e.options={}),data={options:e.options},rest.call({url:ARGUX_BASE+"/rest/1.0/monitor/"+ARGUX_MONITOR_TYPE+"/"+e.hostname+"/"+e.address,type:rest.CallType.CREATE,data:data,success:monitors._create_success,error:monitors._create_error})},_create_error:function(e){},_create_success:function(e){}},user={get_users:function(e){rest.call({url:ARGUX_BASE+"/rest/1.0/admin/user",success:e.success,error:e.error,complete:e.complete})},create:function(e){if(void 0===e.username)throw"Username argument missing";if(void 0===e.password)throw"Password argument missing";data={password:e.password},rest.call({url:ARGUX_BASE+"/rest/1.0/admin/user/"+e.username,type:rest.CallType.CREATE,data:data,success:e.success,error:e.error,complete:e.complete})},remove:function(e){if(void 0===e.username)throw"Username argument missing";rest.call({url:ARGUX_BASE+"/rest/1.0/admin/user/"+e.username,type:rest.CallType.DELETE,success:e.success,error:e.error,complete:e.complete})}},$(function(){$(".btn-graph-full").click(function(){$("#graph-full-modal").modal("show");var e=$(this).data("graphid"),t=$("#graph-full-chart-body"),a=$("<canvas/>");t.empty(),t.append(a),t.data("graphid",e);var s=a[0].getContext("2d"),r=$.extend(!0,{},history_chart_config),o=new Chart(s,r);update_chart(t,o,r,!1)}),$(".argux-chart").each(function(e){var t=$(this),a=t.children(".chart-body"),s=$("<canvas/>");a.append(s);var r=s[0].getContext("2d"),o=$.extend(!0,{},history_chart_config),n=new Chart(r,o);$("#timeframe-window").on("timeframe:change",function(e){update_chart(t,n,o,!1)}),update_chart(t,n,o,!0)})});
