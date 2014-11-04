var eventModalController = function ($scope, $modalInstance, items) {
  $scope.items = items;
  $scope.selected = {
    item: items[0]
  };

  $scope.ok = function () {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
};

angular.module("timeTable.controllers.eventModal", [])
.controller("EventModalController", ["$scope", "$modalInstance", "items", eventModalController]);