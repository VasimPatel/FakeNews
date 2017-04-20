
chrome.runtime.sendMessage("Time to add labels!", function(promise) {
		var sections= document.querySelectorAll('a, article, img, span');

		for (var i=0, length = sections.length; i < length; i++) {
			var label = document.createElement("BUTTON");
			var text = document.createTextNode("Valid?");
			label.appendChild(text);

			label.onmouseover = function() {
				alert("Classification Details Can Go Here!!");
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

