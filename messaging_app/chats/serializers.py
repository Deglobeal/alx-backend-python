from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number'
        ]

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_name = serializers.SerializerMethodField()
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sender_name',
            'conversation',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['sender', 'conversation']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    topic = serializers.CharField(required=False)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
            'topic'
        ]

    def validate_topic(self, value):
        if "spam" in value.lower():
            raise serializers.ValidationError("Topic cannot contain spam")
        return value