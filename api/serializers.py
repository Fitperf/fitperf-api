from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Equipment, Movement, MovementSettings, Exercise, MovementsPerExercise, MovementSettingsPerMovementsPerExercise

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

class MovementSettingsPerMovementsPerExerciseSerializer(serializers.ModelSerializer):
    """
    Used as a nested serializer but MovementPerExercise Serializer
    """

    class Meta:
        model = MovementSettingsPerMovementsPerExercise
        fields = ('id', 'setting', 'setting_value')

class MovementsPerExerciseSerializer(serializers.ModelSerializer):
    """
    Used as a nested serializer by Exercise Serializer
    """
    movement_settings = serializers.SerializerMethodField()

    class Meta:
        model = MovementsPerExercise
        fields = ('id', 'movement', 'movement_number', 'movement_settings')

    def get_movement_settings(self, obj):
        "obj is a movement setting instance and returns a list of dict"
        qset = MovementSettingsPerMovementsPerExercise.objects.filter(exercise_movement=obj)
        return [MovementSettingsPerMovementsPerExerciseSerializer(exercise_movement).data for exercise_movement in qset]

class ExerciseSerializer(serializers.ModelSerializer):
    movements = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ('id', 'name', 'description', 'exercise_type', 'goal_type', 'goal_value', 'founder', 'is_default', 'movements')

    def get_movements(self, obj):
        "obj is a Movement instance and returns a list of dict"
        qset = MovementsPerExercise.objects.filter(exercise=obj)
        return [MovementsPerExerciseSerializer(exercise).data for exercise in qset]

    # def create(self, validated_data):
        
    #     exercise = Exercise.objects.create(**validated_data)
    #     for movement in movements:

        
            
