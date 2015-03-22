var tab = 'log'
function change_tab(page){
tab = page;
}

function load_data(){
$.post('/data',
function(data){
$('#table-container').html(data);
});
}

function change_view(view){
var view = view;
$.post('/view',{view:view},
function(data){
$('#table-container').html(data);
window.location.assign("/");
});
}