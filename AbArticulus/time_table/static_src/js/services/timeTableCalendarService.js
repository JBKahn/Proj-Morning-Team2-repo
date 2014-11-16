angular.module("timeTable.service.calendarService", [])
.factory("CalendarService", ["$q", "$http", "Constants", function($q, $http, Constants) {
    return {
        getCalendars: function() {
            var url = Constants.get('calendarListUrl');
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

        addCalendar: function(title) {
            var url = Constants.get('calendarListUrl');
            var params = {
                title: title,
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
