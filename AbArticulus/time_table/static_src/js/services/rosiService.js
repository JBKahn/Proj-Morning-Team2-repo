angular.module("timeTable.service.rosiService", [])
.factory("RosiService", ["$q", "$http", "Constants", function($q, $http, Constants) {
    return {
        getCourses: function(username, password) {
            var url = Constants.get('rosiCourseListUrl');
            var params = {
                'student_num': username,
                'password': password
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
