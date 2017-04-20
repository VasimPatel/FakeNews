//response: sent by message
//sender: tab info
//sendResponse: send back response (add response to sent message funciton)
chrome.runtime.onMessage.addListener(function(response, sender, sendResponse) {
	sendResponse({response: "true"});
});

//add label to all divs
