var casper = require('casper').create();

var studentID = casper.cli.raw.get(0);
var password = casper.cli.raw.get(1);

casper.start('http://www.rosi.utoronto.ca').thenClick('.rosi-login-content a');

casper.then(function(){
    this.sendKeys('#personId', studentID);
    this.sendKeys('#pin', password);
});

casper.then(function(){
   this.capture('lol.png');
})

casper.run();
