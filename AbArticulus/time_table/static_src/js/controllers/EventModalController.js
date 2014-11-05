var eventModalController = function ($scope, $modalInstance, eventData) {
    $scope.modalData = {
        eventData: {
            'title': eventData.title || '',
            'startDate': eventData.startDate || '',
            'endDate': eventData.endDate || '',
            'allDay': eventData.title || false
        }
    };

    $scope.save = function () {
        //$modalInstance.close($scope.selected.item);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

};

angular.module("timeTable.controllers.eventModal", [])
.controller("EventModalController", ["$scope", "$modalInstance", "eventData", eventModalController]);
