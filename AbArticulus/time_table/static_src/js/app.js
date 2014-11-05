

Error.stackTraceLimit = Infinity;
var myApp = angular.module("TimeTableApp", [
    "ngRoute",
    "AppTemplates",
    "ui.calendar",
    "ui.bootstrap",
    "ui.bootstrap.datetimepicker",
    "timeTable.constants",
    "timeTable.controllers.calendar",
    "timeTable.controllers.eventModal",
    "timeTable.service.eventService"
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
        eventListUrl: jsBootstrap.eventListUrl || "",
        eventUpdateUrl: jsBootstrap.eventUpdateUrl || "",
        staticUrl: jsBootstrap.staticUrl || ""
    };

    return {
        get: function(name) {
            return constants[name];
        }
    };
}]);
