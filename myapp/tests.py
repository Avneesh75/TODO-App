import json
import pytest
from django.test import Client
from myapp.models import Task


@pytest.mark.django_db
class TestTaskCRUD:

    def setup_method(self):
        self.client = Client()


    def test_create_task(self):
        response = self.client.post(
            "/api/",
            data={
                "title": "Test Task",
                "description": "Test Description",
                "status": "pending"
            }
        )

        assert response.status_code == 201
        assert Task.objects.count() == 1
        assert Task.objects.first().title == "Test Task"

 
    def test_list_tasks(self):
        Task.objects.create(
            title="Task 1",
            status="pending"
        )

        response = self.client.get("/api/tasks/")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Task 1"


    def test_get_task_detail(self):
        task = Task.objects.create(
            title="Single Task",
            status="pending"
        )

        response = self.client.get(f"/api/tasks/{task.id}/")
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Single Task"


    def test_update_task(self):
        task = Task.objects.create(
            title="Old Title",
            status="pending"
        )

        response = self.client.post(
            f"/api/tasks/{task.id}/update/",
            data={
                "title": "Updated Title",
                "status": "completed"
            }
        )

        assert response.status_code == 200

        task.refresh_from_db()
        assert task.title == "Updated Title"
        assert task.status == "completed"


    def test_delete_task(self):
        task = Task.objects.create(
            title="Delete Me",
            status="pending"
        )

        response = self.client.post(f"/api/tasks/{task.id}/delete/")
        assert response.status_code == 204
        assert Task.objects.count() == 0
