angular.module("timeTable.services.event", [])
.factory("EventService", ["$q", "$http", "Constants", function($q, $http, Constants) {
    return {
        getEvents: function(){
            var url = Constants.get('timeTableUrl');
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
        },

        updateEvent: function(id, sequence, title, startDate, endDate, allDay){
            var url = Constants.get('eventUpdateUrl').replace(/\/0\//, "/" + id + "/");
            var params = {
                id: id,
                sequence: sequence + 1,
                title: title,
                start: startDate,
                end: endDate,
                all_day: allDay
            };

            var defer = $q.defer();

            $http({method: "PUT", url: url, data: params})
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
