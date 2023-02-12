var emailError =document.getElementById('email-error');
var submitError =document.getElementById('submit-error');
function validateEmailForgot(){
	console.log('2hhhhhhhhhhhhh')
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
function validateFormForgot(){
	if(!validateEmailForgot()){
		submitError.style.display = 'block';
		submitError.innerHTML = 'please correct form';
		setTimeout(function(){submitError.style.display = 'none';},3000);
		return false;
	}
	return true;
}