$(function() {
    var old_money = 0;
    var old_account = 0;
    var url_ajax = 'delete/';
    var form_method = 'DELETE';

    $("#bank_box_line3 input").bind('click', function() {
        if ( $(this).attr("id") == 'checkbox') {
                 console.log('checked');
                 var n = $("input:checked").length;
                 console.log(n);
                 if ( n === 1 ) {
                     $(this).parents("table").find('button').text('Update');
                     url_ajax = 'update/';
                     form_method = 'PUT';
                     $(this).parents("table").find('input').removeAttr('readonly');
                 }
                 else {
                     $(this).parents("table").find('button').text('Delete');
                     url_ajax = 'delete/';
                     form_method = 'DELETE';
                     $(this).parents("table").find('input').attr('readonly', true);
                 }
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
        var dict_form = {};
        // substituir totalmente uso de data_v?
        // o campo update é removido no Django
        // pela '.is_valid()' se passado o dict_form
        // e fica mais claro aqui que usar index aqui
        $.each(data_v,
            function(i, v) {
                dict_form[v.name] = v.value;
            }
        );

        console.log(data_v.length);
        console.log(data_v);
        //console.log(dict_form);

        //if ( data_v.length == 8 ) {
        //    var update = data_v.pop();
        //}
        //else {
        //    var update = 'no';
        //}

        $.ajax({
            url: url_ajax,
            type: form_method,
            data: JSON.stringify(dict_form),
            success: function(content, data) {
                function red_css(number, id_name) {
                    if (Number(number) < 0) {
                        $(id_name).css('color', 'red');
                    } else {
                        $(id_name).css('color', 'black');
                    }
                }

                if (content.js_alert) {
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
                            //if ( index == data_v[6].value ) {
                            if ( index == dict_form["payment"] ) {
                                //console.log('false para data_v');
                                not_present = false;
                            }
                        }

                        $("[id='"+index+"']").text(value['money__sum']);
                        red_css(value['money__sum'], "[id='"+index+"']");

                    });

                    $("#left").text(content.whats_left);
                    red_css(content.whats_left, "#left");

                    if ( not_present ) {
                        if ( old_account) {
                            $("[class='"+old_account+"']").remove();
                        } else {
                            //$("[class='"+data_v[6].value+"").remove();
                            $("[class='"+dict_form["payment"]+"").remove();
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

                    //if ( update == 'no' ) {
                    if ( typeof dict_form["update"] == "undefined" ) {
                        //$('#'+data_v[1].value).remove();
                        $('#'+dict_form["pk"]).remove();
                        //total_value(data_v[3].value, 0);
                        total_value(dict_form["money"], 0);

                    }
                    else {
                        //$('#'+data_v[1].value + " input").attr('readonly', 'true');
                        //$('#'+data_v[1].value + ' input:checkbox[name=update]').removeAttr('readonly');
                        //$('#'+data_v[1].value + ' input:checkbox[name=update]').prop('checked', false);
                        //$('#'+data_v[1].value + ' button').text('Delete');

                        $('#'+dict_form["pk"] + " input").attr('readonly', 'true');
                        $('#'+dict_form["pk"] + ' input:checkbox[name=update]').removeAttr('readonly');
                        $('#'+dict_form["pk"] + ' input:checkbox[name=update]').prop('checked', false);
                        $('#'+dict_form["pk"] + ' button').text('Delete');

                        url_ajax = 'delete/';
                        form_method = 'DELETE';

                        //console.log(old_money);
                        if ( old_money ) {
                            total_value(old_money, data_v[3].value);
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