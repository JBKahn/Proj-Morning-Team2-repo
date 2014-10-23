var EventController =  function(TimeTable) {
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();
    var self = this;
    $scope.eventSources = [];

    TimeTableService.getEvents()
        .then(function (data) {
            self.eventData.events = data;
        })
};
angular.module("timeTable.controllers.event", [])
.controller("EventController", ["TimeTable", EventController]);
