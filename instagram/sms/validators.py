from rest_framework import serializers


def phone_number(value):
    value = value.replace('-', '')
    if len(value) not in (10, 11):
        raise serializers.ValidationError('전화번호 길이가 올바르지 않습니다')
    if not value.startswith('0'):
        raise serializers.ValidationError('전화번호는 0으로 시작해야합니다')


def sms_length(value):
    encoded_str = value.encode('cp949')
    if len(encoded_str) > 90:
        raise serializers.ValidationError(
            f'90바이트 까지만 전송할 수 있습니다 (현재: {len(encoded_str)}bytes)')
