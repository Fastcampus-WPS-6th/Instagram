from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
            'age',
        )


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
            'password1',
            'password2',
            'age',
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다')
        return data

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            img_profile=validated_data.get('img_profile'),
            age=validated_data['age'],
        )

    def to_representation(self, instance):
        # serializer된 형태를 결정
        # super().to_representation()은 serialize된 기본 형태(dict)
        ret = super().to_representation(instance)
        data = {
            'user': ret,
            'token': instance.token,
        }
        # 마지막엔 serializer.data를 출력했을 때 반환될 값을 반환해줘야 함
        return data
