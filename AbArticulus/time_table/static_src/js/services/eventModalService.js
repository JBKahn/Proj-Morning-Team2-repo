angular.module("event.service.event", [])
.factory("EventModalService", ["$q", "$http", "$window", function($q, $http, $window) {
    return {
        getEvents: function(){
            var url = $window.jsBootstrap.todoListUrl; //what is URL for events?
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
        addEvent: function(todoText){ //params? time, comment, tag etc
            var url = $window.jsBootstrap.todoListUrl; // what is URL for events?
            var params = {
                item: todoText,
                is_done: false
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
        updateEvent: function(id, todoText, status){ //params? time, comment, tag etc
            var url = $window.jsBootstrap.todoUpdateUrl.replace(/\/0\//, "/" + id + "/"); // eventUpdate instead of todoUpdateUrl
            var params = {
                id: id,
                item: todoText,
                is_done: status
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
        },
        removeEvent: function(id){
            var url = $window.jsBootstrap.todoUpdateUrl.replace(/\/0\//, "/" + id + "/"); // eventUpdate instead of todoUpdateUrl
            var params = {
                id: id
            };

            var defer = $q.defer();

            $http({method: "DELETE", url: url, data: params})
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
