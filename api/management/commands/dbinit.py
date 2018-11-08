#! /usr/bin/env python3
# coding: utf-8
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Training, Exercise, MovementsPerExercise, MovementSettingsPerMovementsPerExercise, Movement, MovementSettings, Equipment

class DBinit:
    """
    This class creates all the objects by default for the program
    """

    def clean_db(self):
        """
        This method clean all the db
        """
        settings = MovementSettings.objects.all()
        if settings:
            settings.delete()
        
        equipments = Equipment.objects.all()
        if equipments:
            equipments.delete()
        
        movements = Movement.objects.all()
        if movements:
            movements.delete()
        
        exercises = Exercise.objects.all()
        if exercises:
            exercises.delete()

        mvts_per_exos = MovementsPerExercise.objects.all()
        if mvts_per_exos:
            mvts_per_exos.delete()

        settings_per_mvt_per_exo = MovementSettingsPerMovementsPerExercise.objects.all()
        if settings_per_mvt_per_exo:
            settings_per_mvt_per_exo.delete()

        trainings = Training.objects.all()
        if trainings:
            trainings.delete()

        users = User.objects.all()
        if users:
            users.delete()

    def start(self):
        """
        This method creates all the necessary settings
        """
        username = 'juliennuellas'
        email = 'julien.nuellas@gmail.com'
        password = 'fitperf1987'

        try:
            founder = User.objects.get(username=username)
        except:
            founder = User.objects.create_superuser(username=username, email=email, password=password)

        # We create the necessary settings
        rep = MovementSettings.objects.create(name=MovementSettings.REPETITIONS, founder=founder)
        weight = MovementSettings.objects.create(name=MovementSettings.WEIGHT, founder=founder)
        dist = MovementSettings.objects.create(name=MovementSettings.DISTANCE, founder=founder)
        cal = MovementSettings.objects.create(name=MovementSettings.CALORIES, founder=founder)
        lest = MovementSettings.objects.create(name=MovementSettings.LEST, founder=founder)

        # We create the necessary equipments
        kb = Equipment.objects.create(name="kettlebell", founder=founder)
        anyone = Equipment.objects.create(name="aucun", founder=founder)
        ball = Equipment.objects.create(name="wallball", founder=founder)
        drawbar = Equipment.objects.create(name="barre de traction", founder=founder)
        dipbar = Equipment.objects.create(name="barre à dips", founder=founder)
        rope = Equipment.objects.create(name="corde à sauter", founder=founder)
        ring = Equipment.objects.create(name="anneaux", founder=founder)
        box = Equipment.objects.create(name="box", founder=founder)
        vest = Equipment.objects.create(name="veste lestée", founder=founder)
        bar = Equipment.objects.create(name="barre olympique", founder=founder)
        row = Equipment.objects.create(name="rameur", founder=founder)

        # We create some movements
        squat = Movement.objects.create(name="squats", founder=founder, equipment=kb)
        squat.settings.add(rep, lest)

        pushup = Movement.objects.create(name="pushups", founder=founder, equipment=anyone)
        pushup.settings.add(rep, lest)
        
        wallball = Movement.objects.create(name="wallballs", founder=founder, equipment=ball)
        wallball.settings.add(rep, weight)
        
        pullup = Movement.objects.create(name="pullups", founder=founder, equipment=drawbar)
        wallball.settings.add(rep, lest)

        burpees = Movement.objects.create(name="burpees", founder=founder, equipment=anyone)
        burpees.settings.add(rep, lest)

        situp = Movement.objects.create(name="situps", founder=founder, equipment=anyone)
        burpees.settings.add(rep, lest)

        boxjumps = Movement.objects.create(name="box jumps", founder=founder, equipment=box)
        burpees.settings.add(rep, lest)

        run = Movement.objects.create(name="run", founder=founder, equipment=anyone)
        burpees.settings.add(dist, lest)

        deadlift = Movement.objects.create(name="deadlift", founder=founder, equipment=bar)
        deadlift.settings.add(rep, weight)

        handstand_pushup = Movement.objects.create(name="handstand pushup", founder=founder, equipment=anyone)
        handstand_pushup.settings.add(rep, lest)

        clean = Movement.objects.create(name="clean", founder=founder, equipment=bar)
        clean.settings.add(rep, weight)

        ring_dips = Movement.objects.create(name="ring dips", founder=founder, equipment=ring)
        ring_dips.settings.add(rep, lest)

        thruster = Movement.objects.create(name="thruster", founder=founder, equipment=bar)
        thruster.settings.add(rep, weight)

        clean_and_jerk = Movement.objects.create(name="clean and jerk", founder=founder, equipment=bar)
        clean_and_jerk.settings.add(rep, weight)

        kettlebell_swing = Movement.objects.create(name="kettlebell swing", founder=founder, equipment=kb)
        kettlebell_swing.settings.add(rep, weight)

        snatch = Movement.objects.create(name="snatch", founder=founder, equipment=bar)
        clean.settings.add(rep, weight)

        row = Movement.objects.create(name="rameur", founder=founder, equipment=row)
        row.settings.add(dist)

        pistol = Movement.objects.create(name="pistol", founder=founder, equipment=anyone)
        pistol.settings.add(rep, lest)

        overhead_squat = Movement.objects.create(name="overhead squat", founder=founder, equipment=bar)
        overhead_squat.settings.add(rep, weight)

        double_under = Movement.objects.create(name="double-unders", founder=founder, equipment=rope)
        double_under.settings.add(rep, lest)

        # We create some Workouts

        # BENCHMARK GIRLS -> http://www.elementcrossfit.com/benchmark-workouts/
        # 1. Chelsea
        chelsea = Exercise.objects.create(name="chelsea",
                                    exercise_type=Exercise.EMOM,
                                    description="""C'est un WOD Benchmark Girls. Il faut réaliser
                                                    un tour complet chaque minute pendant 30 minutes.
                                                    Si l'athlète n'arrive pas à réaliser un tour complet
                                                    pendant la minute, il est disqualifié.""",
                                    goal_type=Exercise.TIME,
                                    goal_value=30,
                                    is_default=True,
                                    founder=founder)
        chelsea_pullup = MovementsPerExercise.objects.create(exercise=chelsea,
                                                            movement=pullup,
                                                            movement_number=1)
        chelsea_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=5)
        chelsea_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_pullup,
                                                                                   setting=lest,
                                                                                   setting_value=0)
        chelsea_pushup = MovementsPerExercise.objects.create(exercise=chelsea,
                                                            movement=pushup,
                                                            movement_number=2)
        chelsea_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=10)
        chelsea_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_pushup,
                                                                                   setting=lest,
                                                                                   setting_value=0)
        chelsea_squat = MovementsPerExercise.objects.create(exercise=chelsea,
                                                            movement=squat,
                                                            movement_number=3)
        chelsea_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_squat,
                                                                                   setting=rep,
                                                                                   setting_value=15)
        chelsea_squat_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_squat,
                                                                                   setting=lest,
                                                                                   setting_value=0)

        # 2. Angie

        angie = Exercise.objects.create(name="angie",
                                    exercise_type=Exercise.FORTIME,
                                    description="""C'est un WOD Benchmark Girls. Il challenge fortement votre endurance musculaire sur l'ensemble de votre corps. L'objectif est de réaliser l'ensemble des mouvements en un minimum de temps.""",
                                    goal_type=Exercise.ROUND,
                                    goal_value=1,
                                    is_default=True,
                                    founder=founder)
        angie_pullup = MovementsPerExercise.objects.create(exercise=angie,
                                                            movement=pullup,
                                                            movement_number=1)
        angie_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=100)
        angie_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_pullup,
                                                                                    setting=lest,
                                                                                    setting_value=0)
        angie_pushup = MovementsPerExercise.objects.create(exercise=angie,
                                                            movement=pushup,
                                                            movement_number=2)
        angie_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=100)
        angie_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_pushup,
                                                                                   setting=lest,
                                                                                   setting_value=0)
        angie_situp = MovementsPerExercise.objects.create(exercise=angie,
                                                            movement=situp,
                                                            movement_number=3)
        angie_situp_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_situp,
                                                                                   setting=rep,
                                                                                   setting_value=100)
        angie_situp_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_situp,
                                                                                   setting=lest,
                                                                                   setting_value=0)
        angie_squat = MovementsPerExercise.objects.create(exercise=angie,
                                                            movement=squat,
                                                            movement_number=4)
        angie_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_squat,
                                                                                   setting=rep,
                                                                                   setting_value=100)
        angie_squat_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_squat,
                                                                                   setting=lest,
                                                                                   setting_value=0)

        # 3. Barbara
        barbara = Exercise.objects.create(name="barbara",
                                    exercise_type=Exercise.FORTIME,
                                    description="""C'est un WOD Benchmark Girls. Il travaille l'ensemble du corps et fait appel à votre endurance musculaire ainsi qu'à votre cardio. L'objectif est de réaliser l'ensemble des mouvements en un minimum de temps.""",
                                    goal_type=Exercise.ROUND,
                                    goal_value=5,
                                    is_default=True,
                                    founder=founder)
        barbara_pullup = MovementsPerExercise.objects.create(exercise=barbara,
                                                            movement=pullup,
                                                            movement_number=1)
        barbara_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=20)
        barbara_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_pullup,
                                                                                    setting=lest,
                                                                                    setting_value=0)
        barbara_pushup = MovementsPerExercise.objects.create(exercise=barbara,
                                                            movement=pushup,
                                                            movement_number=2)
        barbara_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=30)
        barbara_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_pushup,
                                                                                    setting=lest,
                                                                                    setting_value=0)
        barbara_situp = MovementsPerExercise.objects.create(exercise=barbara,
                                                            movement=situp,
                                                            movement_number=3)
        barbara_situp_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_situp,
                                                                                   setting=rep,
                                                                                   setting_value=40)
        barbara_situp_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_situp,
                                                                                   setting=lest,
                                                                                   setting_value=0) 
        barbara_squat = MovementsPerExercise.objects.create(exercise=barbara,
                                                            movement=squat,
                                                            movement_number=4)
        barbara_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_squat,
                                                                                   setting=rep,
                                                                                   setting_value=50)
        barbara_squat_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_squat,
                                                                                   setting=lest,
                                                                                   setting_value=0)

        # 4. Cindy
        cindy = Exercise.objects.create(name="cindy",
                            exercise_type=Exercise.AMRAP,
                            description="""C'est un WOD Benchmark Girls. Il travaille l'ensemble du corps et sollicite fortement le cardio. L'objectif est de faire le maximum de tours en 20 minutes.""",
                            goal_type=Exercise.TIME,
                            goal_value=20,
                            is_default=True,
                            founder=founder)
        cindy_pullup = MovementsPerExercise.objects.create(exercise=cindy,
                                                            movement=pullup,
                                                            movement_number=1)
        cindy_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=5)
        cindy_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_pullup,
                                                                                    setting=lest,
                                                                                    setting_value=0)
        cindy_pushup = MovementsPerExercise.objects.create(exercise=cindy,
                                                            movement=pushup,
                                                            movement_number=2)
        cindy_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=10)
        cindy_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_pushup,
                                                                                    setting=lest,
                                                                                    setting_value=0)
        cindy_squat = MovementsPerExercise.objects.create(exercise=cindy,
                                                            movement=squat,
                                                            movement_number=3)
        cindy_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_squat,
                                                                                   setting=rep,
                                                                                   setting_value=15)
        cindy_squat_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_squat,
                                                                                   setting=lest,
                                                                                   setting_value=0)

        # 5. Diane

        diane = Exercise.objects.create(name="diane",
                                        exercise_type=Exercise.FORTIME,
                                        description="""C'est un WOD Benchmark Girls. C'est un format 21-15-9 qui travaille principalement sur l'explosion musculaire.""",
                                        goal_type=Exercise.ROUND,
                                        goal_value=1,
                                        is_default=True,
                                        founder=founder)
        diane_deadlift_21 = MovementsPerExercise.objects.create(exercise=diane,
                                                                movement=deadlift,
                                                                movement_number=1)
        diane_deadlift_21_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_deadlift_21,
                                                                                       setting=rep,
                                                                                       setting_value=21)
        diane_deadlift_21_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_deadlift_21,
                                                                                       setting=weight,
                                                                                       setting_value=100)
        diane_handstand_pushup_21 = MovementsPerExercise.objects.create(exercise=diane,
                                                                movement=handstand_pushup,
                                                                movement_number=2)
        diane_handstand_pushup_21_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_handstand_pushup_21,
                                                                                       setting=rep,
                                                                                       setting_value=21)
        diane_handstand_pushup_21_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_handstand_pushup_21,
                                                                                       setting=lest,
                                                                                       setting_value=0)
        diane_deadlift_15 = MovementsPerExercise.objects.create(exercise=diane,
                                                                movement=deadlift,
                                                                movement_number=3)
        diane_deadlift_15_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_deadlift_15,
                                                                                       setting=rep,
                                                                                       setting_value=15)
        diane_deadlift_15_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_deadlift_15,
                                                                                       setting=weight,
                                                                                       setting_value=100)
        diane_handstand_pushup_15 = MovementsPerExercise.objects.create(exercise=diane,
                                                                movement=handstand_pushup,
                                                                movement_number=4)
        diane_handstand_pushup_15_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_handstand_pushup_15,
                                                                                       setting=rep,
                                                                                       setting_value=15)
        diane_handstand_pushup_15_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_handstand_pushup_15,
                                                                                       setting=lest,
                                                                                       setting_value=0)
        diane_deadlift_9 = MovementsPerExercise.objects.create(exercise=diane,
                                                                movement=deadlift,
                                                                movement_number=5)
        diane_deadlift_9_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_deadlift_9,
                                                                                       setting=rep,
                                                                                       setting_value=9)
        diane_deadlift_9_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_deadlift_9,
                                                                                       setting=weight,
                                                                                       setting_value=100)
        diane_handstand_pushup_9 = MovementsPerExercise.objects.create(exercise=diane,
                                                                movement=handstand_pushup,
                                                                movement_number=6)
        diane_handstand_pushup_9_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_handstand_pushup_9,
                                                                                       setting=rep,
                                                                                       setting_value=9)
        diane_handstand_pushup_9_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=diane_handstand_pushup_9,
                                                                                       setting=lest,
                                                                                       setting_value=0)

        # 6. Elizabeth

        elizabeth = Exercise.objects.create(name="elizabeth",
                                        exercise_type=Exercise.FORTIME,
                                        description="""C'est un WOD Benchmark Girls. C'est un format 21-15-9 qui travaille principalement sur l'explosion musculaire. Il fait également mal au niveau du cardio!""",
                                        goal_type=Exercise.ROUND,
                                        goal_value=1,
                                        is_default=True,
                                        founder=founder)

        elizabeth_clean_21 = MovementsPerExercise.objects.create(exercise=elizabeth,
                                                                movement=clean,
                                                                movement_number=1)
        elizabeth_clean_21_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_clean_21,
                                                                                       setting=rep,
                                                                                       setting_value=21)
        elizabeth_clean_21_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_clean_21,
                                                                                       setting=weight,
                                                                                       setting_value=60)
        elizabeth_ring_dips_21 = MovementsPerExercise.objects.create(exercise=elizabeth,
                                                                movement=ring_dips,
                                                                movement_number=2)
        elizabeth_ring_dips_21_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_ring_dips_21,
                                                                                       setting=rep,
                                                                                       setting_value=21)
        elizabeth_ring_dips_21_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_ring_dips_21,
                                                                                       setting=lest,
                                                                                       setting_value=0)
        elizabeth_clean_15 = MovementsPerExercise.objects.create(exercise=elizabeth,
                                                                movement=clean,
                                                                movement_number=3)
        elizabeth_clean_15_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_clean_15,
                                                                                       setting=rep,
                                                                                       setting_value=15)
        elizabeth_clean_15_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_clean_15,
                                                                                       setting=weight,
                                                                                       setting_value=60)
        elizabeth_ring_dips_15 = MovementsPerExercise.objects.create(exercise=elizabeth,
                                                                movement=ring_dips,
                                                                movement_number=4)
        elizabeth_ring_dips_15_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_ring_dips_15,
                                                                                       setting=rep,
                                                                                       setting_value=15)
        elizabeth_ring_dips_15_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_ring_dips_15,
                                                                                       setting=lest,
                                                                                       setting_value=0)
        elizabeth_clean_9 = MovementsPerExercise.objects.create(exercise=elizabeth,
                                                                movement=clean,
                                                                movement_number=5)
        elizabeth_clean_9_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_clean_9,
                                                                                       setting=rep,
                                                                                       setting_value=9)
        elizabeth_clean_9_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_clean_9,
                                                                                       setting=weight,
                                                                                       setting_value=60)
        elizabeth_ring_dips_9 = MovementsPerExercise.objects.create(exercise=elizabeth,
                                                                movement=ring_dips,
                                                                movement_number=6)
        elizabeth_ring_dips_9_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_ring_dips_9,
                                                                                       setting=rep,
                                                                                       setting_value=9)
        elizabeth_ring_dips_9_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=elizabeth_ring_dips_9,
                                                                                       setting=lest,
                                                                                       setting_value=0)

        # 7. Fran

        fran = Exercise.objects.create(name="fran",
                                        exercise_type=Exercise.FORTIME,
                                        description="""C'est un WOD Benchmark Girls. C'est un format 21-15-9 qui travaille principalement sur l'explosion musculaire et le cardio. C'est un entraînement rapide mais intense!""",
                                        goal_type=Exercise.ROUND,
                                        goal_value=1,
                                        is_default=True,
                                        founder=founder)

        fran_thruster_21 = MovementsPerExercise.objects.create(exercise=fran,
                                                                movement=thruster,
                                                                movement_number=1)
        fran_thruster_21_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_thruster_21,
                                                                                       setting=rep,
                                                                                       setting_value=21)
        fran_thruster_21_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_thruster_21,
                                                                                       setting=weight,
                                                                                       setting_value=40)
        fran_pullup_21 = MovementsPerExercise.objects.create(exercise=fran,
                                                                movement=pullup,
                                                                movement_number=2)
        fran_pullup_21_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_pullup_21,
                                                                                       setting=rep,
                                                                                       setting_value=21)
        fran_pullup_21_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_pullup_21,
                                                                                       setting=lest,
                                                                                       setting_value=0)
        fran_thruster_15 = MovementsPerExercise.objects.create(exercise=fran,
                                                                movement=thruster,
                                                                movement_number=3)
        fran_thruster_15_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_thruster_15,
                                                                                       setting=rep,
                                                                                       setting_value=15)
        fran_thruster_15_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_thruster_15,
                                                                                       setting=weight,
                                                                                       setting_value=40)
        fran_pullup_15 = MovementsPerExercise.objects.create(exercise=fran,
                                                                movement=pullup,
                                                                movement_number=4)
        fran_pullup_15_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_pullup_15,
                                                                                       setting=rep,
                                                                                       setting_value=15)
        fran_pullup_15_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_pullup_15,
                                                                                       setting=lest,
                                                                                       setting_value=0)
        fran_thruster_9 = MovementsPerExercise.objects.create(exercise=fran,
                                                                movement=thruster,
                                                                movement_number=5)
        fran_thruster_9_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_thruster_9,
                                                                                       setting=rep,
                                                                                       setting_value=9)
        fran_thruster_9_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_thruster_9,
                                                                                       setting=weight,
                                                                                       setting_value=40)
        fran_pullup_9 = MovementsPerExercise.objects.create(exercise=fran,
                                                                movement=pullup,
                                                                movement_number=6)
        fran_pullup_9_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_pullup_9,
                                                                                       setting=rep,
                                                                                       setting_value=9)
        fran_pullup_9_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=fran_pullup_9,
                                                                                       setting=lest,
                                                                                       setting_value=0)

        # 8. Grace

        grace = Exercise.objects.create(name="grace",
                                        exercise_type=Exercise.FORTIME,
                                        description="""C'est un WOD Benchmark Girls. L'objectif est de faire 30 clean and jerk le plus rapidement possible!""",
                                        goal_type=Exercise.ROUND,
                                        goal_value=1,
                                        is_default=True,
                                        founder=founder)

        grace_clean_and_jerk = MovementsPerExercise.objects.create(exercise=grace,
                                                                   movement=clean_and_jerk,
                                                                    movement_number=1)
        grace_clean_and_jerk_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=grace_clean_and_jerk,
                                                                                          setting=rep,
                                                                                          setting_value=30)
        grace_clean_and_jerk_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=grace_clean_and_jerk,
                                                                                          setting=weight,
                                                                                          setting_value=60)

        # 9. Helen

        helen = Exercise.objects.create(name="helen",
                                exercise_type=Exercise.FORTIME,
                                description="""C'est un WOD Benchmark Girls. C'est un exercice qui sollicite fortement les épaules et le cardios. L'objectif est de réaliser les 3 tours le plus rapidement possible.""",
                                goal_type=Exercise.ROUND,
                                goal_value=3,
                                is_default=True,
                                founder=founder)
        
        helen_run = MovementsPerExercise.objects.create(exercise=helen,
                                                        movement=run,
                                                        movement_number=1)
        helen_run_dist = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=helen_run,
                                                                                setting=dist,
                                                                                setting_value=400)
        helen_run_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=helen_run,
                                                                        setting=lest,
                                                                        setting_value=0)
        helen_kettlebell_swing = MovementsPerExercise.objects.create(exercise=helen,
                                                                    movement=kettlebell_swing,
                                                                    movement_number=2)
        helen_kettlebell_swing_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=helen_kettlebell_swing,
                                                                                            setting=rep,
                                                                                            setting_value=21)
        helen_kettlebell_swing_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=helen_kettlebell_swing,
                                                                                                setting=weight,
                                                                                                setting_value=24)

        helen_pullup = MovementsPerExercise.objects.create(exercise=helen,
                                                                    movement=pullup,
                                                                    movement_number=3)
        helen_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=helen_pullup,
                                                                                            setting=rep,
                                                                                            setting_value=12)
        helen_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=helen_pullup,
                                                                                                setting=lest,
                                                                                                setting_value=0)

        # 10. Isabel

        isabel = Exercise.objects.create(name="isabel",
                                        exercise_type=Exercise.FORTIME,
                                        description="""C'est un WOD Benchmark Girls. L'objectif est de faire 30 snatch le plus rapidement possible!""",
                                        goal_type=Exercise.ROUND,
                                        goal_value=1,
                                        is_default=True,
                                        founder=founder)

        isabel_snatch = MovementsPerExercise.objects.create(exercise=isabel,
                                                                   movement=snatch,
                                                                    movement_number=1)
        isabel_snatch_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=isabel_snatch,
                                                                                          setting=rep,
                                                                                          setting_value=30)
        isabel_snatch_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=isabel_snatch,
                                                                                          setting=weight,
                                                                                          setting_value=60)

        # 11. Jackie

        jackie = Exercise.objects.create(name="jackie",
                                         exercise_type=Exercise.FORTIME,
                                         description="""C'est un WOD Benchmark Girls très cardio qui va vous brûler les épaules!""",
                                         goal_type=Exercise.ROUND,
                                         goal_value=1,
                                         is_default=True,
                                         founder=founder)
        jackie_row = MovementsPerExercise.objects.create(exercise=jackie,
                                                         movement=row,
                                                         movement_number=1)
        jackie_row_dist = MovementSettingsPerMovementsPerExercise(exercise_movement=jackie_row,
                                                                  setting=dist,
                                                                  setting_value=1000)
        jackie_thruster = MovementsPerExercise.objects.create(exercise=jackie,
                                                              movement=thruster,
                                                              movement_number=2)
        jackie_thruster_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=jackie_thruster,
                                                                                     setting=rep,
                                                                                     setting_value=50)
        jackie_thruster_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=jackie_thruster,
                                                                                     setting=weight,   
                                                                                     setting_value=20)
        jackie_pullup = MovementsPerExercise.objects.create(exercise=jackie,
                                                            movement=pullup,
                                                            movement_number=3)
        jackie_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=jackie_pullup,
                                                                                            setting=rep,
                                                                                            setting_value=30)
        jackie_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=jackie_pullup,
                                                                                                setting=lest,
                                                                                                setting_value=0)


        # 12. Karen

        karen = Exercise.objects.create(name="karen",
                                        exercise_type=Exercise.FORTIME,
                                        description="""C'est un WOD Benchmark Girls. L'objectif est de faire 150 wallball shots le plus rapidement possible!""",
                                        goal_type=Exercise.ROUND,
                                        goal_value=1,
                                        is_default=True,
                                        founder=founder)

        karen_wallball = MovementsPerExercise.objects.create(exercise=karen,
                                                                   movement=wallball,
                                                                    movement_number=1)
        karen_wallball_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=karen_wallball,
                                                                                          setting=rep,
                                                                                          setting_value=150)
        karen_wallball_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=karen_wallball,
                                                                                          setting=weight,
                                                                                          setting_value=9)

        # 13. Mary

        mary = Exercise.objects.create(name="mary",
                                       exercise_type=Exercise.AMRAP,
                                       description="""C'est un WOD Benchmark Girls. L'objectif est de faire le plus de tours possible en 20 minutes.""",
                                       goal_type=Exercise.TIME,
                                       goal_value=20,
                                       is_default=True,
                                       founder=founder)

        mary_handstand_pushup = MovementsPerExercise.objects.create(exercise=mary,
                                                                movement=handstand_pushup,
                                                                movement_number=1)
        mary_handstand_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=mary_handstand_pushup,
                                                                                       setting=rep,
                                                                                       setting_value=5)
        mary_handstand_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=mary_handstand_pushup,
                                                                                       setting=lest,
                                                                                       setting_value=0)
        mary_pistol = MovementsPerExercise.objects.create(exercise=mary,
                                                                movement=pistol,
                                                                movement_number=2)
        mary_pistol_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=mary_pistol,
                                                                                       setting=rep,
                                                                                       setting_value=10)
        mary_pistol_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=mary_pistol,
                                                                                       setting=lest,
                                                                                       setting_value=0)
        mary_pullup = MovementsPerExercise.objects.create(exercise=mary,
                                                            movement=pullup,
                                                            movement_number=3)
        mary_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=mary_pullup,
                                                                                            setting=rep,
                                                                                            setting_value=15)
        mary_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=mary_pullup,
                                                                                                setting=lest,
                                                                                                setting_value=0)

        # 14. Nancy

        nancy = Exercise.objects.create(name="nancy",
                                exercise_type=Exercise.FORTIME,
                                description="""C'est un WOD Benchmark Girls. L'objectif est de réaliser 5 tours le plus rapidement possible.""",
                                goal_type=Exercise.ROUND,
                                goal_value=5,
                                is_default=True,
                                founder=founder)
        
        nancy_run = MovementsPerExercise.objects.create(exercise=nancy,
                                                        movement=run,
                                                        movement_number=1)
        nancy_run_dist = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=nancy_run,
                                                                                setting=dist,
                                                                                setting_value=400)
        nancy_run_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=nancy_run,
                                                                        setting=lest,
                                                                        setting_value=0)
        nancy_overhead_squat = MovementsPerExercise.objects.create(exercise=nancy,
                                                                   movement=overhead_squat,
                                                                    movement_number=2)
        nancy_overhead_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=nancy_overhead_squat,
                                                                                          setting=rep,
                                                                                          setting_value=15)
        nancy_overhead_squat_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=nancy_overhead_squat,
                                                                                          setting=weight,
                                                                                          setting_value=40)

        # 15. Annie

        annie = Exercise.objects.create(name="annie",
                                        exercise_type=Exercise.FORTIME,
                                        description="""C'est un WOD Benchmark Girls. C'est un exercise dégressif qu'il faut réaliser le plus rapidement possible""",
                                        goal_type=Exercise.ROUND,
                                        goal_value=1,
                                        is_default=True,
                                        founder=founder)

        annie_double_under_50 = MovementsPerExercise.objects.create(exercise=annie,
                                                                    movement=double_under,
                                                                    movement_number=1)
        annie_double_under_50_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_double_under_50,
                                                                                           setting=rep,
                                                                                           setting_value=50)
        annie_double_under_50_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_double_under_50,
                                                                                            setting=lest,
                                                                                            setting_value=0)
        annie_situp_50 = MovementsPerExercise.objects.create(exercise=annie,
                                                             movement=situp,
                                                             movement_number=2)
        annie_situp_50_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_situp_50,
                                                                                    setting=rep,
                                                                                    setting_value=50)
        annie_situp_50_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_situp_50,
                                                                                     setting=lest,
                                                                                     setting_value=0)
        annie_double_under_40 = MovementsPerExercise.objects.create(exercise=annie,
                                                                    movement=double_under,
                                                                    movement_number=3)
        annie_double_under_40_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_double_under_40,
                                                                                           setting=rep,
                                                                                           setting_value=40)
        annie_double_under_40_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_double_under_40,
                                                                                            setting=lest,
                                                                                            setting_value=0)
        annie_situp_40 = MovementsPerExercise.objects.create(exercise=annie,
                                                             movement=situp,
                                                             movement_number=4)
        annie_situp_40_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_situp_40,
                                                                                    setting=rep,
                                                                                    setting_value=40)
        annie_situp_40_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_situp_40,
                                                                                     setting=lest,
                                                                                     setting_value=0)
        annie_double_under_30 = MovementsPerExercise.objects.create(exercise=annie,
                                                                    movement=double_under,
                                                                    movement_number=5)
        annie_double_under_30_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_double_under_30,
                                                                                           setting=rep,
                                                                                           setting_value=30)
        annie_double_under_30_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_double_under_30,
                                                                                            setting=lest,
                                                                                            setting_value=0)
        annie_situp_30 = MovementsPerExercise.objects.create(exercise=annie,
                                                             movement=situp,
                                                             movement_number=6)
        annie_situp_30_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_situp_30,
                                                                                    setting=rep,
                                                                                    setting_value=30)
        annie_situp_30_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_situp_30,
                                                                                     setting=lest,
                                                                                     setting_value=0)
        annie_double_under_20 = MovementsPerExercise.objects.create(exercise=annie,
                                                                    movement=double_under,
                                                                    movement_number=7)
        annie_double_under_20_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_double_under_20,
                                                                                           setting=rep,
                                                                                           setting_value=20)
        annie_double_under_20_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_double_under_20,
                                                                                            setting=lest,
                                                                                            setting_value=0)
        annie_situp_20 = MovementsPerExercise.objects.create(exercise=annie,
                                                             movement=situp,
                                                             movement_number=8)
        annie_situp_20_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_situp_20,
                                                                                    setting=rep,
                                                                                    setting_value=20)
        annie_situp_20_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_situp_20,
                                                                                     setting=lest,
                                                                                     setting_value=0)
        annie_double_under_10 = MovementsPerExercise.objects.create(exercise=annie,
                                                                    movement=double_under,
                                                                    movement_number=9)
        annie_double_under_10_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_double_under_10,
                                                                                           setting=rep,
                                                                                           setting_value=10)
        annie_double_under_10_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_double_under_10,
                                                                                            setting=lest,
                                                                                            setting_value=0)
        annie_situp_10 = MovementsPerExercise.objects.create(exercise=annie,
                                                             movement=situp,
                                                             movement_number=10)
        annie_situp_10_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_situp_10,
                                                                                    setting=rep,
                                                                                    setting_value=10)
        annie_situp_10_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=annie_situp_10,
                                                                                     setting=lest,
                                                                                     setting_value=0)        
        
        # BENCHMARK HERO
        # 1. Murph
        murph = Exercise.objects.create(name="murph",
                            exercise_type=Exercise.FORTIME,
                            description="""C'est un WOD Benchmark Hero. Certainement l'un des wods benchmarks les plus dur. L'objectif est de réaliser le plus rapidement possible l'ensemble des mouvements le plus rapidement possible avec un gilet lesté de 9 kg.""",
                            goal_type=Exercise.ROUND,
                            goal_value=1,
                            is_default=True,
                            founder=founder)

        murph_run_1 = MovementsPerExercise.objects.create(exercise=murph,
                                                        movement=run,
                                                        movement_number=1)
        murph_run_1_dist = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_run_1,
                                                                                   setting=dist,
                                                                                   setting_value=1600)
        murph_run_1_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_run_1,
                                                                                   setting=lest,
                                                                                   setting_value=9)
        murph_pullup = MovementsPerExercise.objects.create(exercise=murph,
                                                            movement=pullup,
                                                            movement_number=2)
        murph_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=100)
        murph_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_pullup,
                                                                                    setting=lest,
                                                                                    setting_value=9)
        murph_pushup = MovementsPerExercise.objects.create(exercise=murph,
                                                            movement=pushup,
                                                            movement_number=3)
        murph_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=200)
        murph_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_pushup,
                                                                                    setting=lest,
                                                                                    setting_value=9)
        murph_squat = MovementsPerExercise.objects.create(exercise=murph,
                                                            movement=squat,
                                                            movement_number=4)
        murph_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_squat,
                                                                                   setting=rep,
                                                                                   setting_value=300)
        murph_squat_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_squat,
                                                                                    setting=lest,
                                                                                    setting_value=9)
        murph_run_2 = MovementsPerExercise.objects.create(exercise=murph,
                                                        movement=run,
                                                        movement_number=5)
        murph_run_2_dist = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_run_2,
                                                                                   setting=dist,
                                                                                   setting_value=1600)
        murph_run_2_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_run_2,
                                                                                   setting=lest,
                                                                                   setting_value=9)

class Command(BaseCommand):

    def handle(self, *args, **options):
        db_init = DBinit()
        db_init.clean_db()
        db_init.start()

        self.stdout.write("Base de données initialisée")