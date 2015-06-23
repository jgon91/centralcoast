function process_login() {
	console.log("function called")
	$.ajax({
		method: "POST",
		url: "login/",
		data: $('#login-form').serialize(),
		success: function(data, status, xhr){
			if(data.success){
				location.reload();
			}else if(data == 1){
				$("#errorMessage").html("");
			}
		}
	});
}
/*
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
}
*/