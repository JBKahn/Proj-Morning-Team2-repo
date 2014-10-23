

Error.stackTraceLimit = Infinity;
var myApp = angular.module("TimeTable", [
    "ngRoute",
    "templates",
    'ui.calendar'
])
.config(["$httpProvider", "$routeProvider", function($httpProvider, $routeProvider) {
    $httpProvider.defaults.xsrfCookieName = "csrftoken";
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";

    var routeConfig = {
        controller: "CalendarController",
        templateUrl: "templates/calendar.html"
    };
    $routeProvider
    .when("/", routeConfig)
    .otherwise({
        redirectTo: "/"
    });
}]);

angular.module("timeTable.constants", [])
.factory("Constants", ["$window", function($window) {
    var jsBootstrap = $window.jsBootstrap || {};
    var constants = {
        timeTableUrl: jsBootstrap.timeTableUrl || "",
        staticUrl: jsBootstrap.staticUrl || ""
    };

    return {
        get: function(name) {
            return constants[name];
        }
    };
}]);
