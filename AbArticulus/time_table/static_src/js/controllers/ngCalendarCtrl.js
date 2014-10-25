var CalendarController =  function($scope, EventService) {
    var self = this;

    /* event source that contains custom events on the scope */
    this.eventData = {
        events: []
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
        });

    /* event sources array*/
    this.CalendarData = {
        eventSources: [this.eventData.events]
    };
};
angular.module("timeTable.controllers.calendar", [])
.controller("CalendarController", ["$scope", "EventService", CalendarController]);
