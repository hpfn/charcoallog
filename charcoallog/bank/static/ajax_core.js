$(function() {
    var old_money = 0;
    var old_account = 0;
    // aqui o valor padrão deve ser 'delete/'
    // e ajax_post sera renoamedo para 'update/'
    var url_ajax = 'ajax_post/';

    var checked = function() {
        var n = $("input:checked").length;
        console.log(n);
        if ( n === 1 ) {
            // como definir qual botao?
            $("#botao").attr('value', 'Update');
            url_ajax = 'update';
            $(this).parents("table").find('input').removeAttr('readonly');
        }
        else {
            $("#botao").attr('value', 'Delete');
            url_ajax = 'delete';
            $(this).parents("table").find('input').attr('readonly', true);
        }

    };
    $("input[type=checkbox]").on('click', checked);

    // isso vai ser substituido por checked - acima
    $("#bank_box_line3 input").bind('click', function() {
        if ( $(this).val() == 'update') {
            $(this).parents("table").find('input').removeAttr('readonly');
        }
        if ( $(this).val() == 'remove') {
            $(this).parents("table").find('input').attr('readonly', true);
        }
    });
    $("#bank_box_line3 input").focusin(function() {
        if ( Number.isFinite(Number($(this).val())) ) {
            old_money = $(this).val();
        }
        if ( $(this).attr("id") == 'payment') {
            old_account = $(this).val();
            //console.log(old_account);
        }
    });
    $("#bank_box_line3 input").focusout(function() {
        if ( $(this).val() < 0 ) {
            $(this).css('color', 'red');
        } else {
            $(this).css('color', 'black');
        }
    });


    $("#bank_box_line3 form").on('submit', function(e) {
        e.preventDefault();
        var data_v = $(this).serializeArray();

        $.post({
            url: url_ajax,
            data: data_v,
            success: function(content, data) {
                function red_css(number, id_name) {
                    if (Number(number) < 0) {
                        $(id_name).css('color', 'red');
                    } else {
                        $(id_name).css('color', 'black');
                    }
                }

                if (content.no_account) {
                    alert(content.message);
                } else {
                    var not_present = true;
                    $.each(content.accounts, function(index, value) {
                        if ( old_account ) {
                            if ( index == old_account ) {
                                //console.log('false para old_account');
                                not_present = false;
                            }
                        } else {
                            if ( index == data_v[7].value ) {
                                //console.log('false para data_v');
                                not_present = false;
                            }
                        }

                        $("[id='"+index+"']").text(value['money__sum']);
                        red_css(value['money__sum'], "[id='"+index+"']");

                    });

                    $("#left").text(content.whats_left);
                    red_css(content.whats_left, "#left");

                    //console.log(old_account);
                    //console.log(data_v[7].value);
                    console.log(not_present);
                    if ( not_present ) {
                        if ( old_account) {
                            $("[class='"+old_account+"']").remove();
                        } else {
                            $("[class='"+data_v[7].value+"").remove();
                        }

                    }

                    //var new_total_value = content.total_line3;
                    //$("#total").text(new_total_value);
                    //red_css(new_total_value, "#total");

                    function total_value(old_v, new_v) {
                        // update Total in line3.html
                        var old_total_value = $("#total").text().trim();
                        var old_total_value_less_old_money = Number(old_total_value) - Number(old_v);
                        var new_total_value = Number(old_total_value_less_old_money) + Number(new_v);
                        $("#total").text(new_total_value);
                        red_css(new_total_value, "#total");
                    }

                    if ( data_v[8].value == 'remove' ) {
                        $('#'+data_v[2].value).remove();
                        total_value(data_v[4].value, 0);
                    }

                    if ( data_v[8].value == 'update' ) {
                        // form back to default
                        $('#'+data_v[2].value + ' input:radio[name=update_rm]')[1].checked = true;
                        $('#'+data_v[2].value + " input").attr('readonly', 'true');
                        //console.log(old_money);
                        if ( old_money ) {
                            total_value(old_money, data_v[4].value);
                        }
                    }
                }
            },
            error: function(content) {
                console.log(content);
            },
        });
    });
});