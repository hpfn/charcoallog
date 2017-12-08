$(function() {
    var old_money = 0;
    var old_account = 0;
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
        if ( $(this).attr("id") == 'payment') {
            old_account = $(this).val();
            console.log("payment");
            //var old_account = $("[id='payment']").val();
            console.log(old_account);
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
        console.log(data_v);
        //console.log('account name');
        console.log(old_account);

        $.post({
            url: '/',
            data: data_v,
            success: function(content) {
                function whats_left() {
                    // update value
                    var tentativa = $('#box_line1').text().trim();
                    tentativa = tentativa.split(' ');
                    tentativa = tentativa.filter(Number);
                    tentativa.pop();
                    var total_left = 0;
                    for (var i = 0; i < tentativa.length; i++) {
                        tentativa[i] = tentativa[i].trim();
                        total_left = total_left + Number(tentativa[i]);
                    }
                    $('#left').text(total_left);
                    if (Number(total_left) < 0) {
                        $("#left").css('color', 'red');
                    }

                }
                if ( data_v[8].value == 'remove' ) {
                    $('#'+data_v[2].value).remove();
                    // update value. line1.html
                    var old_total_account = $("[id='"+data_v[7].value+"']").text().trim();
                    var less_old_money = Number(old_total_account) - Number(data_v[4].value);
                    $("[id='"+data_v[7].value+"']").text(less_old_money);
                    if (Number(less_old_money) < 0) {
                        $("[id='"+data_v[7].value+"']").css('color', 'red');
                    }
                    whats_left();
                }
                if ( data_v[8].value == 'update' ) {
                    // form back to default
                    $('#'+data_v[2].value + ' input:radio[name=update_rm]')[1].checked = true;
                    $('#'+data_v[2].value + " input").attr('readonly', 'true');
                    if ( old_account ) {
                        if ( old_money ) {
                            old_account_money = $("[id='"+old_account+"']").text().trim();
                            old_actual_money = Number(old_account_money) - Number(old_money);
                            $("[id='"+old_account+"']").text(old_actual_money);
                            old_money = 0;
                        } else {
                            old_account_money = $("[id='"+old_account+"']").text().trim();
                            old_actual_money = Number(old_account_money) - Number(data_v[4].value);
                            $("[id='"+old_account+"']").text(old_actual_money)
                        }
                        new_account_money = $("[id='"+data_v[7].value+"']").text().trim();
                        new_actual_money = Number(new_account_money) + Number(data_v[4].value);
                        $("[id='"+data_v[7].value+"']").text(new_actual_money);
                        whats_left();
                        old_account = 0;
                    } else if ( old_money ) {
                        // update value. line1.html
                        var old_total_account = $("[id='"+data_v[7].value+"']").text().trim();
                        var less_old_money = Number(old_total_account) - Number(old_money);
                        var account_1 = Number(less_old_money) + Number(data_v[4].value);
                        $("[id='"+data_v[7].value+"']").text(account_1);
                        if (Number(account_1) < 0) {
                            $("[id='"+data_v[7].value+"']").css('color', 'red');
                        }
                        whats_left();
                        old_money = 0;
                    }
                }
            },
            error: function(content) {
                console.log(content);
            },
        });
    });
});