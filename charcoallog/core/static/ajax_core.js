$(function() {
    var old_money;
    $("#box_line3 input").bind('click', function() {
        if ( $(this).val() == 'update') {
            //console.log( $(this).val() );
            //console.log("clicked");
            $(this).parents("table").find('input').removeAttr('readonly');
        }
    });
    $("#box_line3 input").focusin(function() {
        if ( Number.isFinite(Number($(this).val())) ) {
            old_money = $(this).val();
            //console.log('focus in');
            //console.log(old_money);
        }
    });
    $("#box_line3 input").focusout(function() {
        if ( $(this).val() < 0 ) {
            $(this).css('color', 'red');
        } else {
            $(this).css('color', 'black');
        }
    });


    $("#box_line3 form").on('submit', function(e) {
        e.preventDefault();
        var data_v = $(this).serializeArray();

        $.post({
            url: '/',
            data: data_v,
            success: function(content) {
                //console.log("old money before submit")
                //console.log(old_money);
                if ( data_v[8].value == 'remove' ) {
                    $('#'+data_v[2].value).remove();
                }
                if ( data_v[8].value == 'update' ) {
                    $('#'+data_v[2].value + ' input:radio[name=update_rm]')[1].checked = true;
                    $('#'+data_v[2].value + " input").attr('readonly', 'true');
                    // update total of each account. line1.html
                    var old_total_account = $('#'+data_v[7].value).text().trim();
                    var less_old_money = Number(old_total_account) - Number(old_money);
                    var account_1 = Number(less_old_money) + Number(data_v[4].value);
                    $('#'+data_v[7].value).text(account_1);
                    //console.log('old total account');
                    //console.log(old_total_account);
                    //console.log('valor antigo');
                    //console.log(old_money);
                    //console.log('total antigo - valor antigo');
                    //console.log(less_old_money);
                    //console.log('resultado da op');
                    //console.log(account_1);
                    var tentativa = $('#box_line1').text().trim();
                    tentativa = tentativa.split(' ');


                    tentativa = tentativa.filter(Number);


//                    console.log(tentativa[0].trim());
                    //console.log(tentativa[1].trim());
                    //console.log(tentativa[2].trim());
                    //console.log(tentativa[55].trim());
                    console.log(tentativa.length);
                    for (var i = 0; i < tentativa.length; i++) {
                        console.log(tentativa[i].trim());
                    }
                    $('#left').text(tentativa[0]);
                    //console.log(nova_tentativa);
                    //console.log();
                    //console.log(data_v[9].value);
                }
            },
            error: function(content) {
                console.log(content);
            },
        });
    });
});