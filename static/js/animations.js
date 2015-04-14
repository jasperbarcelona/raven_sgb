$(document).ready(function(){
$('#confirm-send').attr('disabled',true);
var height = $(window).height()-72;
$("#main-content").css("height",height);

$(window).resize(function(){
    var height = $(window).height()-72;
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

$('#confirm-modal').on('hidden.bs.modal', function () {
    $('#message-confirm-password').val('');
    $('#confirm-send').attr('disabled',true);
})

$('#message-confirm-password').on('keyup', function(){
    if (!$.trim($(this).val())) {
        $('#confirm-send').attr('disabled',true);
    }
    else if (this.value){
        $('#confirm-send').removeAttr('disabled');
    }
});

});