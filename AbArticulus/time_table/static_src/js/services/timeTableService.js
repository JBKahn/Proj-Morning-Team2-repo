angular.module("timeTable.service.eventService", [])
.factory("EventService", ["$q", "$http", "Constants", function($q, $http, Constants) {
    return {
        getEvents: function(){
            var url = Constants.get('eventListUrl');
            var params = {};

            var defer = $q.defer();

            $http({method: "GET", url: url, data: params})
            .success(function(result){
                defer.resolve(result);
            })
            .error(function(error){
                defer.reject(error);
            });

            return defer.promise;
        },

        addEvent: function(title, startDate, endDate, allDay){
            var url = Constants.get('eventListUrl');
            var params = {
                title: title,
                start: startDate,
                end: endDate,
                all_day: allDay
            };

            var defer = $q.defer();

            $http({method: "POST", url: url, data: params})
            .success(function(result){
                defer.resolve(result);
            })
            .error(function(error){
                defer.reject(error);
            });

            return defer.promise;
        }
    };
}]);
