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

class ExerciseSerializer(serializers.ModelSerializer):
    movements = MovementsPerExerciseSerializer(source='exercise_with_movements', many=True, required=False)

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
        instance.save()
        
        if "exercise_with_movements" in validated_data:
            movements_data = validated_data.pop("exercise_with_movements")
            movements_instance = (instance.exercise_with_movements).all()
            movements = list(movements_instance)

            for i, movement_data in enumerate(movements_data):
                movement = movements.pop(0)
                movement.movement = movement_data.get('movement', movement.movement)
                movement.movement_number = movement_data.get('movement_number', movement.movement_number)
                movement.save()

                if "movement_linked_to_exercise" in movement_data:
                    settings_data = movement_data.pop("movement_linked_to_exercise")
                    # Need index because movements_instance is a Queryset with several objects
                    settings_instance = (movements_instance[i].movement_linked_to_exercise).all()
                    settings = list(settings_instance)
                    
                    for setting_data in settings_data:
                        setting = settings.pop(0)
                        setting.setting = setting_data.get('setting', setting.setting)
                        setting.setting_value = setting_data.get('setting_value', setting.setting_value)
                        setting.save()

        return instance