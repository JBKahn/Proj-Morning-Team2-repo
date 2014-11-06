var eventModalController = function ($scope, $modalInstance, EventService, eventData) {
    $scope.modalData = {
        eventData: {
            'title': eventData.title || '',
            'startDate': eventData.startDate || '',
            'endDate': eventData.endDate || '',
            'allDay': eventData.title || false
        }
    };

    $scope.addEvent = function() {
        if (!$scope.modalData.eventData.title || !$scope.modalData.eventData.startDate || !$scope.modalData.eventData.endDate) {
            return;
        }
        EventService.addEvent($scope.modalData.eventData.title, $scope.modalData.eventData.startDate, $scope.modalData.eventData.endDate, $scope.modalData.eventData.allDay)
            .then(function(data) {
                $modalInstance.close(data);
            });
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
