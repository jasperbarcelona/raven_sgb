$(document).ready(function(){

$('.table').tablesorter();

jQuery(function($) {
    $('#logs').bind('scroll', function() {
        if($(this).scrollTop() + $(this).innerHeight() >= this.scrollHeight) {  
            var data = 'logs'
            $.post('/test',{data:data},
            function(data){
            $('#logs').html(data);
            });
        }
    })
});

jQuery(function($) {
    $('#attendance').bind('scroll', function() {
        if($(this).scrollTop() + $(this).innerHeight() >= this.scrollHeight) {  
            var data = 'attendance'
            $.post('/test',{data:data},
            function(data){
            $('#attendance').html(data);
            });
        }
    })
});

jQuery(function($) {
    $('#absent').bind('scroll', function() {
        if($(this).scrollTop() + $(this).innerHeight() >= this.scrollHeight) {  
            var data = 'absent'
            $.post('/test',{data:data},
            function(data){
            $('#absent').html(data);
            });
        }
    })
});

jQuery(function($) {
    $('#late').bind('scroll', function() {
        if($(this).scrollTop() + $(this).innerHeight() >= this.scrollHeight) {  
            var data = 'late'
            $.post('/test',{data:data},
            function(data){
            $('#late').html(data);
            });
        }
    })
});

});