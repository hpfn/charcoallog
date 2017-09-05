$(function() {
    $("#box_line3 form").on('submit', function(e) {
        e.preventDefault();
        var data_v = $(this).serialize();
        console.log(data_v);
        $('input').attr('readonly', 'true');
    });
});