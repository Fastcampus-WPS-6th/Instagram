from rest_framework import serializers

from .validators import phone_number, sms_length


class SMSSerializer(serializers.Serializer):
    receiver = serializers.CharField(
        validators=[phone_number]
    )
    message = serializers.CharField(
        validators=[sms_length]
    )

    def validate_receiver(self, value):
        return value.replace('-', '')
