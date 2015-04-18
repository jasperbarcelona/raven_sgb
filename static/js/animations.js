$(document).ready(function(){

initial_data();

$('.clockpicker').clockpicker({
    autoclose: true,
});

$('.clockpicker-top').clockpicker({
    autoclose: true,
    placement: 'top'
});

$('#confirm-send').attr('disabled',true);
var height = $(window).height()-72;
$("#main-content").css("height",height);
$("tbody").css("height",height-40);

$(window).resize(function(){
    var height = $(window).height()-72;
    $("#main-content").css("height",height);
$("tbody").css("height",height-40);
});

$('#message').on('keyup', function(){
    if (!$.trim($(this).val())) {
        $('#send').attr('disabled',true);
    }
    else if (this.value){
        $('#send').removeAttr('disabled');
    }
});

$('#confirm-modal').on('hidden.bs.modal', function () {
    $('#message-confirm-password').val('');
    $('#confirm-send').attr('disabled',true);
});


$('#message-confirm-password').on('keyup', function(){
    if (!$.trim($(this).val())) {
        $('#confirm-send').attr('disabled',true);
    }
    else if (this.value){
        $('#confirm-send').removeAttr('disabled');
    }
});

$('.time').on('change', function(){
    $('#save-sched').removeAttr('disabled');
});

$('#schedule-modal').on('hidden.bs.modal', function () {
    reset_data();
    $('#save-sched').attr('disabled',true);
});

$('#add-user-modal').on('hidden.bs.modal', function () {
    clear_data();
    $('#save-user').attr('disabled',true);
});

$('#add-user-cancel').on('click', function () {
    clear_data();
    $('#save-user').attr('disabled',true);
});

$('#sched-cancel').on('click', function () {
    reset_data();
    $('#save-sched').attr('disabled',true);
});

$('#search-btn').on('click', function () {
    var $this = jQuery(this);
    if ($this.data('activated')) return false;  // Pending, return
        $this.data('activated', true);
        setTimeout(function() {
            $this.data('activated', false)
        }, 500); // Freeze for 500ms
        
    if ((typeof searchStatus === 'undefined') || (searchStatus == 'off')){
        $('tbody').animate({'margin-top':'35px'},300);
        searchStatus = 'on'
    }
    else{
        $('tbody').animate({'margin-top':'0px'},300);
        searchStatus = 'off'
    }
    
});

$('#refresh-btn').on('click', function(){
    $('#refresh-btn span').css({'display':'none'});
    $('#refresh-btn').css({'background-image':'url(../static/images/preloader_gray.png)','background-repeat': 'no-repeat','background-position': 'center'});
});

$('#save-sched').on('click', function(){
    $('#save-sched span').css({'display':'none'});
    $('#save-sched').css({'background-image':'url(../static/images/preloader_white.png)','background-repeat': 'no-repeat','background-position': 'center'});
    initial_data()
    $.post('/sched',{
        primary_morning_start:primary_morning_start,
        primary_morning_end:primary_morning_end,
        junior_morning_start:junior_morning_start,
        junior_morning_end:junior_morning_end,
        senior_morning_start:senior_morning_start,
        senior_morning_end:senior_morning_end,
        primary_afternoon_start:primary_afternoon_start,
        primary_afternoon_end:primary_afternoon_end,
        junior_afternoon_start:junior_afternoon_start,
        junior_afternoon_end:junior_afternoon_end,
        senior_afternoon_start:senior_afternoon_start,
        senior_afternoon_end:senior_afternoon_end,
    },
    function(data){
        initial_data();
        $('#save-sched').attr('disabled',true);
        $('#save-sched').css({'background-image':'none'});
        $('#save-sched span').show();
    });
});

function reset_data(){
    $('#primary_morning_start').val(primary_morning_start);
    $('#primary_morning_end').val(primary_morning_end);
    $('#junior_morning_start').val(junior_morning_start);
    $('#junior_morning_end').val(junior_morning_end);
    $('#senior_morning_start').val(senior_morning_start);
    $('#senior_morning_end').val(senior_morning_end);

    $('#primary_afternoon_start').val(primary_afternoon_start);
    $('#primary_afternoon_end').val(primary_afternoon_end);
    $('#junior_afternoon_start').val(junior_afternoon_start);
    $('#junior_afternoon_end').val(junior_afternoon_end);
    $('#senior_afternoon_start').val(senior_afternoon_start);
    $('#senior_afternoon_end').val(senior_afternoon_end);
}

function initial_data(){
    primary_morning_start = $('#primary_morning_start').val();
    primary_morning_end = $('#primary_morning_end').val();
    junior_morning_start = $('#junior_morning_start').val();
    junior_morning_end = $('#junior_morning_end').val();
    senior_morning_start = $('#senior_morning_start').val();
    senior_morning_end = $('#senior_morning_end').val();
    primary_afternoon_start = $('#primary_afternoon_start').val();
    primary_afternoon_end = $('#primary_afternoon_end').val();
    junior_afternoon_start = $('#junior_afternoon_start').val();
    junior_afternoon_end = $('#junior_afternoon_end').val();
    senior_afternoon_start = $('#senior_afternoon_start').val();
    senior_afternoon_end = $('#senior_afternoon_end').val();
}

function clear_data(){
    $('#add_last_name').val('');
    $('#add_first_name').val('');
    $('#add_middle_name').val('');
    $('#add_level').val('');
    $('#add_section').val('');
    $('#add_contact').val('');
    $('#add_id_no').val('');
}

$('.add-user-modal-body .form-control').on('change', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_last_name').val() != "") && ($('#add_first_name').val() != "") && ($('#add_middle_name').val() != "") && 
        (re.test($('#add_last_name').val())) && (re.test($('#add_first_name').val())) && (re.test($('#add_middle_name').val()))&& 
        ($('#add_level').val() != null) && ($('#add_section').val() != null) && ($('#add_contact').val() != null) &&
        (!isNaN($('#add_contact').val())) &&  ($('#add_contact').val().length == 11) ){
        $('#save-user').removeAttr('disabled'); 
    }
    else{
        $('#save-user').attr('disabled',true);
    }
});

$('.add-user-modal-body .form-control').on('keyup', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_last_name').val() != "") && ($('#add_first_name').val() != "") && ($('#add_middle_name').val() != "") && 
        (re.test($('#add_last_name').val())) && (re.test($('#add_first_name').val())) && (re.test($('#add_middle_name').val()))&& 
        ($('#add_level').val() != null) && ($('#add_section').val() != null) && ($('#add_contact').val() != null) &&
        (!isNaN($('#add_contact').val())) &&  ($('#add_contact').val().length == 11) ){
        $('#save-user').removeAttr('disabled'); 
    }
    else{
        $('#save-user').attr('disabled',true);
    }
});


$('#save-user').on('click', function(){
    $('#save-user span').css({'display':'none'});
    $('#save-user').css({'background-image':'url(../static/images/preloader_white.png)','background-repeat': 'no-repeat','background-position': 'center'});
    
    var last_name = $('#add_last_name').val();
    var first_name = $('#add_first_name').val();
    var middle_name = $('#add_middle_name').val();
    var level = $('#add_level').val();
    var section = $('#add_section').val();
    var contact = $('#add_contact').val();
    var id_no = $('#add_id_no').val();

    $.post('/user/add',{
        last_name:last_name,
        first_name:first_name,
        middle_name:middle_name,
        level:level,
        section:section,
        contact:contact,
        id_no:id_no
    },
    function(data){
        clear_data();
        $('#save-user').attr('disabled',true);
        $('#save-user').css({'background-image':'none'});
        $('#save-user span').show();
    });
});


});