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


    $scope.$watch('modalData.eventData', function(newValue, oldValue) {
        $scope.validateForm();
        if (newValue != oldValue) {
            $scope.modalData.eventChanged = true;
        }
    }, true);

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
        return !($scope.modalData.eventData.calendar && (!$scope.modalData.eventData.calendar.isAppCalendar || !$scope.modalData.eventData.calendar.canEditEvents)) && $scope.validateForm().errors.length > 0;
    };

    $scope.getUserVote = function(votes) {
        for (var i = 0; i < votes.length; i++) {
            if (votes[i].user === parseInt(Constants.get('userId'))) {
                return votes[i].number;
            }
        }
        return 0;
    };

    $scope.setUserVoteOnAlternative = function(alternative, vote) {
        for (var i = 0; i < alternative.votes.length; i++) {
            if (alternative.votes[i].user === parseInt(Constants.get('userId'))) {
                alternative.votes[i].number = vote;
                return;
            }
        }
        alternative.votes.push({number: vote, user: parseInt(Constants.get('userId'))});
    };

    $scope.getVoteTotalForEvent = function(votes) {
        var total = 0;
        for (var i = 0; i < votes.length; i++) {
            total = total + votes[i].number;
        }
        return total;
    };

    $scope.voteOnAlternative = function(alternative, vote) {
        for (var i = 0; i < $scope.modalData.alternateTimes.length; i++) {
            if (vote === 1) {
                $scope.setUserVoteOnAlternative($scope.modalData.alternateTimes[i], 0);
                $scope.modalData.alternateTimes[i].userVote = 0;
                $scope.modalData.alternateTimes[i].voteTotal = $scope.getVoteTotalForEvent($scope.modalData.alternateTimes[i]);
            }
        }
        $scope.setUserVoteOnAlternative(alternative, vote);
        alternative.userVote = vote;
        alternative.voteTotal = $scope.getVoteTotalForEvent(alternative.votes);
    };

    $scope.init = function() {
        var appEventFields;
        var userEventFields;
        if (eventData.id) {
            // editing
            appEventFields = ['calendar', 'id', 'tagType', 'tagNumber', 'sequence', 'startDate', 'endDate', 'startTime', 'endTime', 'alternateTimes', 'comments', 'allDay'];
            userEventFields = ['calendar', 'id', 'title', 'sequence', 'startDate', 'endDate', 'startTime', 'endTime', 'allDay'];
            var calendar = $scope.getCalendarOption(calendars, eventData.calendar.id),
                hasJsonDescription = (Object(eventData.description) === eventData.description);
            if (hasJsonDescription) {
                for (var i = 0; i < eventData.description.events.length; i++) {
                    var formatStr;
                    if (eventData.description.events[i].allDay) {
                        formatStr = 'ddd, MMM Do';
                    } else {
                        formatStr = "ddd, MMM Do YYYY, h:mma";
                    }
                    eventData.description.events[i].startFormatted = moment(eventData.description.events[i].start).format(formatStr);
                    eventData.description.events[i].endFormatted = moment(eventData.description.events[i].end).format(formatStr);
                    eventData.description.events[i].userVote = $scope.getUserVote(eventData.description.events[i].votes);
                    eventData.description.events[i].voteTotal = $scope.getVoteTotalForEvent(eventData.description.events[i].votes);
                }
            }
            if (calendar.isAppCalendar && !eventData.isreccuring) {
                $scope.modalData = {
                    'modalTitle': "Vote or Suggest a New Date and Time",
                    'saveButtonText': 'Suggest New Date',
                    'appEventFields': appEventFields,
                    'userEventFields': userEventFields,
                    'disabledEventFields': ['calendar', 'id', 'tagType', 'tagNumber'],
                    'isUserEvent': false,
                    'alternateTimes': (hasJsonDescription && eventData.description.events) || '',
                    'comments': (hasJsonDescription && eventData.description.comments) || '',
                    'calendars': [calendar],
                    'tagTypes': (hasJsonDescription && eventData.description.tag && [(eventData.description.tag.tag_type.charAt(0).toUpperCase() + eventData.description.tag.tag_type.slice(1).toLowerCase())]) || [],
                    'eventChanged': false,
                    eventData: {
                        'errors': {},
                        'calendar': calendar,
                        'id': eventData.id,
                        'sequence': eventData.sequence,
                        'startDay': moment(eventData.start).format("YYYY/MM/DD"),
                        'endDay': moment(eventData.end).format("YYYY/MM/DD"),
                        'startTime': moment(eventData.start).format("h:mma"),
                        'endTime': moment(eventData.end).format("h:mma"),
                        'allDay': eventData.allDay,
                        'tagType':(hasJsonDescription && eventData.description.tag  && (eventData.description.tag.tag_type.charAt(0).toUpperCase() + eventData.description.tag.tag_type.slice(1).toLowerCase())) || '',
                        'tagNumber':hasJsonDescription && eventData.description.tag && eventData.description.tag.number || 0
                    }
                };
            } else {
                if (eventData.canEditEvents && !eventData.isReccuring) {
                    $scope.modalData = {
                        'saveButtonText': 'Save Changes',
                        'modalTitle': "Edit Event",
                        'appEventFields': appEventFields,
                        'userEventFields': userEventFields,
                        'disabledEventFields': [],
                        'isUserEvent': true,
                        'calendars': [calendar],
                        eventData: {
                            'errors': {},
                            'calendar': calendar,
                            'id': eventData.id,
                            'sequence': eventData.sequence,
                            'title': eventData.title,
                            'startDay': moment(eventData.start).format("YYYY/MM/DD"),
                            'endDay': moment(eventData.end).add('hours', 1).format("YYYY/MM/DD"),
                            'startTime': moment(eventData.start).format("h:mma"),
                            'endTime': moment(eventData.end).add('hours', 1).format("h:mma"),
                            'allDay': eventData.allDay,
                        }
                    };
                } else {
                    $scope.modalData = {
                        'saveButtonText': '',
                        'modalTitle': "View Event",
                        'appEventFields': appEventFields,
                        'userEventFields': userEventFields,
                        'disabledEventFields': ['title', 'startDay', 'endDay', 'startTime', 'endTime', 'allDay', 'calendar'],
                        'isUserEvent': true,
                        'calendars': [calendar],
                        eventData: {
                            'errors': {},
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
            for (var i = 0; i < calendars.length; i++) {
                if (calendars[i].isAppCalendar || calendars[i].canCreateEvents) {
                    eligableCreationCalendars.push(calendars[i]);
                }
            }
            appEventFields = ['calendar', 'tagType', 'tagNumber', 'startDate', 'endDate', 'startTime', 'endTime', 'allDay'];
            userEventFields = ['calendar', 'title', 'startDate', 'endDate', 'startTime', 'endTime', 'allDay'];
            $scope.modalData = {
                'saveButtonText': 'Add Event',
                'modalTitle': "Create Event",
                'calendars': eligableCreationCalendars,
                'tagTypes': Constants.get('tagTypes'),
                'appEventFields': appEventFields,
                'userEventFields': userEventFields,
                'disabledEventFields': [],
                'isUserEvent': false,
                eventData: {
                    'errors': {},
                    'title': '',
                    'startDay': moment(eventData.start).format("YYYY/MM/DD"),
                    'endDay': moment(eventData.end).add('hours', 1).format("YYYY/MM/DD"),
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
        if (!$scope.modalData) {
            return {
                'errors': ['modal data is not defined']
            };
        }
        var eventData = $scope.modalData.eventData;
        var fields;
        var errors = [];
        $scope.modalData.eventData.errors = {};
        if ($scope.modalData.isUserEvent) {
            fields = $scope.modalData.userEventFields;
        } else {
            fields = $scope.modalData.appEventFields;
        }
        // Check if missing data
        for (var i = 0; i < fields.length; i++) {
            if (eventData[fields[i]] === '') {
                if ((fields[i] === 'startDate' && (!eventData.startDay || !eventData.startTime)) || (fields[i] === 'endDate' && (!eventData.endDay || !eventData.endTime))) {
                    if (!eventData.startDay) {
                        $scope.modalData.eventData.errors.startDay = 'Start Date is required';
                    }
                    if (!eventData.startTime) {
                        $scope.modalData.eventData.errors.startTime = 'Start Time is required';
                    }
                    if (!eventData.endDay) {
                        $scope.modalData.eventData.errors.endDay = 'End Date is required';
                    }
                    if (!eventData.endTime) {
                        $scope.modalData.eventData.errors.endTime = 'End Time is required';
                    }
                    errors.push('missing ' + fields[i]);
                } else {
                    if (['startDate', 'endDate', 'comments', 'alternateTimes', 'allDay'].indexOf(fields[i]) === -1) {
                        $scope.modalData.eventData.errors[fields[i]] = fields[i] + ' is required';
                        errors.push('missing ' + fields[i]);
                    }
                }
            }
        }

        if ((fields.indexOf('tagNumber') > -1 ) && eventData.tagNumber !== '' && isNaN(parseInt(eventData.tagNumber))) {
            $scope.modalData.eventData.errors.tagNumber = 'Tag Number must be a number';
            errors.push('tagNumber is not an number');
        }
        if (eventData.startDay && !moment(eventData.startDay, 'YYYY/MM/DD').isValid() || !eventData.startDay.match("^[0-9]{4}\/[0-9]{2}\/[0-9]{2}$")) {
            $scope.modalData.eventData.errors.startDay = 'Start Date must be proper date';
            errors.push('startDate is not correctly formated');
        }
        if (eventData.endDay && !moment(eventData.endDay, 'YYYY/MM/DD').isValid() || !eventData.endDay.match("^[0-9]{4}\/[0-9]{2}\/[0-9]{2}$")) {
            $scope.modalData.eventData.errors.endDay = 'End Date must be proper date';
            errors.push('endDate is not correctly formated');
        }
        if (eventData.startDay && eventData.endDay && moment(eventData.endDay, 'YYYY/MM/DD') < moment(eventData.startDay, 'YYYY/MM/DD')) {
            errors.push('endDate is before start date');
            $scope.modalData.eventData.errors.endDay = 'End Date must be after start date';
        }
        var startTime = eventData.startTime.match("^([0-9]{1,2}):([0-9]{2})(am|pm)$");
        if (!eventData.allDay && !startTime || parseInt(startTime[1]) > 12 || parseInt(startTime[2]) > 60) {
            errors.push('start time format wrong');
            $scope.modalData.eventData.errors.startTime = 'Start Time must be a valid time';
        }
        var endTime = eventData.endTime.match("^([0-9]{1,2}):([0-9]{2})(am|pm)$");
        if (!eventData.allDay && !endTime || parseInt(endTime[1]) > 12 || parseInt(endTime[2]) > 60) {
            errors.push('end time format wrong');
            $scope.modalData.eventData.errors.endTime = 'End Time must be a valid time';
        }
        if (startTime && endTime) {
            var startHour = parseInt(startTime[1]),
                startMinutes = parseInt(startTime[2]),
                endHour = parseInt(endTime[1]),
                endMinutes = parseInt(endTime[2]);
            if (
                !eventData.allDay && endTime && startTime &&
                (moment(eventData.endDay).format('YYYY/MM/DD') ===  moment(eventData.startDay).format('YYYY/MM/DD')) &&
                (((endTime[3] === startTime[3]) && ((endHour < startHour) || ((endHour === startHour) && (endMinutes <= startMinutes)))) ||
                (endTime[3] === 'am') && (startTime[3] === 'pm'))) {

                errors.push('start time is before end time on the same date');
                $scope.modalData.eventData.errors.endDay = 'End Time must be after start time';
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
        if (eventData.id === undefined || eventData.calendar.isAppCalendar) {
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
