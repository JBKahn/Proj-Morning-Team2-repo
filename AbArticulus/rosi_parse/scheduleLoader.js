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

       /* page.onResourceReceived = function(response) {
              console.log('Receive ' + JSON.stringify(response, undefined, 4));
        };*/
       
       page.evaluate(function() {
              function click(el){
                  var ev = document.createEvent("MouseEvent");
                  ev.initMouseEvent(
                      "click",
                      true, true ,
                      window, null,
                      0, 0, 0, 0, 
                      false, false, false, false, 
                      0, null
                  );
           
                  el.dispatchEvent(ev);
             }
              
              var el = document.querySelector('.rosi-login-content a');
              click(el);
              });


              window.setTimeout(function(){
                    console.log(page.frameUrl);
                        page.render("lol.png");
              phantom.exit();

    
              }, 6000);
 
                  /*var element = page.evaluate(function(){
            return document.querySelector('.rosi-login-content a');
        });

        page.sendEvent('click', element.offsetLeft, element.offsetTop, 'left');
        window.setTimeout(function(){
          console.log(page.frameUrl);
          page.render("afterclick.png");
          phantom.exit()
        }, 9000);
        */
        console.log("print me first");
    }

 
});
