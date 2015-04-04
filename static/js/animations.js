$(document).ready(function(){

var height = $(window).height()-112;
$("#main-content").css("height",height);

$(window).resize(function(){
	var height = $(window).height()-112;
	$("#main-content").css("height",height);
});

});