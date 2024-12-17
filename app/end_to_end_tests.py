from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Task, Tag


class TaskE2ETests(APITestCase):

    def setUp(self):
        """Setup a user and tasks for E2E test flow."""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="OPEN",
            created_by=self.user,
        )

    def test_end_to_end_task_flow(self):
        """Test the full CRUD flow from create -> retrieve -> update -> delete"""

        # Step 1: Create a task
        create_data = {
            "title": "End to End Task",
            "description": "End to end description",
            "status": "WORKING",
        }
        response = self.client.post("/api/tasks/", create_data)
        self.assertEqual(response.status_code, 201)
        task_id = response.data["id"]

        # Step 2: Retrieve the created task
        response = self.client.get(f"/api/tasks/{task_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "End to End Task")

        # Step 3: Update the task
        update_data = {
            "title": "Updated End to End Task",
            "description": "Updated description",
            "status": "COMPLETED",
        }
        response = self.client.put(f"/api/tasks/{task_id}/", update_data)
        self.assertEqual(response.status_code, 200)

        # Verify the updated task
        response = self.client.get(f"/api/tasks/{task_id}/")
        self.assertEqual(response.data["title"], "Updated End to End Task")
        self.assertEqual(response.data["status"], "COMPLETED")

        # Step 4: Delete the task
        response = self.client.delete(f"/api/tasks/{task_id}/")
        self.assertEqual(response.status_code, 204)

        # Verify the task is deleted
        response = self.client.get(f"/api/tasks/{task_id}/")
        self.assertEqual(response.status_code, 404)
