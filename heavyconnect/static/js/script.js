/* Script checklist page */

//Variables
var answer1 = 9;
var answer2 = 9;
var answer3 = 9;
var answer4 = 9;
var answer5 = 9;

// Events
$("input[name=q1]:radio").change(firstQuestionChecked);
$("input[name=q2]:radio").change(secondQuestionChecked);
$("input[name=q3]:radio").change(thirdQuestionChecked);
$("input[name=q4]:radio").change(fourthQuestionChecked);
$("input[name=q5]:radio").change(fifthQuestionChecked);

$("#q1").click(showQuestion1);
$("#q2").click(showQuestion2);
$("#q3").click(showQuestion3);
$("#q4").click(showQuestion4);
$("#q5").click(showQuestion5);

$("#buttonSubmit").click(function() {
	alert("Data has been updated!!" + "\n" + answer1 + "\n" + answer2 + "\n" + answer3 + "\n" + answer4 + "\n" + answer5);

	return false;
});

$("#buttonBack").click(function() {

});

//Functions
function showQuestion1() {
	$("#checkList1").show();
	$(this).css("border", "solid 5px #80982D");
	$(this).css("padding", "10px");
	$("#checkList2").hide();
	$("#q2").css("border", "");
	$("#checkList3").hide();
	$("#q3").css("border", "");
	$("#checkList4").hide();
	$("#q4").css("border", "");
	$("#checkList5").hide();
	$("#q5").css("border", "");
}

function showQuestion2() {
	$("#checkList2").show();
	$(this).css("border", "solid 5px #80982D");
	$(this).css("padding", "10px");
	$("#checkList1").hide();
	$("#q1").css("border", "");
	$("#checkList3").hide();
	$("#q3").css("border", "");
	$("#checkList4").hide();
	$("#q4").css("border", "");
	$("#checkList5").hide();
	$("#q5").css("border", "");
}

function showQuestion3() {
	$("#checkList3").show();
	$(this).css("border", "solid 5px #80982D");
	$(this).css("padding", "10px");
	$("#checkList1").hide();
	$("#q1").css("border", "");
	$("#checkList2").hide();
	$("#q2").css("border", "");
	$("#checkList4").hide();
	$("#q4").css("border", "");
	$("#checkList5").hide();
	$("#q5").css("border", "");
}

function showQuestion4() {
	$("#checkList4").show();
	$(this).css("border", "solid 5px #80982D");
	$(this).css("padding", "10px");
	$("#checkList1").hide();
	$("#q1").css("border", "");
	$("#checkList2").hide();
	$("#q2").css("border", "");
	$("#checkList3").hide();
	$("#q3").css("border", "");
	$("#checkList5").hide();
	$("#q5").css("border", "");
}

function showQuestion5() {
	$("#checkList5").show();
	$(this).css("border", "solid 5px #80982D");
	$(this).css("padding", "10px");
	$("#checkList1").hide();
	$("#q1").css("border", "");
	$("#checkList2").hide();
	$("#q2").css("border", "");
	$("#checkList4").hide();
	$("#q3").css("border", "");
	$("#checkList3").hide();
	$("#q4").css("border", "");
}

function firstQuestionChecked() {
	showQuestion2();

	if ($("input[name='q1']:checked").val() == 1) {
		$("#q1").css("background-color", "#80982D");
		$("#q1").css("color", "white");
		answer1 = $("input[name='q1']:checked").val();

	} else if ($("input[name='q1']:checked").val() == 0) {
		$("#q1").css("background-color", "#B9341A");
		$("#q1").css("color", "white");
		answer1 = $("input[name='q1']:checked").val();
	}
}

function secondQuestionChecked() {
	showQuestion3();

	if ($("input[name='q2']:checked").val() == 1) {
		$("#q2").css("background-color", "#80982D");
		$("#q2").css("color", "white");
		answer2 = $("input[name='q2']:checked").val();

	} else if ($("input[name='q2']:checked").val() == 0) {
		$("#q2").css("background-color", "#B9341A");
		$("#q2").css("color", "white");
		answer2 = $("input[name='q2']:checked").val();
	}
}

function thirdQuestionChecked() {
	showQuestion4();

	if ($("input[name='q3']:checked").val() == 1) {
		$("#q3").css("background-color", "#80982D");
		$("#q3").css("color", "white");
		answer3 = $("input[name='q3']:checked").val();

	} else if ($("input[name='q3']:checked").val() == 0) {
		$("#q3").css("background-color", "#B9341A");
		$("#q3").css("color", "white");
		answer3 = $("input[name='q3']:checked").val();
	}
}

function fourthQuestionChecked() {
	showQuestion5();

	if ($("input[name='q4']:checked").val() == 1) {
		$("#q4").css("background-color", "#80982D");
		$("#q4").css("color", "white");
		answer4 = $("input[name='q4']:checked").val();

	} else if ($("input[name='q4']:checked").val() == 0) {
		$("#q4").css("background-color", "#B9341A");
		$("#q4").css("color", "white");
		answer4 = $("input[name='q4']:checked").val();
	}
}

function fifthQuestionChecked() {

	if ($("input[name='q5']:checked").val() == 1) {
		$("#q5").css("background-color", "#80982D");
		$("#q5").css("color", "white");
		answer5 = $("input[name='q5']:checked").val();

	} else if ($("input[name='q5']:checked").val() == 0) {
		$("#q5").css("background-color", "#B9341A");
		$("#q5").css("color", "white");
		answer5 = $("input[name='q5']:checked").val();
	}
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
		lat = position.coords.latitude;
		lon = position.coords.longitude;
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