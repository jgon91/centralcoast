function process_login() {
	console.log("function called")
	$.ajax({
		method: "POST",
		url: "login/",
		data: $('#login-form').serialize(),
		success: function(data, status, xhr){
			//if(data.success){
			alert();
			if(true){
				
				location.reload();
			} else if (data.code == 1){
				$("#errorMessage").html("User Inactive. Call your manager.");
				$("#errorMessage").attr("class", "alert-danger alert");
			} else if (data.code == 2){
				$("#errorMessage").html("Wrong Username/Password. Try it again.");
				$("#errorMessage").attr("class", "alert-danger alert");
			}
		}
	});
}
/*
data: {"csrf_token": '{{csrf_token}}', }
							"qr_code": qr_code
							"idEquipment": idEquipment
							
							{{QR_CODE}} ID_IDENTIFICATION
							
function getUserInformation(token) {
	console.log("function called")
	$.ajax({
		method: "POST",
		url: "login/",
		data: 'csrf_token':token ,
		success: function(data, status, xhr){
			$("#lastName").html(data.lastName);
		}
	});
	
	$.ajax({
		method: "POST",
		url: "login/",
		data: 'csrf_token':token ,
		success: function(data, status, xhr){
			if(data.success){
				location.reload();
			}
		}
	});
	
	$.ajax({
		method: "POST",
		url: "login/",
		data: 'csrf_token':token ,
		success: function(data, status, xhr){
			if(data.success){
				location.reload();
			}
		}
	});
}*/