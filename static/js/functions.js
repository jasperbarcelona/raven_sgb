var tab = 'log'
function change_tab(page){
tab = page;
}

function textCounter(field,field2,maxlimit)
{
 var countfield = document.getElementById(field2);
 if ( field.value.length > maxlimit ) {
  field.value = field.value.substring( 0, maxlimit );
  return false;
 } else {
  countfield.value = "Remaining: " + (maxlimit - field.value.length);
 }
}

function blast_message(){
var message = $("#message").val();
var password = $("#message-confirm-password").val();
if ((navigator.onLine==true) && ($.trim($("#message").val()))) {
    $.post('/blast',{message:message,password:password},
    function(data){
    $('#status-modal-body').html(data);
    });
    $('.modal').modal('hide');
    $('#message-status-modal').modal('show');
}
else if (navigator.onLine==false) {
    alert('You are offline!');
}
else{
    alert('Message is empty!');
}
}





