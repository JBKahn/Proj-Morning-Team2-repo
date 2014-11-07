var eventModalController = function ($scope, $modalInstance, EventService, eventData) {
    $scope.modalData = {
        eventData: {
            'title': eventData.title || '',
            'startDate': eventData.start || '',
            'endDate': eventData.end || '',
            'allDay': eventData.title || false,
            'id': eventData.id || '',
            'sequence': eventData.sequence || 0
        }
    };

    $scope.addEvent = function() {
        var eventData = $scope.modalData.eventData;
        if (!eventData.title || !eventData.startDate || !eventData.endDate) {
            return;
        }
        if (eventData.id === '') {
            EventService.addEvent(eventData.title, eventData.startDate, eventData.endDate, eventData.allDay)
                .then(function(data) {
                    $modalInstance.close(data);
                });
        } else {
            EventService.updateEvent(eventData.id, eventData.sequence, eventData.title, eventData.startDate, eventData.endDate, eventData.allDay)
                .then(
                    function (data) {
                        $modalInstance.close(data);
                    }, function (reason) {
                        // Do nothing. The update failed.
                    }
                );
        }
    };

    $scope.save = function () {
        $scope.addEvent();
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

};

angular.module("timeTable.controllers.eventModal", [])
.controller("EventModalController", ["$scope", "$modalInstance", "EventService", "eventData", eventModalController]);
