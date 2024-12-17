from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Task, Tag

class TaskAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and login
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
        """Test retrieving the list of tasks."""
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Task", str(response.data))

    def test_create_task(self):
        """Test creating a new task."""
        data = {
            "title": "New Task",
            "description": "New Description",
            "status": "WORKING",
        }
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)  # Verify a new task is created

    def test_create_task_with_tags(self):
        """Test creating a task with multiple tags."""
        # Create tags first
        tag1 = Tag.objects.create(name="Urgent")
        tag2 = Tag.objects.create(name="Home")

        data = {
            "title": "Tagged Task",
            "description": "Task with tags",
            "status": "PENDING_REVIEW",
            "tags": [tag1.id, tag2.id],
        }

        response = self.client.post("/api/tasks/", data)
        
        # Ensure the task and tags are created successfully
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)  # Only 1 task should be created
        self.assertEqual(Tag.objects.count(), 2)  # Both tags should exist

    def test_task_detail(self):
        """Test retrieving a single task's details."""
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Test Task")

    def test_update_task(self):
        """Test updating an existing task."""
        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "COMPLETED",
        }
        response = self.client.put(f"/api/tasks/{self.task.id}/", data)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()  # Refresh the task to get the updated values
        self.assertEqual(self.task.title, "Updated Task")
        self.assertEqual(self.task.status, "COMPLETED")

    def test_delete_task(self):
        """Test deleting a task."""
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 0)  # Verify the task is deleted

    def test_permission_denied_for_unauthenticated_user(self):
        """Test that unauthenticated users can't access task endpoints."""
        self.client.logout()  # Log out the test user
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 403)  # Permission denied


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

