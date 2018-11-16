from django.urls import path

from .views import EquipmentList, EquipmentDetail, MovementList, MovementDetail, MovementSettingsList, MovementSettingsDetail, ExerciseList, ExerciseDetail, MovementsPerExerciseList, TrainingList, TrainingDetail

urlpatterns = [
    path('equipments/', EquipmentList.as_view(), name='equipments_list'),
    path('equipments/<int:pk>/', EquipmentDetail.as_view(), name='equipment_detail'),
    path('movements/', MovementList.as_view(), name='movements_list'),
    path('movements/<int:pk>/', MovementDetail.as_view(), name="movement_detail"),
    path('movement-settings/', MovementSettingsList.as_view(), name='movement_settings_list'),
    path('movement-settings/<int:pk>/', MovementSettingsDetail.as_view(), name='movement_setting_detail'),
    path('exercises/', ExerciseList.as_view(), name="exercises_list"),
    path('exercises/<int:pk>/', ExerciseDetail.as_view(), name="exercise_detail"),
    path('trainings/', TrainingList.as_view(), name="trainings_list"),
    path('trainings/<int:pk>/', TrainingDetail.as_view(), name="training_detail"),
    path('movements-per-exercise/', MovementsPerExerciseList.as_view(), name="mvts_per_exercise_list"),
]