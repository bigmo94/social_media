import random

from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from .tasks import send_verification_code_task

from .models import Profile, Message, Follow
from .utils import send_verification_code


def code_generator():
    return random.randint(10000, 99999)


class ProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']

        try:
            profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            profile = Profile.objects.create_user(
                username=validated_data.get('email'),
                password=validated_data.get('password'),
                email=validated_data.get('email'),
                is_active=False
            )
        if not profile.is_active:
            verify_code = code_generator()
            cache_key = 'login_code_{}'.format(email)
            cache.set(cache_key, verify_code, timeout=120)
            send_verification_code_task.delay(profile.email, verify_code)

        return profile


class ProfileVerifySerializer(serializers.ModelSerializer):
    verify_code = serializers.IntegerField(write_only=True)

    class Meta:
        model = Profile
        fields = ['email', 'verify_code']

    def update(self, instance, validated_data):
        cache_key = 'login_code_{}'.format(instance.email)
        sent_code = cache.get(cache_key, None)
        input_code = validated_data.get('verify_code')

        if sent_code and sent_code == input_code:
            instance.is_active = True
            instance.save()
        else:
            raise ValidationError('Wrong verify code')
        return instance

    # todo: must remove
    # def create(self, validated_data):
    #     email = validated_data['email']
    #     try:
    #         profile = Profile.objects.get(email=email)
    #
    #     except Profile.DoesNotExist:
    #         raise ValidationError("Wrong email")
    #
    #     cache_key = 'login_code_{}'.format(email)
    #     sent_code = cache.get(cache_key, None)
    #     input_code = validated_data.get('verify_code')
    #
    #     if sent_code and sent_code == input_code:
    #         profile.is_active = True
    #         profile.save()
    #     else:
    #         raise ValidationError('Wrong verify code')
    #     return profile


class ProfileLoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['email', 'password', 'token']
        extra_kwargs = {'email': {"validators": []}, 'password': {'write_only': True}}

    def create(self, validated_data):
        profile = authenticate(**validated_data)
        if profile is None:
            raise ValidationError('Wrong credentials sent')
        Token.objects.get_or_create(user=profile)

        return profile

    def get_token(self, obj):
        return obj.auth_token.key


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'email', 'gender', 'birth_date',
            'profile_picture', 'bio')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile = Profile.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            gender=validated_data.get('gender'),
            birth_day=validated_data.get('birth_day'),
            profile_picture=validated_data.get('profile_picture'),
            bio=validated_data.get('bio'),

        )

        return profile


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField(read_only=True, required=False)
    target = serializers.SerializerMethodField(read_only=True, required=False)
    receiver = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'body', 'target']

    def create(self, validated_data):
        request = self.context.get('request')
        receiver = Profile.objects.get(username=validated_data.pop('receiver'))
        instance = Message.objects.create(sender=request.user, receiver=receiver, **validated_data)
        return instance

    def get_target(self, obj):
        return obj.receiver.username

    def get_sender(self, obj):
        return obj.sender.username


class FollowSerializer(serializers.ModelSerializer):
    following = ProfileSerializer(read_only=True)
    follower = serializers.CharField(write_only=True)

    class Meta:
        model = Follow
        fields = ('following', 'follower', 'created_time')
