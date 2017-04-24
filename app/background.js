//response: sent by message
//sender: tab info
//sendResponse: send back response (add response to sent message funciton)
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.type == "addLabels")
		sendResponse({request: "true"});
	else if (request.type == "sendData" ){
		sendResponse(request.data);
	}
});

//add label to all divs
