from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import List, Task, SubTask
from .views import CreateTaskView, DeleteTaskView, ToDoListView, UpdateTaskView, CreateSubTaskView, DeleteSubTaskView, UpdateSubTaskView
from django.contrib.auth.models import User

# Create your tests here.

class ListTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'test@test.com', 'test1234')

    def test_profile_exists(self):
        exists = List.objects.filter(user__username='test').exists() 
        self.assertEqual(exists, True)

class ViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="jacob", email="jacob@…", password="top_secret")
        self.task = Task.objects.create(title="diablos", list=self.user.list)
        self.sub_task = SubTask.objects.create(title="sub-diablos", task=self.task)
    
    def test_create_view(self):
        request = self.factory.post("/list/jacob/create", {"title": "cruzar el puente"})
        request.user = self.user
        view = CreateTaskView()
        view.setup(request)
        CreateTaskView.as_view()(request)
        task = Task.objects.filter(title='cruzar el puente').exists()
        self.assertEqual(task, True)

    def test_reverse_route_create_view(self):
        self.client.login(username="jacob", password="top_secret")
        response = self.client.get(reverse('create', args=["jacob"]))
        self.assertEqual(response.status_code, 200)

    def test_delete_view(self):
        request = self.factory.post("/list/jacob/create", {"title": "deslizarse con mamanda"})
        request.user = self.user
        view = CreateTaskView()
        view.setup(request)
        view.dispatch(request)
        request = self.factory.post("/list/jacob/1/delete")
        request.user = self.user
        view = DeleteTaskView()
        view.setup(request)
        DeleteTaskView.as_view()(request, **{'pk': 2})
        task = Task.objects.filter(title='deslizarse con mamanda').exists()
        self.assertEqual(task, False)

    def test_reverse_route_delete_view(self):
        self.client.login(username="jacob", password="top_secret")
        response = self.client.get(reverse('delete', args=[self.user.username, self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_list_view_get_queryset(self):
        request = self.factory.get("/list/jacob/")
        request.user = self.user
        expected_list_id = List.objects.filter(title=f"lista de {request.user.get_username()}").first().id
        view = ToDoListView()
        view.setup(request)
        #ToDoListView.as_view()(request)
        tasks_list = view.get_queryset()
        for task in tasks_list:
            self.assertEqual(task.list_id, expected_list_id)

    def test_reverse_route_list_view(self):
        self.client.login(username="jacob", password="top_secret")
        response = self.client.get(reverse('lista', args=["jacob"]))
        self.assertEqual(response.status_code, 200)

    def test_update_view(self):
        request = self.factory.post("/list/jacob/1/update", {"is_completed": True})
        request.user = self.user
        view = UpdateTaskView()
        view.setup(request)
        UpdateTaskView.as_view()(request, **{'pk': 1})
        self.task.refresh_from_db()
        self.assertEqual(self.task.is_completed, True)

    def test_reverse_route_update_view(self):
        self.client.login(username="jacob", password="top_secret")
        response = self.client.get(reverse('update', args=[self.user.username, self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_create_subtask_view(self):
        request = self.factory.post("/list/jacob/1/create-subtask", {"title": "cruzar el puente"})
        request.user = self.user
        view = CreateSubTaskView()
        view.setup(request)
        CreateSubTaskView.as_view()(request, **{'task_pk': 1})
        task = SubTask.objects.filter(title='cruzar el puente').exists()
        self.assertEqual(task, True)

    def test_reverse_route_create_subtask_view(self):
        self.client.login(username="jacob", password="top_secret")
        response = self.client.get(reverse('sub-create', args=["jacob", self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_subtask_view(self):
        request = self.factory.post("/list/jacob/1/create-subtask", {"title": "deslizarse con mamanda"})
        request.user = self.user
        view = CreateSubTaskView()
        view.setup(request)
        CreateSubTaskView.as_view()(request, **{'task_pk': 1})
        request = self.factory.post("/list/jacob/1/delete-subtask/1")
        request.user = self.user
        view = DeleteSubTaskView()
        view.setup(request)
        DeleteSubTaskView.as_view()(request, **{'pk': 2, 'task_pk': 1})
        task = SubTask.objects.filter(title='deslizarse con mamanda').exists()
        self.assertEqual(task, False)

    def test_reverse_route_delete_subtask_view(self):
        self.client.login(username="jacob", password="top_secret")
        response = self.client.get(reverse('sub-delete', args=[self.user.username, self.task.pk, self.sub_task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_subtask_view(self):
        request = self.factory.post("/list/jacob/1/sub-update/1", {"is_completed": True})
        request.user = self.user
        view = UpdateSubTaskView()
        view.setup(request)
        UpdateSubTaskView.as_view()(request, **{'pk': 1, 'task_pk': 1})
        self.sub_task.refresh_from_db()
        self.assertEqual(self.sub_task.is_completed, True)

    def test_reverse_route_update_subtask_view(self):
        self.client.login(username="jacob", password="top_secret")
        response = self.client.get(reverse('sub-update', args=[self.user.username, self.task.pk, self.sub_task.pk]))
        self.assertEqual(response.status_code, 200)
