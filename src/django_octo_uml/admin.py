from django.contrib import admin, messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from .models import UmlSnapshot
from .services import create_uml_snapshot, render_dot_to_svg


@admin.register(UmlSnapshot)
class UmlSnapshotAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "include_contrib", "apps_count", "models_count")
    readonly_fields = ("created_at", "include_contrib", "apps_count", "models_count", "dot_source")

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        if request.method == "POST":
            if "generate_uml" in request.POST:
                include_contrib = request.POST.get("include_contrib") == "true"
                snapshot = create_uml_snapshot(include_contrib=include_contrib)
                self.message_user(
                    request,
                    f"New UML snapshot #{snapshot.id} generated successfully.",
                    level=messages.SUCCESS,
                )
                return redirect(f"{request.path}?snapshot={snapshot.id}")

            if "delete_snapshot" in request.POST:
                target_id = request.POST.get("delete_snapshot")
                deleted_count, _ = UmlSnapshot.objects.filter(pk=target_id).delete()
                if deleted_count:
                    self.message_user(
                        request,
                        f"UML snapshot #{target_id} deleted.",
                        level=messages.WARNING,
                    )
                return redirect(request.path)

        snapshot_id = request.GET.get("snapshot")
        if snapshot_id:
            active_snapshot = UmlSnapshot.objects.filter(pk=snapshot_id).first()
        else:
            active_snapshot = UmlSnapshot.objects.first()

        if active_snapshot is None:
            active_snapshot = create_uml_snapshot(include_contrib=False)

        if request.GET.get("download") == "dot":
            response = HttpResponse(active_snapshot.dot_source, content_type="text/vnd.graphviz")
            response["Content-Disposition"] = (
                f'attachment; filename="django_octo_uml_{active_snapshot.id}.dot"'
            )
            return response

        svg_markup = render_dot_to_svg(active_snapshot.dot_source)
        history = UmlSnapshot.objects.only(
            "id", "created_at", "include_contrib", "apps_count", "models_count"
        )[:50]

        context = {
            **self.admin_site.each_context(request),
            "title": "UML Entity Architecture",
            "active_snapshot": active_snapshot,
            "svg_markup": svg_markup,
            "history": history,
            **(extra_context or {}),
        }
        return TemplateResponse(
            request,
            "admin/django_octo_uml/uml_dashboard.html",
            context,
        )
