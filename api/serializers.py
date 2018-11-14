from rest_framework import serializers

from django.db import transaction
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

    movement_settings = MovementSettingsPerMovementsPerExerciseSerializer(source='movement_linked_to_exercise', many=True)
    
    class Meta:
        model = MovementsPerExercise
        fields = ('id', 'movement', 'movement_number', 'movement_settings')

    def get_movement_settings(self, obj):
        "obj is a movement setting instance and returns a list of dict"
        qset = MovementSettingsPerMovementsPerExercise.objects.filter(exercise_movement=obj)
        return [MovementSettingsPerMovementsPerExerciseSerializer(exercise_movement).data for exercise_movement in qset]

class ExerciseSerializer(serializers.ModelSerializer):
    movements = MovementsPerExerciseSerializer(source='exercise_with_movements', many=True)

    class Meta:
        model = Exercise
        fields = ('id', 'name', 'description', 'exercise_type', 'goal_type', 'goal_value', 'founder', 'is_default', 'movements')

    @transaction.atomic
    def create(self, validated_data):    
        exercise = Exercise.objects.create(name=validated_data["name"],
                                            exercise_type=validated_data["exercise_type"],
                                            description=validated_data["description"],
                                            goal_type=validated_data["goal_type"],
                                            goal_value=validated_data["goal_value"],
                                            founder=validated_data["founder"])
        if validated_data["founder"].is_superuser:
            exercise.is_default = True
            exercise.save()

        for movement in validated_data["exercise_with_movements"]:
            mvt = Movement.objects.get(pk=movement["movement"].pk)
            mvt_associated = MovementsPerExercise.objects.create(exercise=exercise,
                                                                movement=mvt,
                                                                movement_number=movement["movement_number"])
            for setting in movement["movement_linked_to_exercise"]:
                setting_obj = MovementSettings.objects.get(pk=setting['setting'].pk)
                setting_associated = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=mvt_associated,
                                                                                            setting=setting_obj,
                                                                                            setting_value=setting['setting_value'])
        return exercise

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.exercise_type = validated_data.get('exercise_type', instance.exercise_type)
        instance.goal_type = validated_data.get('goal_type', instance.goal_type)
        instance.goal_value = validated_data.get('goal_value', instance.goal_value)
        instance.founder = validated_data.get('founder', instance.founder)
        instance.is_default = validated_data.get('is_default', instance.is_default)
        
        for movement in validated_data["exercise_with_movements"]:
            pass
            # instance.movement = validated_data.get(movement['movement'], instance.movement)
            # instance.movement_number = validated_data.get(movement['movement_number'], instance.movement_number)

            # for setting in validated_data["movement_linked_to_exercise"]:
            #     instance = MovementSettings.objects.get(pk=setting.pk)
            #     instance.setting = validated_data.get(setting['setting'], instance.setting)
            #     instance.setting_value = validated_data.get(setting['setting_value'], instance.setting_value)
        instance.save()
        return instance