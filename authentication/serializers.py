from rest_framework.serializers import ModelSerializer, ValidationError, CharField
from django.contrib.auth.password_validation import validate_password

from authentication.models import User, Group


class RegisterSerializer(ModelSerializer):
    """ Serializer du modèle User avec contrôle du mot de passe selon les règles de validation définies dans
        Django et confirmation du mot de passe par double saisie """

    password1 = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password1', 'password2', 'first_name', 'last_name']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise ValidationError({'password': 'Les deux mots de passe ne sont pas identiques'})
        return data

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password1'])
        user.username = validated_data['username']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.is_active = True
        user.save()
        return user


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(ModelSerializer):

    groups = GroupSerializer(many=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'groups']


class UpdateUsersGroupsSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'groups']
