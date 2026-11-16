import os
from locust import HttpUser, between, task


class UmlDashboardUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Authenticates against Django Admin before running load tasks."""
        username = os.getenv("OCTO_LOAD_USER", "admin")
        password = os.getenv("OCTO_LOAD_PASS", "admin")

        login_url = "/admin/login/"
        response = self.client.get(login_url)
        csrf_token = response.cookies.get("csrftoken", "")

        self.client.post(
            login_url,
            data={
                "username": username,
                "password": password,
                "csrfmiddlewaretoken": csrf_token,
                "next": "/admin/django_octo_uml/umlsnapshot/",
            },
            headers={"Referer": f"{self.host}{login_url}"},
        )

    @task(3)
    def load_uml_dashboard_archived(self):
        """Simulates fast read access to the latest archived UML snapshot."""
        self.client.get(
            "/admin/django_octo_uml/umlsnapshot/",
            name="/admin/django_octo_uml/umlsnapshot/ (archived)",
        )

    @task(1)
    def download_uml_dot(self):
        """Simulates downloading the raw DOT file from the active snapshot."""
        self.client.get(
            "/admin/django_octo_uml/umlsnapshot/?download=dot",
            name="/admin/django_octo_uml/umlsnapshot/?download=dot",
        )
