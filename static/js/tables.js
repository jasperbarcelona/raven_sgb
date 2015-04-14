$(document).ready(function(){

var isPreviousEventComplete = true;

$('.tab-pane').scroll(function () {
    if($(this).scrollTop() + $(this).height() > (this.scrollHeight * .7))  {
        var that = this;
        if (isPreviousEventComplete) {
            load_next(String(that.getAttribute('id')));
        }
    }
});

function load_next(tab){
    isPreviousEventComplete = false;
    var data = tab
    $.post('/loadmore',{data:data},
    function(data){
        $('#'+tab).append(data);
        isPreviousEventComplete = true;
    });
}

});