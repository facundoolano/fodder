
//The URLS are not very restful, to avoid having to carry around the username everywhere.
//The user info is already saved in the session_id cookie

function show_registerform(){
	load_template('registerform.html', {}, function(html){
		$('#submit-container').html(html);
		$('#register_form').submit(function() {
			
			var url = '/users/'; 
			$.ajax({
				type: 'PUT',
				url: url, 
				success: login,
				data : {
					username: $('#username').val(),
					email: $('#email').val(),
					password1: $('#password1').val(),
					password2: $('#password2').val()
					}, 
				dataType: 'json'
			})
			
			return false;
		});	
	});
	
}

function show_loginform() {
	load_template('loginform.html', {}, function(html){
		$('#submit-container').html(html);
		$('#login_form').submit(function() {
			
			var url = '/users/'; 
			$.ajax({
				type: 'POST',
				url: url, 
				success: login,
				data : {
					username: $('#username').val(),
					password: $('#password').val()
					}, 
				dataType: 'json'
			})
			
			return false;
		});	
	});
}

function is_logged_in(){
	return document.cookie.indexOf("session_key") >= 0;
}



function login() {
	show_entryform();
	inline_template('#userbar-template', {username: getCookie('username')})
}

function logout(){
	console.log('call logout');
	var url = '/users/'; 
	$.ajax({
		type: 'DELETE',
		url: url, 
		success: function() {
			show_loginform();
			$('#userbar').remove();
		},
		dataType: 'json'
	})
}


$(function() {
	if (!is_logged_in()){	
		show_loginform();
	}
});