$(document).ready(function(){

initial_data();
searchStatus = 'off'

$('.loading').hide();
$('.add-user-footer-left').hide();
$('#snackbar').hide();
$('.id-loader').hide();

$(window).load(function() {
    $('#intro-mask').hide();
    $('#intro').fadeOut();
});

$( ".datepicker " ).datepicker({
  dateFormat: "MM dd, yy"
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

$('.add-modal').on('hidden.bs.modal', function () {
    clear_data();
    $('.save-btn').attr('disabled',true);
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
        resize_tbody($(window).height()-49,110);
        searchStatus = 'on'
    }
    else{
        $('.search-panel').hide();
        resize_tbody($(window).height()-49,40);
        $(".search-text").val('');
        searchStatus = 'off'
        back_home()
    }
    
});

$('#save-sched').on('click', function(){
    save_sched();
});

$('#add-student-modal .add-user-modal-body .form-control').on('change', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_student_last_name').val() != "") && ($('#add_student_first_name').val() != "") && ($('#add_student_middle_name').val() != "") && 
        (re.test($('#add_student_last_name').val())) && (re.test($('#add_student_first_name').val())) && (re.test($('#add_student_middle_name').val())) && 
        ($('#add_student_level').val() != null) && ($('#add_student_section').val() != null) && ($('#add_student_contact').val() != null) &&
        (!isNaN($('#add_student_contact').val())) && ($('#add_student_contact').val().length == 11) && ($('#student-id-error').text().length == 0)  &&
        ($('#add_student_id_no').val().length == 10)){
        $('#save-student').removeAttr('disabled'); 
    }
    else{
        $('#save-student').attr('disabled',true);
    }
});

$('#add-user-modal .add-user-modal-body .form-control').on('change', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_user_last_name').val() != "") && ($('#add_user_first_name').val() != "") && 
        ($('#add_user_middle_name').val() != "") && (re.test($('#add_user_last_name').val())) && 
        (re.test($('#add_user_first_name').val())) && (re.test($('#add_user_middle_name').val())) &&
        ($('#user-id-error').text().length == 0) && ($('#add_user_id_no').val().length == 10)){
        $('#save-user').removeAttr('disabled'); 
    }
    else{
        $('#save-user').attr('disabled',true);
    }
});

$('#add-student-modal .add-user-modal-body .form-control').on('keyup', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_student_last_name').val() != "") && ($('#add_student_first_name').val() != "") && ($('#add_student_middle_name').val() != "") && 
        (re.test($('#add_student_last_name').val())) && (re.test($('#add_student_first_name').val())) && (re.test($('#add_student_middle_name').val())) && 
        ($('#add_student_level').val() != null) && ($('#add_student_section').val() != null) && ($('#add_student_contact').val() != null) &&
        (!isNaN($('#add_student_contact').val())) && ($('#add_student_contact').val().length == 11)){
        validate_student_form(true);
    }
    else{
        validate_student_form(false);
    }
});

$('#add-user-modal .add-user-modal-body .form-control').on('keyup', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_user_last_name').val() != "") && ($('#add_user_first_name').val() != "") && ($('#add_user_middle_name').val() != "") && 
        (re.test($('#add_user_last_name').val())) && (re.test($('#add_user_first_name').val())) && (re.test($('#add_user_middle_name').val()))){
        validate_user_form(true);
    }
    else{
        validate_user_form(false);
    }
});

$('#save-student').on('click', function(){
    $('#save-student').attr('disabled',true);
    $('#save-student span').css({'display':'none'});
    $('#save-student').css({'background-image':'url(../static/images/assets/white.GIF)','background-repeat': 'no-repeat','background-position': 'center'});

    var last_name = $('#add_student_last_name').val();
    var first_name = $('#add_student_first_name').val();
    var middle_name = $('#add_student_middle_name').val();
    var level = $('#add_student_level').val();
    var section = $('#add_student_section').val();
    var contact = $('#add_student_contact').val();
    var id_no = $('#add_student_id_no').val();
    save_student(last_name, first_name, middle_name, level, section, contact, id_no);
});

$('#save-user').on('click', function(){
    $('#save-user').attr('disabled',true);

    var last_name = $('#add_user_last_name').val();
    var first_name = $('#add_user_first_name').val();
    var middle_name = $('#add_user_middle_name').val();
    var id_no = $('#add_user_id_no').val();
    save_user(last_name, first_name, middle_name, id_no);
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