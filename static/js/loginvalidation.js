var passwordError =document.getElementById('password-error');
var submitError =document.getElementById('submit-error');
function validatePassword(){
	var password = document.getElementById('password').value;
	if(password.length==0){
	    passwordError.innerHTML = 'password required'
	    return false;
	}
	if(password.length !==6){
		passwordError.innerHTML = 'password should 6 characters';
		return false;
	}
	if(!password.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/)){
	    passwordError.innerHTML = 'Atleat one character and one number';
		return false;
	} 
	passwordError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
		return true;
}
function validateFormlog(){
	if( !validateEmail() || !validatePassword()){
		submitError.style.display = 'block';
		submitError.innerHTML = 'please correct form';
		setTimeout(function(){submitError.style.display = 'none';},3000);
		return false;
	}
    return true;
}