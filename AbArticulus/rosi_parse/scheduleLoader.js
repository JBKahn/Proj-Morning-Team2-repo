
var page = require('webpage').create();
var system = require('system');

var studentID = system.args[1];
var password = system.args[2];


//Error handling
page.onResourceError = function(resourceError){
	page.reason=resourceError.errorString;
	page.reason_url = resourceError.url;
};


page.open('http://www.rosi.utoronto.ca', function(status){
	if (status !== 'success') {
		console.log('FAIL to load the address ' 
			+ page.reason_url 
			+ " " 
			+ page.reason);
	} else {
		//Parse the stuff in ROSI
		page.onResourceRequested = function(request) {
  			console.log('Request ' + JSON.stringify(request, undefined, 4));
		};

		page.onResourceReceived = function(response) {
  			console.log('Receive ' + JSON.stringify(response, undefined, 4));
		};

		page.evaluate(function() {
			$(".secondary-btn").click(function(){
			});
		});
		
			page.render("rosi.png");	

	}
	phantom.exit();

});
