$(function() {
    $("#box_line3 form").on('submit', function(e) {
        e.preventDefault();
        var data_v = $(this).serializeArray();

        $('input').attr('readonly', 'true');

        if ( data_v[8].value == 'remove' ) {
            $('#'+data_v[2].value).remove();
        }
    });
});