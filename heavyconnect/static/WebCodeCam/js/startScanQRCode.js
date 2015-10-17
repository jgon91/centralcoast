
function startScan(decoder, si, sl, sQ, sv, sp, spAll, url, machine, implement, implement2) {
	if (typeof decoder.data().plugin_WebCodeCam == "undefined") {
			decoder.WebCodeCam({
				videoSource: {
					id: $('select#cameraId').val(),
					maxWidth: 210,
					maxHeight: 210
				},
				autoBrightnessValue: 120,
				resultFunction: function(text, imgSrc) {
					si.attr('src', imgSrc);
					
					 alert(text);// Shows the QRCode scanned

					 if(url.val() != undefined){
					 	checkEquipment("{{ csrf_token }}", "/home/getEquipmentInfo/", text);
						
					}if($("#machineBtn").val() == 1){
						loadEquipmentInfo("{{ csrf_token }}", "/home/getEquipmentInfo/", text);
						machine.val(text);//Create Task
						
						$('#machineScannedQRCode').val(text);// Start Task
						$('#scanQRCode').modal("hide");
						
						//check machine in start task page
						checkMachine = checkQRCode("machineTab", $("#machineSelectedStart").val(), $("#machineScannedQRCode").val());
					}if($("#implementBtn").val() == 1){
						loadEquipmentInfo("{{ csrf_token }}", "/home/getEquipmentInfo/", text);
						implement.val(text);// Create Task
					
						$('#implementScannedQRCode').val(text);// Start Task
						$('#scanQRCode').modal("hide");
						
						//check implment in start task page
						checkImplement = checkQRCode("implementTab", $("#implementSelectedStart").val(), $("#implementScannedQRCode").val());
					}if($("#implementBtn2").val() == 1){
						loadEquipmentInfo("{{ csrf_token }}", "/home/getEquipmentInfo/", text);
						implement2.val(text);// Create Task
						
						$('#implement2ScannedQRCode').val(text);// Start Task
						$('#scanQRCode').modal("hide");
						
						//check implment in start task page
						checkImplement2 = checkQRCode("implementTab", $("#implement2SelectedStart").val(), $("#implement2ScannedQRCode").val());
					}
					 //document.location="#";
					sl.fadeOut(150, function() {
						sl.fadeIn(150);
					});
				},
				getUserMediaError: function() {
					alert('Sorry, the browser you are using doesn\'t support getUserMedia');
				},
				cameraError: function(error) {
					var p, message = 'Error detected with the following parameters:\n';
					for (p in error) {
						message += p + ': ' + error[p] + '\n';
					}
					alert(message);
				}
			});
			sQ.text('Scanning ...');
			sv.removeClass('disabled');
			sp.click(function(event) {
				sv.addClass('disabled');
				sQ.text('Stopped');
				decoder.data().plugin_WebCodeCam.cameraStop();
			});
			spAll.click(function(event) {
				sv.addClass('disabled');
				sQ.text('Stopped');
				decoder.data().plugin_WebCodeCam.cameraStopAll();
			});
	}else{
		sv.removeClass('disabled');
		sQ.text('Scanning ...');
		decoder.data().plugin_WebCodeCam.cameraPlay();
	}
}