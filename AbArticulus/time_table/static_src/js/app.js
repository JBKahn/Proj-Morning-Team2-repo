

Error.stackTraceLimit = Infinity;
var myApp = angular.module("TimeTable", [
    "ngRoute",
    "templates",
    "todo.controllers.todo",
    "todo.service.todo",
    "todo.constants"
    'ui.calendar'
])
.config(["$httpProvider", "$routeProvider", function($httpProvider, $routeProvider) {
    $httpProvider.defaults.xsrfCookieName = "csrftoken";
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";

    var routeConfig = {
        controller: "EventController",
        templateUrl: "templates/calendar.html"
    };
    $routeProvider
    .when("/", routeConfig)
    .otherwise({
        redirectTo: "/"
    });
}]);

angular.module("todo.constants", [])
.factory("Constants", ["$window", function($window) {
    var jsBootstrap = $window.jsBootstrap || {};
    var constants = {
        todoListUrl: jsBootstrap.todoListUrl || "",
        todoUpdateUrl: jsBootstrap.todoUpdateUrl || "",
        staticUrl: jsBootstrap.staticUrl || ""
    };

    return {
        get: function(name) {
            return constants[name];
        }
    };
}]);
