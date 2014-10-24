var CalendarController =  function(EventService) {
    var self = this;
    self.eventData = {
        events: []
    };

    //EventService.getEvents()
    //    .then(function (data) {
    //        self.eventData.events = data;
    //    })
};
angular.module("timeTable.controllers.calendar", [])
.controller("CalendarController", ["EventService", CalendarController]);
