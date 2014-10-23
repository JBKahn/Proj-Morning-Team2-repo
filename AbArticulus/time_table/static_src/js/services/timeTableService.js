angular.module("timeTable.service.event", [])
.factory("TimeTableService", ["$q", "$http", "$window", function($q, $http, $window) {
    return {
        getEvents: function(){
            var url = $window.jsBootstrap.todoListUrl;
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
    };
}]);
