$(document).ready(function(){

searchStatus = 'off'
profile_options = 'closed'

$('.loading').hide();
$('.add-user-footer-left').hide();
$('#snackbar').hide();
$('.id-loader').hide();
$('#profile-options').hide();
$('#message-modal-right-preloader').hide();
$('#message-modal-body-right').hide();

$(".menu-item-container").css('height',$(".menu-item-container").width());

$(window).load(function() {
    $('#intro-mask').hide();
    $('#intro').fadeOut();
});

$(".datepicker").datepicker({
    dateFormat: "MM dd, yy"
});

/*$(".datepicker").datepicker({
        dateFormat: 'MM yy',
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,

        onClose: function(dateText, inst) {
            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
            $(this).val($.datepicker.formatDate('MM yy', new Date(year, month, 1)));
        }
    });

    $(".datepicker").focus(function () {
        $(".ui-datepicker-calendar").hide();
        $("#ui-datepicker-div").position({
            my: "center top",
            at: "center bottom",
            of: $(this)
        });
    });*/

$('.add-user-modal-body .form-control').floatlabel({
    labelEndTop:'-2px'
});

$('.add-fee-modal-body .form-control').floatlabel({
    labelEndTop:'-2px'
});

$('.search-panel').hide();

$('.clockpicker').clockpicker({
    autoclose: true
});

$('.clockpicker-top').clockpicker({
    autoclose: true,
    placement: 'top'
});

$('#confirm-send').attr('disabled',true);

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

$('#collect-payment-modal').on('hidden.bs.modal', function () {
    $('#amountPaid').val('');
    $('#tenderedDoneBtn').attr('disabled',true);
    $('#amountPaid').css('border','1px solid #ccc');
});

$('#message-modal').on('hidden.bs.modal', function () {
    $('#message-modal-cover').hide();
    $('#new-message-btn').attr('disabled', false);
    $('.message-modal-dialog').css('width','600px');
    $('.message-row').css('padding-left','20px');
    $('.message-row').css('padding-right','20px');
    $('#message-modal-body-left').css('width','100%');
    $('#message-modal-body-right').hide();
    $('#message-modal-right-preloader').hide();
});

$('#message-status-modal').on('hidden.bs.modal', function () {
    open_messages();
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
    $('#save-sched').attr('disabled',true);
});

$('.calendar-time').on('change', function(){
    $('#save-calendar-sched').removeAttr('disabled');
});

$('.no-class-checkbox').on('change', function(){
    listen_to_checkbox();
});

$('#calendar-schedule-modal').on('hidden.bs.modal', function () {
    $('#save-calendar-sched').attr('disabled',true);
});

$('.add-modal').on('hidden.bs.modal', function () {
    clear_data();
    clear_fee_data();
    $('.save-btn').attr('disabled',true);
});

$('#compose-message-modal').on('shown.bs.modal', function () {
    $('#message').focus();
});

$('#confirm-modal').on('shown.bs.modal', function () {
    $('#message-confirm-password').focus();
});

$('#add-student-modal').on('shown.bs.modal', function () {
    $('#add_student_last_name').focus();
});

$('#add-user-modal').on('shown.bs.modal', function () {
    $('#add_user_id_no').focus();
});

$('#sched-cancel').on('click', function () {
    $('#save-sched').attr('disabled',true);
});

$('#tenderedDoneBtn').on('click', function () {
    var amount = $('#amountPaid').val();
    $('#tenderedDoneBtn').button('loading');
    collect_payment(amount);
});

$('#user-icon-container').on('click', function () {
    var $this = jQuery(this);
    if ($this.data('activated')) return false;  // Pending, return
    $this.data('activated', true);
    setTimeout(function() {
      $this.data('activated', false)
    }, 500); // Freeze for 500ms

    if ((typeof profile_options === 'undefined') || (profile_options == 'closed')){
        var travel_width = $('#profile-options').width();
        $('#user-icon-container').animate({'margin-right':travel_width+2});
        profile_options = 'open'
        setTimeout(function() {
            $('#profile-options').fadeIn();
        }, 500); // Freeze for 500ms
    }
    else{
        $('#profile-options').fadeOut();
        profile_options = 'closed'
        setTimeout(function() {
            $('#user-icon-container').animate({'margin-right':'0'});
        }, 500); // Freeze for 500ms
    }
});

$('#add-student-modal .add-user-modal-body .form-control').on('change', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_student_last_name').val() != "") && ($('#add_student_first_name').val() != "") && 
        (re.test($('#add_student_last_name').val())) && (re.test($('#add_student_first_name').val())) && 
        ($('#add_student_level').val() != null) && ($('#add_student_section').val() != null) && ($('#add_guardian_mobile').val() != null) &&
        ($('#add_guardian_last_name').val() != "") && ($('#add_guardian_first_name').val() != "") && ($('#add_guardian_middle_name').val() != "") &&
        ($('#add_guardian_relation').val() != "") && ($('#add_guardian_address').val() != "") && ($('#add_guardian_email').val() != "") &&
        (!isNaN($('#add_guardian_mobile').val())) && ($('#add_guardian_mobile').val().length == 11)){
        validate_student_form(true);
    }
    else{
        validate_student_form(false);
    }
});

$('#amountPaid').on('keyup', function () {
    if (($(this).val() != '') && (!isNaN($(this).val())) && (parseFloat($(this).val()) <= parseFloat($('#cashTotal').html()))){
        $('#tenderedDoneBtn').attr('disabled',false);
        $(this).css('border','1px solid #ccc');
    }
    else{
        $('#tenderedDoneBtn').attr('disabled',true);
        $(this).css('border','1px solid #d9534f');
    }
});

$('#add-student-modal .add-user-modal-body .form-control').on('keyup', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_student_last_name').val() != "") && ($('#add_student_first_name').val() != "") && 
        (re.test($('#add_student_last_name').val())) && (re.test($('#add_student_first_name').val())) && 
        ($('#add_student_level').val() != null) && ($('#add_student_section').val() != null) && ($('#add_guardian_mobile').val() != null) &&
        ($('#add_guardian_last_name').val() != "") && ($('#add_guardian_first_name').val() != "") && ($('#add_guardian_middle_name').val() != "") &&
        ($('#add_guardian_relation').val() != "") && ($('#add_guardian_address').val() != "") && ($('#add_guardian_email').val() != "") &&
        (!isNaN($('#add_guardian_mobile').val())) && ($('#add_guardian_mobile').val().length == 11)){
        validate_student_form(true);
    }
    else{
        validate_student_form(false);
    }
});

$('#add-fee-modal .add-fee-modal-body .form-control').on('keyup', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_fee_name').val() != "") && ($('#add_fee_price').val() != "") && (!isNaN($('#add_fee_price').val())) && 
        ($('#add_fee_category').val() != null)){
        $('#save-fee').attr('disabled',false);
    }
    else{
        $('#save-fee').attr('disabled',true);
    }
});

$('#add-college-modal .add-user-modal-body .form-control').on('keyup', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_college_last_name').val() != "") && ($('#add_college_first_name').val() != "") && 
        (re.test($('#add_college_last_name').val())) && (re.test($('#add_college_first_name').val())) && 
        ($('#add_college_level').val() != null) && ($('#add_college_department').val() != null) &&
        ($('#add_college_email').val() != null) && ($('#add_college_mobile').val().length == 11)){
        validate_college_form(true);
    }
    else{
        validate_college_form(false);
    }
});

$('#add-college-modal .add-user-modal-body .form-control').on('change', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_college_last_name').val() != "") && ($('#add_college_first_name').val() != "") && 
        (re.test($('#add_college_last_name').val())) && (re.test($('#add_college_first_name').val())) && 
        ($('#add_college_level').val() != null) && ($('#add_college_department').val() != null) &&
        ($('#add_college_email').val() != null) && ($('#add_college_mobile').val().length == 11)){
        validate_college_form(true);
    }
    else{
        validate_college_form(false);
    }
});

$('#add-staff-modal .add-user-modal-body .form-control').on('keyup', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_staff_last_name').val() != "") && ($('#add_staff_first_name').val() != "") && 
        (re.test($('#add_staff_last_name').val())) && (re.test($('#add_staff_first_name').val())) && 
        ($('#add_staff_department').val() != null) && ($('#add_staff_email').val() != null) && 
        ($('#add_staff_mobile').val().length == 11)){
        validate_staff_form(true);
    }
    else{
        validate_staff_form(false);
    }
});

$('#add-staff-modal .add-user-modal-body .form-control').on('change', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_staff_last_name').val() != "") && ($('#add_staff_first_name').val() != "") && 
        (re.test($('#add_staff_last_name').val())) && (re.test($('#add_staff_first_name').val())) && 
        ($('#add_staff_department').val() != null) && ($('#add_staff_email').val() != null) && 
        ($('#add_staff_mobile').val().length == 11)){
        validate_staff_form(true);
    }
    else{
        validate_staff_form(false);
    }
});


$('#add-user-modal .add-user-modal-body .form-control').on('change', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_user_last_name').val() != "") && ($('#add_user_first_name').val() != "") && 
        (re.test($('#add_user_last_name').val())) && 
        (re.test($('#add_user_first_name').val())) &&
        ($('#user-id-error').text().length == 0) && ($('#add_user_id_no').val().length == 10)){
        $('#save-user').removeAttr('disabled'); 
    }
    else{
        $('#save-user').attr('disabled',true);
    }
});

$('#add-user-modal .add-user-modal-body .form-control').on('keyup', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_user_last_name').val() != "") && ($('#add_user_first_name').val() != "") && 
        (re.test($('#add_user_last_name').val())) && 
        (re.test($('#add_user_first_name').val())) &&
        ($('#user-id-error').text().length == 0) && ($('#add_user_id_no').val().length == 10)){
        $('#save-user').removeAttr('disabled'); 
    }
    else{
        $('#save-user').attr('disabled',true);
    }
});

/*$('#add-user-modal .add-user-modal-body .form-control').donetyping(function(){
    var re = /[A-Za-z]+$/;
    if (($('#add_user_last_name').val() != "") && ($('#add_user_first_name').val() != "") && 
        (re.test($('#add_user_last_name').val())) && (re.test($('#add_user_first_name').val()))){
        validate_user_form(true);
    }
    else{
        validate_user_form(false);
    }
});
*/
$('#save-fee').on('click', function(){
    $('#save-fee').button('loading');
    var name = $('#add_fee_name').val();
    var category = $('#add_fee_category').val();
    var price = $('#add_fee_price').val();
    var desc = $('#add_fee_desc').val();
    var add_to = $('#add_fee_to').val();
    save_fee(name,category,price,desc,add_to);
});

$('#save-student').on('click', function(){
    $('#save-student').button('loading');
    var last_name = $('#add_student_last_name').val();
    var first_name = $('#add_student_first_name').val();
    var middle_name = $('#add_student_middle_name').val();
    var level = $('#add_student_level').val();
    var section = $('#add_student_section').val();
    var id_no = $('#add_student_id_no').val();

    var guardian_mobile = $('#add_guardian_mobile').val();
    var guardian_last_name = $('#add_guardian_last_name').val();
    var guardian_first_name = $('#add_guardian_first_name').val();
    var guardian_middle_name = $('#add_guardian_middle_name').val();
    var guardian_email = $('#add_guardian_email').val();
    var guardian_address = $('#add_guardian_address').val();
    var guardian_relation = $('#add_guardian_relation').val();
    save_k12(last_name, first_name, middle_name, level, section, id_no, guardian_mobile, guardian_last_name, guardian_first_name, guardian_middle_name, guardian_email, guardian_address, guardian_relation);
});

$('#save-college').on('click', function(){
    $('#save-college').button('loading');
    var last_name = $('#add_college_last_name').val();
    var first_name = $('#add_college_first_name').val();
    var middle_name = $('#add_college_middle_name').val();
    var level = $('#add_college_level').val();
    var department = $('#add_college_department').val();
    var email = $('#add_college_email').val();
    var mobile = $('#add_college_mobile').val();
    var id_no = $('#add_college_id_no').val();

    save_college(last_name, first_name, middle_name, level, department, email, mobile, id_no);
});

$('#save-staff').on('click', function(){
    $('#save-staff').button('loading');
    var last_name = $('#add_staff_last_name').val();
    var first_name = $('#add_staff_first_name').val();
    var middle_name = $('#add_staff_middle_name').val();
    var department = $('#add_staff_department').val();
    var email = $('#add_staff_email').val();
    var mobile = $('#add_staff_mobile').val();
    var id_no = $('#add_staff_id_no').val();

    save_staff(last_name, first_name, middle_name, department, email, mobile, id_no);
});

$('.search-logs').keypress(function(e){
    if (e.which == 13) {
        show_search_load();
        search_logs()
    }
});

$('.search-logs-options').on('change', function(){
    show_search_load();
    search_logs()
});

$('.search-absent').keypress(function(e){
    if (e.which == 13) {
        show_search_load();
        search_absent()
    }
});

$('.search-absent-options').on('change', function(){
    show_search_load();
    search_absent()
});

$('.search-late').keypress(function(e){
    if (e.which == 13) {
        show_search_load();
        search_late()
    }
});

$('.search-late-options').on('change', function(){
    search_late()
});

$('.add-fee-row').on('click', function(){
    if ($(this).find('.fee-check-td').html() == ''){
        add_fee($(this).attr('id'));
        $(this).find('.fee-check-td').html('<span class="glyphicon glyphicon-ok"></span>');
    }
    else{
        remove_fee($(this).attr('id'));
        $(this).find('.fee-check-td').html('');
    }
});


$('.no-class-checkbox').change(function() {
        if($(this).is(":checked")) {
            $('#'+$(this).attr('id')+'_calendar_sched').find('.input-group-addon').css('background-color','#4485F5');
            $('#'+$(this).attr('id')+'_calendar_sched .schedule-text').removeClass('unbind');
        }
        else{
            $('#'+$(this).attr('id')+'_calendar_sched').find('.input-group-addon').css('background-color','#999');
            $('#'+$(this).attr('id')+'_calendar_sched .schedule-text').addClass('unbind');
        }    
    });

$('#add_guardian_mobile').donetyping(function(){
    fill_guardian_data($(this).val());
});

});