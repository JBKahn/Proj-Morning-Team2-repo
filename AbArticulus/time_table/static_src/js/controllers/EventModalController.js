var eventModalController = function ($scope, $modalInstance, Constants, EventService, eventData, calendars) {
    $scope.open = function($event, opened) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope[opened] = true;
    };

    $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
    };

    // Required as the original calendar passed in references a different object than modalData.calendars
    $scope.getCalendarOption = function(calendars, calendar_id) {
        var i;
        for (i = 0; i < calendars.length; i++) {
            if (calendars[i].id === calendar_id) {
                return calendars[i];
            }
        }
        return '';
    };

    $scope.modalData = {
        eventData: {
            'title': eventData.title || '',
            'startDay': eventData.start || new Date(),
            'endDay': eventData.end || new Date(),
            'startTime': eventData.start || new Date(),
            'endTime': eventData.end || new Date(),
            'allDay': eventData.allDay || false,
            'id': eventData.id || '',
            'sequence': eventData.sequence || 0,
            'description': eventData.description || '',
            'calendar': eventData.calendar && $scope.getCalendarOption(calendars, eventData.calendar.id) || '',
            'tagType': eventData.tag_type || Constants.get('tagTypes')[0],
            'tagNumber': eventData.tag_number || 0
        },
        'calendars': calendars,
        'tagTypes': Constants.get('tagTypes'),
        'editable': !eventData.calendar || eventData.calendar.editable,
        'initialData': eventData
    };

    $scope.addEvent = function() {
        var eventData = $scope.modalData.eventData;
        if (!eventData.title || !eventData.startTime || !eventData.startDay || !eventData.endTime || !eventData.endDay || !eventData.calendar) {
            return;
        }
        var startDate = eventData.startDay;
        startDate.setHours(eventData.startTime.getHours());
        startDate.setMinutes(eventData.startTime.getMinutes());
        var endDate = eventData.endDay;
        endDate.setHours(eventData.endTime.getHours());
        endDate.setMinutes(eventData.endTime.getMinutes());

        var promise;
        if (eventData.id === '') {
            promise = EventService.addEvent(eventData.calendar.id, eventData.title, startDate, endDate, eventData.allDay);
        } else {
            promise = EventService.updateEvent(eventData.calendar.id, eventData.id, eventData.sequence, eventData.title, startDate, endDate, eventData.allDay);
        }

        promise.then(
            function (data) {
                $modalInstance.close(data);
            }, function (reason) {
                // Do nothing. The update failed.
            }
        );
    };

    $scope.save = function () {
        $scope.addEvent();
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

};

angular.module("timeTable.controllers.eventModal", [])
.controller("EventModalController", ["$scope", "$modalInstance", "Constants", "EventService", "eventData", "calendars", eventModalController]);
