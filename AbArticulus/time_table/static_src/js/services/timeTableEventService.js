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

        addEvent: function(calendar, title, startDate, endDate, allDay, tagType, tagNumber){
            var url = Constants.get('eventListUrl');
            var params = {
                calendar: calendar,
                title: title,
                start: startDate,
                end: endDate,
                all_day: allDay,
                tag_type: tagType.toUpperCase(),
                number: tagNumber
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

        updateEvent: function(calendar, id, sequence, title, startDate, endDate, allDay){
            var url = Constants.get('eventUpdateUrl').replace(/\/0\//, "/" + id + "/");
            var params = {
                calendar: calendar,
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
        },

        voteForEvent: function(calendar, title, startDate, endDate, allDay, tagType, tagNumber, vote) {
            var url = Constants.get('voteCreateUrl');
            var params = {
                calendar: calendar,
                title: title,
                start: startDate,
                end: endDate,
                all_day: allDay,
                tag_type: tagType.toUpperCase(),
                number: tagNumber,
                vote: vote
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

        commentOnEvent: function(calendar, tagType, tagNumber, comment) {
            var url = Constants.get('commentCreateUrl');
            var params = {
                calendar: calendar,
                tag_type: tagType.toUpperCase(),
                number: tagNumber,
                comment: comment
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
