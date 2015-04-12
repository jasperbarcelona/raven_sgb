$(document).ready(function(){

var height = $(window).height()-112;
$("#main-content").css("height",height);

$(window).resize(function(){
    var height = $(window).height()-112;
    $("#main-content").css("height",height);
});

$('#message').on('keyup', function(){
    if (!$.trim($(this).val())) {
        $('#send').attr('disabled',true);
    }
    else if (this.value){
        $('#send').removeAttr('disabled');
    }
});

$('#message-confirm-password').on('keyup', function(){
    if (!$.trim($(this).val())) {
        $('#confirm-send').attr('disabled',true);
    }
    else if (this.value){
        $('#confirm-send').removeAttr('disabled');
    }
});

});