(function () {
    $(function () {
        return $('.notes').isotope({
            itemSelector: '.note',
            layoutMode: 'masonry'
        });
    });

}).call(this);

function textFilter() {
    var input = document.getElementById("myInput");
    var filter = input.value;
    var content = $(this).find('span.content').text();
    var categories = $(this).find('span.categories').text();
    var titles = $(this).find('h4.title').text();
    return content.indexOf(filter) > -1 || categories.indexOf(filter) > -1 || titles.indexOf(filter) > -1;
}

function myFunction() {
    $('#all_notes').isotope({filter: textFilter});
}

