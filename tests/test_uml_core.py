import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django_octo_uml.models import UmlSnapshot
from django_octo_uml.services import build_uml_dot, create_uml_snapshot, get_available_apps


@pytest.mark.django_db
def test_get_available_apps_excludes_core_by_default():
    apps_default = get_available_apps(include_contrib=False)
    assert "auth" not in apps_default
    assert "django_octo_uml" in apps_default


@pytest.mark.django_db
def test_build_uml_dot_generates_valid_graphviz_syntax():
    dot_output = build_uml_dot(include_contrib=True)
    assert "digraph model_graph" in dot_output
    assert "UmlSnapshot" in dot_output


@pytest.mark.django_db
def test_create_uml_snapshot_persists_history():
    snapshot = create_uml_snapshot(include_contrib=False)
    assert UmlSnapshot.objects.count() == 1
    assert snapshot.models_count >= 1
    assert "UmlSnapshot" in snapshot.dot_source


@pytest.mark.django_db
def test_admin_uml_dashboard_renders_for_superuser(client):
    admin_user = User.objects.create_superuser(
        username="octoadmin",
        email="admin@octo.dev",
        password="strongpassword123",
    )
    client.force_login(admin_user)

    url = reverse("admin:django_octo_uml_umlsnapshot_changelist")
    response = client.get(url)

    assert response.status_code == 200
    assert b"UmlSnapshot" in response.content


@pytest.mark.django_db
def test_admin_uml_dot_download_endpoint(client):
    admin_user = User.objects.create_superuser(
        username="octoadmin",
        email="admin@octo.dev",
        password="strongpassword123",
    )
    client.force_login(admin_user)
    snapshot = create_uml_snapshot(include_contrib=True)

    url = reverse("admin:django_octo_uml_umlsnapshot_changelist")
    response = client.get(f"{url}?snapshot={snapshot.id}&download=dot")

    assert response.status_code == 200
    assert response["Content-Type"] == "text/vnd.graphviz"
    assert f"django_octo_uml_{snapshot.id}.dot" in response["Content-Disposition"]
