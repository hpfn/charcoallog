$(function() {
  $('.money-delete').on('click', function() {
    let url = $(this).data('url')
    let $this = $(this)
    $.get(url, function(data) {
      $this.parent().parent().remove()
    });
  });
});