$(function() {
    $("#box_line3 form").on('submit', function(e) {
        e.preventDefault();
        var data_v = $(this).serializeArray();

        $.post({
            url: '/',
            data: data_v,
            success: function(content) {
                if ( data_v[8].value == 'remove' ) {
                    $('#'+data_v[2].value).remove();
                }
                if ( data_v[8].value == 'update' ) {
                    //$('#'+data_v[2].value + ' input:radio[name=update_rm]').attr('checked', false);
                    $('#'+data_v[2].value + ' input:radio[name=update_rm]')[1].checked = true;
                    $('#'+data_v[2].value + " input").attr('readonly', 'true');
                    var account_1 = $('#'+data_v[7].value).text().trim();
                    account_1 = Number(data_v[4].value) + Number(account_1) ;
                    $('#'+data_v[7].value).text(account_1);
                    console.log(account_1);
                    console.log(data_v[7].value);
                }
            },
            error: function(content) {
                console.log(content);
            },
        });
    });
});