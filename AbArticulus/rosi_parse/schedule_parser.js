var casper = require('casper').create();
var x = require('casper').selectXPath;

var studentID = casper.cli.raw.get(0);
var password = casper.cli.raw.get(1);

function getCourses() {
    var courses = document.querySelectorAll('#APPTable tr[valign="top"]');
    return Array.prototype.map.call(courses, function(e) {
        return e.querySelector('b').innerHTML.substring(0, 10) + ' ' + e.querySelector('td').innerText.split('\n')[1].replace(' ', '-');
    });
}

casper.start('http://www.rosi.utoronto.ca').thenClick('.rosi-login-content a');

casper.then(function(){
    this.sendKeys('#personId', studentID);
    this.sendKeys('#pin', password);
});

//If login failed
casper.thenClick('.button[value="Login"]', function(){
    if(this.exists('#error')){
         this.die("bad credentials");
    }

});

// Go to list courses page
casper.thenClick(x('//a[text()="Course Enrolment"]'));
casper.thenClick(x('//a[text()="List Courses"]'));

// Print the courses, comma seperated as Course-Section.
casper.then(function(){
   var courses = this.evaluate(getCourses);
   this.echo(courses);
});

casper.run();
