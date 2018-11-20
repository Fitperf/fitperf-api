from datetime import datetime
from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Exercise, MovementsPerExercise, MovementSettingsPerMovementsPerExercise, Training
from .helper_dbtestdata import TestDatabase

class TrainingTest(APITestCase):
    """
    This class will test all the interactions we can have with
    Training views. What will be tested:
        -> Not Connected:
            FAIL:
                -> Get all trainings
                -> Get one specific exercise
        -> With admin account:
            SUCCESS:
                -> Get all trainings
                -> Get one specific training
                -> Create a new training from an existing exercise
                -> Delete a training
                -> Update a training
            FAIL:
                -> Update the exercise linked to the selected training (read_only)
        -> With non admin account:
            SUCCESS:
                -> Get the trainings only if founder == request.user
                -> Get one specific training only if founder == request.user
                -> Create a new training from an existing exercise only if exercise is_default or 
                    exercise founder == request.user
                -> Delete a training only if founder == request.user
                -> Update a training only if founder == request.user
            FAIL:
                -> Get one training if founder != request.user
                -> Delete a training if founder != request.user
                -> Update a training if founder != request.user
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a database for test with TestDatabase helper
        """
        TestDatabase.create()

    def test_not_connected_get_all_trainings(self):
        """
        Test if, we are not authenticated, the API returns a 403 status on this request
        Not allowed to get all trainings
        """
        url = reverse('trainings_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_not_connected_get_one_exercise(self):
        """
        Test if, we are not authenticated, the API returns a 403 status on this request
        not allowed to get one training
        """
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_trainings(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - all the trainings
        """
        self.client.login(username='admin_user', password='admin_password')
        trainings = Training.objects.count()
        url = reverse('trainings_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), trainings)

    def test_admin_get_one_training(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - get the adequate training
        """
        self.client.login(username='admin_user', password='admin_password')
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        training_response = {
            "id": connie_training.pk,
            "founder": connie_training.founder.pk,
            "date": connie_training.date,
            "performance_type": connie_training.performance_type,
            "performance_value": connie_training.performance_value,
            "done": connie_training.done,
            "exercise": {
                'id': connie.pk,
                'name': connie.name,
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
                "movements": [],
            }
        }

        for movement in connie.movements.all():
            mvt_per_exo = MovementsPerExercise.objects.filter(exercise=connie,
                                                            movement=movement)
            for mvt in mvt_per_exo:
                movement_dict = {
                    "id": mvt.pk ,
                    "movement": movement.pk,
                    "movement_number": mvt.movement_number,
                    "movement_settings": []
                }
                for setting in mvt.movement_settings.all():
                    set_per_mvt = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=mvt,
                                                                                      setting=setting)
                    
                    setting_dict = {
                        "id": set_per_mvt.pk,
                        "setting": setting.pk,
                        "setting_value": set_per_mvt.setting_value
                    }
                    movement_dict['movement_settings'].append(setting_dict)
            training_response['exercise']['movements'].append(movement_dict)
        
        self.assertCountEqual(response.data, training_response)

    def test_admin_create_one_exercise(self):
        """
        Test if, when we are logged with an admin account, the API creates correctly
        a training
        """
        self.client.login(username='admin_user', password='admin_password')
        founder = User.objects.get(username='admin_user')
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        initial_trainings = Training.objects.count()
        url = reverse('trainings_list')

        data = {
            "founder": founder.pk,
            "date": date,
            "performance_type": 'duree',
            "performance_value": 0,
            "done": False,
            "exercise": {
                'id': connie.pk,
                'name': connie.name,
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Training.objects.count(), initial_trainings + 1)

    def test_admin_update_one_training(self):
        """
        Test if, when we are logged with an admin account, the API updates the training
        with the adequate information. Moreover, it is not possible to update movements linked to
        an exercise
        """
        self.client.login(username='admin_user', password='admin_password')
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})

        data = {
            "founder": connie_training.founder.pk,
            "date": connie_training.date,
            "performance_type": connie_training.performance_type,
            "performance_value": 50,
            "done": connie_training.done,
            "exercise": {
                'id': connie.pk,
                'name': connie.name,
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
            }
        }

        response_expected = {
            "id": connie_training.pk,
            "founder": connie_training.founder.pk,
            "date": connie_training.date,
            "performance_type": connie_training.performance_type,
            "performance_value": 50,
            "done": connie_training.done,
            "exercise": {
                'id': connie.pk,
                'name': connie.name,
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
                "movements": [],
            }
        }

        for movement in connie.movements.all():
            mvt_per_exo = MovementsPerExercise.objects.filter(exercise=connie,
                                                            movement=movement)
            for mvt in mvt_per_exo:
                movement_dict = {
                    "id": mvt.pk ,
                    "movement": movement.pk,
                    "movement_number": mvt.movement_number,
                    "movement_settings": []
                }
                for setting in mvt.movement_settings.all():
                    set_per_mvt = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=mvt,
                                                                                      setting=setting)
                    
                    setting_dict = {
                        "id": set_per_mvt.pk,
                        "setting": setting.pk,
                        "setting_value": set_per_mvt.setting_value
                    }
                    movement_dict['movement_settings'].append(setting_dict)
            response_expected['exercise']['movements'].append(movement_dict)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data, response_expected)

    def test_admin_update_one_training_on_exercise_element(self):
        """
        Test if, when we are logged with an admin account, the API does not record the change
        """

        self.client.login(username='admin_user', password='admin_password')
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})

        data = {
            "founder": connie_training.founder.pk,
            "date": connie_training.date,
            "performance_type": connie_training.performance_type,
            "performance_value": connie_training.performance_value,
            "done": connie_training.done,
            "exercise": {
                'id': connie.pk,
                'name': "another name",
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
            }
        }

        response_expected = {
            "id": connie_training.pk,
            "founder": connie_training.founder.pk,
            "date": connie_training.date,
            "performance_type": connie_training.performance_type,
            "performance_value": 50,
            "done": connie_training.done,
            "exercise": {
                'id': connie.pk,
                'name': connie.name,
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
                "movements": [],
            }
        }

        for movement in connie.movements.all():
            mvt_per_exo = MovementsPerExercise.objects.filter(exercise=connie,
                                                            movement=movement)
            for mvt in mvt_per_exo:
                movement_dict = {
                    "id": mvt.pk ,
                    "movement": movement.pk,
                    "movement_number": mvt.movement_number,
                    "movement_settings": []
                }
                for setting in mvt.movement_settings.all():
                    set_per_mvt = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=mvt,
                                                                                      setting=setting)
                    
                    setting_dict = {
                        "id": set_per_mvt.pk,
                        "setting": setting.pk,
                        "setting_value": set_per_mvt.setting_value
                    }
                    movement_dict['movement_settings'].append(setting_dict)
            response_expected['exercise']['movements'].append(movement_dict)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data, response_expected)

    def test_admin_delete_one_exercise(self):
        """
        Test if, when we are logged with an admin account, the API deletes correctly the training
        """
        self.client.login(username='admin_user', password='admin_password')
        initial_trainings = Training.objects.count()
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Training.objects.count(), initial_trainings - 1)

    def test_non_admin_get_filtered_trainings(self):
        """
        Test if, when we are logged with a non admin account, the API returns:
            - a 200 status on this request
            - all the trainings where the request user is the founder
        """
        self.client.login(username='new_user', password='new_password')
        user = User.objects.get(username='new_user')
        allowed_trainings = Training.objects.filter(founder=user)
        url = reverse('trainings_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), allowed_trainings.count())

    def test_non_admin_get_founder_training(self):
        """
        Test if, when we are logged with a non admin account, the API returns:
            - a 200 status on this request
            - get the adequate training if the user is the founder of this training 
        """
        self.client.login(username='new_user', password='new_password')
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        training_response = {
            "id": connie_training.pk,
            "founder": connie_training.founder.pk,
            "date": connie_training.date,
            "performance_type": connie_training.performance_type,
            "performance_value": connie_training.performance_value,
            "done": connie_training.done,
            "exercise": {
                'id': connie.pk,
                'name': connie.name,
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
                "movements": [],
            }
        }

        for movement in connie.movements.all():
            mvt_per_exo = MovementsPerExercise.objects.filter(exercise=connie,
                                                            movement=movement)
            for mvt in mvt_per_exo:
                movement_dict = {
                    "id": mvt.pk ,
                    "movement": movement.pk,
                    "movement_number": mvt.movement_number,
                    "movement_settings": []
                }
                for setting in mvt.movement_settings.all():
                    set_per_mvt = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=mvt,
                                                                                      setting=setting)
                    
                    setting_dict = {
                        "id": set_per_mvt.pk,
                        "setting": setting.pk,
                        "setting_value": set_per_mvt.setting_value
                    }
                    movement_dict['movement_settings'].append(setting_dict)
            training_response['exercise']['movements'].append(movement_dict)
        
        self.assertCountEqual(response.data, training_response)

    def test_non_admin_get_non_founder_training(self):
        """
        Test if, when we are logged with a non admin account, the API returns:
            - a 403 FORBIDDEN status on this request because the user is not allowed to
                request a training where he is not the founder
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_create_one_training(self):
        """
        Test if, when we are logged with a non admin account, the API creates correctly
        a training
        """
        self.client.login(username='new_user', password='new_password')
        founder = User.objects.get(username='admin_user')
        date = datetime(2018, 11, 11)
        connie = Exercise.objects.get(name="connie")
        initial_trainings = Training.objects.count()
        url = reverse('trainings_list')

        data = {
            "founder": founder.pk,
            "date": date,
            "performance_type": 'duree',
            "performance_value": 0,
            "done": False,
            "exercise": {
                'id': connie.pk,
                'name': connie.name,
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Training.objects.count(), initial_trainings + 1)

    def test_non_admin_delete_one_founder_training(self):
        """
        Test if, when we are logged with a non admin account, the API deletes correctly the training
        """
        self.client.login(username='new_user', password='new_password')
        initial_trainings = Training.objects.count()
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Training.objects.count(), initial_trainings - 1)

    def test_non_admin_delete_one_non_founder_training(self):
        """
        Test if, when we are logged with a non admin account, the API returns a 403 error if
        the user he is not the founder of the training he wants to delete.
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        initial_trainings = Training.objects.count()
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Training.objects.count(), initial_trainings)

    def test_non_admin_update_one_founder_training(self):
        """
        Test if, when we are logged with a non admin account, the API updates the training
        with the adequate information. The user has to be the founder
        """
        self.client.login(username='new_user', password='new_password')
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})

        data = {
            "founder": connie_training.founder.pk,
            "date": connie_training.date,
            "performance_type": connie_training.performance_type,
            "performance_value": 50,
            "done": connie_training.done,
            "exercise": {
                'id': connie.pk,
                'name': connie.name,
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
            }
        }

        response_expected = {
            "id": connie_training.pk,
            "founder": connie_training.founder.pk,
            "date": connie_training.date,
            "performance_type": connie_training.performance_type,
            "performance_value": 50,
            "done": connie_training.done,
            "exercise": {
                'id': connie.pk,
                'name': connie.name,
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
                "movements": [],
            }
        }

        for movement in connie.movements.all():
            mvt_per_exo = MovementsPerExercise.objects.filter(exercise=connie,
                                                            movement=movement)
            for mvt in mvt_per_exo:
                movement_dict = {
                    "id": mvt.pk ,
                    "movement": movement.pk,
                    "movement_number": mvt.movement_number,
                    "movement_settings": []
                }
                for setting in mvt.movement_settings.all():
                    set_per_mvt = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=mvt,
                                                                                      setting=setting)
                    
                    setting_dict = {
                        "id": set_per_mvt.pk,
                        "setting": setting.pk,
                        "setting_value": set_per_mvt.setting_value
                    }
                    movement_dict['movement_settings'].append(setting_dict)
            response_expected['exercise']['movements'].append(movement_dict)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data, response_expected)

    def test_non_admin_update_one_non_founder_training(self):
        """
        Test if, when we are logged with a non admin account, the API returns a 403 error when the user
        tries to update a training where he is not the founder
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        date = datetime(2018, 4, 5)
        connie = Exercise.objects.get(name="connie")
        connie_training = Training.objects.get(Q(exercise=connie), Q(date=date))
        url = reverse('training_detail', kwargs={'pk': connie_training.pk})

        data = {
            "founder": connie_training.founder.pk,
            "date": connie_training.date,
            "performance_type": connie_training.performance_type,
            "performance_value": 50,
            "done": connie_training.done,
            "exercise": {
                'id': connie.pk,
                'name': connie.name,
                'description': connie.description,
                'exercise_type': connie.exercise_type,
                'goal_type': connie.goal_type,
                'goal_value': connie.goal_value,
                'founder': connie.founder.pk,
                'is_default': False,
            }
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)