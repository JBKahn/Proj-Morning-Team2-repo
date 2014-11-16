var calendarModalController = function ($scope, $mdDialog, Constants, CalendarService, calendars) {
    var usersAppCalendars = [];
    for (i = 0; i < calendars.length; i++) {
        if (calendars[i].isAppCalendar) {
            usersAppCalendars.push(calendars[i].name);
        }
    }
    $scope.init = function() {
        $scope.modalData = {
            'modalTitle': "Manage Calendars",
            'calendars': [],
            'usersCalendars': usersAppCalendars,
            calendarData: {
                'title': '',
            }
        };
        CalendarService.getCalendars().then(function (data) {
            var calendarsToExclude = [];
            for (i = 0; i < $scope.modalData.usersCalendars.length; i++) {
                calendarsToExclude.push($scope.modalData.usersCalendars[i]);
            }

            for (i = 0; i < data.length; i++) {
                if (calendarsToExclude.indexOf(data[i].name) === -1) {
                    $scope.modalData.calendars.push(data[i]);
                }
            }
        });
    };

    $scope.validateForm = function() {
        var calendarData = $scope.modalData.calendarData;
        var errors = [];
        if (!calendarData.title) {
            errors.push('title is required');
        } else {
            var validCourse = calendarData.title.match("^([A-Z]{3})[0-9]{3}(H|Y)1 (F|S|Y) (LEC|TUT)-[0-9]{4}$");
            if (!validCourse) {
                errors.push('invalid course format');
            }
        }
        return {
            'errors': errors
        };
    };

    $scope.addCalendar = function() {
        var calendarData = $scope.modalData.calendarData;
        var validate = $scope.validateForm();
        if (validate.errors.length > 0) {
            console.log(validate.errors);
            return;
        }

        var promise;
        promise = CalendarService.addCalendar(calendarData.title);

        promise.then(
            function (data) {
                $mdDialog.hide(data);
            }, function (reason) {
                // Do nothing. The update failed.
            }
        );
    };

    $scope.save = function () {
        $scope.addCalendar();
    };

    $scope.cancel = function () {
        $mdDialog.cancel();
    };

    $scope.init();
};

angular.module("timeTable.controllers.calendarModal", [])
.controller("CalendarModalController", ["$scope", "$mdDialog", "Constants", "CalendarService", "calendars", calendarModalController]);
