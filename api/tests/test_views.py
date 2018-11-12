import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Equipment, Movement, MovementSettings
from .helper_dbtestdata import TestDatabase

class EquipmentTest(APITestCase):
    """
    This class will test all the interactions we can have with
    Equipment views. What will be tested:
        -> Not Connected:
            FAIL:
                -> Get all equipments
                -> Get one specific equipment
        -> With admin account:
            SUCCESS:
                -> Get all equipments
                -> Get one specific equipment
                -> Create a new equipment
                -> Delete an equipment
                -> Modify an equipment
            FAIL:
                -> Create a new equipment where the name already exists
        -> With non admin account:
            SUCCESS:
                -> Get all the equipments
                -> Get one specific equipment
            FAIL:
                -> Create a new equipment
                -> Delete a equipment
                -> Modify a equipment
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a database for test with TestDatabase helper
        """
        TestDatabase.create()

    def test_not_connected_get_all_equipements(self):
        """
        Test if, we are not authenticated, the API returns a 403 status on this request
        """
        url = reverse('equipments_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_not_connected_get_one_equipment(self):
        """
        Test if, we are not authenticated, the API returns a 403 status on this request
        """
        kb = Equipment.objects.get(name="kettlebell")
        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_equipements(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - all the equipments
        """
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('equipments_list')
        equipments = Equipment.objects.count()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), equipments)
    
    def test_admin_get_one_equipment(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - get the adequate equipment
        """
        self.client.login(username='admin_user', password='admin_password')
        kb = Equipment.objects.get(name="kettlebell")

        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        equipment_response = {
            'id': kb.pk,
            'name': kb.name,
            'founder': kb.founder.pk
        }
        self.assertEqual(response.data, equipment_response)

    def test_admin_create_one_equipment(self):
        """
        Test if, when we are logged with an admin account, the API creates correctly
        the equipment
        """
        self.client.login(username='admin_user', password='admin_password')
        founder = User.objects.get(username='admin_user')
        initial_equipments = Equipment.objects.count()
        url = reverse('equipments_list')
        data = {
            'name': 'box',
            'founder': founder.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Equipment.objects.count(), initial_equipments + 1)

    def test_admin_create_one_equipment_which_already_exists(self):
        """
        Test if, when we are logged with an admin account, the API does not create
        the equipment because the name is already used in the database
        """
        self.client.login(username='admin_user', password='admin_password')
        founder = User.objects.get(username='admin_user')
        initial_equipments = Equipment.objects.count()
        url = reverse('equipments_list')
        data = {
            'name': 'kettlebell',
            'founder': founder.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Equipment.objects.count(), initial_equipments)


    def test_admin_update_one_equipment(self):
        """
        Test if, when we are logged with an admin account, the API updates correctly
        the equipment
        """
        self.client.login(username='admin_user', password='admin_password')
        kb = Equipment.objects.get(name="kettlebell")
        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        data = {
            "id": kb.pk,
            "name": "big kettlebell",
            "founder": kb.founder.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": kb.pk, "name": "big kettlebell", "founder": kb.founder.pk})

    def test_admin_delete_one_equipment(self):
        """
        Test if, when we are logged with an admin account, the API deletes correctly the equipment
        """
        self.client.login(username='admin_user', password='admin_password')
        initial_equipments = Equipment.objects.count()
        kb = Equipment.objects.get(name="kettlebell")
        data = {
            "id": kb.pk,
            "name": kb.name,
            "founder": kb.founder.pk
        }
        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Equipment.objects.count(), initial_equipments - 1)

    def test_non_admin_get_all_equipements(self):
        """
        Test if, when we are logged with a non admin account, the API returns:
            - a 200 status on this request
            - all the equipments
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        url = reverse('equipments_list')
        equipments = Equipment.objects.count()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), equipments)
    
    def test_non_admin_get_one_equipment(self):
        """
        Test if, when we are logged with a non admin account, the API returns:
            - a 200 status on this request
            - get the adequate equipment
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        kb = Equipment.objects.get(name="kettlebell")

        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        equipment_response = {
            'id': kb.pk,
            'name': kb.name,
            'founder': kb.founder.pk
        }
        self.assertEqual(response.data, equipment_response)

    def test_non_admin_create_one_equipment(self):
        """
        Test if, when we are logged with a non admin account, the API does not create
        the equipment
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        founder = User.objects.get(username='ordinary_user')
        initial_equipments = Equipment.objects.count()
        url = reverse('equipments_list')
        data = {
            'name': 'box',
            'founder': founder.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Equipment.objects.count(), initial_equipments)

    def test_non_admin_update_one_equipment(self):
        """
        Test if, when we are logged with a non admin account, the API does not update
        the equipment
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        kb = Equipment.objects.get(name="kettlebell")
        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        data = {
            "id": kb.pk,
            "name": "big kettlebell",
            "founder": kb.founder.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_delete_one_equipment(self):
        """
        Test if, when we are logged with a non admin account, the API does not delete the
        equipment
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        initial_equipments = Equipment.objects.count()
        kb = Equipment.objects.get(name="kettlebell")
        data = {
            "id": kb.pk,
            "name": kb.name,
            "founder": kb.founder.pk
        }
        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Equipment.objects.count(), initial_equipments)

class MovementSettingsTest(APITestCase):
    """
    This class will test all the interactions we can have with
    MovementSettings views. What will be tested:
        -> Not Connected:
            FAIL:
                -> Get all movement's settings
                -> Get one specific movement setting
        -> With admin account:
            SUCCESS:
                -> Get all movement's settings
                -> Get one specific movement setting
                -> Create a new movementsetting in list choice
                -> Delete a movement setting
                -> Modify a movement setting
            FAIL:
                -> Create a new movementsetting not in the list
        -> With non admin account:
            SUCCESS:
                -> Get all the movement's settings
                -> Get one specific movement setting
            FAIL:
                -> Create a new movementsetting in list choice
                -> Delete a movement setting
                -> Modify a movement setting
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a database for test with TestDatabase helper
        """
        TestDatabase.create()

    def test_not_connected_get_all_movement_settings(self):
        """
        Test if, we are not authenticated,  the API returns a 403 status on this request
        """
        url = reverse('movement_settings_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_not_connected_get_one_movement_settings(self):
        """
        Test if, we are not authenticated,  the API returns a 403 status on this request
        """
        url = reverse('movement_setting_detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_movement_settings(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - all the movement settings
        """
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('movement_settings_list')
        settings = MovementSettings.objects.count()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), settings)
    
    def test_admin_get_one_movement_settings(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - get the adequate movement setting
        """
        self.client.login(username='admin_user', password='admin_password')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)

        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        setting_response = {
            'id': rep.pk,
            'name': rep.name,
            'founder': rep.founder.pk
        }
        self.assertEqual(response.data, setting_response)

    def test_admin_create_one_movement_settings(self):
        """
        Test if, when we are logged with an admin account, the API creates correctly
        the movement settings
        """
        self.client.login(username='admin_user', password='admin_password')
        founder = User.objects.get(username='admin_user')
        initial_movement_settings = MovementSettings.objects.count()
        url = reverse('movement_settings_list')
        data = {
            'name': 'lestes',
            'founder': founder.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MovementSettings.objects.count(), initial_movement_settings + 1)

    def test_admin_update_one_movement_settings_in_list(self):
        """
        Test if, when we are logged with an admin account, the API updates the movement settings
        because the name is in the choice list
        """
        self.client.login(username='admin_user', password='admin_password')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        data = {
            "id": rep.pk,
            "name": MovementSettings.LEST,
            "founder": rep.founder.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": rep.pk, "name": "lestes", "founder": rep.founder.pk})

    def test_admin_update_one_movement_settings_not_in_list(self):
        """
        Test if, when we are logged with an admin account, the API does not update the movement settings
        because it is not in the choice list
        """
        self.client.login(username='admin_user', password='admin_password')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        data = {
            "id": rep.pk,
            "name": "new_repetitions",
            "founder": rep.founder.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_delete_one_movement_settings(self):
        """
        Test if, when we are logged with an admin account, the API deletes correctly the movement settings
        """
        self.client.login(username='admin_user', password='admin_password')
        initial_movement_settings = MovementSettings.objects.count()
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        data = {
            "id": rep.pk,
            "name": rep.name,
            "founder": rep.founder.pk
        }
        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MovementSettings.objects.count(), initial_movement_settings - 1)

    def test_non_admin_get_all_movement_settings(self):
        """
        Test if, when we are logged with a non-admin account, the API returns:
            - a 200 status on this request
            - all the movement settings
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        settings = MovementSettings.objects.count()
        url = reverse('movement_settings_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), settings)
    
    def test_non_admin_get_one_movement_settings(self):
        """
        Test if, when we are logged with a non-admin account, the API returns:
            - a 200 status on this request
            - get the adequate movement
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)

        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        setting_response = {
            'id': rep.pk,
            'name': rep.name,
            'founder': rep.founder.pk
        }
        self.assertEqual(response.data, setting_response)

    def test_non_admin_create_one_movement_settings(self):
        """
        Test if, when we are logged with a non admin account, the API forbids the creation of
        a movement settings
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        founder = User.objects.get(username='ordinary_user')
        initial_movement_settings = MovementSettings.objects.count()
        url = reverse('movement_settings_list')
        data = {
            'name': 'lestes',
            'founder': founder.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MovementSettings.objects.count(), initial_movement_settings)

    def test_non_admin_update_one_movement_settings(self):
        """
        Test if, when we are logged with a non admin account, the API does not allowed the 
        update.
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        data = {
            "id": rep.pk,
            "name": MovementSettings.LEST,
            "founder": rep.founder.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_delete_one_movement_settings(self):
        """
        Test if, when we are logged with a non admin account, the API does not allowed the 
        deleting.
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        initial_movement_settings = MovementSettings.objects.count()
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        data = {
            "id": rep.pk,
            "name": rep.name,
            "founder": rep.founder.pk
        }
        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class MovementTest(APITestCase):
    """
    This class will test all the interactions we can have with
    Movement views. What will be tested:
        -> Not Connected:
            FAIL:
                -> Get all movements
                -> Get one specific movement
        -> With admin account:
            SUCCESS:
                -> Get all movements
                -> Get one specific movement
                -> Create a new movement
                -> Delete a movement
                -> Modify a movement
            FAIL:
                -> Create a new movement with a name which already exists in the database
        -> With non admin account:
            SUCCESS:
                -> Get all the movements
                -> Get one specific movements
            FAIL:
                -> Create a new movements
                -> Delete a movement
                -> Modify a movement
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a database for test with TestDatabase helper
        """
        TestDatabase.create()

    def test_not_connected_get_all_movements(self):
        """
        Test if, we are not authenticated, the API returns a 403 status on this request
        Not allowed to get all movements
        """
        url = reverse('movements_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_not_connected_get_one_movement(self):
        """
        Test if, we are not authenticated, the API returns a 403 status on this request
        not allowed to get one movement
        """
        url = reverse('movement_detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_movements(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - all the movements
        """
        self.client.login(username='admin_user', password='admin_password')
        movements = Movement.objects.count()
        url = reverse('movements_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), movements)
    
    def test_admin_get_one_movement(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - get the adequate movement
        """
        self.client.login(username='admin_user', password='admin_password')
        squat = Movement.objects.get(name='squat')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        weight = MovementSettings.objects.get(name=MovementSettings.WEIGHT)
        url = reverse('movement_detail', kwargs={'pk': squat.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        movement_response = {
            'id': squat.pk,
            'name': squat.name,
            'equipment': squat.equipment.pk,
            'founder': squat.founder.pk,
            'settings': [rep.pk, weight.pk]
        }
        self.assertEqual(response.data, movement_response)


    def test_admin_create_one_movement(self):
        """
        Test if, when we are logged with an admin account, the API creates correctly
        the movement
        """
        self.client.login(username='admin_user', password='admin_password')
        founder = User.objects.get(username='admin_user')
        no_equipment = Equipment.objects.get(name='aucun')
        rep = MovementSettings.objects.get(name='repetitions')
        initial_movements = Movement.objects.count()
        url = reverse('movements_list')
        data = {
            'name': 'burpees',
            'founder': founder.pk,
            'equipment': no_equipment.pk,
            'settings': [
                rep.pk
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movement.objects.count(), initial_movements + 1)

    def test_admin_create_one_movement_which_already_exists(self):
        """
        Test if, when we are logged with an admin account, the API does not create
        the movement if it's already exist
        """
        self.client.login(username='admin_user', password='admin_password')
        founder = User.objects.get(username='admin_user')
        no_equipment = Equipment.objects.get(name='aucun')
        rep = MovementSettings.objects.get(name='repetitions')
        initial_movements = Movement.objects.count()
        url = reverse('movements_list')
        data = {
            'name': 'squat',
            'founder': founder.pk,
            'equipment': no_equipment.pk,
            'settings': [
                rep.pk
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Movement.objects.count(), initial_movements)

    def test_admin_update_one_movement(self):
        """
        Test if, when we are logged with an admin account, the API updates the movement
        """
        self.client.login(username='admin_user', password='admin_password')
        wallball = Movement.objects.get(name='wallball')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        weight = MovementSettings.objects.get(name=MovementSettings.WEIGHT)

        url = reverse('movement_detail', kwargs={'pk': wallball.pk})
        data = {
            "id": wallball.pk,
            "name": "heavy wallball",
            "founder": wallball.founder.pk,
            "equipment": wallball.equipment.pk,
            "settings": [rep.pk, weight.pk]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_admin_delete_one_movement(self):
        """
        Test if, when we are logged with an admin account, the API deletes correctly the movement
        """
        self.client.login(username='admin_user', password='admin_password')
        initial_movements = Movement.objects.count()
        wallball = Movement.objects.get(name='wallball')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        weight = MovementSettings.objects.get(name=MovementSettings.WEIGHT)
        data = {
            "id": wallball.pk,
            "name": "heavy wallball",
            "founder": wallball.founder.pk,
            "equipment": wallball.equipment.pk,
            "settings": [rep.pk, weight.pk]
        }
        url = reverse('movement_detail', kwargs={'pk': wallball.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movement.objects.count(), initial_movements - 1)

    def test_non_admin_get_all_movements(self):
        """
        Test if, when we are logged with a non admin account, the API returns:
            - a 200 status on this request
            - all the movements
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        movements = Movement.objects.count()
        url = reverse('movements_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), movements)
    
    def test_non_admin_get_one_movement(self):
        """
        Test if, when we are logged with a non admin account, the API returns:
            - a 200 status on this request
            - get the adequate movement
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        squat = Movement.objects.get(name='squat')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        weight = MovementSettings.objects.get(name=MovementSettings.WEIGHT)
        url = reverse('movement_detail', kwargs={'pk': squat.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        movement_response = {
            'id': squat.pk,
            'name': squat.name,
            'equipment': squat.equipment.pk,
            'founder': squat.founder.pk,
            'settings': [rep.pk, weight.pk]
        }
        self.assertEqual(response.data, movement_response)

    def test_non_admin_create_one_movement(self):
        """
        Test if, when we are logged with a non admin account, the API does not
        the movement
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        founder = User.objects.get(username='ordinary_user')
        no_equipment = Equipment.objects.get(name='aucun')
        rep = MovementSettings.objects.get(name='repetitions')
        initial_movements = Movement.objects.count()
        url = reverse('movements_list')
        data = {
            'name': 'burpees',
            'founder': founder.pk,
            'equipment': no_equipment.pk,
            'settings': [
                rep.pk
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Movement.objects.count(), initial_movements)

    def test_non_admin_update_one_movement(self):
        """
        Test if, when we are logged with a non admin account, the API does not allow
        the update of a movement
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        wallball = Movement.objects.get(name='wallball')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        weight = MovementSettings.objects.get(name=MovementSettings.WEIGHT)

        url = reverse('movement_detail', kwargs={'pk': wallball.pk})
        data = {
            "id": wallball.pk,
            "name": "heavy wallball",
            "founder": wallball.founder.pk,
            "equipment": wallball.equipment.pk,
            "settings": [rep.pk, weight.pk]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_delete_one_movement(self):
        """
        Test if, when we are logged with a non admin account, the API does not allow 
        the deleting of a movement
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        initial_movements = Movement.objects.count()
        wallball = Movement.objects.get(name='wallball')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        weight = MovementSettings.objects.get(name=MovementSettings.WEIGHT)
        data = {
            "id": wallball.pk,
            "name": "heavy wallball",
            "founder": wallball.founder.pk,
            "equipment": wallball.equipment.pk,
            "settings": [rep.pk, weight.pk]
        }
        url = reverse('movement_detail', kwargs={'pk': wallball.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Movement.objects.count(), initial_movements)