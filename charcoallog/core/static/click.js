$(function() {
    $("#box_line3 input").bind('click', function() {
        if ( $(this).val() == 'update') {
            //console.log( $(this).val() );
            //console.log("clicked");
            $(this).parents("table").find('input').removeAttr('readonly');
        }
    });
    $("#box_line3 input").focusout(function() {
        if ( $(this).val() < 0 ) {
            $(this).css('color', 'red');
        }
    });
});
