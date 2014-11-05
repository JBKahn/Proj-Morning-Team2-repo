var CalendarController =  function($scope, $modal, EventService) {
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

    // test modal stuff

    this.open = function (size, eventData) {

        var modalInstance = $modal.open({
            templateUrl: 'templates/eventModal.html',
            controller: 'EventModalController',
            size: size,
            resolve: {
                eventData: function () {
                    return eventData || {};
                }
            }
        });

        modalInstance.result.then(function (newEvent) {
            self.eventData.events.push(newEvent);
        }, function () {
            console.log("I failed to save the event");
        });
    };
    // When a user clicks save you want to call your new service (which is currently
    // just a copy of todo code) and then when that comes back, you'll want to either
    // update the event the user clicked on with new information or if it's a new event
    // You want to add it to self.eventData.events using push like I do in the above code.
    //title start, end, all-day(boolean)

    //full cal api, on click of event
    //vs create new event
};
angular.module("timeTable.controllers.calendar", [])
.controller("CalendarController", ["$scope", "$modal", "EventService", CalendarController]);
