//Script Time Keeper Off-line
//This event call the function syncronaze always when the connection is on
window.addEventListener('load', function() {
  function updateOnlineStatus(event) {
    sync();
  }

  window.addEventListener('online',  updateOnlineStatus);
});
//Constructor
if(localStorage.getItem('dataTimeKeeper') == null){
    var	dataTimeKeeper = [];
    localStorage.setItem('dataTimeKeeper', JSON.stringify(dataTimeKeeper));
}
//Object to count actions
var count = {};
if(localStorage.getItem('count') == null){
	initializeCounter();
}
if(localStorage.getItem('savedEditions') == null){
    var savedEditions = [];
    localStorage.setItem('savedEditions', JSON.stringify(savedEditions));
}

function saveData(actionLocal){
	//actionLocal: 1 = start shift, 2 = start break, 3 = stop break, 4 = start lunch, 5 = stop lunch, 6 = end shift
	offilne = -1;
	var currentdate = new Date();
	var datetime = getCurrentDate(currentdate);


	switch(actionLocal){
		case 1:
			return checkStartShift(actionLocal, datetime); // Start Shift
			break;
		case 2:
			return checkStartBreakLunch(actionLocal, datetime, 1, 0);// Start Break
			break;
		case 3:
			return checkStopBreakLunch(actionLocal, datetime, 1, 0);// Stop Break
			break;
		case 4:
			return checkStartBreakLunch(actionLocal, datetime, 0, 1);// Start Lunch
			break;
		case 5:
			return checkStopBreakLunch(actionLocal, datetime, 0, 1);// Stop Lunch
			break;
		case 6:
			return checkStopShift(actionLocal, datetime);// Stop Lunch
		 	break;
		 default:
		 	break;
	}
}

function saveAction(actionLocal, time, pend){

	action = {};

	action.actionLocal = actionLocal;
	action.timeLocal = time;
	action.pendent = pend;
	dataTimeKeeper.push(action);

	localStorage.setItem('dataTimeKeeper', JSON.stringify(dataTimeKeeper));
}

function checkStartBreakLunch(actionLocal, datetime, tmp_break, tmp_lunch){

	getValueStorage();
	console.log(count.startShift + " - " + count.endShift);
	if (count.startShift == count.endShift+1){
		if (count.startBreak == count.stopBreak){
			if(count.startLunch == count.stopLunch){
				saveAction(actionLocal, datetime, true);
				if (tmp_break){
					count.startBreak += tmp_break;
					localStorage.setItem('count', JSON.stringify(count));
					$("#messageTimekeeper").html("{% trans 'Break started' %}");
                    breakStarted = 1;
				}else{
					count.startLunch += tmp_lunch;
					localStorage.setItem('count', JSON.stringify(count));
					$("#messageTimekeeper").html("{% trans 'Lunch started' %}");
                    lunchStarted = 1;
				}
				return true;
			}else{
				console.log("Lunch In Progress");

				return false;
			}

		}else{
			console.log("Break In Progress");

			return false;
		}
	}else{
		console.log("Shift doesn't started or Shift is already ended.");

		return false;
	}
}

function checkStopBreakLunch(actionLocal, datetime, tmp_break, tmp_lunch){

	getValueStorage();

	if (count.startShift == count.endShift+1){
		if (count.startBreak == count.stopBreak+tmp_break){
			if(count.startLunch == count.stopLunch+tmp_lunch){
				saveAction(actionLocal, datetime, true);
				if (tmp_break){
					count.stopBreak += tmp_break;
					localStorage.setItem('count', JSON.stringify(count));
					$("#messageTimekeeper").html("{% trans 'Break ended' %}");
                    breakStarted = 0;
				}
				else{
					count.stopLunch += tmp_lunch;
					localStorage.setItem('count', JSON.stringify(count));
					$("#messageTimekeeper").html("{% trans 'Lunch ended' %}");
                    lunchStarted = 0;
				}
				return true;
			} else{
				console.log("Lunch in Progress");

				return false;
			}

		} else{
			console.log("Break in Progress");

			return false;
		}
	} else{
		console.log("Shift doesn't started or Shift is already ended");

		return false;
	}

}

function checkStartShift(actionLocal, datetime){

	getValueStorage();

	if (count.startShift == count.endShift){
		if (dataTimeKeeper.length == 0 || (dataTimeKeeper[dataTimeKeeper.length-1].actionLocal == 6 && dataTimeKeeper[dataTimeKeeper.length-1].pendent == false)){
			localStorage.clear();
			initializeCounter();
			saveAction(actionLocal, datetime, true);

			count.startShift += 1;
			localStorage.setItem('count', JSON.stringify(count));

			$("#messageTimekeeper").html("{% trans 'Clock-in successful' %}");
			shiftStarted = 1;

			return true;
		} else{
			console.log("You can't start the shift, previous shift is pendent");

			return false;
		}

	}else{
		console.log("Shift doesn't started or Shift is already ended");

		return false;
	}

}

function checkStopShift(actionLocal, datetime){

	var checked;
	checked = checkStartBreakLunch(actionLocal, datetime, 0, 0);

	if (checked){
		count.endShift += 1;
		localStorage.setItem('count', JSON.stringify(count));
		$("#messageTimekeeper").html("{% trans 'Shift ended' %}");
		shiftStarted = 0;
	}

	return checked;

}
function getCurrentDate(currentdate){

	var yyyy = currentdate.getFullYear();
	var mm = (currentdate.getMonth()+1);
	var dd = currentdate.getDate();
	var hh = currentdate.getHours();
	var min = currentdate.getMinutes();
	var ss = currentdate.getSeconds();

	if (mm < 10)
		mm = "0" + mm;
	if (dd < 10)
		dd = "0" + dd;
	if (hh < 10)
		hh = "0" + hh;
	if (min < 10)
		min = "0" + min;
	if (ss < 10)
		ss = "0" + ss;

	var datetime = hh + ":" + min + ":" + ss + " " + yyyy + "-" + mm + "-" + dd;
    return datetime;
}
function initializeCounter(){

	count.startShift = 0;
	count.endShift = 0;
	count.startBreak = 0;
	count.stopBreak = 0;
	count.startLunch = 0;
	count.stopLunch = 0;
	count.signed = 0;
	//console.log(count);
	localStorage.setItem('count', JSON.stringify(count));

	dataTimeKeeper = [];
    localStorage.setItem('dataTimeKeeper', JSON.stringify(dataTimeKeeper));
}

function getValueStorage(){

	//Getting values from the storage
	var value = localStorage.getItem('count');
	count.startShift = JSON.parse(value).startShift;
	count.endShift = JSON.parse(value).endShift;
	count.startBreak = JSON.parse(value).startBreak;
	count.stopBreak = JSON.parse(value).stopBreak;
	count.startLunch = JSON.parse(value).startLunch;
	count.stopLunch = JSON.parse(value).stopLunch;
    count.signed = JSON.parse(value).signed;
}

//action: 1 = edit start shift, 2 = edit break, 3 = edit stop shift
function saveEdition(action, pendent, newTime, id, position)  {
    savedEditions = [];
    var savedEditions = localStorage.getItem('savedEditions');
    var aux = {};
    aux.action = action;
    aux.newTime = newTime;
    aux.id = id;
    aux.position = position;
    aux.pendent = pendent;
    console.log(aux);
    console.log(savedEditions);
    savedEditions.push(aux);
    localStorage.setItem('savedEditions', JSON.stringify(savedEditions));
    sync();
}

// Variable used to check updates in shift
var data = [];

function checkEditStartShift(newTime){
	
	var timeEnd;		
	var timeFirstBreak;

	data = JSON.parse(localStorage.getItem('dataTimeKeeper'));		
	timeEnd = data[data.length-1].timeLocal;
	
	// console.log(timeEnd);
	// console.log(newTime);
	
	if (data.length > 2){ // This shift contains at least 1 break
		if (newTime < timeEnd){	   		
	   		timeFirstBreak = data[1].timeLocal; // Get time first Break
	   		if (newTime > timeFirstBreak){
	   			console.log("You can Edit Start Shift");
	   			return true;
	   			// data[0].timeLocal = newTime; // Set new time in local storage
	   			// localStorage.setItem('dataTimeKeeper', JSON.stringify(data));
	   		}else{
	   			console.log("Error: New time is greater than your First Break");
	   			return false;
	   		}
		}
	}else{ // No breaks in the shift
		if (timeEnd > newTime){
	   		console.log("You can Edit Start Shift");
	   		return true;
	   		// data[0].timeLocal = newTime; // Set new time in local storage
	   		// localStorage.setItem('dataTimeKeeper', JSON.stringify(data));
		}else{
			console.log("Error: New time is greater than end shift time. ");
			return false;
		}
	}	
}

function checkEditStopShift(newTime){
		
	var timeStart;
	var timeLastBreak;

	data = JSON.parse(localStorage.getItem('dataTimeKeeper'));	
	timeStart = data[0].timeLocal;	
	
	// console.log(timeEnd);
	// console.log(newTime);
	
	if (data.length > 2){ // This shift contains at least 1 break
		if (newTime > timeStart){	   		
	   		timeLastBreak = data[length-2].timeLocal;// Get time last break
	   		if (newTime > timeLastBreak){
	   			console.log("You can Edit Stop Shift");
	   			return true;
	   			//data[length-1].timeLocal = newTime;
	   			//localStorage.setItem('dataTimeKeeper', JSON.stringify(data));
	   		}else{
	   			console.log("Error: New time is lesser than your Last Break");
	   			return false;
	   		}
		}
	}else{ // No breaks in this shift
		if (newTime > timeStart){
	   		console.log("You can Edit Start Shift");
	   		return true;
	   		//data[length-1].timeLocal = newTime;
	   		//localStorage.setItem('dataTimeKeeper', JSON.stringify(data));
		}else{
			console.log("Error: New time is lesser than Start Shift time. ");
			return true;
		}
	}	
}