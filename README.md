# Django-Octo UML

**Interactive runtime Django entity-relationship and UML architecture visualizer under the Django-Octo ecosystem.**

`django-octo-uml` inspects your active Django models at runtime, renders interactive SVG diagrams inside Django Admin, and archives timestamped snapshots so you can track your data model evolution over time.

## Requirements

- Python >= 3.12
- Django >= 6.0
- System Graphviz (`dot` binary) for SVG/PNG rendering (`sudo apt install graphviz` or `brew install graphviz`)

## Installation

```bash
pip install django-octo-uml
```

## Quick Start

1. Add `django_octo_uml` to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    "django.contrib.admin",
    "django_octo_uml",
]
```

2. Run migrations to create the snapshot history table:

```bash
python manage.py migrate django_octo_uml
```

3. Open **Admin -> UML -> UML Architecture** to generate snapshots, browse architecture history, and export `.dot`, `.svg`, or `.png` files.

## License

MIT License.
