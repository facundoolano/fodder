
function show_registerform(){
	replace_template('registerform.html', {}, '#submit-container');
}

function show_loginform() {
	replace_template('loginform.html', {}, '#submit-container');
}

function login(){
	
}

function logout(){
	
}


$(function() {
	//TODO if not logged in
	show_loginform();
});