var eventModalController = function ($scope, $mdDialog, Constants, EventService, eventData, calendars) {
    $scope.open = function($event, opened) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope[opened] = true;
    };

    $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
    };

    // Required as the original calendar passed in references a different object than modalData.calendars
    $scope.getCalendarOption = function(calendars, calendar_id) {
        var i;
        for (i = 0; i < calendars.length; i++) {
            if (calendars[i].id === calendar_id) {
                return calendars[i];
            }
        }
        return '';
    };

    $scope.shouldShowField = function(field) {
        if ($scope.modalData.isUserEvent) {
            return $scope.modalData.userEventFields.indexOf(field) > -1;
        } else {
            return $scope.modalData.appEventFields.indexOf(field) > -1;
        }
    };

    $scope.shouldDisabledField = function(field) {
        return $scope.modalData.disabledEventFields.indexOf(field) > -1;
    };

    $scope.selectCalendar = function() {
        $scope.modalData.isUserEvent = !$scope.modalData.eventData.calendar.isAppCalendar;
    };

    $scope.isSaveDisabled = function() {
        return !($scope.modalData.eventData.calendar && (!$scope.modalData.eventData.calendar.isAppCalendar || !$scope.modalData.eventData.calendar.canEditEvents));
    };

    $scope.init = function() {
        var appEventFields;
        var userEventFields;
        if (eventData.id) {
            // editing
            appEventFields = ['calendar', 'id', 'tagType', 'tagNumber', 'sequence', 'startDate', 'endDate', 'startTime', 'endTime', 'alternateTimes', 'comments'];
            userEventFields = ['calendar', 'id', 'title', 'sequence', 'startDate', 'endDate', 'startTime', 'endTime'];
            var calendar = $scope.getCalendarOption(calendars, eventData.calendar.id);
            if (calendar.isAppCalendar) {
                $scope.modalData = {
                    'modalTitle': "Edit Event",
                    'appEventFields': appEventFields,
                    'userEventFields': userEventFields,
                    'disabledEventFields': ['calendar', 'id', 'tagType', 'tagNumber'],
                    'isUserEvent': false,
                    'alternateTimes': eventData.description && JSON.parse(eventData.description).events,
                    'comments': eventData.description && JSON.parse(eventData.description).comments,
                    'calendars': [calendar],
                    'tagTypes': [JSON.parse(eventData.description).tag.tag_type.charAt(0).toUpperCase() + JSON.parse(eventData.description).tag.tag_type.slice(1).toLowerCase()],
                    eventData: {
                        'calendar': calendar,
                        'id': eventData.id,
                        'sequence': eventData.sequence,
                        'startDay': moment(eventData.start).format("YYYY/MM/DD"),
                        'endDay': moment(eventData.end).format("YYYY/MM/DD"),
                        'startTime': moment(eventData.start).format("h:mma"),
                        'endTime': moment(eventData.end).add('hours', 1).format("h:mma"),
                        'allDay': eventData.allDay,
                        'tagType': eventData.description && JSON.parse(eventData.description).tag.tag_type.charAt(0).toUpperCase() + JSON.parse(eventData.description).tag.tag_type.slice(1).toLowerCase(),
                        'tagNumber': eventData.description && JSON.parse(eventData.description).tag.number || 0
                    }
                };
            } else {
                if (eventData.canEditEvents) {
                    $scope.modalData = {
                        'modalTitle': "Edit Event",
                        'appEventFields': appEventFields,
                        'userEventFields': userEventFields,
                        'disabledEventFields': [],
                        'isUserEvent': true,
                        'calendars': [calendar],
                        eventData: {
                            'calendar': calendar,
                            'id': eventData.id,
                            'sequence': eventData.sequence,
                            'title': eventData.title,
                            'startDay': moment(eventData.start).format("YYYY/MM/DD"),
                            'endDay': moment(eventData.end).format("YYYY/MM/DD"),
                            'startTime': moment(eventData.start).format("h:mma"),
                            'endTime': moment(eventData.end).add('hours', 1).format("h:mma"),
                            'allDay': eventData.allDay,
                        }
                    };
                } else {
                    $scope.modalData = {
                        'modalTitle': "Edit Event",
                        'appEventFields': appEventFields,
                        'userEventFields': userEventFields,
                        'disabledEventFields': ['title', 'startDay', 'endDay', 'startTime', 'endTime', 'allDay', 'calendar'],
                        'isUserEvent': true,
                        'calendars': [calendar],
                        eventData: {
                            'calendar': calendar,
                            'id': eventData.id,
                            'sequence': eventData.sequence,
                            'title': eventData.title,
                            'startDay': moment(eventData.start).format("YYYY/MM/DD"),
                            'endDay': moment(eventData.end).format("YYYY/MM/DD"),
                            'startTime': moment(eventData.start).format("h:mma"),
                            'endTime': moment(eventData.end).add('hours', 1).format("h:mma"),
                            'allDay': eventData.allDay,
                        }
                    };
                }
            }
        } else {
            // new
            var eligableCreationCalendars = [];
            for (i =0; i < calendars.length; i++) {
                if (calendars[i].isAppCalendar || calendars[i].canCreateEvents) {
                    eligableCreationCalendars.push(calendars[i]);
                }
            }
            appEventFields = ['calendar', 'tagType', 'tagNumber', 'startDate', 'endDate', 'startTime', 'endTime'];
            userEventFields = ['calendar', 'title', 'startDate', 'endDate', 'startTime', 'endTime'];
            $scope.modalData = {
                'modalTitle': "Create Event",
                'calendars': eligableCreationCalendars,
                'tagTypes': Constants.get('tagTypes'),
                'appEventFields': appEventFields,
                'userEventFields': userEventFields,
                'disabledEventFields': [],
                'isUserEvent': false,
                eventData: {
                    'title': '',
                    'startDay': moment(eventData.start).format("YYYY/MM/DD"),
                    'endDay': moment(eventData.end).format("YYYY/MM/DD"),
                    'startTime': moment().format("h:mma"),
                    'endTime': moment().add('hours', 1).format("h:mma"),
                    'allDay': false,
                    'calendar': undefined,
                    'tagType': undefined,
                    'tagNumber': ''
                }
            };
        }
    };

    $scope.validateForm = function() {
        var eventData = $scope.modalData.eventData;
        var fields;
        var errors = [];
        if ($scope.modalData.isUserEvent) {
            fields = $scope.modalData.userEventFields;
        } else {
            fields = $scope.modalData.appEventFields;
        }
        // Check if missing data
        for (var i = 0; i < fields.length; i++) {
            if (!eventData[fields[i]]) {
                if ((fields[i] === 'startDate' && (!eventData.startDay || !eventData.startTime)) || (fields[i] === 'endDate' && (!eventData.endDay || !eventData.endTime))) {
                    errors.push('missing ' + fields[i]);
                } else {
                    if (['startDate', 'endDate', 'comments', 'alternateTimes'].indexOf(fields[i]) === -1) {
                        errors.push('missing ' + fields[i]);
                    }
                }
            }
        }
        if (errors.length > 0) {
            return {
                'errors': errors,
            };
        }
        if ((fields.indexOf('tagNumber') > -1 ) && isNaN(parseInt(eventData.tagNumber))) {
            errors.push('tagNumber is not an number');
        }
        if (!moment(eventData.startDay, 'YYYY/MM/DD').isValid()) {
            errors.push('startDate is not correctly formated');
        }
        if (!moment(eventData.endDay, 'YYYY/MM/DD').isValid()) {
            errors.push('endDate is not correctly formated');
        }
        if (moment(eventData.endDay, 'YYYY/MM/DD') < moment(eventData.startDay, 'YYYY/MM/DD')) {
            errors.push('endDate is before start date');
        }
        var startTime = eventData.startTime.match("^([0-9]{1,2}):([0-9]{2})(am|pm)$");
        if (eventData.allDay || !startTime || parseInt(startTime[1]) > 12 || parseInt(startTime[2]) > 60) {
            errors.push('start time format wrong');
        }
        var endTime = eventData.endTime.match("^([0-9]{1,2}):([0-9]{2})(am|pm)$");
        if (eventData.allDay ||!endTime || parseInt(endTime[1]) > 12 || parseInt(endTime[2]) > 60) {
            errors.push('end time format wrong');
        }
        if (startTime && endTIme) {
            var startHour = parseInt(startTime[1]),
                startMinutes = parseInt(startTime[2]),
                endHour = parseInt(endTime[1]),
                endMinutes = parseInt(endTime[2]);
            if (
                !eventData.allDay && endTime && startTime &&
                (moment(eventData.endDay).format('YYYY/MM/DD') !==  moment(eventData.startDay).format('YYYY/MM/DD')) &&
                (((endTime[3] === startTime[3]) && ((endHour < startHour) || ((endHour === startHour) && (endMinutes < startMinutes)))) ||
                (endTime[3] === 'am') && (startTime[3] === 'pm'))) {

                errors.push('start time is before end time on the same date');
            }
        }
        return {
            'startDate': moment(eventData.startDay + ' ' + startTime, 'YYYY/MM/DD h:mma').format(),
            'endDate': moment(eventData.endDay + ' ' + endTime, 'YYYY/MM/DD h:mma').format(),
            'errors': errors
        };
    };

    $scope.addEvent = function() {
        var eventData = $scope.modalData.eventData;
        var validate = $scope.validateForm();
        if (validate.errors.length > 0) {
            console.log(validate.errors);
            return;
        }

        var promise;
        if (eventData.id === undefined) {
            promise = EventService.addEvent(eventData.calendar.id, eventData.title, validate.startDate, validate.endDate, eventData.allDay, eventData.tagType || '', eventData.tagNumber);
        } else {
            promise = EventService.updateEvent(eventData.calendar.id, eventData.id, eventData.sequence, eventData.title, validate.startDate, validate.endDate, eventData.allDay);
        }

        promise.then(
            function (data) {
                $mdDialog.hide(data);
            }, function (reason) {
                // Do nothing. The update failed.
            }
        );
    };

    $scope.save = function () {
        $scope.addEvent();
    };

    $scope.cancel = function () {
        $mdDialog.cancel();
    };

    $scope.init();
};

angular.module("timeTable.controllers.eventModal", [])
.controller("EventModalController", ["$scope", "$mdDialog", "Constants", "EventService", "eventData", "calendars", eventModalController]);
