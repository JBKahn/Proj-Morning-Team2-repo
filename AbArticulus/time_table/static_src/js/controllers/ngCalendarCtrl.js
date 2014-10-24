var CalendarController =  function($scope, EventService) {
    var self = this;

    /* event source that contains custom events on the scope */
    this.eventData = {
        events: []
    };

    /* Change View */
    this.changeView = function(view) {
      myCalendar1.fullCalendar('changeView',view);
    };
    /* Change View */
    this.renderCalender = function(calendar) {
      if(calendar){
        calendar.fullCalendar('render');
      }
    };
    /* config object */
    this.eventData.uiConfig = {
      calendar:{
        height: 450,
        editable: true,
        header:{
          left: 'title',
          center: '',
          right: 'today prev,next'
        },
      }
    };

    EventService.getEvents()
        .then(function (data) {
            for (var i = 0; i < data.length; i++) {
                self.eventData.events.push(data[i]);
            }
            //console.log(data);
        });

    /* event sources array*/
    this.CalendarData = {
        eventSources: [this.eventData.events]
    };
};
angular.module("timeTable.controllers.calendar", [])
.controller("CalendarController", ["$scope", "EventService", CalendarController]);
