
chrome.runtime.sendMessage({type: "addLabels"}, function(promise) {
		//alert(promise['request']);
		var sections= document.querySelectorAll('a, article, img, span');

		for (var i=0, length = sections.length; i < length; i++) {
			var label = document.createElement("BUTTON");
			var text = document.createTextNode("Valid?");
			label.appendChild(text);

			label.onclick = function() {
				alert("posting");
				chrome.runtime.sendMessage({type: "sendData", data: "Something Creative"}, function(promise) {
					alert(promise);
				})
			}

			if(sections[i].innerText.split(" ").length != 0) {
				if(sections[i].innerText.split(" ").length > 5) {
					sections[i].before(label);
				}
			}
			else {
				sections[i].before(label);
			}
		}

});

var handle_classification = function(response) {
	alert(response);
}

