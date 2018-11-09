from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Training(models.Model):
    """
    This class represents the trainings created
    """
    TIME = 'duree'
    ROUND = 'round'
    DISTANCE = 'distance'
    ANYONE = "anyone"
    PERFORMANCE_TYPE = (
        (TIME, 'duree'),
        (ROUND, 'round'),
        (DISTANCE, 'distance'),
        (ANYONE, 'anyone')
    )

    founder = models.ForeignKey(User, 
                                on_delete=models.CASCADE, 
                                verbose_name="the training's creator")
    exercise = models.ForeignKey('Exercise',
                                on_delete=models.CASCADE)

    date = models.DateTimeField(default=timezone.now)

    done = models.BooleanField(default=False)

    performance_type = models.CharField(max_length=20, 
                                        null=False,
                                        choices=PERFORMANCE_TYPE)
    performance_value = models.IntegerField(null=True)

    def __str__(self):
        return "{} - {}".format(self.exercise.name, self.date)

class Exercise(models.Model):
    """
    This class represents the exercises created
    """
    RUNNING = 'RUNNING'
    FORTIME = 'FORTIME'
    AMRAP = 'AMRAP'
    WARMUP = 'WARMUP'
    STRENGTH = 'STRENGTH'
    EMOM = 'EMOM'
    CONDITIONNING = "CONDITIONNING"
    EXERCISE_TYPE = (
        (RUNNING, 'RUNNING'),
        (FORTIME, 'FORTIME'),
        (AMRAP, 'AMRAP'),
        (WARMUP, 'ECHAUFFEMENT'),
        (STRENGTH, 'FORCE'),
        (EMOM, 'EMOM'),
        (CONDITIONNING, 'CONDITIONNEMENT'),
    )

    TIME = 'duree'
    ROUND = 'round'
    DISTANCE = 'distance'
    ANYONE = "anyone"
    PERFORMANCE_TYPE = (
        (TIME, 'duree'),
        (ROUND, 'round'),
        (DISTANCE, 'distance'),
        (ANYONE, 'anyone')
    )
    name = models.CharField(max_length=200,
                            verbose_name="Nom")
    description = models.TextField(null=True,
                                    verbose_name="Description")
    exercise_type = models.CharField(max_length=20, 
                                     choices=EXERCISE_TYPE,
                                     verbose_name="Type")
    goal_type = models.CharField(max_length=20, 
                                        null=False,
                                        choices=PERFORMANCE_TYPE)
    goal_value = models.IntegerField(null=True)
    founder = models.ForeignKey(User, 
                                on_delete=models.CASCADE,
                                verbose_name="the execise's creator")
    is_default = models.BooleanField(default=False)
    movements = models.ManyToManyField('Movement',
                                      through='MovementsPerExercise', 
                                      related_name='exercises',
                                      verbose_name="list of movements per exercise")

    class Meta:
        verbose_name = 'exercice'

    def __str__(self):
        return self.name

class MovementsPerExercise(models.Model):
    """
    This class represents the movements per exercise.
    This is an association table between exercises and movements
    where we add the setting value (number of repetitions, etc...)
    """
    exercise = models.ForeignKey('Exercise',
                                 on_delete=models.CASCADE)
    movement = models.ForeignKey('Movement',
                                 on_delete=models.CASCADE)

    movement_number = models.IntegerField()

    movement_settings = models.ManyToManyField('MovementSettings',
                                                through='MovementSettingsPerMovementsPerExercise',
                                                related_name="exercise_movements",
                                                verbose_name="settings value per movement for one exercise")

    def __str__(self):
        return "{} - {} - {}".format(self.exercise.name, self.movement.name, self.movement_number)

class MovementSettingsPerMovementsPerExercise(models.Model):
    """
    This class represents the different settings for each movement linked to
    an exercise.
    It will set a value for each settings linked to the movement
    """

    exercise_movement = models.ForeignKey('MovementsPerExercise',
                                              on_delete=models.CASCADE,
                                              verbose_name="the settings value for each movement per exercise")
    setting = models.ForeignKey('MovementSettings',
                                on_delete=models.CASCADE,
                                verbose_name="the setting linked to the movement associated to the exercise")  
    setting_value = models.IntegerField(default=0)

    def __str__(self):
        return "{} : {} -> {} : {}".format(self.exercise_movement.exercise.name,
                                           self.exercise_movement.movement.name,
                                           self.setting, 
                                           self.setting_value)

class Movement(models.Model):
    """
    This class represents the movements created
    """
    name = models.CharField(max_length=50, 
                            unique=True,
                            verbose_name="Nom")
    equipment = models.ForeignKey('Equipment',
                                on_delete=models.CASCADE,
                                verbose_name="Equipement")
    founder = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="movements",
                                verbose_name="Createur")
    settings = models.ManyToManyField('MovementSettings',
                                     related_name='movements',
                                     verbose_name="Caracteristiques")

    class Meta:
        verbose_name = 'mouvement'

    def __str__(self):
        return self.name

class MovementSettings(models.Model):
    """
    This class represents the different settings a movement can be
    associated with.
    """
    REPETITIONS = "repetitions"
    WEIGHT = "poids"
    DISTANCE = "distance"
    CALORIES = "calories"
    LEST = "lestes"
    MOVEMENTS_SETTINGS = (
        (REPETITIONS, 'repetitions'),
        (WEIGHT, 'poids'),
        (DISTANCE, 'distance'),
        (CALORIES, 'calories'),
        (LEST, 'lestes')
    )
    name = models.CharField(max_length=20,
                            choices=MOVEMENTS_SETTINGS,
                            unique=True)
    founder = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name="movement_settings",
                            verbose_name="the movement setting's creator")

    setting_values = models.ManyToManyField('MovementsPerExercise',
                                            through='MovementSettingsPerMovementsPerExercise',
                                            related_name="exercise_settings",
                                            verbose_name="all the values linked to a setting")

    class Meta:
        verbose_name = 'configuration des mouvements'

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=20,
                            unique=True)

    founder = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="equipments",
                                verbose_name="the movement's creator")

    class Meta:
        verbose_name = 'equipement'

    def __str__(self):
        return self.name