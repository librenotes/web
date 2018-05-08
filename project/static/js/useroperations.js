$('#editModal').on('show.bs.modal', function (event) {

    function unescapeHtml(safe) {
        return safe.replace(/&amp;/g, '&')
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>')
            .replace(/&quot;/g, '"')
            .replace(/&#039;/g, "'");
    }

    let button = $(event.relatedTarget)
    let id = button.data('whatever')
    let title = document.getElementById("t" + id).innerHTML;
    let body = document.getElementById("b" + id).innerHTML;
    let privacy = document.getElementById("p" + id).getAttribute("value");
    let categories = document.getElementById("c" + id).innerHTML;
    let modal = $(this);
    modal.find('#edit-title').val(unescapeHtml(title));
    modal.find('#edit-note').val(unescapeHtml(body));
    modal.find('#edit-id').val(id);

    modal.find('#edit-category').val(unescapeHtml(categories));
    if (privacy === "True") {
        modal.find('#edit-privacy-toggle').addClass("active");
        modal.find('#edit-isprivate').prop('checked', true);

    }
    else {
        modal.find('#edit-privacy-toggle').removeClass("active");
        modal.find('#edit-isprivate').prop('checked', false);

    }
    modal.find('#edit-privacy-toggle').click(function () {
        var checked = modal.find('#edit-isprivate').prop('checked');
        modal.find('#edit-isprivate').prop('checked', !checked);
    });
});
$('#deleteModal').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let id = button.data('whatever');
    let modal = $(this);
    modal.find('#delete-id').val(id);
});

function textFilter() {
    var input = document.getElementById("myInput");
    var filter = input.value;
    var content = $(this).find('span.content').text();
    var categories = $(this).find('span.categories').text();
    var titles = $(this).find('h4.title').text();
    console.log(content);
    return content.indexOf(filter) > -1 || categories.indexOf(filter) > -1 || titles.indexOf(filter) > -1;
}

function myFunction() {
    $('#all_notes').isotope({filter: textFilter});
}
