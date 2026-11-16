import shutil
import subprocess
from io import StringIO
from pathlib import Path
import django_extensions
from django.apps import apps
from django.core.management import call_command
from django.template import engines
from django_extensions.management.commands.graph_models import Command as GraphModelsCommand
from django_extensions.templatetags import indent_text
from .models import UmlSnapshot

DJANGO_CORE_APPS = {
    "admin",
    "auth",
    "contenttypes",
    "sessions",
    "messages",
    "staticfiles",
}


def _ensure_extensions_templates_registered() -> None:
    """Registers django_extensions template directory and tag libraries without requiring INSTALLED_APPS changes."""
    ext_templates = Path(django_extensions.__file__).resolve().parent / "templates"
    for engine in engines.all():
        if hasattr(engine, "engine"):
            if ext_templates not in engine.engine.dirs:
                engine.engine.dirs = list(engine.engine.dirs) + [ext_templates]
            if "indent_text" not in engine.engine.template_libraries:
                engine.engine.template_libraries["indent_text"] = indent_text.register


def get_available_apps(include_contrib: bool = False) -> list[str]:
    """Returns app labels containing at least one managed Django model."""
    labels = []
    for app_config in apps.get_app_configs():
        if not include_contrib and app_config.label in DJANGO_CORE_APPS:
            continue
        real_models = [m for m in app_config.get_models() if m._meta.managed]
        if real_models:
            labels.append(app_config.label)
    return labels


def count_managed_models(app_labels: list[str]) -> int:
    """Counts total managed models across the given app labels."""
    total = 0
    for label in app_labels:
        app_config = apps.get_app_config(label)
        total += len([m for m in app_config.get_models() if m._meta.managed])
    return total


def build_uml_dot(
    include_contrib: bool = False,
    selected_apps: list[str] | None = None,
) -> str:
    """Generates a Graphviz DOT string representing the project's models."""
    _ensure_extensions_templates_registered()
    target_apps = selected_apps or get_available_apps(include_contrib=include_contrib)

    if not target_apps:
        return 'digraph model_graph { label="No managed models found"; }'

    out = StringIO()
    call_command(
        GraphModelsCommand(),
        *target_apps,
        group_models=True,
        dot=True,
        stdout=out,
    )
    return out.getvalue()


def render_dot_to_svg(dot_source: str) -> str | None:
    """Compiles a Graphviz DOT string into an SVG markup string using the system dot binary."""
    dot_bin = shutil.which("dot")
    if not dot_bin:
        return None
    result = subprocess.run(
        [dot_bin, "-Tsvg"],
        input=dot_source,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


def create_uml_snapshot(include_contrib: bool = False) -> UmlSnapshot:
    """Generates a new UML diagram and archives it as a persistent snapshot."""
    target_apps = get_available_apps(include_contrib=include_contrib)
    dot_source = build_uml_dot(include_contrib=include_contrib, selected_apps=target_apps)
    return UmlSnapshot.objects.create(
        include_contrib=include_contrib,
        apps_count=len(target_apps),
        models_count=count_managed_models(target_apps),
        dot_source=dot_source,
    )
