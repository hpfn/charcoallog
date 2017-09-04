$(function() {
    $('form').submit(function(e) {
        e.preventDefault();
        var data_v = $(this).serialize();
        console.log(data_v);
    });
});