var eventModalController = function ($scope, $modalInstance, EventService, eventData, calendars) {
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
            'startDate': eventData.start || '',
            'endDate': eventData.end || '',
            'allDay': eventData.allDay || false,
            'id': eventData.id || '',
            'sequence': eventData.sequence || 0,
            'calendar': eventData.calendar && $scope.getCalendarOption(calendars, eventData.calendar.id) || '',
        },
        'calendars': calendars,
        'editable': !eventData.calendar || eventData.calendar.editable
    };

    $scope.addEvent = function() {
        var eventData = $scope.modalData.eventData;
        if (!eventData.title || !eventData.startDate || !eventData.endDate || !eventData.calendar) {
            return;
        }
        var promise;
        if (eventData.id === '') {
            promise = EventService.addEvent(eventData.calendar.id, eventData.title, eventData.startDate, eventData.endDate, eventData.allDay);
        } else {
            promise = EventService.updateEvent(eventData.calendar.id, eventData.id, eventData.sequence, eventData.title, eventData.startDate, eventData.endDate, eventData.allDay);
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
.controller("EventModalController", ["$scope", "$modalInstance", "EventService", "eventData", "calendars", eventModalController]);
