var mobilenumberError =document.getElementById('mobilenumber-error');
var submitError =document.getElementById('submit-error');
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
function validateFormmob(){
	if( !validateMobilenumber()){
		submitError.style.display = 'block';
		submitError.innerHTML = 'please correct form';
		setTimeout(function(){submitError.style.display = 'none';},3000);
		return false;
	}
    return true;
}