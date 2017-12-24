from rest_framework import serializers

from accounts import models


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    verified = serializers.ReadOnlyField()
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)
    team = serializers.HiddenField(default=None)

    class Meta:
        model = models.User
        fields = [
            'email', 'password', 'first_name', 'last_name', 'verified', 'team'
        ]


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    class Meta:
        model = models.Team
        fields = ['name', 'members']
