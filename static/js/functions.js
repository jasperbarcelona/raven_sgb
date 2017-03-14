tab = '';
is_done = true;
form_validated = false
id_no_validated = false

college_form_validated = false
college_id_no_validated = false

staff_form_validated = false
staff_id_no_validated = false

college_edit_form_validated = false
college_edit_id_no_validated = true

staff_edit_form_validated = true
staff_edit_id_no_validated = true

edit_form_validated = false
edit_id_no_validated = true

logsSearchStatus = 'off'
k12SearchStatus = 'off'
collegeSearchStatus = 'off'
feesSearchStatus = 'off'
staffSearchStatus = 'off'

absentSearchStatus = 'off'
lateSearchStatus = 'off'

logs_result = false;
attendance_result = false;
absent_result = false;
late_result = false;
fees_result = false;
staff_result = false;

fees_to_add = [];

if (tab == 'attendance'){
    $('#add-user-btn').show();
  }
  else{
    $('#add-user-btn').hide();
  }

function add_fee(fee_id){
  fees_to_add.push(fee_id);
  if (fees_to_add.length == 0){
    $('#add-fee-btn').attr('disabled',true);
  }
  else{
    $('#add-fee-btn').attr('disabled',false);
  }
}

function remove_fee(fee_id){
  fees_to_add.pop(fee_id);
  if (fees_to_add.length == 0){
    $('#add-fee-btn').attr('disabled',true);
  }
  else{
    $('#add-fee-btn').attr('disabled',false);
  }
}

function show_students(){
    tab = 'k12';
    $.post('/students',
    function(data){
      $('.content').html(data);
      $('.menu-container').fadeOut(800);
      setTimeout(function(){ 
        $('.content').fadeIn(800);
      }, 800);
    });
}

function show_logs(){
    tab = 'logs';
    $.post('/logs',
    function(data){
      $('.content').html(data);
      $('.menu-container').fadeOut(800);
      setTimeout(function(){ 
        $('.content').fadeIn(800);
      }, 800);
    });
}

function show_transactions(){
    tab = 'transactions';
    $.post('/transactions',
    function(data){
      $('.content').html(data);
      $('.menu-container').fadeOut(800);
      setTimeout(function(){ 
        $('.content').fadeIn(800);
      }, 800);
    });
}

function show_home(){
  $('.content').fadeOut(800);
  setTimeout(function(){ 
    $('.menu-container').fadeIn(800);
    $('.content').html('');
  }, 800);
}

function show_staff(){
    tab = 'staff';
    $.post('/staff',
    function(data){
      $('.content').html(data);
      $('.menu-container').fadeOut(800);
      setTimeout(function(){ 
        $('.content').fadeIn(800);
      }, 800);
    });
}

function show_fees(){
    tab = 'fees';
    $.post('/fees',
    function(data){
      $('.content').html(data);
      $('.menu-container').fadeOut(800);
      setTimeout(function(){ 
        $('.content').fadeIn(800);
      }, 800);
    });
}

function show_attendance(){
    tab = 'absent';
    $.post('/attendance',
    function(data){
      $('.content').html(data);
      $('.menu-container').fadeOut(800);
      setTimeout(function(){ 
        $('.content').fadeIn(800);
      }, 800);
    });
}

function view_message(message_id){
  $('.message-row').removeClass('active-message');
  $('.message-modal-dialog').animate({'width':'900px'});
  $('.message-row').css('padding-left','10px');
  $('.message-row').css('padding-right','10px');
  $('#message-modal-body-left').animate({'width':'340px'});
  $('#message-modal-body-right').show();
  $('#message-modal-right-preloader').show();
  $('#'+message_id).addClass('active-message');
  $.post('/messages/view',{
      message_id:message_id,
  },
  function(data){
      $('#message-modal-body-right').html(data);
      $('#message-modal-right-preloader').hide();
  });
}

function compose_message(){
  $('.message-row').removeClass('active-message');
  $('.message-modal-dialog').animate({'width':'900px'});
  $('.message-row').css('padding-left','10px');
  $('.message-row').css('padding-right','10px');
  $('#message-modal-body-left').animate({'width':'340px'});
  $('#message-modal-body-right').show();
  $('#message-modal-right-preloader').show();
  $.post('/messages/new',
  function(data){
      $('#message-modal-body-right').html(data);
      $('#new-message-btn').attr('disabled', true);
      $('#message-modal-right-preloader').hide();
      setTimeout(function(){ 
        $('#message-modal-cover').show();
      }, 500);
  });
}

function close_message(){
    $('.message-row').removeClass('active-message');
    $('.message-modal-dialog').css('width','600px');
    $('.message-row').css('padding-left','20px');
    $('.message-row').css('padding-right','20px');
    $('#message-modal-body-left').css('width','100%');
    $('#message-modal-body-right').hide();
    $('#message-modal-right-preloader').hide();
}

function close_compose(){
    $('#message-modal-cover').hide();
    $('.message-modal-dialog').css('width','600px');
    $('.message-row').css('padding-left','20px');
    $('.message-row').css('padding-right','20px');
    $('#message-modal-body-left').css('width','100%');
    $('#message-modal-body-right').hide();
    $('#message-modal-right-preloader').hide();
    $('#new-message-btn').attr('disabled', false);
}

function validate_student_form(status){
  form_validated = status;
  if ((form_validated == true) && (id_no_validated == true)){
    $('#save-student').removeAttr('disabled');
  }
  else{
    $('#save-student').attr('disabled',true);
  }
}

function validate_college_form(status){
  college_form_validated = status;
  if ((college_form_validated == true) && (college_id_no_validated == true)){
    $('#save-college').removeAttr('disabled');
  }
  else{
    $('#save-college').attr('disabled',true);
  }
}

function validate_staff_form(status){
  staff_form_validated = status;
  if ((staff_form_validated == true) && (staff_id_no_validated == true)){
    $('#save-staff').removeAttr('disabled');
  }
  else{
    $('#save-staff').attr('disabled',true);
  }
}

function validate_college_form_edit(status){
  college_edit_form_validated = status;
  if ((college_edit_form_validated == true) && (college_edit_id_no_validated == true)){
    $('.edit-college-done-btn').removeAttr('disabled');
  }
  else{
    $('.edit-college-done-btn').attr('disabled',true);
  }
}

function validate_staff_form_edit(status){
  staff_edit_form_validated = status;
  if ((staff_edit_form_validated == true) && (staff_edit_id_no_validated == true)){
    $('.edit-staff-done-btn').removeAttr('disabled');
  }
  else{
    $('.edit-staff-done-btn').attr('disabled',true);
  }
}

function validate_student_form_edit(status){
  edit_form_validated = status;
  if ((edit_form_validated == true) && (edit_id_no_validated == true)){
    $('.edit-done-btn').removeAttr('disabled');
  }
  else{
    $('.edit-done-btn').attr('disabled',true);
  }
}

function validate_student_id_no(){
  if (($('#student-id-error').text().length == 0) && ($('#add_student_id_no').val().length == 10)){
    id_no_validated = true;
  }
  else{
    id_no_validated = false;
  }
  if ((form_validated == true) && (id_no_validated == true)){
    $('#save-student').removeAttr('disabled');
  }
  else{
    $('#save-student').attr('disabled',true);
  }
}

function validate_college_id_no(){
  if (($('#college-id-error').text().length == 0) && ($('#add_college_id_no').val().length == 10)){
    college_id_no_validated = true;
  }
  else{
    college_id_no_validated = false;
  }
  if ((college_form_validated == true) && (college_id_no_validated == true)){
    $('#save-college').removeAttr('disabled');
  }
  else{
    $('#save-college').attr('disabled',true);
  }
}

function validate_staff_id_no(){
  if (($('#staff-id-error').text().length == 0) && ($('#add_staff_id_no').val().length == 10)){
    staff_id_no_validated = true;
  }
  else{
    staff_id_no_validated = false;
  }
  if ((staff_form_validated == true) && (staff_id_no_validated == true)){
    $('#save-staff').removeAttr('disabled');
  }
  else{
    $('#save-staff').attr('disabled',true);
  }
}

function validate_student_id_no_edit(){
  if (($('#edit-student-id-error').text().length == 0) && ($('#edit_id_no').val().length == 10)){
    edit_id_no_validated = true;
  }
  else{
    edit_id_no_validated = false;
  }
  if ((edit_form_validated == true) && (edit_id_no_validated == true)){
    $('.edit-done-btn').removeAttr('disabled');
  }
  else{
    $('.edit-done-btn').attr('disabled',true);
  }
}

function validate_staff_id_no_edit(){
  if (($('#edit-staff-id-error').text().length == 0) && ($('#edit_staff_id_no').val().length == 10)){
    staff_edit_id_no_validated = true;
  }
  else{
    staff_edit_id_no_validated = false;
  }
  if ((staff_edit_form_validated == true) && (staff_edit_id_no_validated == true)){
    $('.edit-staff-done-btn').removeAttr('disabled');
  }
  else{
    $('.edit-staff-done-btn').attr('disabled',true);
  }
}

function validate_college_id_no_edit(){
  if (($('#edit-college-id-error').text().length == 0) && ($('#edit_college_id_no').val().length == 10)){
    college_edit_id_no_validated = true;
  }
  else{
    college_edit_id_no_validated = false;
  }
  if ((college_edit_form_validated == true) && (college_edit_id_no_validated == true)){
    $('.edit-college-done-btn').removeAttr('disabled');
  }
  else{
    $('.edit-college-done-btn').attr('disabled',true);
  }
}

function validate_user_id_no(){
  if (($('#user-id-error').text().length == 0) && ($('#add_user_id_no').val().length == 10)){
    id_no_validated = true;
  }
  else{
    id_no_validated = false;
  }
  if ((form_validated == true) && (id_no_validated == true)){
    $('#save-user').removeAttr('disabled');
  }
  else{
    $('#save-user').attr('disabled',true);
  }
}

function change_tab(page){
  tab = page;
  if (tab == 'k12'){
    $('#add-student-btn').show();
    $('#add-college-btn').hide();
  }
  else{
    $('#add-student-btn').hide();
    $('#add-college-btn').show();
  }


  if ((eval(tab+'SearchStatus') == 'on') && (eval(tab+'_result') == false)){
    $('#search-loading').show();
  }
  else{
    $('#search-loading').hide();
  }
  $.post('/tab/change',{
      tab:tab,
    });
}

function validate_student_id(id_no){
  $('#student-id-error').hide();
  $('#student-id-loader').show();
  $.post('/id/validate',{
        id_no:id_no,
    },
    function(data){
        $('#student-id-error').html(data);
        $('#student-id-loader').hide();
        $('#student-id-error').show();
        validate_student_id_no();
    });
}

function validate_college_id(id_no){
  $('#college-id-error').hide();
  $('#college-id-loader').show();
  $.post('/id/validate',{
        id_no:id_no,
    },
    function(data){
        $('#college-id-error').html(data);
        $('#college-id-loader').hide();
        $('#college-id-error').show();
        validate_college_id_no();
    });
}

function validate_staff_id(id_no){
  $('#staff-id-error').hide();
  $('#staff-id-loader').show();
  $.post('/id/validate',{
        id_no:id_no,
    },
    function(data){
        $('#staff-id-error').html(data);
        $('#staff-id-loader').hide();
        $('#staff-id-error').show();
        validate_staff_id_no();
    });
}

function validate_college_id_edit(id_no,student_id){
  var group = 'college';
  $('#edit-college-id-error').hide();
  $('#edit-college-id-loader').show();
  $.post('/id/validate/edit',{
        id_no:id_no,
        student_id:student_id,
        group:group
    },
    function(data){
        $('#edit-college-id-error').html(data);
        $('#edit-college-id-loader').hide();
        $('#edit-college-id-error').show();
        validate_college_id_no_edit();
    });
}

function validate_staff_id_edit(id_no,staff_id){
  var group = 'staff';
  $('#edit-staff-id-error').hide();
  $('#edit-staff-id-loader').show();
  $.post('/id/validate/edit',{
        id_no:id_no,
        staff_id:staff_id,
        group:group
    },
    function(data){
        $('#edit-staff-id-error').html(data);
        $('#edit-staff-id-loader').hide();
        $('#edit-staff-id-error').show();
        validate_staff_id_no_edit();
    });
}

function validate_student_id_edit(id_no,student_id){
  var group = 'k12';
  $('#edit-student-id-error').hide();
  $('#edit-student-id-loader').show();
  $.post('/id/validate/edit',{
        id_no:id_no,
        student_id:student_id,
        group:group
    },
    function(data){
        $('#edit-student-id-error').html(data);
        $('#edit-student-id-loader').hide();
        $('#edit-student-id-error').show();
        validate_student_id_no_edit();
    });
}

function validate_user_id(id_no){
  $('#user-id-error').hide();
  $('#user-id-loader').show();
  $.post('/id/validate',{
        id_no:id_no,
    },
    function(data){
        $('#user-id-error').html(data);
        $('#user-id-loader').hide();
        $('#user-id-error').show();
        validate_user_id_no();
    });
}

function supply_data(studentId){
  $.post('/student/info/get',{
        student_id:studentId,
    },
    function(data){
        $('.edit-user-modal-dialog .modal-content').html(data);
    });
}

function supply_college_data(studentId){
  $.post('/college/info/get',{
        student_id:studentId,
    },
    function(data){
        $('.edit-user-modal-dialog .modal-content').html(data);
    });
}

function supply_staff_data(staffId){
  $.post('/staff/info/get',{
        staff_id:staffId,
    },
    function(data){
        $('.edit-staff-modal-dialog .modal-content').html(data);
    });
}

function textCounter(field,field2,maxlimit){
 var countfield = document.getElementById(field2);
  if( field.value.length > maxlimit ){
    field.value = field.value.substring( 0, maxlimit );
  return false;
  }
  else{
    countfield.value = "Remaining: " + (maxlimit - field.value.length);
  }
}

function blast_message(){
  var message = $("#message").val();
  var password = $("#message-confirm-password").val();
  if ((navigator.onLine==true) && ($.trim($("#message").val()))) {
    $.post('/blast',{message:message,password:password},
    function(data){
      $('#status-modal-body').html(data);
      $("#message").val('');
      $('#confirm-modal').modal('hide');
      $('#compose-message-modal').modal('hide');
      $('#message-status-modal').modal('show');
    });
    
  }
  else if (navigator.onLine==false) {
    alert('You are offline!');
  }
  else{
    alert('Message is empty!');
  }
}

function open_messages(){
  $('#message-modal-preloader').show();
  $.post('/messages',
  function(data){
    $('#message-modal-body-left').html(data);
    $('#message-modal-preloader').hide();
  });
}

/*function reset_data(){
    $('#kinder_morning_start').val(kinder_morning_start);
    $('#kinder_morning_end').val(kinder_morning_end);
    $('#primary_morning_start').val(primary_morning_start);
    $('#primary_morning_end').val(primary_morning_end);
    $('#junior_morning_start').val(junior_morning_start);
    $('#junior_morning_end').val(junior_morning_end);
    $('#senior_morning_start').val(senior_morning_start);
    $('#senior_morning_end').val(senior_morning_end);

    $('#kinder_afternoon_start').val(kinder_afternoon_start);
    $('#kinder_afternoon_end').val(kinder_afternoon_end);
    $('#primary_afternoon_start').val(primary_afternoon_start);
    $('#primary_afternoon_end').val(primary_afternoon_end);
    $('#junior_afternoon_start').val(junior_afternoon_start);
    $('#junior_afternoon_end').val(junior_afternoon_end);
    $('#senior_afternoon_start').val(senior_afternoon_start);
    $('#senior_afternoon_end').val(senior_afternoon_end);
    $('.no-class-checkbox').prop('checked',true);
    $('.no-class-checkbox').change();
    $('.no-class-checkbox').hide();
}*/

/*function initial_data(){

    kinder_morning_start = $('#kinder_morning_start').val();
    kinder_morning_end = $('#kinder_morning_end').val();
    primary_morning_start = $('#primary_morning_start').val();
    primary_morning_end = $('#primary_morning_end').val();
    junior_morning_start = $('#junior_morning_start').val();
    junior_morning_end = $('#junior_morning_end').val();
    senior_morning_start = $('#senior_morning_start').val();
    senior_morning_end = $('#senior_morning_end').val();
    kinder_afternoon_start = $('#kinder_afternoon_start').val();
    kinder_afternoon_end = $('#kinder_afternoon_end').val();
    primary_afternoon_start = $('#primary_afternoon_start').val();
    primary_afternoon_end = $('#primary_afternoon_end').val();
    junior_afternoon_start = $('#junior_afternoon_start').val();
    junior_afternoon_end = $('#junior_afternoon_end').val();
    senior_afternoon_start = $('#senior_afternoon_start').val();
    senior_afternoon_end = $('#senior_afternoon_end').val();
}*/

function clear_data(){
    input_fields = $('.add-user-modal-body').find('.form-control');
    input_fields.val('');
    input_fields.change();
    $('#id-error').text('');
}

function clear_fee_data(){
    input_fields = $('.add-fee-modal-body').find('.form-control');
    input_fields.val('');
    input_fields.change();
}

;(function($){
  $.fn.extend({
    donetyping: function(callback,timeout){
      timeout = timeout || 1e3;
      var timeoutReference,
      doneTyping = function(el){
        if (!timeoutReference) return;
        timeoutReference = null;
        callback.call(el);
      };
      return this.each(function(i,el){
        var $el = $(el);
        $el.is(':input') && $el.on('keyup keypress',function(e){
          if (e.type=='keyup' && e.keyCode!=8) return;
          if (timeoutReference) clearTimeout(timeoutReference);
          timeoutReference = setTimeout(function(){
            doneTyping(el);
          }, timeout);
        }).on('blur',function(){
          doneTyping(el);
        });
      });
    }
  });
})(jQuery);


function search_k12(){
  show_search_load();
  var last_name = $('#attendance_search_last_name').val();
  var first_name = $('#attendance_search_first_name').val();
  var middle_name = $('#attendance_search_middle_name').val();
  var id_no = $('#attendance_search_id_no').val();
  var level = $('#attendance_search_level').val();
  var section = $('#attendance_search_section').val();
  var contact = $('#attendance_search_contact').val();
  var absences = $('#attendance_search_absences').val();
  var lates = $('#attendance_search_lates').val();
  var reset = 'yes';

  $.post('/search/k12',{
      needed:tab,
      last_name:last_name,
      first_name:first_name,
      middle_name:middle_name,
      id_no:id_no,
      level:level,
      section:section,
      contact:contact,    
      absences:absences,
      lates:lates,
      reset:reset
  },
  function(data){
      $('#'+tab).html(data);
      $('#search-loading').hide();
      attendance_result = true;
      is_done = true;
  });
}

function search_college(){
  show_search_load();
  var last_name = $('#college_search_last_name').val();
  var first_name = $('#college_search_first_name').val();
  var middle_name = $('#college_search_middle_name').val();
  var id_no = $('#college_search_id_no').val();
  var level = $('#college_search_level').val();
  var department = $('#college_search_department').val();
  var reset = 'yes';

  $.post('/search/college',{
      needed:tab,
      last_name:last_name,
      first_name:first_name,
      middle_name:middle_name,
      id_no:id_no,
      level:level,
      department:department,
      reset:reset
  },
  function(data){
      $('#'+tab).html(data);
      $('#search-loading').hide();
      attendance_result = true;
      is_done = true;
  });
}

function search_staff(){
  show_search_load();
  var last_name = $('#staff_search_last_name').val();
  var first_name = $('#staff_search_first_name').val();
  var middle_name = $('#staff_search_middle_name').val();
  var id_no = $('#staff_search_id_no').val();
  var department = $('#staff_search_department').val();
  var reset = 'yes';

  $.post('/search/staff',{
      needed:tab,
      last_name:last_name,
      first_name:first_name,
      middle_name:middle_name,
      id_no:id_no,
      department:department,
      reset:reset
  },
  function(data){
      $('#'+tab).html(data);
      $('#search-loading').hide();
      attendance_result = true;
      is_done = true;
  });
}


function fill_guardian_data(mobile_number){
  $('#guardianInfoLoading').show();
  $.post('/guardians/info',{
      mobile_number:mobile_number,
  },
  function(data){
    if (data['status'] == 'success'){
      $('#add_guardian_last_name').val(data['last_name']);
      $('#add_guardian_first_name').val(data['first_name']);
      $('#add_guardian_middle_name').val(data['middle_name']);
      $('#add_guardian_email').val(data['email']);
      $('#add_guardian_address').val(data['address']);
      $('#add_guardian_relation').val('');
      $('.guardian-info-section').find('div').find('.form-control').change();
      $('#add_guardian_relation').focus();
    }
    $('#guardianInfoLoading').hide();
  });
}

function fill_guardian_data_edit(mobile_number){
  $('#guardianInfoLoadingEdit').show();
  $.post('/guardians/info',{
      mobile_number:mobile_number,
  },
  function(data){
    if (data['status'] == 'success'){
      $('#edit_guardian_last_name').val(data['last_name']);
      $('#edit_guardian_first_name').val(data['first_name']);
      $('#edit_guardian_middle_name').val(data['middle_name']);
      $('#edit_guardian_email').val(data['email']);
      $('#edit_guardian_address').val(data['address']);
      $('#edit_guardian_relation').val('');
      $('.guardian-info-section').find('div').find('.form-control').change();
      $('#edit_guardian_relation').focus();
    }
    $('#guardianInfoLoadingEdit').hide();
  });
}

function attendance_next_search(){
  var last_name = $('#attendance_search_last_name').val();
  var first_name = $('#attendance_search_first_name').val();
  var middle_name = $('#attendance_search_middle_name').val();
  var id_no = $('#attendance_search_id_no').val();
  var level = $('#attendance_search_level').val();
  var section = $('#attendance_search_section').val();
  var contact = $('#attendance_search_contact').val();
  var absences = $('#attendance_search_absences').val();
  var lates = $('#attendance_search_lates').val();
  var reset = 'no';

  $.post('/search/attendance',{
      needed:tab,
      last_name:last_name,
      first_name:first_name,
      middle_name:middle_name,
      id_no:id_no,
      level:level,
      section:section,
      contact:contact,    
      absences:absences,
      lates:lates,
      reset:reset
  },
  function(data){
      $('#'+tab).append(data);
  });
}


function search_logs(){
  isPreviousEventComplete = false;
  var date = $('#log_search_date').val();
  var id_no = $('#log_search_id_no').val();
  var name = $('#log_search_name').val();
  var department = $('#log_search_department').val();
  var reset = 'yes';
  
  $.post('/search/logs',{
      needed:tab,
      date:date,
      id_no:id_no,
      name:name,
      department:department,
      reset:reset
  },
  function(data){
      $('#'+tab).html(data);
      $('#search-loading').hide();
      logs_result = true;
      is_done = true
      isPreviousEventComplete = true
  });
}

function search_fees(){
  isPreviousEventComplete = false;
  var name = $('#fee_search_name').val();
  var category = $('#fee_search_category').val();
  var reset = 'yes';
  
  $.post('/search/fees',{
      name:name,
      category:category,
      reset:reset
  },
  function(data){
      $('#'+tab).html(data);
      $('#search-loading').hide();
      fees_result = true;
      is_done = true
      isPreviousEventComplete = true
  });
}

function logs_next_search(elem){
  var date = $('#log_search_date').val();
  var id_no = $('#log_search_id_no').val();
  var name = $('#log_search_name').val();
  var level = $('#log_search_level').val();
  var section = $('#log_search_section').val();
  var reset = 'no';

    $.post('/search/logs',{
        needed:tab,
        date:date,
        id_no:id_no,
        name:name,
        level:level,
        section:section,
        reset:reset
    },
    function(data){
        $('#'+tab).append(data);
        $('tbody').data('activated', false)
    });
}


function search_absent(){
  var date = $('#absent_search_date').val();
  var id_no = $('#absent_search_id_no').val();
  var name = $('#absent_search_name').val();
  var level = $('#absent_search_level').val();
  var section = $('#absent_search_section').val();
  var reset = 'yes';

  $.post('/search/absent',{
      needed:tab,
      date:date,
      id_no:id_no,
      name:name,
      level:level,
      section:section,
      reset:reset
  },
  function(data){
      $('#'+tab).html(data);
      $('#search-loading').hide();
      absent_result = true;
      is_done = true
  });
}

function absent_next_search(){
  var date = $('#absent_search_date').val();
  var id_no = $('#absent_search_id_no').val();
  var name = $('#absent_search_name').val();
  var level = $('#absent_search_level').val();
  var section = $('#absent_search_section').val();
  var reset = 'no';

    $.post('/search/absent',{
        needed:tab,
        date:date,
        id_no:id_no,
        name:name,
        level:level,
        section:section,
        reset:reset
    },
    function(data){
        $('#'+tab).append(data);
    });
}


function search_late(){
  var date = $('#late_search_date').val();
  var id_no = $('#late_search_id_no').val();
  var name = $('#late_search_name').val();
  var level = $('#late_search_level').val();
  var section = $('#late_search_section').val();
  var reset = 'yes';

  $.post('/search/late',{
      needed:tab,
      date:date,
      id_no:id_no,
      name:name,
      level:level,
      section:section,
      reset:reset
  },
  function(data){
      $('#'+tab).html(data);
      $('#search-loading').hide();
      late_result = true;
      is_done = true
  });
}

function late_next_search(){
  var date = $('#late_search_date').val();
  var id_no = $('#late_search_id_no').val();
  var name = $('#late_search_name').val();
  var level = $('#late_search_level').val();
  var section = $('#late_search_section').val();
  var reset = 'no';

    $.post('/search/late',{
        needed:tab,
        date:date,
        id_no:id_no,
        name:name,
        level:level,
        section:section,
        reset:reset
    },
    function(data){
        $('#'+tab).append(data);
    });
}

function load_next(tab,elem){
    isPreviousEventComplete = false;
    var data = tab
    $.post('/loadmore',{data:data},
    function(data){
        $('#'+tab).append(data);
        isPreviousEventComplete = true;
        $('tbody').data('activated', false)
    });
}

/*function render_watermark(){
  
path = $('#path').val();
alert(path)
$(".tab-pane").css({'background-image':'url(../static/images/watermark.png)','background-repeat': 'no-repeat','background-position': 'center'});
}*/

function save_sched(){
    schedules = []
    for (var i = 0; i <= days.length - 1; i++) {
        schedules.push($('#'+days[i]+'_junior_kinder_morning_start').val());
        schedules.push($('#'+days[i]+'_junior_kinder_morning_end').val());
        schedules.push($('#'+days[i]+'_junior_kinder_afternoon_start').val());
        schedules.push($('#'+days[i]+'_junior_kinder_afternoon_end').val());
        schedules.push($('#'+days[i]+'_senior_kinder_morning_start').val());
        schedules.push($('#'+days[i]+'_senior_kinder_morning_end').val());
        schedules.push($('#'+days[i]+'_senior_kinder_afternoon_start').val());
        schedules.push($('#'+days[i]+'_senior_kinder_afternoon_end').val());
        schedules.push($('#'+days[i]+'_first_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_first_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_first_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_first_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_second_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_second_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_second_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_second_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_third_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_third_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_third_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_third_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_fourth_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_fourth_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_fourth_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_fourth_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_fifth_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_fifth_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_fifth_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_fifth_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_sixth_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_sixth_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_sixth_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_sixth_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_seventh_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_seventh_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_seventh_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_seventh_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_eight_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_eight_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_eight_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_eight_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_ninth_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_ninth_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_ninth_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_ninth_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_tenth_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_tenth_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_tenth_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_tenth_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_eleventh_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_eleventh_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_eleventh_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_eleventh_grade_afternoon_end').val());
        schedules.push($('#'+days[i]+'_twelfth_grade_morning_start').val());
        schedules.push($('#'+days[i]+'_twelfth_grade_morning_end').val());
        schedules.push($('#'+days[i]+'_twelfth_grade_afternoon_start').val());
        schedules.push($('#'+days[i]+'_twelfth_grade_afternoon_end').val());
    };

    $('#save-sched').button('loading');
    $.post('/schedule/regular/save',{
        'schedule[]':schedules
    },
    function(data){
      $('#save-sched').button('complete');
      setTimeout(function(){ 
          $('#save-sched').attr('disabled',true);
      }, 0); 
    });
}

function save_calendar_sched(){
    if ($('#junior_kinder_morning_class').is(":checked")){
      save_junior_kinder_morning_class = true;
    }
    else{
      save_junior_kinder_morning_class = false;
    }
    if ($('#junior_kinder_afternoon_class').is(":checked")){
      save_junior_kinder_afternoon_class = true;
    }
    else{
      save_junior_kinder_afternoon_class = false;
    }
    if ($('#senior_kinder_morning_class').is(":checked")){
      save_senior_kinder_morning_class = true;
    }
    else{
      save_senior_kinder_morning_class = false;
    }
    if ($('#senior_kinder_afternoon_class').is(":checked")){
      save_senior_kinder_afternoon_class = true;
    }
    else{
      save_senior_kinder_afternoon_class = false;
    }
    if ($('#first_grade_morning_class').is(":checked")){
      save_first_grade_morning_class = true;
    }
    else{
      save_first_grade_morning_class = false;
    }
    if ($('#first_grade_afternoon_class').is(":checked")){
      save_first_grade_afternoon_class = true;
    }
    else{
      save_first_grade_afternoon_class = false;
    }
    if ($('#second_grade_morning_class').is(":checked")){
      save_second_grade_morning_class = true;
    }
    else{
      save_second_grade_morning_class = false;
    }
    if ($('#second_grade_afternoon_class').is(":checked")){
      save_second_grade_afternoon_class = true;
    }
    else{
      save_second_grade_afternoon_class = false;
    }
    if ($('#third_grade_morning_class').is(":checked")){
      save_third_grade_morning_class = true;
    }
    else{
      save_third_grade_morning_class = false;
    }
    if ($('#third_grade_afternoon_class').is(":checked")){
      save_third_grade_afternoon_class = true;
    }
    else{
      save_third_grade_afternoon_class = false;
    }
    if ($('#fourth_grade_morning_class').is(":checked")){
      save_fourth_grade_morning_class = true;
    }
    else{
      save_fourth_grade_morning_class = false;
    }
    if ($('#fourth_grade_afternoon_class').is(":checked")){
      save_fourth_grade_afternoon_class = true;
    }
    else{
      save_fourth_grade_afternoon_class = false;
    }
    if ($('#fifth_grade_morning_class').is(":checked")){
      save_fifth_grade_morning_class = true;
    }
    else{
      save_fifth_grade_morning_class = false;
    }
    if ($('#fifth_grade_afternoon_class').is(":checked")){
      save_fifth_grade_afternoon_class = true;
    }
    else{
      save_fifth_grade_afternoon_class = false;
    }
    if ($('#sixth_grade_morning_class').is(":checked")){
      save_sixth_grade_morning_class = true;
    }
    else{
      save_sixth_grade_morning_class = false;
    }
    if ($('#sixth_grade_afternoon_class').is(":checked")){
      save_sixth_grade_afternoon_class = true;
    }
    else{
      save_sixth_grade_afternoon_class = false;
    }
    if ($('#seventh_grade_morning_class').is(":checked")){
      save_seventh_grade_morning_class = true;
    }
    else{
      save_seventh_grade_morning_class = false;
    }
    if ($('#seventh_grade_afternoon_class').is(":checked")){
      save_seventh_grade_afternoon_class = true;
    }
    else{
      save_seventh_grade_afternoon_class = false;
    }
    if ($('#eight_grade_morning_class').is(":checked")){
      save_eight_grade_morning_class = true;
    }
    else{
      save_eight_grade_morning_class = false;
    }
    if ($('#eight_grade_afternoon_class').is(":checked")){
      save_eight_grade_afternoon_class = true;
    }
    else{
      save_eight_grade_afternoon_class = false;
    }
    if ($('#ninth_grade_morning_class').is(":checked")){
      save_ninth_grade_morning_class = true;
    }
    else{
      save_ninth_grade_morning_class = false;
    }
    if ($('#ninth_grade_afternoon_class').is(":checked")){
      save_ninth_grade_afternoon_class = true;
    }
    else{
      save_ninth_grade_afternoon_class = false;
    }
    if ($('#tenth_grade_morning_class').is(":checked")){
      save_tenth_grade_morning_class = true;
    }
    else{
      save_tenth_grade_morning_class = false;
    }
    if ($('#tenth_grade_afternoon_class').is(":checked")){
      save_tenth_grade_afternoon_class = true;
    }
    else{
      save_tenth_grade_afternoon_class = false;
    }
    if ($('#eleventh_grade_morning_class').is(":checked")){
      save_eleventh_grade_morning_class = true;
    }
    else{
      save_eleventh_grade_morning_class = false;
    }
    if ($('#eleventh_grade_afternoon_class').is(":checked")){
      save_eleventh_grade_afternoon_class = true;
    }
    else{
      save_eleventh_grade_afternoon_class = false;
    }
    if ($('#twelfth_grade_morning_class').is(":checked")){
      save_twelfth_grade_morning_class = true;
    }
    else{
      save_twelfth_grade_morning_class = false;
    }
    if ($('#twelfth_grade_afternoon_class').is(":checked")){
      save_twelfth_grade_afternoon_class = true;
    }
    else{
      save_twelfth_grade_afternoon_class = false;
    }

    save_junior_kinder_morning_start = $('#junior_kinder_morning_start').val();
    save_junior_kinder_morning_end = $('#junior_kinder_morning_end').val();
    save_junior_kinder_afternoon_start = $('#junior_kinder_afternoon_start').val();
    save_junior_kinder_afternoon_end = $('#junior_kinder_afternoon_end').val();

    save_senior_kinder_morning_start = $('#senior_kinder_morning_start').val();
    save_senior_kinder_morning_end = $('#senior_kinder_morning_end').val();
    save_senior_kinder_afternoon_start = $('#senior_kinder_afternoon_start').val();
    save_senior_kinder_afternoon_end = $('#senior_kinder_afternoon_end').val();

    save_first_grade_morning_start = $('#first_grade_morning_start').val();
    save_first_grade_morning_end = $('#first_grade_morning_end').val();
    save_first_grade_afternoon_start = $('#first_grade_afternoon_start').val();
    save_first_grade_afternoon_end = $('#first_grade_afternoon_end').val();

    save_second_grade_morning_start = $('#second_grade_morning_start').val();
    save_second_grade_morning_end = $('#second_grade_morning_end').val();
    save_second_grade_afternoon_start = $('#second_grade_afternoon_start').val();
    save_second_grade_afternoon_end = $('#second_grade_afternoon_end').val();

    save_third_grade_morning_start = $('#third_grade_morning_start').val();
    save_third_grade_morning_end = $('#third_grade_morning_end').val();
    save_third_grade_afternoon_start = $('#third_grade_afternoon_start').val();
    save_third_grade_afternoon_end = $('#third_grade_afternoon_end').val();

    save_fourth_grade_morning_start = $('#fourth_grade_morning_start').val();
    save_fourth_grade_morning_end = $('#fourth_grade_morning_end').val();
    save_fourth_grade_afternoon_start = $('#fourth_grade_afternoon_start').val();
    save_fourth_grade_afternoon_end = $('#fourth_grade_afternoon_end').val();

    save_fifth_grade_morning_start = $('#fifth_grade_morning_start').val();
    save_fifth_grade_morning_end = $('#fifth_grade_morning_end').val();
    save_fifth_grade_afternoon_start = $('#fifth_grade_afternoon_start').val();
    save_fifth_grade_afternoon_end = $('#fifth_grade_afternoon_end').val();

    save_sixth_grade_morning_start = $('#sixth_grade_morning_start').val();
    save_sixth_grade_morning_end = $('#sixth_grade_morning_end').val();
    save_sixth_grade_afternoon_start = $('#sixth_grade_afternoon_start').val();
    save_sixth_grade_afternoon_end = $('#sixth_grade_afternoon_end').val();

    save_seventh_grade_morning_start = $('#seventh_grade_morning_start').val();
    save_seventh_grade_morning_end = $('#seventh_grade_morning_end').val();
    save_seventh_grade_afternoon_start = $('#seventh_grade_afternoon_start').val();
    save_seventh_grade_afternoon_end = $('#seventh_grade_afternoon_end').val();

    save_eight_grade_morning_start = $('#eight_grade_morning_start').val();
    save_eight_grade_morning_end = $('#eight_grade_morning_end').val();
    save_eight_grade_afternoon_start = $('#eight_grade_afternoon_start').val();
    save_eight_grade_afternoon_end = $('#eight_grade_afternoon_end').val();

    save_ninth_grade_morning_start = $('#ninth_grade_morning_start').val();
    save_ninth_grade_morning_end = $('#ninth_grade_morning_end').val();
    save_ninth_grade_afternoon_start = $('#ninth_grade_afternoon_start').val();
    save_ninth_grade_afternoon_end = $('#ninth_grade_afternoon_end').val();

    save_tenth_grade_morning_start = $('#tenth_grade_morning_start').val();
    save_tenth_grade_morning_end = $('#tenth_grade_morning_end').val();
    save_tenth_grade_afternoon_start = $('#tenth_grade_afternoon_start').val();
    save_tenth_grade_afternoon_end = $('#tenth_grade_afternoon_end').val();

    save_eleventh_grade_morning_start = $('#eleventh_grade_morning_start').val();
    save_eleventh_grade_morning_end = $('#eleventh_grade_morning_end').val();
    save_eleventh_grade_afternoon_start = $('#eleventh_grade_afternoon_start').val();
    save_eleventh_grade_afternoon_end = $('#eleventh_grade_afternoon_end').val();

    save_twelfth_grade_morning_start = $('#twelfth_grade_morning_start').val();
    save_twelfth_grade_morning_end = $('#twelfth_grade_morning_end').val();
    save_twelfth_grade_afternoon_start = $('#twelfth_grade_afternoon_start').val();
    save_twelfth_grade_afternoon_end = $('#twelfth_grade_afternoon_end').val();


    $('#save-calendar-sched').attr('disabled',true);
    $('#save-calendar-sched').button('loading');
    $.post('/schedule/irregular/save',{
      save_junior_kinder_morning_class:save_junior_kinder_morning_class,
      save_junior_kinder_afternoon_class:save_junior_kinder_afternoon_class,
      save_senior_kinder_morning_class:save_senior_kinder_morning_class,
      save_senior_kinder_afternoon_class:save_senior_kinder_afternoon_class,
      save_first_grade_morning_class:save_first_grade_morning_class,
      save_first_grade_afternoon_class:save_first_grade_afternoon_class,
      save_second_grade_morning_class:save_second_grade_morning_class,
      save_second_grade_afternoon_class:save_second_grade_afternoon_class,
      save_third_grade_morning_class:save_third_grade_morning_class,
      save_third_grade_afternoon_class:save_third_grade_afternoon_class,
      save_fourth_grade_morning_class:save_fourth_grade_morning_class,
      save_fourth_grade_afternoon_class:save_fourth_grade_afternoon_class,
      save_fifth_grade_morning_class:save_fifth_grade_morning_class,
      save_fifth_grade_afternoon_class:save_fifth_grade_afternoon_class,
      save_sixth_grade_morning_class:save_sixth_grade_morning_class,
      save_sixth_grade_afternoon_class:save_sixth_grade_afternoon_class,
      save_seventh_grade_morning_class:save_seventh_grade_morning_class,
      save_seventh_grade_afternoon_class:save_seventh_grade_afternoon_class,
      save_eight_grade_morning_class:save_eight_grade_morning_class,
      save_eight_grade_afternoon_class:save_eight_grade_afternoon_class,
      save_ninth_grade_morning_class:save_ninth_grade_morning_class,
      save_ninth_grade_afternoon_class:save_ninth_grade_afternoon_class,
      save_tenth_grade_morning_class:save_tenth_grade_morning_class,
      save_tenth_grade_afternoon_class:save_tenth_grade_afternoon_class,
      save_eleventh_grade_morning_class:save_eleventh_grade_morning_class,
      save_eleventh_grade_afternoon_class:save_eleventh_grade_afternoon_class,
      save_twelfth_grade_morning_class:save_twelfth_grade_morning_class,
      save_twelfth_grade_afternoon_class:save_twelfth_grade_afternoon_class,

      save_junior_kinder_morning_start:save_junior_kinder_morning_start,
      save_junior_kinder_morning_end:save_junior_kinder_morning_end,
      save_junior_kinder_afternoon_start:save_junior_kinder_afternoon_start,
      save_junior_kinder_afternoon_end:save_junior_kinder_afternoon_end,
      save_senior_kinder_morning_start:save_senior_kinder_morning_start,
      save_senior_kinder_morning_end:save_senior_kinder_morning_end,
      save_senior_kinder_afternoon_start:save_senior_kinder_afternoon_start,
      save_senior_kinder_afternoon_end:save_senior_kinder_afternoon_end,
      save_first_grade_morning_start:save_first_grade_morning_start,
      save_first_grade_morning_end:save_first_grade_morning_end,
      save_first_grade_afternoon_start:save_first_grade_afternoon_start,
      save_first_grade_afternoon_end:save_first_grade_afternoon_end,
      save_second_grade_morning_start:save_second_grade_morning_start,
      save_second_grade_morning_end:save_second_grade_morning_end,
      save_second_grade_afternoon_start:save_second_grade_afternoon_start,
      save_second_grade_afternoon_end:save_second_grade_afternoon_end,
      save_third_grade_morning_start:save_third_grade_morning_start,
      save_third_grade_morning_end:save_third_grade_morning_end,
      save_third_grade_afternoon_start:save_third_grade_afternoon_start,
      save_third_grade_afternoon_end:save_third_grade_afternoon_end,
      save_fourth_grade_morning_start:save_fourth_grade_morning_start,
      save_fourth_grade_morning_end:save_fourth_grade_morning_end,
      save_fourth_grade_afternoon_start:save_fourth_grade_afternoon_start,
      save_fourth_grade_afternoon_end:save_fourth_grade_afternoon_end,
      save_fifth_grade_morning_start:save_fifth_grade_morning_start,
      save_fifth_grade_morning_end:save_fifth_grade_morning_end,
      save_fifth_grade_afternoon_start:save_fifth_grade_afternoon_start,
      save_fifth_grade_afternoon_end:save_fifth_grade_afternoon_end,
      save_sixth_grade_morning_start:save_sixth_grade_morning_start,
      save_sixth_grade_morning_end:save_sixth_grade_morning_end,
      save_sixth_grade_afternoon_start:save_sixth_grade_afternoon_start,
      save_sixth_grade_afternoon_end:save_sixth_grade_afternoon_end,
      save_seventh_grade_morning_start:save_seventh_grade_morning_start,
      save_seventh_grade_morning_end:save_seventh_grade_morning_end,
      save_seventh_grade_afternoon_start:save_seventh_grade_afternoon_start,
      save_seventh_grade_afternoon_end:save_seventh_grade_afternoon_end,
      save_eight_grade_morning_start:save_eight_grade_morning_start,
      save_eight_grade_morning_end:save_eight_grade_morning_end,
      save_eight_grade_afternoon_start:save_eight_grade_afternoon_start,
      save_eight_grade_afternoon_end:save_eight_grade_afternoon_end,
      save_ninth_grade_morning_start:save_ninth_grade_morning_start,
      save_ninth_grade_morning_end:save_ninth_grade_morning_end,
      save_ninth_grade_afternoon_start:save_ninth_grade_afternoon_start,
      save_ninth_grade_afternoon_end:save_ninth_grade_afternoon_end,
      save_tenth_grade_morning_start:save_tenth_grade_morning_start,
      save_tenth_grade_morning_end:save_tenth_grade_morning_end,
      save_tenth_grade_afternoon_start:save_tenth_grade_afternoon_start,
      save_tenth_grade_afternoon_end:save_tenth_grade_afternoon_end,
      save_eleventh_grade_morning_start:save_eleventh_grade_morning_start,
      save_eleventh_grade_morning_end:save_eleventh_grade_morning_end,
      save_eleventh_grade_afternoon_start:save_eleventh_grade_afternoon_start,
      save_eleventh_grade_afternoon_end:save_eleventh_grade_afternoon_end,
      save_twelfth_grade_morning_start:save_twelfth_grade_morning_start,
      save_twelfth_grade_morning_end:save_twelfth_grade_morning_end,
      save_twelfth_grade_afternoon_start:save_twelfth_grade_afternoon_start,
      save_twelfth_grade_afternoon_end:save_twelfth_grade_afternoon_end
    },
    function(data){
        $('#save-calendar-sched').button('complete');
        setTimeout(function(){ 
            $('#save-calendar-sched').attr('disabled',true);
        }, 0); 

    });
}

function save_k12(last_name, first_name, middle_name, level, section, id_no, guardian_mobile, guardian_last_name, guardian_first_name, guardian_middle_name, guardian_email, guardian_address, guardian_relation){
  department = 'k12';
  $.post('/user/new',{
      last_name:last_name,
      first_name:first_name,
      middle_name:middle_name,
      level:level,
      section:section,
      id_no:id_no,
      department:department,
      guardian_mobile:guardian_mobile,
      guardian_last_name:guardian_last_name,
      guardian_first_name:guardian_first_name,
      guardian_middle_name:guardian_middle_name,
      guardian_email:guardian_email,
      guardian_address:guardian_address,
      guardian_relation:guardian_relation
  },
  function(data){
      clear_data();
      form_validated = false
      id_no_validated = false
      $('#k12').html(data);
      $('#save-student').button('complete');
      setTimeout(function(){ 
          $('#save-student').attr('disabled',true);
      }, 0); 
      $('.add-user-footer-left').fadeIn();
      setTimeout(function() {
          $('.add-user-footer-left').fadeOut();
      }, 2000);
      
  });
}

function save_college(last_name, first_name, middle_name, level, college_department, email, mobile, id_no){
  department = 'college';
  $.post('/user/new',{
      department:department,
      last_name:last_name,
      first_name:first_name,
      middle_name:middle_name,
      level:level,
      id_no:id_no,
      college_department:college_department,
      email:email,
      mobile:mobile
  },
  function(data){
      clear_data();
      college_form_validated = false
      college_id_no_validated = false
      $('#college').html(data);
      $('#save-college').button('complete');
      setTimeout(function(){ 
          $('#save-college').attr('disabled',true);
      }, 0); 
      $('.add-user-footer-left').fadeIn();
      setTimeout(function() {
          $('.add-user-footer-left').fadeOut();
      }, 2000);
  });
}

function save_staff(last_name, first_name, middle_name, staff_department, email, mobile, id_no){
  department = 'staff';
  $.post('/user/new',{
      department:department,
      last_name:last_name,
      first_name:first_name,
      middle_name:middle_name,
      id_no:id_no,
      staff_department:staff_department,
      email:email,
      mobile:mobile
  },
  function(data){
      clear_data();
      staff_form_validated = false
      staff_id_no_validated = false
      $('#staff').html(data);
      $('#save-staff').button('complete');
      setTimeout(function(){ 
          $('#save-staff').attr('disabled',true);
      }, 0); 
      $('.add-user-footer-left').fadeIn();
      setTimeout(function() {
          $('.add-user-footer-left').fadeOut();
      }, 2000);
  });
}

function save_fee(name,category,price,desc,add_to){ 
  $.post('/fees/new',{
      name:name,
      category:category,
      price:price,
      desc:desc,
      add_to:add_to
  },
  function(data){
      $('#fees').html(data);
      $('#save-fee').button('complete');
      $('#add-fee-modal').modal('hide');
      $('#snackbar').fadeIn();
        setTimeout(function() {
          $('#snackbar').fadeOut();
      }, 2000);
  });
}

function back_home(){
  $('#table-loading').show();
  
  $.post('/home',{
    tab:tab
  },
    function(data){
    $('#'+tab).html(data);
    $('#table-loading').hide();
    });
}

function edit_student(last_name, first_name, middle_name, level, section, id_no, user_id, guardian_first_name , guardian_last_name, guardian_middle_name, guardian_address, guardian_mobile, guardian_email, guardian_relation){
    $.post('/student/edit',{
        last_name:last_name,
        first_name:first_name,
        middle_name:middle_name,
        level:level,
        section:section,
        id_no:id_no,
        user_id:user_id,
        guardian_first_name:guardian_first_name,
        guardian_last_name:guardian_last_name,
        guardian_middle_name:guardian_middle_name,
        guardian_address:guardian_address,
        guardian_mobile:guardian_mobile,
        guardian_email:guardian_email,
        guardian_relation:guardian_relation
    },
    function(data){
        $('.edit-user-modal-footer .edit-done-btn').button('complete');
        setTimeout(function(){ 
            $('.edit-user-modal-footer .edit-done-btn').attr('disabled',true);
        }, 0);
        $('#k12').html(data);
        $('#edit-user-modal').modal('hide');
        $('#snackbar').fadeIn();
        setTimeout(function() {
          $('#snackbar').fadeOut();
      }, 2000);
    });
}

function edit_college(last_name, first_name, middle_name, level, college_department, contact, email, id_no, user_id){
    $.post('/college/edit',{
        last_name:last_name,
        first_name:first_name,
        middle_name:middle_name,
        level:level,
        college_department:college_department,
        contact:contact,
        email:email,
        id_no:id_no,
        user_id:user_id
    },
    function(data){
        $('.edit-user-modal-footer .edit-college-done-btn').button('complete');
        setTimeout(function(){ 
            $('.edit-user-modal-footer .edit-college-done-btn').attr('disabled',true);
        }, 0);
        $('#college').html(data);
        $('#edit-user-modal').modal('hide');
        $('#snackbar').fadeIn();
        setTimeout(function() {
          $('#snackbar').fadeOut();
      }, 2000);
    });
}

function edit_staff(last_name, first_name, middle_name, staff_department, contact, email, id_no, user_id){
    $.post('/staff/edit',{
        last_name:last_name,
        first_name:first_name,
        middle_name:middle_name,
        staff_department:staff_department,
        contact:contact,
        email:email,
        id_no:id_no,
        user_id:user_id
    },
    function(data){
        $('.edit-user-modal-footer .edit-staff-done-btn').button('complete');
        setTimeout(function(){ 
            $('.edit-staff-modal-footer .edit-staff-done-btn').attr('disabled',true);
        }, 0);
        $('#staff').html(data);
        $('#edit-staff-modal').modal('hide');
        $('#snackbar').fadeIn();
        setTimeout(function() {
          $('#snackbar').fadeOut();
      }, 2000);
    });
}

function go_to_date(){
  $('#calendar-loading').show()
  var month = $('#calendar-month').val();
  var year = $('#calendar-year').val();
  $.post('/calendar/date/go',{
    month:month,
    year:year
  },
    function(data){
        $('#calendar-modal-body').html(data);
        $('#calendar-loading').hide()
    });
}

function populate_calendar(){
  $('#calendar-loading').show()
  $.post('/calendar/data/get',
    function(data){
        $('#calendar-modal-body').html(data);
        $('#calendar-month option[value='+((new Date).getMonth()+1)+']').prop('selected',true);
        $('#calendar-year option[value='+(new Date).getFullYear()+']').prop('selected',true);
        $('#calendar-loading').hide()
    });
}

function next_month(){
  $.post('/calendar/next/get',
    function(data){
        $('#calendar-modal-content').html(data);
    });
}

function prev_month(){
  $.post('/calendar/prev/get',
    function(data){
        $('#calendar-modal-content').html(data);
    });
}

function show_search_load(){
  if (is_done == true){
  $('#search-loading').show();
  is_done = false
  }
}

function toggle_search(){
  if ((typeof eval(tab+'SearchStatus') === 'undefined') || (eval(tab+'SearchStatus') == 'off')){
        $('#'+tab+'-search-panel').show();
        /*$('#search-loading').show();*/
        $('#'+tab).removeClass('maximized');
        $('#'+tab).addClass('minimized');
        window[tab+'SearchStatus'] = 'on';
    }
    else{
        $('#'+tab+'-search-panel').hide();
        $('#search-loading').hide();
        $('#'+tab).addClass('maximized');
        $('#'+tab).removeClass('minimized');
        $('#'+tab+'-search-panel .search-text').val('');
        window[tab+'SearchStatus'] = 'off';
        window[tab+'_result'] = false;
        back_home();
    }
}

function populate_regular_schedule(date){
  $('#calendar-schedule-modal-header').html(date)
  $('.no-class-checkbox').show();
  $('.no-class-checkbox').prop('checked',true);
  $('.no-class-checkbox').change();
}

function populate_irregular_schedule(date,month,day,year){
  $('#calendar-schedule-loading').show();
  $.post('/schedule/irregular/get',{
        month:month,
        day:day,
        year:year
    },
    function(data){
      if (data['junior_kinder_morning_class']){
        $('#junior_kinder_morning_class').prop('checked', true);
        junior_kinder_morning_class = true;
      }
      else{
        $('#junior_kinder_morning_class').prop('checked', false);
        junior_kinder_morning_class =  false;
      }
      if (data['junior_kinder_afternoon_class']){
        $('#junior_kinder_afternoon_class').prop('checked', true);
        junior_kinder_afternoon_class = true;
      }
      else{
        $('#junior_kinder_afternoon_class').prop('checked', false);
        junior_kinder_afternoon_class =  false;
      }

      if (data['senior_kinder_morning_class']){
        $('#senior_kinder_morning_class').prop('checked', true);
        senior_kinder_morning_class = true;
      }
      else{
        $('#senior_kinder_morning_class').prop('checked', false);
        senior_kinder_morning_class =  false;
      }
      if (data['senior_kinder_afternoon_class']){
        $('#senior_kinder_afternoon_class').prop('checked', true);
        senior_kinder_afternoon_class = true;
      }
      else{
        $('#senior_kinder_afternoon_class').prop('checked', false);
        senior_kinder_afternoon_class =  false;
      }

      if (data['first_grade_morning_class']){
        $('#first_grade_morning_class').prop('checked', true);
        first_grade_morning_class = true;
      }
      else{
        $('#first_grade_morning_class').prop('checked', false);
        first_grade_morning_class =  false;
      }
      if (data['first_grade_afternoon_class']){
        $('#first_grade_afternoon_class').prop('checked', true);
        first_grade_afternoon_class = true;
      }
      else{
        $('#first_grade_afternoon_class').prop('checked', false);
        first_grade_afternoon_class =  false;
      }

      if (data['second_grade_morning_class']){
        $('#second_grade_morning_class').prop('checked', true);
        second_grade_morning_class = true;
      }
      else{
        $('#second_grade_morning_class').prop('checked', false);
        second_grade_morning_class =  false;
      }
      if (data['second_grade_afternoon_class']){
        $('#second_grade_afternoon_class').prop('checked', true);
        second_grade_afternoon_class = true;
      }
      else{
        $('#second_grade_afternoon_class').prop('checked', false);
        second_grade_afternoon_class =  false;
      }

      if (data['third_grade_morning_class']){
        $('#third_grade_morning_class').prop('checked', true);
        third_grade_morning_class = true;
      }
      else{
        $('#third_grade_morning_class').prop('checked', false);
        third_grade_morning_class =  false;
      }
      if (data['third_grade_afternoon_class']){
        $('#third_grade_afternoon_class').prop('checked', true);
        third_grade_afternoon_class = true;
      }
      else{
        $('#third_grade_afternoon_class').prop('checked', false);
        third_grade_afternoon_class =  false;
      }

      if (data['fourth_grade_morning_class']){
        $('#fourth_grade_morning_class').prop('checked', true);
        fourth_grade_morning_class = true;
      }
      else{
        $('#fourth_grade_morning_class').prop('checked', false);
        fourth_grade_morning_class =  false;
      }
      if (data['fourth_grade_afternoon_class']){
        $('#fourth_grade_afternoon_class').prop('checked', true);
        fourth_grade_afternoon_class = true;
      }
      else{
        $('#fourth_grade_afternoon_class').prop('checked', false);
        fourth_grade_afternoon_class =  false;
      }

      if (data['fifth_grade_morning_class']){
        $('#fifth_grade_morning_class').prop('checked', true);
        fifth_grade_morning_class = true;
      }
      else{
        $('#fifth_grade_morning_class').prop('checked', false);
        fifth_grade_morning_class =  false;
      }
      if (data['fifth_grade_afternoon_class']){
        $('#fifth_grade_afternoon_class').prop('checked', true);
        fifth_grade_afternoon_class = true;
      }
      else{
        $('#fifth_grade_afternoon_class').prop('checked', false);
        fifth_grade_afternoon_class =  false;
      }

      if (data['sixth_grade_morning_class']){
        $('#sixth_grade_morning_class').prop('checked', true);
        sixth_grade_morning_class = true;
      }
      else{
        $('#sixth_grade_morning_class').prop('checked', false);
        sixth_grade_morning_class =  false;
      }
      if (data['sixth_grade_afternoon_class']){
        $('#sixth_grade_afternoon_class').prop('checked', true);
        sixth_grade_afternoon_class = true;
      }
      else{
        $('#sixth_grade_afternoon_class').prop('checked', false);
        sixth_grade_afternoon_class =  false;
      }

      if (data['seventh_grade_morning_class']){
        $('#seventh_grade_morning_class').prop('checked', true);
        seventh_grade_morning_class = true;
      }
      else{
        $('#seventh_grade_morning_class').prop('checked', false);
        seventh_grade_morning_class =  false;
      }
      if (data['seventh_grade_afternoon_class']){
        $('#seventh_grade_afternoon_class').prop('checked', true);
        seventh_grade_afternoon_class = true;
      }
      else{
        $('#seventh_grade_afternoon_class').prop('checked', false);
        seventh_grade_afternoon_class =  false;
      }

      if (data['eight_grade_morning_class']){
        $('#eight_grade_morning_class').prop('checked', true);
        eight_grade_morning_class = true;
      }
      else{
        $('#eight_grade_morning_class').prop('checked', false);
        eight_grade_morning_class =  false;
      }
      if (data['eight_grade_afternoon_class']){
        $('#eight_grade_afternoon_class').prop('checked', true);
        eight_grade_afternoon_class = true;
      }
      else{
        $('#eight_grade_afternoon_class').prop('checked', false);
        eight_grade_afternoon_class =  false;
      }

      if (data['ninth_grade_morning_class']){
        $('#ninth_grade_morning_class').prop('checked', true);
        ninth_grade_morning_class = true;
      }
      else{
        $('#ninth_grade_morning_class').prop('checked', false);
        ninth_grade_morning_class =  false;
      }
      if (data['ninth_grade_afternoon_class']){
        $('#ninth_grade_afternoon_class').prop('checked', true);
        ninth_grade_afternoon_class = true;
      }
      else{
        $('#ninth_grade_afternoon_class').prop('checked', false);
        ninth_grade_afternoon_class =  false;
      }

      if (data['tenth_grade_morning_class']){
        $('#tenth_grade_morning_class').prop('checked', true);
        tenth_grade_morning_class = true;
      }
      else{
        $('#tenth_grade_morning_class').prop('checked', false);
        tenth_grade_morning_class =  false;
      }
      if (data['tenth_grade_afternoon_class']){
        $('#tenth_grade_afternoon_class').prop('checked', true);
        tenth_grade_afternoon_class = true;
      }
      else{
        $('#tenth_grade_afternoon_class').prop('checked', false);
        tenth_grade_afternoon_class =  false;
      }

      if (data['eleventh_grade_morning_class']){
        $('#eleventh_grade_morning_class').prop('checked', true);
        eleventh_grade_morning_class = true;
      }
      else{
        $('#eleventh_grade_morning_class').prop('checked', false);
        eleventh_grade_morning_class =  false;
      }
      if (data['eleventh_grade_afternoon_class']){
        $('#eleventh_grade_afternoon_class').prop('checked', true);
        eleventh_grade_afternoon_class = true;
      }
      else{
        $('#eleventh_grade_afternoon_class').prop('checked', false);
        eleventh_grade_afternoon_class =  false;
      }

      if (data['twelfth_grade_morning_class']){
        $('#twelfth_grade_morning_class').prop('checked', true);
        twelfth_grade_morning_class = true;
      }
      else{
        $('#twelfth_grade_morning_class').prop('checked', false);
        twelfth_grade_morning_class =  false;
      }
      if (data['twelfth_grade_afternoon_class']){
        $('#twelfth_grade_afternoon_class').prop('checked', true);
        twelfth_grade_afternoon_class = true;
      }
      else{
        $('#twelfth_grade_afternoon_class').prop('checked', false);
        twelfth_grade_afternoon_class =  false;
      } 

      $('.no-class-checkbox').change();

      $('#junior_kinder_morning_start').val(data['junior_kinder_morning_start']);
      $('#junior_kinder_morning_end').val(data['junior_kinder_morning_end']);
      $('#junior_kinder_afternoon_start').val(data['junior_kinder_afternoon_start']);
      $('#junior_kinder_afternoon_end').val(data['junior_kinder_afternoon_end']);

      $('#senior_kinder_morning_start').val(data['senior_kinder_morning_start']);
      $('#senior_kinder_morning_end').val(data['senior_kinder_morning_end']);
      $('#senior_kinder_afternoon_start').val(data['senior_kinder_afternoon_start']);
      $('#senior_kinder_afternoon_end').val(data['senior_kinder_afternoon_end']);

      $('#first_grade_morning_start').val(data['first_grade_morning_start']);
      $('#first_grade_morning_end').val(data['first_grade_morning_end']);
      $('#first_grade_afternoon_start').val(data['first_grade_afternoon_start']);
      $('#first_grade_afternoon_end').val(data['first_grade_afternoon_end']);

      $('#second_grade_morning_start').val(data['second_grade_morning_start']);
      $('#second_grade_morning_end').val(data['second_grade_morning_end']);
      $('#second_grade_afternoon_start').val(data['second_grade_afternoon_start']);
      $('#second_grade_afternoon_end').val(data['second_grade_afternoon_end']);

      $('#third_grade_morning_start').val(data['third_grade_morning_start']);
      $('#third_grade_morning_end').val(data['third_grade_morning_end']);
      $('#third_grade_afternoon_start').val(data['third_grade_afternoon_start']);
      $('#third_grade_afternoon_end').val(data['third_grade_afternoon_end']);

      $('#fourth_grade_morning_start').val(data['fourth_grade_morning_start']);
      $('#fourth_grade_morning_end').val(data['fourth_grade_morning_end']);
      $('#fourth_grade_afternoon_start').val(data['fourth_grade_afternoon_start']);
      $('#fourth_grade_afternoon_end').val(data['fourth_grade_afternoon_end']);

      $('#fifth_grade_morning_start').val(data['fifth_grade_morning_start']);
      $('#fifth_grade_morning_end').val(data['fifth_grade_morning_end']);
      $('#fifth_grade_afternoon_start').val(data['fifth_grade_afternoon_start']);
      $('#fifth_grade_afternoon_end').val(data['fifth_grade_afternoon_end']);

      $('#sixth_grade_morning_start').val(data['sixth_grade_morning_start']);
      $('#sixth_grade_morning_end').val(data['sixth_grade_morning_end']);
      $('#sixth_grade_afternoon_start').val(data['sixth_grade_afternoon_start']);
      $('#sixth_grade_afternoon_end').val(data['sixth_grade_afternoon_end']);

      $('#seventh_grade_morning_start').val(data['seventh_grade_morning_start']);
      $('#seventh_grade_morning_end').val(data['seventh_grade_morning_end']);
      $('#seventh_grade_afternoon_start').val(data['seventh_grade_afternoon_start']);
      $('#seventh_grade_afternoon_end').val(data['seventh_grade_afternoon_end']);

      $('#eight_grade_morning_start').val(data['eight_grade_morning_start']);
      $('#eight_grade_morning_end').val(data['eight_grade_morning_end']);
      $('#eight_grade_afternoon_start').val(data['eight_grade_afternoon_start']);
      $('#eight_grade_afternoon_end').val(data['eight_grade_afternoon_end']);

      $('#ninth_grade_morning_start').val(data['ninth_grade_morning_start']);
      $('#ninth_grade_morning_end').val(data['ninth_grade_morning_end']);
      $('#ninth_grade_afternoon_start').val(data['ninth_grade_afternoon_start']);
      $('#ninth_grade_afternoon_end').val(data['ninth_grade_afternoon_end']);

      $('#tenth_grade_morning_start').val(data['tenth_grade_morning_start']);
      $('#tenth_grade_morning_end').val(data['tenth_grade_morning_end']);
      $('#tenth_grade_afternoon_start').val(data['tenth_grade_afternoon_start']);
      $('#tenth_grade_afternoon_end').val(data['tenth_grade_afternoon_end']);

      $('#eleventh_grade_morning_start').val(data['eleventh_grade_morning_start']);
      $('#eleventh_grade_morning_end').val(data['eleventh_grade_morning_end']);
      $('#eleventh_grade_afternoon_start').val(data['eleventh_grade_afternoon_start']);
      $('#eleventh_grade_afternoon_end').val(data['eleventh_grade_afternoon_end']);

      $('#twelfth_grade_morning_start').val(data['twelfth_grade_morning_start']);
      $('#twelfth_grade_morning_end').val(data['twelfth_grade_morning_end']);
      $('#twelfth_grade_afternoon_start').val(data['twelfth_grade_afternoon_start']);
      $('#twelfth_grade_afternoon_end').val(data['twelfth_grade_afternoon_end']);

      $('#calendar-schedule-modal-header').html(data['date'])
      $('#calendar-schedule-loading').hide();
    });
}

function listen_to_checkbox(){
  if (($('#junior_kinder_morning_class').prop('checked') == junior_kinder_morning_class) &&
     ($('#junior_kinder_afternoon_class').prop('checked') == junior_kinder_afternoon_class) &&
     ($('#senior_kinder_morning_class').prop('checked') == senior_kinder_morning_class) &&
     ($('#senior_kinder_afternoon_class').prop('checked') == senior_kinder_afternoon_class) &&
     ($('#first_grade_morning_class').prop('checked') == first_grade_morning_class) &&
     ($('#first_grade_afternoon_class').prop('checked') == first_grade_afternoon_class) &&
     ($('#second_grade_morning_class').prop('checked') == second_grade_morning_class) &&
     ($('#second_grade_afternoon_class').prop('checked') == second_grade_afternoon_class) &&
     ($('#third_grade_morning_class').prop('checked') == third_grade_morning_class) &&
     ($('#third_grade_afternoon_class').prop('checked') == third_grade_afternoon_class) &&
     ($('#fourth_grade_morning_class').prop('checked') == fourth_grade_morning_class) &&
     ($('#fourth_grade_afternoon_class').prop('checked') == fourth_grade_afternoon_class) &&
     ($('#fifth_grade_morning_class').prop('checked') == fifth_grade_morning_class) &&
     ($('#fifth_grade_afternoon_class').prop('checked') == fifth_grade_afternoon_class) &&
     ($('#sixth_grade_morning_class').prop('checked') == sixth_grade_morning_class) &&
     ($('#sixth_grade_afternoon_class').prop('checked') == sixth_grade_afternoon_class) &&
     ($('#seventh_grade_morning_class').prop('checked') == seventh_grade_morning_class) &&
     ($('#seventh_grade_afternoon_class').prop('checked') == seventh_grade_afternoon_class) &&
     ($('#eight_grade_morning_class').prop('checked') == eight_grade_morning_class) &&
     ($('#eight_grade_afternoon_class').prop('checked') == eight_grade_afternoon_class) &&
     ($('#ninth_grade_morning_class').prop('checked') == ninth_grade_morning_class) &&
     ($('#ninth_grade_afternoon_class').prop('checked') == ninth_grade_afternoon_class) &&
     ($('#tenth_grade_morning_class').prop('checked') == tenth_grade_morning_class) &&
     ($('#tenth_grade_afternoon_class').prop('checked') == tenth_grade_afternoon_class) &&
     ($('#eleventh_grade_morning_class').prop('checked') == eleventh_grade_morning_class) &&
     ($('#eleventh_grade_afternoon_class').prop('checked') == eleventh_grade_afternoon_class) &&
     ($('#twelfth_grade_morning_class').prop('checked') == twelfth_grade_morning_class) &&
     ($('#twelfth_grade_afternoon_class').prop('checked') == twelfth_grade_afternoon_class)) {

        $('#save-calendar-sched').attr('disabled',true);

     }
     else{

        $('#save-calendar-sched').removeAttr('disabled');

     }
}

function populate_schedule(){
  days = ['monday','tuesday','wednesday','thursday','friday']
  $('#schedule-loading').show();
  $('.schedule-nav-tabs li').addClass('disabled');
  $.post('/schedule/regular/get',
    function(data){
      $('#monday-tab').addClass('active');
      $('.schedule-nav-tabs li').removeClass('disabled');
      
      for (var i = 0; i <= days.length - 1; i++) {
        $('#'+days[i]+'_junior_kinder_morning_start').val(data[days[i]]['junior_kinder_morning_start']);
        $('#'+days[i]+'_junior_kinder_morning_end').val(data[days[i]]['junior_kinder_morning_end']);
        $('#'+days[i]+'_junior_kinder_afternoon_start').val(data[days[i]]['junior_kinder_afternoon_start']);
        $('#'+days[i]+'_junior_kinder_afternoon_end').val(data[days[i]]['junior_kinder_afternoon_end']);

        $('#'+days[i]+'_senior_kinder_morning_start').val(data[days[i]]['senior_kinder_morning_start']);
        $('#'+days[i]+'_senior_kinder_morning_end').val(data[days[i]]['senior_kinder_morning_end']);
        $('#'+days[i]+'_senior_kinder_afternoon_start').val(data[days[i]]['senior_kinder_afternoon_start']);
        $('#'+days[i]+'_senior_kinder_afternoon_end').val(data[days[i]]['senior_kinder_afternoon_end']);

        $('#'+days[i]+'_first_grade_morning_start').val(data[days[i]]['first_grade_morning_start']);
        $('#'+days[i]+'_first_grade_morning_end').val(data[days[i]]['first_grade_morning_end']);
        $('#'+days[i]+'_first_grade_afternoon_start').val(data[days[i]]['first_grade_afternoon_start']);
        $('#'+days[i]+'_first_grade_afternoon_end').val(data[days[i]]['first_grade_afternoon_end']);

        $('#'+days[i]+'_second_grade_morning_start').val(data[days[i]]['second_grade_morning_start']);
        $('#'+days[i]+'_second_grade_morning_end').val(data[days[i]]['second_grade_morning_end']);
        $('#'+days[i]+'_second_grade_afternoon_start').val(data[days[i]]['second_grade_afternoon_start']);
        $('#'+days[i]+'_second_grade_afternoon_end').val(data[days[i]]['second_grade_afternoon_end']);

        $('#'+days[i]+'_third_grade_morning_start').val(data[days[i]]['third_grade_morning_start']);
        $('#'+days[i]+'_third_grade_morning_end').val(data[days[i]]['third_grade_morning_end']);
        $('#'+days[i]+'_third_grade_afternoon_start').val(data[days[i]]['third_grade_afternoon_start']);
        $('#'+days[i]+'_third_grade_afternoon_end').val(data[days[i]]['third_grade_afternoon_end']);

        $('#'+days[i]+'_fourth_grade_morning_start').val(data[days[i]]['fourth_grade_morning_start']);
        $('#'+days[i]+'_fourth_grade_morning_end').val(data[days[i]]['fourth_grade_morning_end']);
        $('#'+days[i]+'_fourth_grade_afternoon_start').val(data[days[i]]['fourth_grade_afternoon_start']);
        $('#'+days[i]+'_fourth_grade_afternoon_end').val(data[days[i]]['fourth_grade_afternoon_end']);

        $('#'+days[i]+'_fifth_grade_morning_start').val(data[days[i]]['fifth_grade_morning_start']);
        $('#'+days[i]+'_fifth_grade_morning_end').val(data[days[i]]['fifth_grade_morning_end']);
        $('#'+days[i]+'_fifth_grade_afternoon_start').val(data[days[i]]['fifth_grade_afternoon_start']);
        $('#'+days[i]+'_fifth_grade_afternoon_end').val(data[days[i]]['fifth_grade_afternoon_end']);

        $('#'+days[i]+'_sixth_grade_morning_start').val(data[days[i]]['sixth_grade_morning_start']);
        $('#'+days[i]+'_sixth_grade_morning_end').val(data[days[i]]['sixth_grade_morning_end']);
        $('#'+days[i]+'_sixth_grade_afternoon_start').val(data[days[i]]['sixth_grade_afternoon_start']);
        $('#'+days[i]+'_sixth_grade_afternoon_end').val(data[days[i]]['sixth_grade_afternoon_end']);

        $('#'+days[i]+'_seventh_grade_morning_start').val(data[days[i]]['seventh_grade_morning_start']);
        $('#'+days[i]+'_seventh_grade_morning_end').val(data[days[i]]['seventh_grade_morning_end']);
        $('#'+days[i]+'_seventh_grade_afternoon_start').val(data[days[i]]['seventh_grade_afternoon_start']);
        $('#'+days[i]+'_seventh_grade_afternoon_end').val(data[days[i]]['seventh_grade_afternoon_end']);

        $('#'+days[i]+'_eight_grade_morning_start').val(data[days[i]]['eight_grade_morning_start']);
        $('#'+days[i]+'_eight_grade_morning_end').val(data[days[i]]['eight_grade_morning_end']);
        $('#'+days[i]+'_eight_grade_afternoon_start').val(data[days[i]]['eight_grade_afternoon_start']);
        $('#'+days[i]+'_eight_grade_afternoon_end').val(data[days[i]]['eight_grade_afternoon_end']);

        $('#'+days[i]+'_ninth_grade_morning_start').val(data[days[i]]['ninth_grade_morning_start']);
        $('#'+days[i]+'_ninth_grade_morning_end').val(data[days[i]]['ninth_grade_morning_end']);
        $('#'+days[i]+'_ninth_grade_afternoon_start').val(data[days[i]]['ninth_grade_afternoon_start']);
        $('#'+days[i]+'_ninth_grade_afternoon_end').val(data[days[i]]['ninth_grade_afternoon_end']);

        $('#'+days[i]+'_tenth_grade_morning_start').val(data[days[i]]['tenth_grade_morning_start']);
        $('#'+days[i]+'_tenth_grade_morning_end').val(data[days[i]]['tenth_grade_morning_end']);
        $('#'+days[i]+'_tenth_grade_afternoon_start').val(data[days[i]]['tenth_grade_afternoon_start']);
        $('#'+days[i]+'_tenth_grade_afternoon_end').val(data[days[i]]['tenth_grade_afternoon_end']);

        $('#'+days[i]+'_eleventh_grade_morning_start').val(data[days[i]]['eleventh_grade_morning_start']);
        $('#'+days[i]+'_eleventh_grade_morning_end').val(data[days[i]]['eleventh_grade_morning_end']);
        $('#'+days[i]+'_eleventh_grade_afternoon_start').val(data[days[i]]['eleventh_grade_afternoon_start']);
        $('#'+days[i]+'_eleventh_grade_afternoon_end').val(data[days[i]]['eleventh_grade_afternoon_end']);

        $('#'+days[i]+'_twelfth_grade_morning_start').val(data[days[i]]['twelfth_grade_morning_start']);
        $('#'+days[i]+'_twelfth_grade_morning_end').val(data[days[i]]['twelfth_grade_morning_end']);
        $('#'+days[i]+'_twelfth_grade_afternoon_start').val(data[days[i]]['twelfth_grade_afternoon_start']);
        $('#'+days[i]+'_twelfth_grade_afternoon_end').val(data[days[i]]['twelfth_grade_afternoon_end']);
      };

      $('#schedule-loading').hide();
    });
}

function save_admin(){
  $('#save-admin').button('loading');
  if ($('#is_super_admin').is(":checked")){
    is_super_admin = true;
  }
  else{
    is_super_admin = false;
  }
  first_name = $('#add_admin_first_name').val();
  last_name = $('#add_admin_last_name').val();
  email = $('#add_admin_email').val();
  $.post('/accounts/new',{
      first_name:first_name,
      last_name:last_name,
      email:email,
      is_super_admin:is_super_admin
  },
  function(data){
    $('#add-admin-error').html('');
    $('#save-admin').button('complete');
    if (data['status']){
      $('#add-admin-error').html(data['error']);
    }
    else{
      $('#accounts-table tbody').html(data);
      setTimeout(function(){ 
          $('#save-admin').attr('disabled',true);
          $('#add_admin_first_name').focus();
          $('#add_admin_email').val('');
          $('#add_admin_first_name').val('');
          $('#add_admin_last_name').val('');
          $('#is_super_admin').prop('checked',false);
          $('.add-admin-modal-body .form-control').change();
      }, 0); 
      $('.add-admin-footer-left').fadeIn();
      setTimeout(function() {
          $('.add-admin-footer-left').fadeOut();
      }, 2000);
    }
  });
}

function isNumberKey(evt){
    var charCode = (evt.which) ? evt.which : event.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}

function display_balance(balance){
  $('#cashTotal').html(balance);
  setTimeout(function() {
    $('#amountPaid').focus();
  }, 500);
}

function collect_payment(amount){
  $.post('/fees/collect',{
      amount:amount
  },
  function(data){
    $('#tenderedDoneBtn').button('complete');
    $('#collect-payment-modal').modal('hide');
    $('#studentFeesContainer').html(data);
  });
}

function add_fees_to_student(){
  $('#add-fee-btn').button('loading');
  $.post('/students/fees/add',{
    fees_to_add:fees_to_add
  },
    function(data){
      fees_to_add = [];
      $('.add-fee-row').find('.fee-check-td').html('');
      $('#add-fee-btn').button('complete');
      $('#add-student-fee-modal').modal('hide');
      $('#studentFeesContainer').html(data);
      setTimeout(function() {
        $('#add-fee-btn').attr('disabled',true);
      }, 500);
    });
}
