/*!
 * script.js
 *
 * Licensed GPLv3
 *
 * https://librenotes.org
 *
 */


(function () {
    $(function () {
        return $('.notes').isotope({
            itemSelector: '.note',
            layoutMode: 'masonry'
        });
    });

}).call(this);

function textFilter() {
    let input = document.getElementById("myInput");
    let filter = input.value.toLowerCase();
    let content = $(this).find('span.content').text().toLowerCase();
    let categories = $(this).find('span.categories').text().toLowerCase();
    let titles = $(this).find('h4.title').text().toLowerCase();
    return content.indexOf(filter) > -1 || categories.indexOf(filter) > -1 || titles.indexOf(filter) > -1;
}

function myFunction() {
    $('#all_notes').isotope({filter: textFilter});
}
