tab = 'log'
function change_tab(page){
  tab = page;
  if (tab == 'attendance'){
    $('#add-user-btn').show();
  }
  else{
    $('#add-user-btn').hide();
  }
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
    $('#add_last_name').val('');
    $('#add_first_name').val('');
    $('#add_middle_name').val('');
    $('#add_level').val('');
    $('#add_section').val('');
    $('#add_contact').val('');
    $('#add_id_no').val('');
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


function search_data(){
    var last_name = $('#search_last_name').val();
    var first_name = $('#search_first_name').val();
    var middle_name = $('#search_middle_name').val();
    var id_no = $('#search_id_no').val();
    var level = $('#search_level').val();
    var section = $('#search_section').val();
    var contact = $('#search_contact').val();
    var absences = $('#search_absences').val();
    var lates = $('#search_lates').val();

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
        lates:lates
        
    },
    function(data){
        $('#'+tab).html(data);
    });
}


function save_sched(){
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
}

function save_user(last_name, first_name, middle_name, level, section, contact, id_no){
  $('#save-user span').css({'display':'none'});
    $('#save-user').css({'background-image':'url(../static/images/preloader_white.png)','background-repeat': 'no-repeat','background-position': 'center'});
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
}





