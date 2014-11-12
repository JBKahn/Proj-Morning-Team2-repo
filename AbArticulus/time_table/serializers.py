from rest_framework import serializers

from abcalendar.constants import TAG_CHOICES


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
