angular.module("timeTable.controllers.calendar", [])
.controller("CalendarController", ["$scope", "$mdDialog", "Constants", "EventService", function($scope, $mdDialog, Constants, EventService) {
    var self = this;
    $scope.staticUrl = Constants.get('staticUrl');
    /* event source that contains custom events on the scope */
    this.eventData = {
        events: []
    };

    $scope.$on('EventInsert', function (event, data) {
        var a = 1;
        // UI-calendar can't properly handle this case so I incriment minutes by 1.
        if (data.start === data.end) {
            data.end = data.start.substr(0,15) + (parseInt(data.start.substr(15,1)) + 1) + data.start.substr(16);
        }
        for (var i = 0; i < $scope.CalendarData.eventSources.length; i++) {
            if ($scope.CalendarData.eventSources[i].calendar_id !== data.calendar_id) {
                continue;
            }
            var found = false;
            for (var j = 0; j < $scope.CalendarData.eventSources[i].events.length; j++) {
                if ($scope.CalendarData.eventSources[i].events[j].id === data.id) {
                    $scope.CalendarData.eventSources[i].events[j].sequence = data.sequence;
                    $scope.CalendarData.eventSources[i].events[j].title = data.title;
                    $scope.CalendarData.eventSources[i].events[j].start = data.start;
                    $scope.CalendarData.eventSources[i].events[j].end = data.end;
                    $scope.CalendarData.eventSources[i].events[j].allDay = data.allDay;
                    $scope.CalendarData.eventSources[i].events[j].description = data.description;
                    found = true;
                }
            }
            // We did not find the id.
            if (!found) {
                data.calendar =  self.sources[i];
                self.eventData.events[i].events.push(data);
            }
        }
    });

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
        dayClick: $scope.dayClick,
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
                    canCreateEvents: data[source].canCreateEvents,
                    isAppCalendar: data[source].isAppCalendar
                });
                self.eventData.events[i] = {
                    color: eventColors[i],
                    events: [],
                    calendar_id: data[source].id,
                    canEditEvents: data[source].canCreateEvents
                };
                for (var j = 0; j < data[source].events.length; j++) {
                    var calEvent = data[source].events[j];
                    calEvent.calendar = self.sources[i];
                    if (calEvent.start === calEvent.end) {
                        calEvent.end = calEvent.start.substr(0,15) + (parseInt(calEvent.start.substr(15,1)) + 1) + calEvent.start.substr(16);
                    }
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

        self.open('lg', event, true);
    };

    $scope.editEvent = function (event, allDay, jsEvent, view) {
        self.open('lg', event);
    };

    $scope.dropEvent = function (event, dayDelta, minuteDelta, allDay, revertFunc, jsEvent, ui, view) {
        EventService.updateEvent(event.calendar.id, event.id, event.sequence, event.title, event.start, event.end, event.allDay)
            .then(
                function (data) {
                    $scope.$broadcast("EventEdited", data);
                }, function (reason) {
                    revertFunc();
                }
            );
    };

    $scope.resizeEvent = function (event, dayDelta, minuteDelta, revertFunc, jsEvent, ui, view) {
        EventService.updateEvent(event.calendar.id, event.id, event.sequence, event.title, event.start, event.end, event.allDay)
            .then(
                function (data) {
                    $scope.$broadcast("EventEdited", data);
                }, function (reason) {
                    revertFunc();
                }
            );
    };

    /* event sources array*/
    this.CalendarData = {
        eventSources: this.eventData.events
    };
    $scope.CalendarData = this.CalendarData;

    this.open = function (size, eventData, isCalendarScope) {
        eventData = eventData || {};

        var modalInstance = $mdDialog.show({
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
        }).then(function (newEvent) {
            $scope.$broadcast("EventInsert", newEvent);
            $scope.$emit("EventInsert", newEvent);
        }, function () {
            // Clicked Cancel on Modal; Do Nothing
        });
    };
}]);
