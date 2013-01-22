
function show_registerform(){
	load_template('registerform.html', {}, function(html){
		$('#submit-container').html(html);
		$('#register_form').submit(function() {
			
			$.post('/users/', {
				username: $('#username').val(),
				email: $('#email').val(),
				password1: $('#password1').val(),
				password2: $('#password2').val()
			}, function() {
				show_entryform();
			}, 'json')
			
			return false;
		});	
	});
	
}

function show_loginform() {
	replace_template('loginform.html', {}, '#submit-container');
}

function is_logged_in(){
	return document.cookie.indexOf("session_key") >= 0;
}

function login(){
	
}

function logout(){
	
}


$(function() {
	if (!is_logged_in()){	
		show_loginform();
	}
});