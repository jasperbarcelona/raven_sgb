$(document).ready(function(){

var height = $(window).height()-118;
$("#main-content").css("height",height);

$(window).resize(function(){
	var height = $(window).height()-118;
	$("#main-content").css("height",height);
});

});