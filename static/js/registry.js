$( document ).ready(function() {
    $("#repo_table").DataTable({
        "ajax": "/manage/registry/repos",
        "columns": [
            {"data": "repository"},
            {"data": "image"},
            {"data": undefined,
             "render": function(data, type, full, meta) {
				var actionDiv = $("<div></div>");
				var tagsButton = $("<button id='"+full['image']+"'class='tag_button'></button>")
					.append("<span aria-hidden='true'></span>")
					.addClass("glyphicon glyphicon-tags");
				actionDiv.append(tagsButton);
				return actionDiv.html();
			}
	    }
        ]
    });
	$("#repo_table").on("click", ".tag_button", function(e) {
		console.log(e.target);
		location.href='/manage/registry/'+e.target.id+'/tags';
	});
});
