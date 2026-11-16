from behave import given, then, when
from django.contrib.auth.models import User
from django.urls import reverse


@given("an authenticated superuser exists")
def step_create_and_login_superuser(context):
    user = User.objects.create_superuser(
        username="bdd_admin",
        email="bdd@octo.dev",
        password="bddpassword123",
    )
    context.test.client.force_login(user)
    context.uml_url = reverse("admin:django_octo_uml_umlsnapshot_changelist")


@when("the user navigates to the UML Entity Diagram dashboard")
def step_visit_uml_dashboard(context):
    context.response = context.test.client.get(context.uml_url)


@when("the user navigates to the UML Entity Diagram dashboard with core apps enabled")
def step_visit_uml_dashboard_with_contrib(context):
    context.response = context.test.client.post(
        context.uml_url,
        data={"generate_uml": "1", "include_contrib": "true"},
        follow=True,
    )


@when("the user requests the DOT file download")
def step_download_dot_file(context):
    context.response = context.test.client.get(f"{context.uml_url}?download=dot")


@then("the response status code should be {status_code:d}")
def step_verify_status_code(context, status_code):
    assert context.response.status_code == status_code


@then("the page should contain a valid Graphviz DOT payload")
def step_verify_dot_payload_in_html(context):
    body = context.response.content.decode("utf-8")
    snapshot = context.response.context["active_snapshot"]
    assert "digraph model_graph" in snapshot.dot_source
    assert "<svg" in body or "uml-viewport" in body


@then("Django core auth models should be hidden by default")
def step_verify_core_apps_hidden(context):
    snapshot = context.response.context["active_snapshot"]
    assert "django_contrib_auth" not in snapshot.dot_source


@then('the DOT payload should include the "{model_name}" model')
def step_verify_model_in_dot(context, model_name):
    snapshot = context.response.context["active_snapshot"]
    assert model_name in snapshot.dot_source


@then('the response should return a downloadable ".dot" file')
def step_verify_dot_attachment(context):
    assert context.response.status_code == 200
    assert context.response["Content-Type"] == "text/vnd.graphviz"
    assert "django_octo_uml_" in context.response["Content-Disposition"]
