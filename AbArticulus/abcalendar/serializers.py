from rest_framework import serializers

from django.utils import timezone

from abcalendar.models import Vote, Comment, Tag, Event, GoogleEvent


class DateTimeTzAwareField(serializers.DateTimeField):

    def to_native(self, value):
        if value:
            value = timezone.localtime(value)
        return super(DateTimeTzAwareField, self).to_native(value)


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ('number', 'user')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('comment', 'created', 'user')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_type', 'number')


class EventSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True)
    start = DateTimeTzAwareField()
    end = DateTimeTzAwareField()
    reccur_until = DateTimeTzAwareField()

    class Meta:
        model = Event
        fields = ('start', 'end', 'reccur_until', 'all_day', 'votes')


class GoogleEventSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    comments = CommentSerializer(many=True)
    tag = TagSerializer()

    class Meta:
        model = GoogleEvent
        fields = ('events', 'comments', 'revision', 'tag')
