var casper = require('casper').create();
var x = require('casper').selectXPath;

var studentID = casper.cli.raw.get(0);
var password = casper.cli.raw.get(1);

casper.start('http://www.rosi.utoronto.ca').thenClick('.rosi-login-content a');

casper.then(function(){
    this.sendKeys('#personId', studentID);
    this.sendKeys('#pin', password);
});

var course_name = [];

//If login failed
casper.thenClick('.button[value="Login"]', function(){
    if(this.exists('#error')){
         this.die("error found");
    }

});

casper.thenClick(x('//a[text()="Personal Timetable"]'));

//Fall term
casper.thenClick('html body#subpage div#wrapper div#content.content div#right table tbody tr td.section table.decorated tbody tr td form#sessionForm input.button');

casper.then(function(){
    var rows = this.getElementsInfo('tr[valign="top"] td:first-child');
    
    this.each(rows, function(self, row){
        course_name.push(row.html);
    });
    //Get the course section
    //courses_section = this.getElementsInfo('')
    
    for(var i=0; i<course_name.length;i++){
        require('utils').dump(course_name[i]);
    }
});

/*
casper.evaluate(function(){
     var rows = document.querySelector('td');
     for(var i = 0; i < rows.length; i++ ){
          courses.push(rows[i].text);
     }    
});



casper.start.each(courses, function(self, course){
    this.echo(course);
});


//Winter term
casper.thenClick('html body#subpage div#wrapper div#content.content div#right table tbody tr td.section table.decorated tbody tr td form#sessionForm input.button');

*/


casper.then(function(){
   this.capture('lol.png');
})

casper.run();
