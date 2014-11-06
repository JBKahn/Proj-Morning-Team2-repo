var casper = require('casper').create();
var x = require('casper').selectXPath;

var studentID = casper.cli.raw.get(0);
var password = casper.cli.raw.get(1);

casper.start('http://www.rosi.utoronto.ca').thenClick('.rosi-login-content a');

casper.then(function(){
    this.sendKeys('#personId', studentID);
    this.sendKeys('#pin', password);
});

var courses = [];

//If login failed
casper.thenClick('.button[value="Login"]', function(){
    if(this.exists('#error')){
         this.die("error found");
    }

});

casper.thenClick(x('//a[text()="Personal Timetable"]'));

//Fall term
casper.thenClick('html body#subpage div#wrapper div#content.content div#right table tbody tr td.section table.decorated tbody tr td form#sessionForm input.button');




//Winter term
casper.thenClick('html body#subpage div#wrapper div#content.content div#right table tbody tr td.section table.decorated tbody tr td form#sessionForm input.button');


casper.then(function(){
   this.capture('lol.png');
})

casper.run();
