function load_data(){
$.post('/data',
function(data){
$('#main-content').html(data);
});
}