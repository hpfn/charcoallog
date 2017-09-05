$(function() {
    $("#box_line3 input").bind('click', function() {
        if ( $(this).val() == 'update') {
            console.log( $(this).val() );
            console.log("clicked");
            console.log( $(this).parents("table").find('input').removeAttr('readonly') );
            //console.log( $(this).parent().parent().parent().find('#category').val() );
            //console.log( $(this).parent().parent().parent().parent().find('input').removeAttr('readonly') );
            //console.log( $(this).parent().parent().parent().parent().parent().find('#money').val() );
            //console.log( $(this).parent().parent().parent().parent().parent().parent().find('#date').val() );
            //console.log( $(this).parent().parent().parent().parent().parent().parent().parent().find('#id').val() );
            //console.log( $(this).parent().parent().parent().parent().parent().parent().parent().parent().find('#user_name').val() );

            //$('#payment').removeAttr('readonly');
        }
    });//$("input").attrRemove("readonly");
});
