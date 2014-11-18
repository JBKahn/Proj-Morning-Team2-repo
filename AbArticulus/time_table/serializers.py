import re

from rest_framework import serializers

from abcalendar.constants import TAG_CHOICES

course_matcher = re.compile(u'^[A-Za-z]{3}[0-9]{3}(H1 S|H1 F|Y1 Y) (LEC|TUT)-[0-9]{4}$')


class SimpleEventSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    all_day = serializers.BooleanField()


class SimpleEventUpdateSerializer(SimpleEventSerializer):
    id = serializers.CharField(max_length=100)
    sequence = serializers.IntegerField()


class SimpleTagSerializer(serializers.Serializer):
    tag_type = serializers.ChoiceField(choices=(TAG_CHOICES))
    number = serializers.IntegerField()


class SimpleCalendarSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)

    def validate_title(self, attrs, source):
        course_match = course_matcher.match(attrs[source])
        if not course_match:
            raise serializers.ValidationError("This is not a valid calendar name")
        return attrs


class SimpleDatabaseCalendarSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    gid = serializers.CharField(max_length=100)
