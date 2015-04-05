var tab = 'log'
function change_tab(page){
tab = page;
}

function load_data(){
$.post('/data',
function(data){
$('#table-container').html(data);
$("#big-preloader-container").hide();
});
}

function change_view(view){
$("#big-preloader-container").show();
var view = view;
$.post('/view',{view:view},
function(data){
$('#table-container').html(data);
window.location.assign("/");
});
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