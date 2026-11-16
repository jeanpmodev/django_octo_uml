from django.db import models


class UmlSnapshot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Generated At")
    include_contrib = models.BooleanField(default=False, verbose_name="Include Core Apps")
    apps_count = models.PositiveIntegerField(default=0, verbose_name="Apps Count")
    models_count = models.PositiveIntegerField(default=0, verbose_name="Models Count")
    dot_source = models.TextField(verbose_name="Graphviz DOT Source")

    class Meta:
        app_label = "django_octo_uml"
        verbose_name = "UML Snapshot"
        verbose_name_plural = "UML Architecture"
        ordering = ["-created_at"]

    def __str__(self):
        scope = "Full (with Core)" if self.include_contrib else "Project Apps"
        return f"UML #{self.id} — {self.created_at:%Y-%m-%d %H:%M} ({scope})"
