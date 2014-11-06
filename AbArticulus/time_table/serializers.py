from rest_framework import serializers


class SimpleEventSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    all_day = serializers.BooleanField()
