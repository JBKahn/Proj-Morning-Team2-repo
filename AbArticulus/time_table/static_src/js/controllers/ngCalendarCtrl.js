var CalendarController =  function($scope, $modal, EventService) {
    var self = this;

    /* event source that contains custom events on the scope */
    this.eventData = {
        events: []
    };

    /* config object */
    this.eventData.uiConfig = {
      calendar:{
        height: 850,
        editable: true,
        header:{
          left: 'title',
          center: 'month agendaWeek agendaDay',
          right: 'today prev,next'
        },
        eventClick: $scope.editEvent,
        //dayClick: $scope.dayClick, // Commented out due to looking at the wrong scope. I'll look into this.
        eventDrop: $scope.dropEvent,
        eventResize: $scope.resizeEvent
      }
    };

    EventService.getEvents()
        .then(function (data) {
            for (var i = 0; i < data.length; i++) {
                self.eventData.events.push(data[i]);
            }
        });

    $scope.dayClick = function(date, allDay, jsEvent, view) {
        var event = {
            allDay: true,
            start: date,
            end: date
        };

        self.open('lg', event);
    };

    $scope.editEvent = function (event, allDay, jsEvent, view) {
        self.open('lg', event);
    };

    $scope.dropEvent = function (event, dayDelta, minuteDelta, allDay, revertFunc, jsEvent, ui, view) {
        EventService.updateEvent(event.id, event.sequence, event.title, event.start, event.end, event.allDay)
            .then(
                function (data) {
                    // Success case, fullcalendar moved the event so nothing more.
                }, function (reason) {
                    revertFunc();
                }
            );
    };

    $scope.resizeEvent = function (event, dayDelta, minuteDelta, revertFunc, jsEvent, ui, view) {
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
        eventData = eventData || {};
        var modalInstance = $modal.open({
            templateUrl: 'templates/eventModal.html',
            controller: 'EventModalController',
            size: size,
            resolve: {
                eventData: function () {
                    return eventData;
                }
            }
        });

        modalInstance.result
            .then(function (newEvent) {
                if (!eventData.id) {
                    newEvent.start = new Date(newEvent.start);
                    newEvent.end = new Date(newEvent.end);
                    console.log(newEvent);
                    self.eventData.events.push(newEvent);
                } else {
                    eventData.title = newEvent.title;
                    eventData.start = newEvent.start;
                    eventData.end = newEvent.end;
                    eventData.sequence = newEvent.sequence;
                    eventData.allDay = newEvent.allDay;
                }
            }, function () {
                // Clicked Cancel on Modal; Do Nothing
            });
    };
};
angular.module("timeTable.controllers.calendar", [])
.controller("CalendarController", ["$scope", "$modal", "EventService", CalendarController]);
