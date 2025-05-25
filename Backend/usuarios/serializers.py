from rest_framework import serializers
from .models import Usuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_rol(self, obj):
        return {
            'id': obj.rol.id,
            'nombre': obj.rol.nombre
        } if obj.rol else None

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])

        user = Usuario(**validated_data)

        if password:
            user.set_password(password)

        user.save()

        if groups:
            user.groups.set(groups)
        if user_permissions:
            user.user_permissions.set(user_permissions)

        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'codigo'