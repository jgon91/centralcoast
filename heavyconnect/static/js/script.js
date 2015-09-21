//SCRIPT LOGIN PAGE***

function process_login() {
	$.ajax({
		method: "POST",
		url: "login/",
		data: $('#login-form').serialize(),
		success: function(data, status, xhr){
			if(data.success){
				location.reload();
			} else if (data.code == 1){
				$("#errorMessage").html("User Inactive. Call your manager.");
				$("#errorMessage").attr("class", "fade in");
				$("#errorMessage").css('display', 'block');
			} else if (data.code == 2){
				$("#errorMessage").html("Wrong Username/Password.");
				$("#errorMessage").attr("class", "fade in");
				$("#errorMessage").css('display', 'block');
			} else if (data.code == 3){
				$("#errorMessage").html("Enter the username and password.");
				$("#errorMessage").attr("class", "fade in");
				$("#errorMessage").css('display', 'block');
			} else if (data.code == 4 || data.code == 5){
				$("#errorMessage").html("Error. Please, contact the suport.");
				$("#errorMessage").attr("class", "fade in");
				$("#errorMessage").css('display', 'block');
			}
		}
	});
}
//END SCRIPT LOGIN PAGE


/*** SAVE TASK BEGIN ***/
function saveTask(token, url, urlScheduler){
	$.ajax({
		method: "POST",
		url: url,
		data: {"csrfmiddlewaretoken": token,
				"category": $("#category").val(),
				"employeeId": $("#employee").val(), 
				"field": $("#field").val(), 
				"passes": $("#passes").val(), 
				"hours_prediction": $("#hours_prediction").val(), 
				"time": $("#time").val(), 
				"date": $("#date").val(), 
				"description": $("#description").val(),
				"machine": $("#machineSelected").val(), 
				"implement": $("#implementSelected").val(),
				"implement2": $("#implement2Selected").val(),
				},
		async: false,
		datatype: "json",
		success: function(data, status, xhr){
			if(data.success){
				alert("Task created");
				document.location = urlScheduler;
			}else if(data.code == 3){
				var errorsMessage = "";
				if(data.errors.category != null){
					errorsMessage += "\nCategory: " + data.errors.category;
				}
				if(data.errors.machine != null){
					errorsMessage += "\nMachine: " + data.errors.machine;
				}
				if(data.errors.implement != null){
					errorsMessage += "\nImplement: " + data.errors.implement;
				}
				if(data.errors.field != null){
					errorsMessage += "\nField: " + data.errors.field;
				}
				if(data.errors.date != null){
					errorsMessage += "\nDate: " + data.errors.date;
				}
				if(data.errors.time != null){
					errorsMessage += "\nTime: " + data.errors.time;
				}
				if(data.errors.hours_prediction != null){
					errorsMessage += "\nHours Prediction: " + data.errors.hours_prediction;
				}
				if(data.errors.passes != null){
					errorsMessage += "\nPasses: " + data.errors.passes;
				}
				if(data.errors.description != null){
					errorsMessage += "\nDescription: " + data.errors.description;
				}
				alert("Erros:" + errorsMessage);
			}
			console.log(data.errors);
		}	
	});
}
/*** CREATE TASK END ***/


/* Script Profile 
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
 End Profile */

/* Script to Active Page */
	function setActivePage(btn){
		//alert(btn);
		//$("#" + btn).css('background', 'url(/static/img/' + btn + "Hover.jpg)");
		//$("#" + btn).append("TESTE");
	}

/* End Active Page */

/* Get parameters from url's */
	function getParametersUrl(){
		var url   = window.location.search.replace("?", "");
		var parametersList = url.split("&");
		var item = {};
		
		for(var i = 0; i < parametersList.length; i++){
		    var parameter = parametersList[i].split("=");
		    var key = parameter[0];
		    var value = parameter[1];
		    item[key] = value;
		}

		return item;
	}

/*End function getParametersUrl */

/* Script checklist page */
	function getCheckListQuestions(token, url, qr_code) {
		var questions;
		$.ajax({
			method : "POST",
			url : url,
			async: false,
			data : {
				"csrfmiddlewaretoken" : token,
				"qr_code" : qr_code,
				"category" : 5
			},
			datatype : "json",
			success : function(data, status, xhr) {	
				if(data.success){
					questions = data.questions;
					showQuestion(questions[0]);
				}else{
					window.history.back(-1);
				}
			}

		});		
		return questions;
	}

	function saveCheckList(token, url, qr_code, answers){
		var saveSucess;

		console.log(answers);

		$.ajax({
			method : "POST",
			url : url,
			async: false,
			data : {
				"csrfmiddlewaretoken" : token,
				"qr_code" : qr_code,
				"answers" : JSON.stringify(answers),
				"engine_hours" : $("#engine_hours").val()
			},
			datatype : "json",
			success : function(data, status, xhr) {	
				console.log(data);
			}

		});	

		//inside of ajax sucess
		$("#checkListBtns").html("");

		return saveSucess;
	}

	function showQuestion(question){
		$("#question").html(question.description);
	}
	
/*End checklist page */
/*Begin MAP function*/
	var x = document.getElementById("demo");
	function getLocation() {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(showPosition, showError);
		} else {
			x.innerHTML = "Geolocalização não é suportada nesse browser.";
		}
	}
	function showPosition(position) {
		var lat = position.coords.latitude;
		var lon = position.coords.longitude;
		latlon = new google.maps.LatLng(lat, lon)
		mapholder = document.getElementById('mapholder')
		
	
		var myOptions = {
			center : latlon,
			zoom : 17,
			mapTypeId : google.maps.MapTypeId.ROADMAP,
			mapTypeControl : false,
			navigationControlOptions : {
				style : google.maps.NavigationControlStyle.SMALL
			}
		};
		var map = new google.maps.Map(document.getElementById("mapholder"), myOptions);
		var marker = new google.maps.Marker({
			position : latlon,
			map : map,
			title : "You Are Here!"
		});
	}
	function showError(error) {
		switch(error.code) {
		case error.PERMISSION_DENIED:
			x.innerHTML = "Usuário rejeitou a solicitação de Geolocalização."
			break;
		case error.POSITION_UNAVAILABLE:
			x.innerHTML = "Localização indisponível."
			break;
		case error.TIMEOUT:
			x.innerHTML = "O tempo da requisição expirou."
		break;
		case error.UNKNOWN_ERROR:
			x.innerHTML = "Algum erro desconhecido aconteceu."
			break;
		}
	}
/*End MAP function*/

/* Begin Fleet page*/
	
	// Variables
	var status_ok = 1;
	var	status_attention = false;
	var	status_broken = false;
	var	status_quarantine = false;

	function switchStatus(status) {
		switch (status){
			case 1:
				status_attention = false;
				status_broken = false;
				status_quarantine = false;
				status_ok = 1;
				break;
			case 2:
				status_ok = false;
				status_broken = false;
				status_quarantine = false;
				status_attention = 1;
				break;
			case 3:
				status_attention = false;
				status_ok = false;
				status_quarantine = false;
				status_broken = 1;
				break;
			case 4:
				status_attention = false;
				status_broken = false;
				status_ok = false;
				status_quarantine = 1;
				break;
			default:
				status_attention = false;
				status_broken = false;
				status_ok = false;
				status_quarantine = false;
		}
	}
	//Events

	// Functions
	function showTractorStatus(tab, number_of_tractors, imgs, tractor) {
		$("#" + tab).html("");

		for (var i = 1; i < number_of_tractors; i++) {

			if (i > 35) {
				$("#" + tab).append("<div class=\"infoTractor hideout\"><a href=\"../equipmentManager/?qr_code="+ tractor[i].qr_code+"\"><img src=\"/static/img/" + imgs + "\"/><p>"+ tractor[i].qr_code+"</p></a></div>");
				//if(i == 36)
				//$("#container").append("<button id=\"viewMore\" type=\"button\" class=\"btn btn-info btn-block\">View More</button>")
			} else
				//$("#" + tab).append("<div class=\"infoTractor\"><a href=\"equipmentManager.html?equipmentId\"><img src=\"../img/" + imgs + "\"/><p>ID</p></a></div>");
				$("#" + tab).append("<div class=\"infoTractor\"><a href=\"../equipmentManager/?qr_code="+ tractor[i].qr_code+"\"><img src=\"/static/img/" + imgs + "\"/><p>"+ tractor[i].qr_code+"</p></a></div>");

		}

		$("#" + tab + " .hideout").hide();
	}

	function showTractors(token, url) {
		
		//Variables 
		//Number of tractors 
		var tractors = {
			good : 0,
			service : 0,
			broken : 0,
			repair : 0
		};

		$.ajax({
			method: "POST",
			url: url,
			data: {"csrfmiddlewaretoken": token, 
					"manufacturer": "", 
					"hitch_capacity": 0, 
					"horse_power": 0, 
					"implement_qr_code": "",
					"status_ok": status_ok,
					"status_attention": status_attention,
					"status_broken": status_broken,
					"status_quarantine": status_quarantine},
			datatype: "json",

			success: function(data, status, xhr){
				var len = data.length;

				if (status_ok == 1)//Green Tab
				{
					tractors.good = len;
					$("#viewMore").css("background-color", "#809A21");
					showTractorStatus("goodTab", tractors["good"], "TractorGood.png", data);

				}else if (status_attention == 1)//Yellow Tab
				{
					tractors.service = len;
					$("#viewMore").css("background-color", "#F3C902");
					showTractorStatus("serviceTab", tractors["service"], "TractorService.png", data);

				}else if (status_broken == 1)//Red Tab
				{

					tractors.broken = len;
					$("#viewMore").css("background-color", "#BB330C");
					showTractorStatus("brokenTab", tractors["broken"], "TractorBroken.png", data);

				}else if (status_quarantine == 1)//Gray Tab
				{

					tractors.repair = len;
					$("#viewMore").css("background-color", "#434343");
					showTractorStatus("repairTab", tractors["repair"], "TractorRepair.png", data);

				}else
				{
					return false;
				}
			}
		});

	}

/* End Fleet page*/

	function checkFields(fields){

		var formOK = true;

		for (var i = 0; i < fields.length; i++) {
			if($(fields[i]).val() == ""){
				if(formOK == true)						
					$(fields[i]).focus()
				$(fields[i]).css('box-shadow', '0px 0px 10px red');
				formOK = false;
			}else{
				$(fields[i]).css('box-shadow', '1px 1px 5px 0px');
			}
		}

		return formOK;
	}