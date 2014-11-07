var CalendarController =  function($scope, EventService) {
    var self = this;

    /* event source that contains custom events on the scope */
    this.eventData = {
        events: []
    };

    /* config object */
    this.eventData.uiConfig = {
      calendar:{
        height: 650,
        editable: true,
        header:{
          left: 'title',
          center: 'month basicWeek basicDay agendaWeek agendaDay',
          right: 'today prev,next'
        },
        eventClick: $scope.editEvent,
        dayClick: $scope.alertOnEventClick,
        eventDrop: $scope.dragEvent,
        eventResize: $scope.dragEvent
      }
    };

    EventService.getEvents()
        .then(function (data) {
            for (var i = 0; i < data.length; i++) {
                self.eventData.events.push(data[i]);
            }
        });

    $scope.dayClick = function(date, allDay, jsEvent, view) {
        event = {
            allDay: true,
            start: date,
            end: date
        }
        self.open('lg', event);
    };

    $scope.editEvent = function(event, allDay, jsEvent, view) {
        self.open('lg', event);
    };

    $scope.dragEvent = function(event, dayDelta, minuteDelta, revertFunc, jsEvent, ui, view) {
        EventService.updateEvent(event.id, event.sequence, event.title, event.start, event.end, event.allDay)
            .then(
                function (data) {
                    // Success case, fullcalendar moved the event so nothing more.
                }, function (reason) {
                    revertFunc();
                }
            );
    };

    /* event sources array*/
    this.CalendarData = {
        eventSources: [this.eventData.events]
    };

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

        modalInstance.result
            .then(function (newEvent) {
                //if (newEvent !== null) {
                //    self.eventData.events.push(newEvent);
                //}
                debugger;
            }, function () {
                console.log("I failed to save the event");
            });
    };
};
angular.module("timeTable.controllers.calendar", [])
.controller("CalendarController", ["$scope", "EventService", CalendarController]);
