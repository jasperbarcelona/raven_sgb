tab = $('#tab').val();
is_done = true;
form_validated = false
id_no_validated = false

if (tab == 'attendance'){
    $('#add-user-btn').show();
  }
  else{
    $('#add-user-btn').hide();
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

function validate_user_form(status){
  form_validated = status;
  if ((form_validated == true) && (id_no_validated == true)){
    $('#save-user').removeAttr('disabled');
  }
  else{
    $('#save-user').attr('disabled',true);
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
  if (tab == 'attendance'){
    $('#add-user-btn').show();
  }
  else{
    $('#add-user-btn').hide();
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
  $('#student-info-loading').show();
  $.post('/student/info/get',{
        student_id:studentId,
    },
    function(data){
        $('.edit-user-modal-dialog .modal-content').html(data);
    });
}

function resize_tbody(height,subtrahend){
  $("#main-content").css("height",height);
  $("tbody").css("height",height-subtrahend);
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
    });
    $('.modal').modal('hide');
    $('#message-status-modal').modal('show');
  }
  else if (navigator.onLine==false) {
    alert('You are offline!');
  }
  else{
    alert('Message is empty!');
  }
}

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
    $('.add-user-modal-body').find('.form-control').val('');
    $('#id-error').text('');
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


function search_attendance(){
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
      $('#'+tab).html(data);
      $('#search-loading').hide();
      is_done = true
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
  var level = $('#log_search_level').val();
  var section = $('#log_search_section').val();
  var reset = 'yes';
  
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
      $('#'+tab).html(data);
      $('#search-loading').hide();
      is_done = true
      isPreviousEventComplete = true
  });
}

function logs_next_search(){
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

function load_next(tab){
    isPreviousEventComplete = false;
    var data = tab
    $.post('/loadmore',{data:data},
    function(data){
        $('#'+tab).append(data);
        isPreviousEventComplete = true;
    });
}

/*function render_watermark(){
  
path = $('#path').val();
alert(path)
$(".tab-pane").css({'background-image':'url(../static/images/watermark.png)','background-repeat': 'no-repeat','background-position': 'center'});
}*/

function save_sched(){
  $('#save-sched span').css({'display':'none'});
    $('#save-sched').css({'background-image':'url(../static/images/assets/white.GIF)','background-repeat': 'no-repeat','background-position': 'center'});
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
}

function save_student(last_name, first_name, middle_name, level, section, contact, id_no){
  department = 'student'
  $.post('/user/new',{
      last_name:last_name,
      first_name:first_name,
      middle_name:middle_name,
      level:level,
      section:section,
      contact:contact,
      id_no:id_no,
      department:department
  },
  function(data){
      clear_data();
      form_validated = false
      id_no_validated = false
      $('#attendance').html(data);
      $('#save-student').css({'background-image':'none'});
      $('#save-student span').show();
      $('.add-user-footer-left').fadeIn();
      setTimeout(function() {
          $('.add-user-footer-left').fadeOut();
      }, 2000);
      
  });
}

function save_user(last_name, first_name, middle_name, id_no){
  department = 'faculty'
  $.post('/user/new',{
      last_name:last_name,
      first_name:first_name,
      middle_name:middle_name,
      id_no:id_no,
      department:department
  },
  function(data){
      clear_data();
      form_validated = false
      id_no_validated = false
      $('#attendance').html(data);
      $('#save-user').css({'background-image':'none'});
      $('#save-user span').show();
      $('.add-user-footer-left').fadeIn();
      setTimeout(function() {
          $('.add-user-footer-left').fadeOut();
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

function edit_user(last_name, first_name, middle_name, level, section, contact, id_no, user_id){
  $('.edit-user-modal-footer .done-btn span').css({'display':'none'});
    $('.edit-user-modal-footer .done-btn').css({'background-image':'url(../static/images/assets/white.GIF)','background-repeat': 'no-repeat','background-position': 'center'});
    $.post('/user/edit',{
        last_name:last_name,
        first_name:first_name,
        middle_name:middle_name,
        level:level,
        section:section,
        contact:contact,
        id_no:id_no,
        user_id:user_id
    },
    function(data){
        $('.edit-user-modal-footer .done-btn').attr('disabled',true);
        $('.edit-user-modal-footer .done-btn').css({'background-image':'none'});
        $('.edit-user-modal-footer .done-btn span').show();
        $('#attendance').html(data);
        $('#edit-user-modal').modal('hide');
        $('#snackbar').fadeIn();
        setTimeout(function() {
          $('#snackbar').fadeOut();
      }, 2000);
    });
}

function populate_calendar(){
  $.post('/calendar/data/get',
    function(data){
        $('#calendar-container table').html(data);
    });
}

function show_search_load(){
  if (is_done == true){
  console.log('showing');
  $('#search-loading').show();
  is_done = false
  }
}




