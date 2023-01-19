var firstnameError =document.getElementById('firstname-error');
var lastnameError =document.getElementById('lastname-error');
var mobilenumberError =document.getElementById('mobilenumber-error');
var emailError =document.getElementById('email-error');
var password1Error =document.getElementById('password1-error');
var password2Error =document.getElementById('password2-error');
var submitError =document.getElementById('submit-error');
function validateFirstname(){
	var firstname = document.getElementById('firstname').value;
	if(firstname.length==0){
		firstnameError.innerHTML = 'name is required';
		return false;
	}
	if(!firstname.match(/^[A-Za-z]*$/)){
		firstnameError.innerHTML = 'write first name';
		return false;
	} 
	firstnameError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
	return true;
}
function validateLastname(){
	var lastname = document.getElementById('lastname').value;
	if(lastname.length==0){
		lastnameError.innerHTML = 'name is required';
		return false;
	}
	if(!lastname.match(/^[A-Za-z]*$/)){
		lastnameError.innerHTML = 'write last name';
		return false;
	} 
	lastnameError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
	return true;
}
function validateMobilenumber(){
	var mobilenumber = document.getElementById('mobilenumber').value;
	if(mobilenumber.length==0){
		mobilenumberError.innerHTML = 'mobile no required';
		return false;
	}
	if(mobilenumber.length !==10){
		mobilenumberError.innerHTML = 'mobile no should 10 digits';
		return false;
	}
	if(!mobilenumber.match(/^[0-9]{10}$/)){
		mobilenumberError.innerHTML = 'only digits please';
		return false;
	}
	mobilenumberError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
	return true;

}
function validateEmail(){
	var email = document.getElementById('email').value;
	if(email.length==0){
		emailError.innerHTML = 'email required';
		return false;
	}
	if(!email.match(/^[A-Za-z\._\-[0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/)){
		emailError.innerHTML = 'email invalid'
		return false;
	}
	emailError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
	return true;

}
function validatePassword1(){
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
function validatePassword2(){
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
function validateForm(){
	if(!validateFirstname() || !validateLastname() || !validateMobilenumber() || !validateEmail() || !validatePassword1() || !validatePassword2()){
		submitError.style.display = 'block';
		submitError.innerHTML = 'please correct form';
		setTimeout(function(){submitError.style.display = 'none';},3000);
		return false;
	}
	return true;
}