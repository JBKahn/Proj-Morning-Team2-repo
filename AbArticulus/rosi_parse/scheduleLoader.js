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
        console.log('FAIL to load the address ' + page.reason_url + " " + page.reason);
    } else {
        //Parse the stuff in ROSI
        page.onResourceRequested = function(request) {
              console.log('Request ' + JSON.stringify(request, undefined, 4));
        };

        page.onResourceReceived = function(response) {
              console.log('Receive ' + JSON.stringify(response, undefined, 4));
        };
       
       // page.includeJs("http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js", function() {
        page.evaluate(function() {
              function click(el){
                  var ev = document.createEvent("MouseEvent");
                  ev.initMouseEvent(
                      "click",
                      true /* bubble */, true /* cancelable */,
                      window, null,
                      0, 0, 0, 0, /* coordinates */
                      false, false, false, false, /* modifier keys */
                      0 /*left*/, null
                  );
           
                  el.dispatchEvent(ev);
              }
      
              var el = document.querySelector('.rosi-login-content a');
              click(el);   
        });

	console.log("about to run finish");
        page.onLoadFinished = function(status){
            if(status !== 'success'){
              console.log('FAIL to load the address ' + page.reason_url + " " + page.reason);
            }else{
              console.log("yeyeyeyey");
              page.render('rosi.png');
            }
        }
        console.log("finishing now");
        phantom.exit();
        //});
    }

 
});
