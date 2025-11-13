import uuid

from locust import HttpUser, between, task


class MicroserviceUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Called when a user starts"""
        self.client.get("/health")

    @task(3)
    def list_items(self):
        """List all items - most common operation"""
        self.client.get("/api/v1/items")

    @task(1)
    def create_item(self):
        """Create new item"""
        self.client.post(
            "/api/v1/items",
            json={
                "name": f"Load Test Item {uuid.uuid4()}",
                "description": "Created during load test",
            },
        )

    @task(2)
    def get_item(self):
        """Get specific item"""
        self.client.get("/api/v1/items/1")

    @task(1)
    def slow_endpoint(self):
        """Test slow endpoint"""
        self.client.get("/api/v1/slow")
