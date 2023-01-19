var otpError =document.getElementById('otp-error');
function validateOtp(){
	var otp = document.getElementById('otp').value;
	if(otp.length==0){
		otpError.innerHTML = 'otp required';
		return false;
	}
	if(otp.length !== 6){
		otpError.innerHTML = 'otp should 6 digits';
		return false;
	}
	if(!otp.match(/^[0-9]{6}$/)){
		otpError.innerHTML = 'only digits please';
		return false;
	}
	otpError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
	return true;
}
function validateFormotp(){
	if( !validateOtp()){
		submitError.style.display = 'block';
		submitError.innerHTML = 'please correct form';
		setTimeout(function(){submitError.style.display = 'none';},3000);
		return false;
	}
    return true;
}