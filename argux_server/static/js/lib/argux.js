function hex2rgba(e,t){return e=e.replace("#",""),r=parseInt(e.substring(0,2),16),g=parseInt(e.substring(2,4),16),b=parseInt(e.substring(4,6),16),"rgba("+r+","+g+","+b+","+t+")"}function get_palette_color(e){return e>=palette.length&&(e=0),color=palette[e],e++,[color,e]}function update_chart(e,t,a,r){var s=e.data("graphid");rest.call({url:ARGUX_BASE+"/rest/1.0/graph/"+s+"?get_values=true&start="+ARGUX_TIMEFRAME_START+"&end="+ARGUX_TIMEFRAME_END+"&interval="+ARGUX_TIMEFRAME_INTERVAL,dataType:"json",success:function(r){e.children(".heading").children(".title").text(r.name),a.data.datasets=[],counter=0,$.each(r.items,function(e,t){var s={label:t.name,borderWidth:1,pointHoverRadius:4,data:[{x:"0",y:"1"}]},o=[];o.push({x:ARGUX_TIMEFRAME_START});var i="";void 0!==t.color&&null!==t.color?color=t.color:(pc=get_palette_color(counter),color=pc[0],counter=pc[1]),s.borderColor=hex2rgba(color,1),s.backgroundColor=hex2rgba(color,.2),"false"===t["color-fill"]?s.fill=!1:s.fill=!0,t.unit&&(r.max_value<.1&&r.min_value>-.1&&(i="m"),r.max_value<1e-4&&r.min_value>-1e-4&&(i="µ"),r.max_value>100&&r.min_value<-100&&(i="k"),r.max_value>1e6&&r.min_value<-1e5&&(i="M"),r.max_value>1e9&&r.min_value<-1e8&&(i="G")),$.each(t.values,function(e,t){if(null!=t.value){switch(i){case"µ":item_value=1e6*t.value;break;case"m":item_value=1e3*t.value;break;default:item_value=t.value}item_value=Math.round(100*item_value)/100}else item_value=t.value;o.push({x:t.ts,y:item_value})}),o.push({x:ARGUX_TIMEFRAME_END}),s.data=o,a.data.datasets.push(s);var n="";t.unit&&(n=t.unit.symbol),a.options.scales.yAxes[0].ticks.callback=function(e){return""!==i?""+Math.round(10*e)/10+" "+i+n:""+Math.round(10*e)/10}}),t.update()},complete:function(){r===!0&&setTimeout(update_chart,1e4,e,t,a)}})}var argux={VERSION:"0.0.1"};rest={CallType:{CREATE:"POST",READ:"GET",UPDATE:"POST",DELETE:"DELETE"},call:function(e){void 0===e.type&&(e.type=rest.CallType.READ),void 0===e.success&&(e.success=function(e){}),void 0===e.error&&(e.error=function(e){}),void 0===e.complete&&(e.complete=function(){}),void 0===e.data&&(e.data=""),$.ajax({url:e.url,type:e.type,headers:{"X-CSRF-Token":CSRF_TOKEN},dataType:"json",data:JSON.stringify(e.data),success:function(t){e.success(t)},error:function(t,a,r){e.error(t,a,r)},complete:function(){e.complete()}})}};var ARGUX_TIMEFRAME_START,ARGUX_TIMEFRAME_END,ARGUX_TIMEFRAME_INTERVAL=60,unit={},palette=["#ff0000","#00ff00","#0000ff"],history_chart_config={type:"line",data:{datasets:[]},options:{responsive:!0,scales:{xAxes:[{type:"time",display:!0,time:{format:"YYYY-MM-DDTHH:mm:SS",displayFormats:{millisecond:"SSS [ms]",second:"HH:mm:ss",minute:"MM/DD HH:mm",hour:"YY/MM/DD HH:00",day:"YY/MM/DD",month:"MMM YYYY",quarter:"[Q]Q - YYYY",year:"YYYY"}},scaleLabel:{show:!0,labelString:"Date/Time"}}],yAxes:[{display:!0,ticks:{beginAtZero:!0,suggestedMin:0,suggestedMax:1,callback:function(e){return""+Math.round(10*e)/10}},scaleLabel:{show:!0}}]},elements:{line:{tension:0},point:{radius:1}}}},host_overview_chart_config={type:"doughnut",data:{datasets:[{data:[0,0,0,1],backgroundColor:["#419641","#f0ad4e","#c12e2a","#e0e0e0"]}],labels:["Okay","Warning","Critical","Unknown"]},options:{responsive:!0,legend:{display:!1}}};$(function(){var e=!1;$("#timeframe-start").datetimepicker({format:"YYYY/MMM/DD HH:mm",useCurrent:!1,sideBySide:!0}),$("#timeframe-end").datetimepicker({format:"YYYY/MMM/DD HH:mm",sideBySide:!0}),$("#timeframe-start").on("dp.change",function(t){$("#timeframe-end").data("DateTimePicker").minDate(t.date),ARGUX_TIMEFRAME_START=t.date.format("YYYY-MM-DDTHH:mm:ss"),$("#timeframe-window").trigger("timeframe:change"),e===!1&&$("#timeframe-window").val("custom").change()}),$("#timeframe-end").on("dp.change",function(t){$("#timeframe-start").data("DateTimePicker").maxDate(t.date),ARGUX_TIMEFRAME_END=t.date.format("YYYY-MM-DDTHH:mm:ss"),$("#timeframe-window").trigger("timeframe:change"),e===!1&&$("#timeframe-window").val("custom").change()}),$("#timeframe-window").change(function(t){var a,r=moment(),s=moment();switch($(this).val()){case"60m":a=s.subtract(60,"minutes"),ARGUX_TIMEFRAME_INTERVAL=60;break;case"6h":a=s.subtract(6,"hours"),ARGUX_TIMEFRAME_INTERVAL=120;break;case"12h":a=s.subtract(12,"hours"),ARGUX_TIMEFRAME_INTERVAL=300;break;case"24h":a=s.subtract(24,"hours"),ARGUX_TIMEFRAME_INTERVAL=600;break;case"7d":a=s.subtract(7,"days"),ARGUX_TIMEFRAME_INTERVAL=3600;break;case"1M":a=s.subtract(1,"months"),ARGUX_TIMEFRAME_INTERVAL=14400;break;case"custom":break;default:alert("invalid timeframe")}"custom"!==$(this).val()&&(e=!0,$("#timeframe-end").data("DateTimePicker").maxDate(moment()),$("#timeframe-start").data("DateTimePicker").date(a),$("#timeframe-end").data("DateTimePicker").date(r),e=!1)}),$("#timeframe-window").val("60m").change()}),host={get_host_overview:function(e){rest.call({url:ARGUX_BASE+"/rest/1.0/host",success:e.success,error:e.error,complete:e.complete})},get_host_items:function(e){if(void 0===e.hostname)throw"Hostname argument missing";rest.call({url:ARGUX_BASE+"/rest/1.0/host/"+e.hostname+"?alerts=false&items=true",success:e.success,error:e.error,complete:e.complete})},get_host_alerts:function(e){if(void 0===e.hostname)throw"Hostname argument missing";rest.call({url:ARGUX_BASE+"/rest/1.0/host/"+e.hostname+"?alerts=true&items=false",success:e.success,error:e.error,complete:e.complete})},create:function(e){if(void 0===e.hostname)throw"Hostname argument missing";void 0===e.description?description="":description=e.description,void 0===e.addresses?addresses=[]:addresses=e.addresses,data={description:description,address:addresses},rest.call({url:ARGUX_BASE+"/rest/1.0/host/"+e.hostname,type:rest.CallType.CREATE,data:data,success:e.success,error:e.error,complete:e.complete})},get_addresses:function(e){if(void 0===e.hostname)throw"Hostname argument missing";rest.call({url:ARGUX_BASE+"/rest/1.0/host/"+e.hostname+"/addr",success:e.success,error:e.error,complete:e.complete})},get_groups:function(e){rest.call({url:ARGUX_BASE+"/rest/1.0/hostgroup",success:e.success,error:e.error,complete:e.complete})}},monitors={get_monitors:function(e){rest.call({url:ARGUX_BASE+"/rest/1.0/monitor/"+e.type,success:e.success,complete:e.complete})},remove:function(e){if(void 0===e.hostname)throw"Hostname argument missing";if(void 0===e.address)throw"address argument missing";rest.call({url:ARGUX_BASE+"/rest/1.0/monitor/"+ARGUX_MONITOR_TYPE+"/"+e.hostname+"/"+e.address,type:rest.CallType.DELETE})},create:function(e){if(void 0===e.hostname)throw"Hostname argument missing";if(void 0===e.address)throw"address argument missing";void 0===e.options&&(e.options={}),void 0===e.active&&(e.active=!0),data={options:e.options,active:e.active},rest.call({url:ARGUX_BASE+"/rest/1.0/monitor/"+ARGUX_MONITOR_TYPE+"/"+e.hostname+"/"+e.address,type:rest.CallType.CREATE,data:data,success:e.success,error:e.error})}},user={get_users:function(e){rest.call({url:ARGUX_BASE+"/rest/1.0/admin/user",success:e.success,error:e.error,complete:e.complete})},create:function(e){if(void 0===e.username)throw"Username argument missing";if(void 0===e.password)throw"Password argument missing";data={password:e.password},rest.call({url:ARGUX_BASE+"/rest/1.0/admin/user/"+e.username,type:rest.CallType.CREATE,data:data,success:e.success,error:e.error,complete:e.complete})},remove:function(e){if(void 0===e.username)throw"Username argument missing";rest.call({url:ARGUX_BASE+"/rest/1.0/admin/user/"+e.username,type:rest.CallType.DELETE,success:e.success,error:e.error,complete:e.complete})}},$(function(){$(".btn-graph-full").click(function(){$("#graph-full-modal").modal("show");var e=$(this).data("graphid"),t=$("#graph-full-chart-body"),a=$("<canvas/>");t.empty(),t.append(a),t.data("graphid",e);var r=a[0].getContext("2d"),s=$.extend(!0,{},history_chart_config),o=new Chart(r,s);update_chart(t,o,s,!1)}),$(".argux-chart").each(function(e){var t=$(this),a=t.children(".chart-body"),r=$("<canvas/>");a.append(r);var s=r[0].getContext("2d"),o=$.extend(!0,{},history_chart_config),i=new Chart(s,o);$("#timeframe-window").on("timeframe:change",function(e){update_chart(t,i,o,!1)}),update_chart(t,i,o,!0)})});