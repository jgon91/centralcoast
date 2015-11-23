//Script Time Kepper Off-line

//Constructor
var	dataTimeKepper = [];

//Object to count actions
var count = {};
initializeCounter();

function saveData(actionLocal){
	//actionlocal = 1- start shift, 2- start break, 3- stop break, 4- start lunch, 5- stop lunch, 6- end shift
	
	var currentdate = new Date(); 
	var datetime = currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();

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

function saveAction(actionLocal, time){
	//console.log("Starting shift")	
	action = {};	

	action.actionLocal = actionLocal;
	action.timeLocal = time;
	action.pendent = false;
	
	dataTimeKepper.push(action);

	console.log(dataTimeKepper);

	localStorage.setItem('dataTimeKepper', JSON.stringify(dataTimeKepper));
}

function checkStartBreakLunch(actionLocal, datetime, tmp_break, tmp_lunch){
	
	getValueStorage();

	if (count.startShift == count.endShift+1){	
		if (count.startBreak == count.stopBreak){
			if(count.startLunch == count.stopLunch){
				saveAction(actionLocal, datetime);
				if (tmp_break){
					count.startBreak += tmp_break;
					localStorage.setItem('count', JSON.stringify(count));
				}else{
					count.startLunch += tmp_lunch;
					localStorage.setItem('count', JSON.stringify(count));
				}
				return true;
			}else{
				console.log("Lunch Happening");

				return false;
			}
			
		}else{
			console.log("Break Happening");

			return false;
		}
	}else{
		console.log("Shift doesn't started or Shift is already ended");

		return false;
	}
}

function checkStopBreakLunch(actionLocal, datetime, tmp_break, tmp_lunch){

	getValueStorage();

	if (count.startShift == count.endShift+1){	
		if (count.startBreak == count.stopBreak+tmp_break){
			if(count.startLunch == count.stopLunch+tmp_lunch){
				saveAction(actionLocal, datetime);
				if (tmp_break){
					count.stopBreak += tmp_break;
					localStorage.setItem('count', JSON.stringify(count));
				}
				else{
					count.stopLunch += tmp_lunch;
					localStorage.setItem('count', JSON.stringify(count));
				}
				return true;
			}else{
				console.log("Lunch Happening");

				return false;
			}
			
		}else{
			console.log("Break is Happening");

			return false;
		}
	}else{
		console.log("Shift doesn't started or Shift is already ended");

		return false;
	}

}

function checkStartShift(actionLocal, datetime){
	
	getValueStorage();

	if (count.startShift == count.endShift){	
		if (dataTimeKepper.length == 0 || dataTimeKepper[dataTimeKepper.length-1].pendent == false){
			localStorage.clear();
			initializeCounter();
			saveAction(actionLocal, datetime);
			
			count.startShift += 1;
			localStorage.setItem('count', JSON.stringify(count));
			
			return true;
		}else{
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
	}

	return checked;

}

function initializeCounter(){

	count.startShift = 0;
	count.endShift = 0;
	count.startBreak = 0;
	count.stopBreak = 0;
	count.startLunch = 0;
	count.stopLunch = 0;
	console.log(count);
	localStorage.setItem('count', JSON.stringify(count));
}

function getValueStorage(){

	//Getting values from the storage
	var value = localStorage.getItem('count');
	count.starShift = JSON.parse(value).startShift;
	count.endShift = JSON.parse(value).endShift;
	count.startBreak = JSON.parse(value).startBreak;
	count.stopBreak = JSON.parse(value).stopBreak;
	count.startLunch = JSON.parse(value).startLunch;
	count.stopLunch = JSON.parse(value).stopLunch;

}