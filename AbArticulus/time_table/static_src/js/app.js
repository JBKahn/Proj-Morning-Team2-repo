

Error.stackTraceLimit = Infinity;
var myApp = angular.module("TimeTableApp", [
    "ngRoute",
    "AppTemplates",
    "ui.calendar",
    "ui.bootstrap",
    "ngMaterial",
    "timeTable.constants",
    "timeTable.controllers.calendar",
    "timeTable.controllers.eventModal",
    "timeTable.controllers.calendarModal",
    "timeTable.service.eventService",
    "timeTable.service.calendarService"
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
        calendarListUrl: jsBootstrap.calendarListUrl || "",
        eventListUrl: jsBootstrap.eventListUrl || "",
        eventUpdateUrl: jsBootstrap.eventUpdateUrl || "",
        tagTypes: jsBootstrap.tagTypes || "",
        staticUrl: jsBootstrap.staticUrl || "",
        userId: jsBootstrap.userId || ""
    };

    return {
        get: function(name) {
            return constants[name];
        }
    };
}]);
