var CalendarController =  function($scope, EventService) {
    var self = this;
    $scope.eventData = {
        events: []
    };

    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $scope.eventData.events = [
      {title: 'All Day Event',start: new Date(y, m, 1)},
      {title: 'Long Event',start: new Date(y, m, d - 5),end: new Date(y, m, d - 2)},
      {id: 999,title: 'Repeating Event',start: new Date(y, m, d - 3, 16, 0),allDay: false},
      {id: 999,title: 'Repeating Event',start: new Date(y, m, d + 4, 16, 0),allDay: false},
      {title: 'Birthday Party',start: new Date(y, m, d + 1, 19, 0),end: new Date(y, m, d + 1, 22, 30),allDay: false},
      {title: 'Click for Google',start: new Date(y, m, 28),end: new Date(y, m, 29)}
    ];


   $scope.eventData.uiConfig = {
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
            $scope.eventData.events = data;
            //$scope.myCalendar1.fullCalendar( 'rerenderEvents' );
            console.log(data);
        })
};
angular.module("timeTable.controllers.calendar", [])
.controller("CalendarController", ["$scope", "EventService", CalendarController]);
