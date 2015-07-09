$( document ).ready(function() {
    $("#repo_table").DataTable({
        "ajax": "/manage/registry/repos",
        "columns": [
            {"data": "repository"},
            {"data": "image"}
        ]
    });
});
