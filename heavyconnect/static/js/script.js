	/* Script checklist page */
	function eventsCheckList() 
	{
		//Variables
		var answer1 = 9; var answer2 = 9; var answer3 = 9; var answer4 = 9; var answer5 = 9;
		
		$("#q1").css("border", "solid 5px #FFF");
		$("#q1").css("padding", "10px");
		
		// Events
		$("input[name=q1]:radio").change(function(){
			showQuestion("checkList2", "q2");
			answer1 = questionChecked("q1");
		});
		
		$("input[name=q2]:radio").change(function(){
			showQuestion("checkList3", "q3");
			answer2 = questionChecked("q2");
		});
		
		$("input[name=q3]:radio").change(function(){
			showQuestion("checkList4", "q4");
			answer3 = questionChecked("q3");
		});
		
		$("input[name=q4]:radio").change(function(){
			showQuestion("checkList5", "q5");
			answer4 = questionChecked("q4");
		});
		
		$("input[name=q5]:radio").change(function(){
			answer5 = questionChecked("q5");
		});
	
		$("#q1").click(function(){
			showQuestion("checkList1", "q1");
		});
		
		$("#q2").click(function(){
			showQuestion("checkList2", "q2");
		});
		
		$("#q3").click(function(){
			showQuestion("checkList3", "q3");
		});
		
		$("#q4").click(function(){
			showQuestion("checkList4", "q4");
		});
		
		$("#q5").click(function(){
			showQuestion("checkList5", "q5");
		});
	
		$("#buttonSubmit").click(function() {
			alert("Data has been updated!!" + "\n" + answer1 + "\n" + answer2 + "\n" + answer3 + "\n" + answer4 + "\n" + answer5);
			return false;
		});
	}
	
	
	//Functions
	function showQuestion(checkedList, question){
		
		$("#q1").css("border", ""); $("#checkList1").hide();
		$("#q2").css("border", ""); $("#checkList2").hide();
		$("#q3").css("border", ""); $("#checkList3").hide();
		$("#q4").css("border", ""); $("#checkList4").hide();
		$("#q5").css("border", ""); $("#checkList5").hide();
		$("#" + checkedList).fadeIn(500);
		$("#" + question).css("border", "solid 5px #FFF");
		$("#" + question).css("padding", "10px");
	}
	
	function questionChecked(question) 
	{
		
		var answer = 0;
	
		if ($("input[name='"+question+"']:checked").val() == 1) {
			$("#" + question).css("background-color", "#80982D");
			$("#" + question).css("color", "white");
			answer = 1;
			return answer;
	
		} else if ($("input[name='"+question+"']:checked").val() == 0) {
			$("#" + question).css("background-color", "#B9341A");
			$("#" + question).css("color", "white");
			answer = 0;
			return answer;
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

/* Begin Fleet page*/
	
	//Events
	function loadEventsFleet() {
		$("#greenTab").click(function() {
			//alert("Show Good Tractors");

			showTractors($(this).val());
		});

		$("#yellowTab").click(function() {
			//alert("Show Good Tractors");

			showTractors($(this).val());
		});

		$("#redTab").click(function() {
			//alert("Show Good Tractors");

			showTractors($(this).val());
		});

		$("#grayTab").click(function() {
			//alert("Show Good Tractors");

			showTractors($(this).val());
		});
		$("#viewMore").click(function() {
			$(".hideout").slideDown(500);
		});
	}

	// Functions
	function showTractorStatus(tab, number_of_tractors, imgs) {
		$("#" + tab).html("");

		for (var i = 0; i < number_of_tractors; i++) {

			if (i > 35) {
				$("#" + tab).append("<div class=\"infoTractor hideout\"><a href=\"equipmentManager.html?equipmentId\"><img src=\"../static/img/" + imgs + "\"/><p>ID</p></a></div>");
				//if(i == 36)
				//$("#container").append("<button id=\"viewMore\" type=\"button\" class=\"btn btn-info btn-block\">View More</button>")
			} else
				//$("#" + tab).append("<div class=\"infoTractor\"><a href=\"equipmentManager.html?equipmentId\"><img src=\"../img/" + imgs + "\"/><p>ID</p></a></div>");
				$("#" + tab).append("<div class=\"infoTractor\"><img src='../img/TractorGood.png' /><p>ID</p></div>");

		}

		$("#" + tab + " .hideout").hide();
	}

	function showTractors(tractorStatus) {
		
		//Variables 
		//Number of tractors static
		var tractors = {
			good : 54,
			service : 45,
			broken : 27,
			repair : 18
		};

		if (tractorStatus == 0)//Green Tab
		{
			$("#viewMore").css("background-color", "#809A21");
			showTractorStatus("goodTab", tractors["good"], "TractorGood.png");

		} else if (tractorStatus == 1)//Yellow Tab
		{
			$("#viewMore").css("background-color", "#F3C902");
			showTractorStatus("serviceTab", tractors["service"], "TractorService.png");

		} else if (tractorStatus == 2)//Red Tab
		{

			$("#viewMore").css("background-color", "#BB330C");
			showTractorStatus("brokenTab", tractors["broken"], "TractorBroken.png");

		} else//Gray Tab
		{
			$("#viewMore").css("background-color", "#434343");
			showTractorStatus("repairTab", tractors["repair"],"TractorRepair.png");
		}

	}

/* End Fleet page*/