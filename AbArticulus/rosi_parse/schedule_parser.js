var casper = require('casper').create();
var system = require('system');

var studentID = system.args[1];
var password = system.args[2];

casper.start('http://www.rosi.utoronto.ca').thenClick('.rosi-login-content a', function(){
    this.capture('yay.png');
});

casper.then(function(){
    this.sendKeys('#personId', "996776494");
    this.sendKeys('#pin', "abcdefg");
});

casper.then(function(){
   this.capture('lol.png');
})

casper.run();
