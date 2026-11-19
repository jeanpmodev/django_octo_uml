<p align="center">
  <img src="https://raw.githubusercontent.com/jeanpmodev/jeanpmodev/main/assets/django-octo-uml.jpg" alt="Django-Octo-SEO" width="100%" />
</p>

# Django-Octo UML

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![Framework: Django](https://img.shields.io/badge/Framework-Django-darkgreen)](https://djangoproject.com)
[![Package Manager: Rye](https://img.shields.io/badge/Package_Manager-Rye-orange)](https://astral.sh)
![PyPI Version](https://img.shields.io/pypi/v/django_octo_uml)
[![Latest on Django Packages](https://img.shields.io/badge/Django_Packages-django__octo__uml-8c3c26.svg)](https://djangopackages.org/packages/p/django_octo_uml/)
[![Tests: pytest](https://img.shields.io/badge/Tests-pytest%20passed-2ea44f.svg)](https://github.com/jeanpmodev/django_octo_uml/blob/main/TESTING.md)
[![BDD: Behave](https://img.shields.io/badge/BDD-Behave%20verified-009688.svg)](https://github.com/jeanpmodev/django_octo_uml/blob/main/TESTING.md)
[![Load Test: Locust](https://img.shields.io/badge/Load_Test-11ms_median_%7C_0%25_fails-blueviolet.svg)](https://github.com/jeanpmodev/django_octo_uml/blob/main/performance/locust_load_report.pdf)
[![CI](https://img.shields.io/github/actions/workflow/status/jeanpmodev/django_octo_uml/ci.yml?branch=main&label=CI)](https://github.com/jeanpmodev/django_octo_uml/actions/workflows/ci.yml)
[![Code Style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-blue)](https://peps.python.org/pep-0008/)
[![PyPI Provenance](https://img.shields.io/badge/PyPI-With%20Provenance-blue?logo=pypi&logoColor=white)](https://pypi.org/project/django-octo-uml/#provenance)
[![Snyk Vulnerabilities](https://img.shields.io/badge/Snyk%20Vulnerabilities-0%20known-brightgreen?logo=snyk&logoColor=white)](https://uml.snyk.io/package/pip/django-octo-uml)
[![security Audit](https://github.com/jeanpmodev/django_octo_uml/actions/workflows/security.yml/badge.svg)](https://github.com/jeanpmodev/django_octo_uml/actions/workflows/uml.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/jeanpmodev/django_octo_uml/badge)](https://scorecard.dev/viewer/?uri=github.com/jeanpmodev/django_octo_uml)
[![Socket Badge](https://badge.socket.dev/pypi/package/django-octo-uml/0.1.0?artifact_id=tar-gz)](https://badge.socket.dev/pypi/package/django-octo-uml/0.1.0?artifact_id=tar-gz)
[![codecov](https://codecov.io/github/jeanpmodev/django_octo_uml/graph/badge.svg?token=YUOBIXZE9A)](https://codecov.io/github/jeanpmodev/django_octo_uml)
[![Documentation Status](https://readthedocs.org/projects/django-octo/badge/?version=latest)](https://django-octo.readthedocs.io/en/latest/uml/)

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
