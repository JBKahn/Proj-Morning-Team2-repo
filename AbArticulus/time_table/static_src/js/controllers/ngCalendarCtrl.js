var CalendarController =  function($scope, EventService) {
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    /* event source that contains custom events on the scope */
    $scope.events = [
    ];

    /* Change View */
    $scope.changeView = function(view,calendar) {
      calendar.fullCalendar('changeView',view);
    };
    /* Change View */
    $scope.renderCalender = function(calendar) {
      if(calendar){
        calendar.fullCalendar('render');
      }
    };
    /* config object */
    $scope.uiConfig = {
      calendar:{
        height: 450,
        editable: true,
        header:{
          left: 'title',
          center: '',
          right: 'today prev,next'
        },
      }
    };

    EventService.getEvents()
        .then(function (data) {
            for (var i = 0; i < data.length; i++) {
                $scope.events.push(data[i]);
            }
            $scope.eventSources = [$scope.events];
            //$scope.renderCalender($scope.myCalendar1);
            console.log(data);
        });



    /* event sources array*/
    $scope.eventSources = [$scope.events];
};
angular.module("timeTable.controllers.calendar", [])
.controller("CalendarController", ["$scope", "EventService", CalendarController]);
