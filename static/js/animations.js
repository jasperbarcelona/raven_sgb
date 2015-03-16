$(document).ready(function(){

var height = $(window).height()-110;
$("#main-content").css("height",height);

$(window).resize(function(){
	var height = $(window).height()-110;
	$("#main-content").css("height",height);
});

});