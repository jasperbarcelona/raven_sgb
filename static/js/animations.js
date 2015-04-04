$(document).ready(function(){

var page = $('#main-content');  // set to the main content of the page   
    $(window).mousewheel(function(event, delta, deltaX, deltaY){
        if (delta < 0) page.scrollTop(page.scrollTop() + 65);
        else if (delta > 0) page.scrollTop(page.scrollTop() - 65);
        return false;
    })

var height = $(window).height()-118;
$("#main-content").css("height",height);

$(window).resize(function(){
	var height = $(window).height()-118;
	$("#main-content").css("height",height);
});

});