from django.contrib import admin
from .models import Movement, MovementSettings, Equipment, Exercise, MovementsPerExercise, MovementSettingsPerMovementsPerExercise 

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder')
    list_filter = ('founder',)
    search_fields = ('name', 'founder') 

class MovementSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder')
    list_filter = ('founder',)
    search_fields = ('name',)

class MovementAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment', 'founder')
    list_filter = ('founder', )
    search_fields = ('name',)

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder', 'is_default', 'exercise_type', 'goal_type')
    list_filter = ('founder', 'exercise_type', 'is_default')
    search_fields = ('name',)

# Register your models here.
admin.site.register(Movement, MovementAdmin)
admin.site.register(MovementSettings, MovementSettingsAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Exercise, ExerciseAdmin)