$(function() {
    $("#box_line3 form").on('submit', function(e) {
        e.preventDefault();
        var data_v = $(this).serializeArray();

        $('#'+data_v[2]).attr('readonly', 'true');

        $.post({
            url: '/',
            data: data_v,
            success: function(content) {
                if ( data_v[8].value == 'remove' ) {
                    $('#'+data_v[2].value).remove();
                }
            },
            error: function(content) {
                console.log(content);
            },
        });
    });
});