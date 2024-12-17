from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Task, Tag


class TaskAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # Create a test task
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="OPEN",
            created_by=self.user,
        )

    def test_task_list(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Task", str(response.data))

    def test_create_task(self):
        data = {
            "title": "New Task",
            "description": "New Description",
            "status": "WORKING",
        }
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)


    def test_create_task_with_tags(self):
        # Create the tags first
        tag1 = Tag.objects.create(name="Urgent")
        tag2 = Tag.objects.create(name="Home")
        
        data = {
            "title": "Tagged Task",
            "description": "Task with tags",
            "status": "PENDING_REVIEW",
            "tags": [tag1.id, tag2.id],  # Use the IDs of the tags created
        }
        
        response = self.client.post("/api/tasks/", data)
        
        # Ensure the task and tags are created successfully
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)  # Only 1 task should be created
        self.assertEqual(Tag.objects.count(), 2)  # Both tags should exist

    def test_task_detail(self):
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Test Task")

    def test_update_task(self):
        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "COMPLETED",
        }
        response = self.client.put(f"/api/tasks/{self.task.id}/", data)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
        self.assertEqual(self.task.status, "COMPLETED")


    def test_delete_task(self):
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 0)

    def test_permission_denied_for_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 403)  # Permission denied
