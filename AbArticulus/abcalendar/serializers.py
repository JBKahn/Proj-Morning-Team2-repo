from rest_framework import serializers

from abcalendar.models import Vote, Comment, Tag, Event, GoogleEvent


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ('number', 'user')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('comment', 'created', 'user')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_type', 'number')


class EventSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    votes = VoteSerializer(many=True)

    class Meta:
        model = Event
        fields = ('start', 'end', 'reccur_until', 'all_day', 'tag', 'votes')


class GoogleEventSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = GoogleEvent
        fields = ('events', 'comments', 'revision')
