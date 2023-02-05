var firstError =document.getElementById('first-error');
var lastError =document.getElementById('last-error');
var phoneError =document.getElementById('phone-error');
var emailError =document.getElementById('email-error');
var line1Error =document.getElementById('line1-error');
var line2Error =document.getElementById('line2-error');
var cityError =document.getElementById('city-error');
var stateError =document.getElementById('state-error');
var countryError =document.getElementById('country-error');
var submitError =document.getElementById('submit-error');
function validateFirst(){
	var firstname = document.getElementById('id_first_name').value;
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