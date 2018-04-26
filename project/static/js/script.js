(function() {
  $(function() {
    return $('.notes').isotope({
      itemSelector: '.note',
      layoutMode: 'masonry'
    });
  });

}).call(this);
