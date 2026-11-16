from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import UmlSnapshot
from .services import create_uml_snapshot, render_dot_to_svg


@staff_member_required
def uml_dashboard_view(request):
    """Standalone view rendering the latest archived UML snapshot and history."""
    if request.method == "POST" and "generate_uml" in request.POST:
        include_contrib = request.POST.get("include_contrib") == "true"
        snapshot = create_uml_snapshot(include_contrib=include_contrib)
        return redirect(f"{request.path}?snapshot={snapshot.id}")

    snapshot_id = request.GET.get("snapshot")
    active_snapshot = (
        UmlSnapshot.objects.filter(pk=snapshot_id).first()
        if snapshot_id
        else UmlSnapshot.objects.first()
    )
    if active_snapshot is None:
        active_snapshot = create_uml_snapshot(include_contrib=False)

    if request.GET.get("download") == "dot":
        response = HttpResponse(active_snapshot.dot_source, content_type="text/vnd.graphviz")
        response["Content-Disposition"] = (
            f'attachment; filename="django_octo_uml_{active_snapshot.id}.dot"'
        )
        return response

    context = {
        "title": "UML Entity Architecture",
        "active_snapshot": active_snapshot,
        "svg_markup": render_dot_to_svg(active_snapshot.dot_source),
        "history": UmlSnapshot.objects.only(
            "id", "created_at", "include_contrib", "apps_count", "models_count"
        )[:20],
    }
    return render(request, "admin/django_octo_uml/uml_dashboard.html", context)
