from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Equipment, Movement, MovementSettings

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'equipments', 'movements', 'movement_settings')

class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = ('id', 'name', 'founder')

class MovementSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovementSettings
        fields = ('id', 'name', 'founder')

class MovementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movement
        fields = ('id', 'name', 'equipment', 'founder', 'settings')