$(document).ready(function(){

initial_data();
searchStatus = 'off'

$('.loading').hide();
$('.add-user-footer-left').hide();
$('#snackbar').hide();
$('#id-loader').hide();

$('tbody').css('overflow-y','scroll');

$(window).load(function() {
    $('#intro-mask').hide();
    $('#intro').fadeOut();
});

$('.search-panel').hide();

$('.clockpicker').clockpicker({
    autoclose: true,
});

$('.clockpicker-top').clockpicker({
    autoclose: true,
    placement: 'top'
});

$('#confirm-send').attr('disabled',true);

resize_tbody($(window).height()-49,40);

$(window).resize(function(){
    resize_tbody($(window).height()-49,40);
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
        $('.search-panel').show();
        resize_tbody($(window).height()-72,110);
        searchStatus = 'on'
    }
    else{
        $('.search-panel').hide();
        resize_tbody($(window).height()-72,40);
        $(".search-text").val('');
        searchStatus = 'off'
        back_home()
    }
    
});

$('#save-sched').on('click', function(){
    save_sched();
});

$('.add-user-modal-body .form-control').on('change', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_last_name').val() != "") && ($('#add_first_name').val() != "") && ($('#add_middle_name').val() != "") && 
        (re.test($('#add_last_name').val())) && (re.test($('#add_first_name').val())) && (re.test($('#add_middle_name').val())) && 
        ($('#add_level').val() != null) && ($('#add_section').val() != null) && ($('#add_contact').val() != null) &&
        (!isNaN($('#add_contact').val())) && ($('#add_contact').val().length == 11) && ($('#id-error').text().length == 0)  &&
        ($('#add_id_no').val().length == 10)){
        $('#save-user').removeAttr('disabled'); 
    }
    else{
        $('#save-user').attr('disabled',true);
    }
});

$('.add-user-modal-body .form-control').on('keyup', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_last_name').val() != "") && ($('#add_first_name').val() != "") && ($('#add_middle_name').val() != "") && 
        (re.test($('#add_last_name').val())) && (re.test($('#add_first_name').val())) && (re.test($('#add_middle_name').val())) && 
        ($('#add_level').val() != null) && ($('#add_section').val() != null) && ($('#add_contact').val() != null) &&
        (!isNaN($('#add_contact').val())) && ($('#add_contact').val().length == 11) && ($('#id-error').text().length == 0)  &&
        ($('#add_id_no').val().length == 10)){
        $('#save-user').removeAttr('disabled'); 
    }
    else{
        $('#save-user').attr('disabled',true);
    }
});

$('#save-user').on('click', function(){
    $('#save-user').attr('disabled',true);
    $('#save-user span').css({'display':'none'});
    $('#save-user').css({'background-image':'url(../static/images/assets/white.GIF)','background-repeat': 'no-repeat','background-position': 'center'});

    var last_name = $('#add_last_name').val();
    var first_name = $('#add_first_name').val();
    var middle_name = $('#add_middle_name').val();
    var level = $('#add_level').val();
    var section = $('#add_section').val();
    var contact = $('#add_contact').val();
    var id_no = $('#add_id_no').val();
    save_user(last_name, first_name, middle_name, level, section, contact, id_no);
});

$('.search-text').keypress(function(e) {
    if ((e.which !== 0) && (e.which != 13)) {
        show_search_load();
    }
});

$('.search-attendance').donetyping(function(){
    search_attendance()
});

$('.search-attendance').on('change', function(){
    search_attendance()
});

$('.search-logs').donetyping(function(){
    search_logs()
});

$('.search-logs').on('change', function(){
    search_logs()
});

$('.search-absent').donetyping(function(){
    search_absent()
});

$('.search-absent').on('change', function(){
    search_absent()
});

$('.search-late').donetyping(function(){
    search_late()
});

$('.search-late').on('change', function(){
    search_late()
});

});