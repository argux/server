$(function(){function e(e){var t=$("#users");t.empty(),$.each(e.users,function(e,n){t.append("<tr><td>"+n.name+"</td><td>-</td></tr>")})}function t(){}function n(){}"admin.users"===ARGUX_ACTION&&(user.get_users({success:e,complete:t}),$("#user-form").submit(function(e){e.preventDefault(),user.create({username:$("#user-name").val(),error:n})}))});
