tab = $('#tab').val();
is_done = true;
form_validated = false
id_no_validated = false

logsSearchStatus = 'off'
attendanceSearchStatus = 'off'
absentSearchStatus = 'off'
lateSearchStatus = 'off'

logs_result = false;
attendance_result = false;
absent_result = false;
late_result = false;

if (tab == 'attendance'){
    $('#add-user-btn').show();
  }
  else{
    $('#add-user-btn').hide();
  }

function view_message(){
  $('.message-modal-dialog').animate({'width':'900px'});
  $('#message-modal-body').animate({'width':'340px'});
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
  console.log('openning messages')
  $.post('/messages',
  function(data){
    $('#message-modal-body').html(data);
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
      attendance_result = true;
      is_done = true;
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
      logs_result = true;
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
      $('#save-user').button('complete');
      setTimeout(function(){ 
          $('#save-user').attr('disabled',true);
      }, 0);
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
        $('.edit-user-modal-footer .done-btn').button('complete');
        setTimeout(function(){ 
            $('.edit-user-modal-footer .done-btn').attr('disabled',true);
        }, 0);
        $('#attendance').html(data);
        $('#edit-user-modal').modal('hide');
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
  $('#schedule-modal-title').html(date);
  $('.no-class-checkbox').show();
  $('.no-class-checkbox').prop('checked',true);
  $('.no-class-checkbox').change();
}

function populate_irregular_schedule(date,month,day,year){
  $('#schedule-modal-title').html(date + ' (Irregular Schedule)');
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
  first_name = $('#add_admin_first_name').val();
  middle_name = $('#add_admin_middle_name').val();
  last_name = $('#add_admin_last_name').val();
  email = $('#add_admin_email').val();
  status = $('#add_admin_status').val();
  $.post('/accounts/new',{
      first_name:first_name,
      middle_name:middle_name,
      last_name:last_name,
      email:email,
      status:status
  },
  function(data){
    if (data['status']){
      $('#add-admin-error').html(data['error']);
    }
    else{
      $('#accounts-table tbody').html(data);
      $('#save-admin').button('complete');
      setTimeout(function(){ 
          $('#save-admin').attr('disabled',true);
          $('#add_admin_first_name').focus();
          $('#add_admin_email').val('');
          $('#add_admin_first_name').val('');
          $('#add_admin_last_name').val('');
          $('#add_admin_middle_name').val('');
          $('.add-admin-modal-body .form-control').change();
      }, 0); 
      $('.add-admin-footer-left').fadeIn();
      setTimeout(function() {
          $('.add-admin-footer-left').fadeOut();
      }, 2000);
    }
  });
}