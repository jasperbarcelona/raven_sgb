function login(){
  $('#login-form-loader').show()
  school_no = $('#school_no').val();
  user_email = $('#user_email').val();
  user_password = $('#user_password').val();
  $.post('/user/authenticate',{
    school_no:school_no,
  	user_email:user_email,
  	user_password:user_password
  },
  	function(data){
	  	if (data['status'] == 'failed'){
        $('#login-error-container').show();
	  		$('#login-error').html(data['error']);
	  		$('#login-form-loader').hide();
	  	}
	   	else{
	   		$(location).attr('href', '/');
	   	}
  });
}
