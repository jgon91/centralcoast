
function startScan(decoder, si, sl, sQ, sv, sp, spAll, url, machine, implement) {
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
						document.location = url.val() + text;
					}
					if($("#machineBtn").val() == 1){
						machine.val(text);
						$('#scanQRCodeMachine').modal("hide");
						$("#implementBtn").val(0);
					}if($("#implementBtn").val() == 1){
						implement.val(text);
						$('#scanQRCodeMachine').modal("hide");
						$("#machineBtn").val(0);
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