var password1Error =document.getElementById('password1-error');
var password2Error =document.getElementById('password2-error');
var submitError =document.getElementById('submit-error');
function validateForgotPassword1(){
	console.log('1hhhhhhhhhhhhh')
	var password1 = document.getElementById('password1').value;
	if(password1.length==0){
	    password1Error.innerHTML = 'password required'
	    return false;
	}
	if(password1.length !==6){
		password1Error.innerHTML = 'should 6 characters ';
		return false;
	}
	if(!password1.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/)){
		password1Error.innerHTML = 'Atleat one character and one number'
		return false;
	   
	} 
	password1Error.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
	return true;
}
function validateForgotPassword2(){
	console.log('2hhhhhhhhhhhhh')
	var password2 = document.getElementById('password2').value;
	if(password2.length==0){
	    password2Error.innerHTML = 'password required'
	    return false;
	}
	if(password2.length !==6){
		password2Error.innerHTML = 'password should 6 characters';
		return false;
	}
	if(!password2.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/)){
		password2Error.innerHTML = 'Atleat one character and one number'
		return false;
	} 
	password2Error.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
		return true;
}
function validateFormChange(){
	if(!validateForgotPassword1()||!validateForgotPassword2()){
		submitError.style.display = 'block';
		submitError.innerHTML = 'please correct form';
		setTimeout(function(){submitError.style.display = 'none';},3000);
		return false;
	}
	return true;
}