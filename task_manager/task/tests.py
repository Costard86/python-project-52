from django.test import TestCase, Client
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from task_manager.status.models import Status
from .models import Task


class TaskCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        user_data = {
            'user1': {
                'username': 'tota',
                'first_name': 'Tota',
                'last_name': 'Totavich',
                'password': 'adminadmin',
            },
            'user2': {
                'username': 'dada',
                'first_name': 'Dada',
                'last_name': 'Dadavich',
                'password': 'adminadmin',
            },
        }

        cls.author = User.objects.create_user(**user_data['user1'])
        cls.executor = User.objects.create_user(**user_data['user2'])

        status_data = {
            'create': {'name': 'Example status'},
            'update': {'name': 'Updated status'},
        }
        cls.status_original = Status.objects.create(**status_data['create'])
        cls.status_updated = Status.objects.create(**status_data['update'])

        cls.orm_user_create_data = {
            'name': 'Example task',
            'description': 'This is example task',
            'status': cls.status_original,
            'executor': cls.author,
            'author': cls.author,
        }
        cls.data = {
            'create': {
                'name': 'Example task',
                'description': 'This is example task',
                'status': cls.status_original.pk,
                'executor': cls.author.pk,
            },
            'update': {
                'name': 'Updated task',
                'description': 'This is updated task',
                'status': cls.status_updated.pk,
                'executor': cls.executor.pk,
            },
        }

    def setUp(self):
        self.client = Client()
        self.client.force_login(
            user=self.author
        )

    def test_create_task(self):
        url = reverse('task_create')
        task_data = self.data['create']
        self.client.post(url, task_data)

        task = Task.objects.last()
        self.assertEqual(task.name, task_data['name'])
        self.assertEqual(task.description, task_data['description'])
        self.assertEqual(task.status_id, self.status_original.pk)

    def test_read_tasks_index(self):
        url = reverse('tasks_index')
        task_data = self.orm_user_create_data
        task = Task.objects.create(**task_data)

        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn(task.name, content)
        self.assertIn(task.status.name, content)

    def test_update_task(self):
        task_data = self.orm_user_create_data
        task = Task.objects.create(**task_data)
        url = reverse('task_update', kwargs={'pk': task.pk})

        task_updated_data = self.data['update']
        self.client.post(url, task_updated_data)

        task_updated = Task.objects.get(pk=task.pk)
        self.assertEqual(task_updated.name, task_updated_data['name'])
        self.assertEqual(
            task_updated.description, task_updated_data['description']
        )

    def test_delete_task(self):
        task_data = self.orm_user_create_data
        task = Task.objects.create(**task_data)
        url = reverse('task_delete', kwargs={'pk': task.pk})

        self.client.post(url)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=task.pk)
