var calendarModalController = function ($scope, $mdDialog, Constants, CalendarService, RosiService, calendars) {
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
                'courses': [{'title': ''}],
                'errors': {
                    'courses': ['']
                }
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

    $scope.$watch('modalData.calendarData', function(newValue, oldValue) {
        $scope.validateForm();
    }, true);

    $scope.addMoreCourses = function() {
        $scope.modalData.calendarData.courses.push({
            'title': ''
        });
        $scope.modalData.calendarData.errors.courses.push('');
    };

    $scope.removeCourseFromList = function(index) {
        if ($scope.modalData.calendarData.courses.length < 2) {
            return;
        }
        $scope.modalData.calendarData.courses.splice(index, 1);
        $scope.modalData.calendarData.errors.courses.splice(index, 1);
    };

    $scope.getCoursesFromRosi = function() {
        promise = RosiService.getCourses($scope.modalData.calendarData.username, $scope.modalData.calendarData.password);

        promise.then(
            function (data) {
                var calendarsToExclude = [],
                    i;
                for (i = 0; i < $scope.modalData.usersCalendars.length; i++) {
                    calendarsToExclude.push($scope.modalData.usersCalendars[i]);
                }
                for (i = 0; i < $scope.modalData.calendarData.courses.length; i++) {
                    calendarsToExclude.push($scope.modalData.calendarData.courses[i].title);
                }
                for (i = 0; i < data.length; i++) {
                    if (calendarsToExclude.indexOf(data[i].trim()) === -1) {
                        $scope.modalData.calendarData.courses.push({title: data[i].trim()});
                    }
                }
                $scope.validateForm();
            }, function (reason) {
                // Do nothing. The update failed.
            }
        );
    };

    $scope.validateForm = function() {
        var calendarData = $scope.modalData.calendarData;
        for (var i = 0; i < calendarData.courses.length; i++) {
            calendarData.errors.courses[i] = '';
            if (!calendarData.courses[i].title) {
                calendarData.errors.courses[i] = 'title is required';
            } else {
                var validCourse = calendarData.courses[i].title.match("^([A-Z]{3})[0-9]{3}(H|Y)1 (F|S|Y) (LEC|TUT|PRA)-[0-9]{4}$");
                if (!validCourse) {
                    calendarData.errors.courses[i] = 'invalid course format';
                }
            }
        }
        return {
            'errors': calendarData.errors
        };
    };

    $scope.addCalendars = function() {
        var calendarData = $scope.modalData.calendarData;
        var validate = $scope.validateForm();
        if (validate.errors.length > 0) {
            console.log(validate.errors);
            return;
        }

        var promise;
        var courses = [];
        for (var i = 0; i < calendarData.courses.length; i++) {
            courses.push(calendarData.courses[i].title);
        }
        promise = CalendarService.addCalendar(courses);

        promise.then(
            function (data) {
                $mdDialog.hide(data);
            }, function (reason) {
                // Do nothing. The update failed.
            }
        );
    };

    $scope.save = function () {
        $scope.addCalendars();
    };

    $scope.cancel = function () {
        $mdDialog.cancel();
    };

    $scope.init();
};

angular.module("timeTable.controllers.calendarModal", [])
.controller("CalendarModalController", ["$scope", "$mdDialog", "Constants", "CalendarService", "RosiService", "calendars", calendarModalController]);
