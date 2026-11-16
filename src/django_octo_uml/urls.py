from django.urls import path
from .views import uml_dashboard_view

app_name = "django_octo_uml"

urlpatterns = [
    path("octo/uml/", uml_dashboard_view, name="dashboard"),
]
