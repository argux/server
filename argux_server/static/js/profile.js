var bookmarks;$(function(){function o(o){$(".bookmark-remove").click(function(){var o=$(this).parents("tr").data("bookmark");$("#remove-bookmark").val(o),$("#remove-bookmark-message").text('Do you want to remove the bookmark "'+o+'"'),$("#remove-bookmark-modal").modal("show")})}function t(o){bookmarks="desc"===VIEW_SORT?o.bookmarks.sort(function(o,t){return o.title<t.title}):o.bookmarks.sort(function(o,t){return o.title>=t.title}),a()}function a(){list=$("#bookmark-list-body"),list.empty(),bookmarks.length>0?$.each(bookmarks,function(o,t){list.append('<tr data-bookmark="'+t.id+'"><td><a class="host" href="'+t.url+'"><span class="glyphicon glyphicon-bookmark"></span> '+t.title+'</a><div class="pull-right"><a href="#" class="bookmark-remove"><span class="glyphicon glyphicon-remove"></span></a></div></td></tr>')}):list.append("<tr><td><em>Empty</em></tr>"),o()}"bookmarks"===ACTION&&(user.get_bookmarks({success:t}),$(".bookmarks-sort").click(function(o){VIEW_SORT=$(this).data("direction"),"desc"===VIEW_SORT?(bookmarks=bookmarks.sort(function(o,t){return o.title<t.title}),$(".bookmarks-sort-desc").addClass("active"),$(".bookmarks-sort-asc").removeClass("active")):(bookmarks=bookmarks.sort(function(o,t){return o.title>=t.title}),$(".bookmarks-sort-asc").addClass("active"),$(".bookmarks-sort-desc").removeClass("active")),a()}),$("#remove-bookmark-form").submit(function(o){user.delete_bookmark({bookmark:$("#remove-bookmark").val()}),$("#remove-bookmark-modal").modal("hide"),user.get_bookmarks({success:t})})),"details"===ACTION});
