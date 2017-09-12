$(function() {
    var rm;
    var form_rm;
    $("#box_line3 form").on('submit', function(e) {
        e.preventDefault();
        var data_v = $(this).serializeArray();

        console.log(data_v);

        $.each(data_v, function(i, field) {
            if ( field.name == "id") {
                form_rm = '#' + field.value;
            }
            if ( field.value == "remove") {
                console.log('SIMMMM');
                $(form_rm).remove();
            }
        });

        console.log($(data_v));
        $('input').attr('readonly', 'true');

        if ( $(data_v['update_rm']).val() == 'remove' ) {
            console.log('SIMMMM');
        }
    });
});