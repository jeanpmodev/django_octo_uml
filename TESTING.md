#  Quality Assurance & Testing Methodology

[![Tests: pytest](https://img.shields.io/badge/Tests-pytest%20passed-2ea44f.svg)](#2-unit--query-count-validation-pytest)
[![BDD: Behave](https://img.shields.io/badge/BDD-Behave%20verified-009688.svg)](#3-behavioral--bdd-specifications-behave)
[![Load Test: Locust](https://img.shields.io/badge/Load_Test-11ms_median_%7C_0%25_fails-blueviolet.svg)](performance/locust_load_report.pdf)

---

## 1. On-Demand QA Setup
Inside an isolated virtual environment, install the validation stack:
```bash
rye add pytest pytest-django behave locust
```

---

## 2. Unit & Query-Count Validation (`pytest`)
Verifies schema migrations, OSV API vulnerability batch parsing, advisory enrichment, and enforces the **Single Database Lookup (`assertNumQueries(1)`)** contract on `/security-audit/`:
```bash
PYTHONPATH=src rye run pytest
```

---

## 3. Behavioral / BDD Specifications (`behave`)
Executes Gherkin scenarios (`features/security_audit.feature`) validating the runtime posture endpoint and CVE environment audit scanner end-to-end:
```bash
PYTHONPATH=src rye run behave
```

---

## 4. Load & Concurrency Stress Benchmark (`locust`)
Simulates concurrent requests hitting the live `/security-audit/` posture endpoint to verify zero-error stability under load:

```bash
# Terminal 1: Start runtime service
rye run python3 manage.py runserver --noreload

# Terminal 2: Execute headless load benchmark
rye run locust -f performance/locustfile.py --headless -u 20 -r 5 -t 10s --host http://127.0.0.1:8000
```

### Benchmark Summary
* **Failure Rate:** `0.00%` (HTTP 200 OK across all posture audit requests)
* **Query Overhead:** Strict `1 query` per request (`CveAuditScan.objects.first()`)
* **Detailed Metrics:** Available in the exported report below.

 **[View Official Locust Load Test Report (PDF)](performance/locust_load_report.pdf)**

