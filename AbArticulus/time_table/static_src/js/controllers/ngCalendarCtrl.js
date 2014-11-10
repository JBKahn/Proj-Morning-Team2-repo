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

    this.sources = [];
    EventService.getEvents()
        .then(function (data) {
            var sourceNames = Object.keys(data);
            //TODO: Add more before merging.
            var eventColors = ['#E8860C', '#FF0000', '#7C0CE8', '#0D88FF', '#0DFFF9', '#92FF25', '#A8A8FF'];
            for (var i = 0; i < sourceNames.length; i++) {
                var source = sourceNames[i];
                self.sources.push({
                    id: data[source].id,
                    name: source,
                    index: i,
                    editable: ['writer', 'owner'].indexOf(data[source].role) > -1
                });
                self.eventData.events[i] = {
                    color: eventColors[i],
                    events: [],
                    editable: ['writer', 'owner'].indexOf(data[source].role) > -1
                };
                for (var j = 0; j < data[source].events.length; j++) {
                    var calEvent = data[source].events[j];
                    calEvent.calendar = self.sources[i];
                    self.eventData.events[i].events.push(calEvent);
                }
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
        eventSources: this.eventData.events
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
                },
                calendars: function() {
                    return self.sources;
                }
            }
        });

        modalInstance.result
            .then(function (newEvent) {
                var i;
                for (i = 0; i < self.sources.length; i++) {
                    if (self.sources[i].id === newEvent.calendar_id) {
                        break;
                    }
                }
                if (!eventData.id) {
                    newEvent.start = new Date(newEvent.start);
                    newEvent.end = new Date(newEvent.end);
                    console.log(newEvent);
                    self.eventData.events[i].events.push(newEvent);
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
