# Traceability в TestRail + Coverage в Xray + SQL-аудит по всем 100 кейсам

## Состав

| # | Блок | Что внутри |
|---|---|---|
| 1 | TestRail: настройка полей | Custom fields для `RequirementID`, `LinkedIssue`, `AutomationStatus`, `AutomationScript` |
| 2 | TestRail: Traceability Report | Настройка + API + фильтры + экспорт |
| 3 | TestRail: Coverage Report | Requirement Coverage + Automation Coverage |
| 4 | Xray: настройка | Issue types, Test Coverage, Requirement Status |
| 5 | Xray: отчёты | Test Coverage by Requirement, Traceability, Test Runs |
| 6 | Xray: API/GraphQL | Запросы для автоматизации |
| 7 | SQL: схема | DDL для всех таблиц |
| 8 | SQL: 20 запросов | Coverage, orphans, flaky, effectiveness, impact, release gate и др. |
| 9 | SQL: дашборд | Сводные view + materialized views |
| 10 | CI/CD: интеграция | pytest-маркеры + скрипты + gate |

---

## ЧАСТЬ 1. TestRail — настройка custom fields

### 1.1. Создание полей

`Administration → Customizations → Add Field`:

| Поле | Тип | Label | System name | Значения |
|---|---|---|---|---|
| `custom_requirement_id` | String | RequirementID | `requirement_id` | — (свободный ввод) |
| `custom_linked_issue` | String | LinkedIssue | `linked_issue` | — |
| `custom_automation_status` | Dropdown | AutomationStatus | `automation_status` | Auto, Manual, ToDo, Skipped |
| `custom_automation_script` | String | AutomationScript | `automation_script` | — |
| `custom_environment` | String | Environment | `environment` | — |
| `custom_owner` | String | Owner | `owner` | — |
| `custom_sprint` | String | Sprint | `sprint` | — |
| `custom_bug_id` | String | BugID | `bug_id` | — |

### 1.2. Привязка к проекту

`Administration → Projects → <Bank/Exchange> → Edit → Custom Fields`:
- Включить все 8 полей для `Test Case`.
- `custom_requirement_id` и `custom_linked_issue` — **обязательные** (mandatory).
- `custom_automation_status` — default `Manual`.

### 1.3. Импорт значений

Используйте CSV из Части 1 предыдущей поставки — поля автоматически заполнятся при импорте.

---

## ЧАСТЬ 2. TestRail — Traceability Report

### 2.1. Встроенный отчёт

`Reports → Traceability` (для проекта):

**Настройка:**
1. **Source**: `Test Cases` → группировка по `custom_requirement_id`.
2. **Target**: `Tests` (runs) → фильтр `Status`.
3. **Columns**: `RequirementID`, `Title`, `Status`, `Last Run`, `Owner`, `Sprint`.
4. **Filter**: `custom_requirement_id` is not empty.
5. **Format**: HTML / Excel / CSV.

**Что получаете:**

| RequirementID | Всего кейсов | Passed | Failed | Untested | Покрытие |
|---|---|---|---|---|---|
| BRQ-ORDER-001 | 2 | 2 | 0 | 0 | 100% |
| BRQ-PORT-006 | 1 | 0 | 1 | 0 | 100% (failed) |
| BRQ-FUT-011 | 0 | 0 | 0 | 0 | **0% — пробел** |

### 2.2. API: генерация Traceability

```python
# scripts/testrail_traceability.py
import base64, requests, json

HOST = "https://YOUR.testrail.io"
USER, API_KEY = "user@bank.ru", "YOUR_API_KEY"
PROJECT_ID = 1

auth = base64.b64encode(f"{USER}:{API_KEY}".encode()).decode()
headers = {"Authorization": f"Basic {auth}"}

def get_cases():
    cases, offset = [], 0
    while True:
        r = requests.get(
            f"{HOST}/index.php?/api/v2/get_cases/{PROJECT_ID}",
            headers=headers,
            params={"limit": 250, "offset": offset})
        r.raise_for_status()
        batch = r.json()["cases"] if "cases" in r.json() else r.json()
        if not batch:
            break
        cases.extend(batch)
        offset += 250
    return cases

def build_traceability():
    cases = get_cases()
    by_req = {}
    for c in cases:
        req = c.get("custom_requirement_id") or "UNMAPPED"
        by_req.setdefault(req, []).append({
            "id": c["id"],
            "title": c["title"],
            "priority": c.get("priority_id"),
            "owner": c.get("custom_owner"),
            "sprint": c.get("custom_sprint"),
            "linked_issue": c.get("custom_linked_issue"),
            "automation": c.get("custom_automation_status"),
        })
    return by_req

if __name__ == "__main__":
    trace = build_traceability()
    with open("artifacts/traceability.json", "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)
    print(f"Requirements: {len(trace)}")
    for req, cases in sorted(trace.items()):
        print(f"  {req}: {len(cases)} cases")
```

### 2.3. Фильтры для быстрого поиска

**В TestRail UI (поиск):**
```
refs:BRQ-PORT-006                          # все тесты требования
refs:STORY-2604                            # все тесты истории
custom_automation_status:Manual            # только ручные
custom_automation_status:Auto AND refs:BRQ-SEC-*  # авто по безопасности
custom_sprint:SP-19                        # тесты спринта
```

**Через API (bulk):**
```python
def tests_by_requirement(req_id):
    return requests.get(
        f"{HOST}/index.php?/api/v2/get_cases/{PROJECT_ID}",
        headers=headers,
        params={"refs": req_id}).json()
```

---

## ЧАСТЬ 3. TestRail — Coverage Report

### 3.1. Requirement Coverage

`Reports → Coverage → Requirements`:

**Настройка:**
- **Source**: `custom_requirement_id`.
- **Metric**: `Covered` (≥1 тест) / `Uncovered` (0 тестов).
- **Threshold**: критичные BRQ (Priority=Critical) → 100% покрытие обязательно.

**Формула:**
```
Requirement Coverage = COUNT(BRQ с ≥1 тестом) / COUNT(все BRQ) × 100%
```

**Целевые значения по нашему набору:**

| Домен | BRQ | С тестами | Coverage | Target |
|---|---|---|---|---|
| ORDER | 16 | 16 | 100% | ✅ |
| PORT | 12 | 12 | 100% | ✅ |
| STOCK | 10 | 10 | 100% | ✅ |
| BOND | 10 | 10 | 100% | ✅ |
| FUT | 10 | 10 | 100% | ✅ |
| API | 6 | 6 | 100% | ✅ |
| SEC | 5 | 5 | 100% | ✅ |
| NFR | 5 | 5 | 100% | ✅ |
| UI/UX/L10N/COMP/REG | 26 | 26 | 100% | ✅ |
| **Итого** | **100** | **100** | **100%** | ✅ |

### 3.2. Automation Coverage

`Reports → Coverage → Automation`:

**Формула:**
```
Automation Coverage = COUNT(Auto) / COUNT(все тесты) × 100%
```

**Наш набор:**
```
Auto:   60 / 100 = 60%
Manual: 40 / 100 = 40%
```

**По доменам:**

| Домен | Auto | Manual | Auto % |
|---|---|---|---|
| API | 5 | 0 | 100% |
| SEC | 5 | 0 | 100% |
| PERF | 4 | 1 | 80% |
| FUNC | 20 | 15 | 57% |
| UI | 5 | 0 | 100% |
| STOCK | 4 | 6 | 40% |
| BOND | 3 | 7 | 30% |
| FUT | 2 | 8 | 20% |
| ORDER | 8 | 2 | 80% |
| PORT | 7 | 3 | 70% |

**Роадмап автоматизации:**
- Q1: 60% → 75% (добавить авто в STOCK/BOND/FUT).
- Q2: 75% → 80% (порог релиза).

### 3.3. Экспорт в CI

```bash
# scripts/coverage_report.py
import requests, base64, json, sys

HOST = "https://YOUR.testrail.io"
auth = base64.b64encode(b"user:key").decode()
headers = {"Authorization": f"Basic {auth}"}

def get_coverage(project_id):
    r = requests.get(
        f"{HOST}/index.php?/api/v2/get_coverage/{project_id}",
        headers=headers)
    return r.json()

if __name__ == "__main__":
    cov = get_coverage(1)
    json.dump(cov, open("artifacts/coverage.json", "w"), indent=2)
    if cov["requirement_coverage"] < 100:
        print(f"FAIL: coverage {cov['requirement_coverage']}%")
        sys.exit(1)
    print(f"OK: {cov['requirement_coverage']}%")
```

**В CI:**
```yaml
# .github/workflows/coverage-gate.yml
- name: TestRail Coverage Gate
  run: python scripts/coverage_report.py
  env:
    TR_USER: ${{ secrets.TR_USER }}
    TR_KEY: ${{ secrets.TR_KEY }}
```

---

## ЧАСТЬ 4. Xray — настройка

### 4.1. Issue Types

`Jira Administration → Issues → Issue Types`:

| Type | Назначение | Поля |
|---|---|---|
| `Requirement` | BRQ-* | `Requirement Status` (custom), `Priority`, `Sprint` |
| `Test` | TC-* | `Requirement` (link), `Test Type` (Manual/Automated), `Automation Script` |
| `Test Execution` | Прогон | `Test` (link), `Status`, `Environment` |
| `Test Plan` | Спринт/релиз | `Tests`, `Executions` |
| `Bug` | BUG-* | `Detected by Test` (link) |

### 4.2. Связи

`Jira Administration → Issues → Issue Linking`:

| Link type | From | To | Назначение |
|---|---|---|---|
| `tests` | Test | Requirement | Тест покрывает требование |
| `implements` | Test | Story | Тест относится к реализации |
| `detected by` | Bug | Test | Баг найден тестом |
| `covered by` | Requirement | Story | Требование реализовано историей |

### 4.3. Custom Fields

| Field | Type | Values | Где используется |
|---|---|---|---|
| `Requirement Status` | Select | `OK`, `NOK`, `UNKNOWN`, `UNCOVERED` | Авто-вычисляется из тестов |
| `Test Type` | Select | `Manual`, `Cucumber`, `Generic`, `Automated` | Классификация |
| `Automation Script` | URL | — | Ссылка на автотест |
| `Environment` | Multi-select | `Web`, `Mobile`, `Desktop`, `API` | Платформа |
| `Sprint` | Sprint | — | Стандартное поле Jira |

### 4.4. Настройка Requirement Status

`Xray Settings → Requirement Status`:
- Автоматически обновляется при прогоне тестов.
- `OK` — все связанные тесты Passed.
- `NOK` — ≥1 Failed.
- `UNCOVERED` — нет связанных тестов.
- `UNKNOWN` — не было прогонов.

---

## ЧАСТЬ 5. Xray — отчёты

### 5.1. Test Coverage by Requirement

`Xray → Reports → Test Coverage`:

**Настройка:**
- **Requirement**: все `BRQ-*` в проекте.
- **Test**: связанные через `tests`.
- **Execution**: последний Test Plan / Sprint.

**Результат:**

| Requirement | Status | Tests | Passed | Failed | Coverage % |
|---|---|---|---|---|---|
| BRQ-PORT-006 | NOK | TC-PORT-004 | 0 | 1 | 100% (failed) |
| BRQ-ORDER-001 | OK | TC-FUNC-001, TC-ORDER-001 | 2 | 0 | 100% |
| BRQ-FUT-011 | UNCOVERED | — | — | — | **0%** |

### 5.2. Traceability Report

`Xray → Reports → Traceability`:

**Настройка:**
- **Level**: Requirement → Story → Test → Execution.
- **Filter**: Sprint = SP-19 (текущий).

**Результат — дерево:**
```
BRQ-PORT-006 (стоп-аут <5с)
├── STORY-2604 (backend)
│   └── TC-PORT-004 (Failed) ← BUG-4521
├── STORY-2605 (UI уведомление)
│   └── TC-PORT-005 (Passed)
└── STORY-2606 (интеграция)
    └── TC-REG-005 (Passed)
```

### 5.3. Test Runs / Test Plans

`Xray → Test Plans → SP-19`:
- Все тесты спринта сгруппированы по `LinkedIssue`.
- Видно, какие истории покрыты, какие — нет.

**Метрика Sprint Coverage:**
```
Stories with tests = COUNT(STORY с ≥1 тестом) / COUNT(все STORY) × 100%
```

---

## ЧАСТЬ 6. Xray — API/GraphQL

### 6.1. REST API — Requirement Coverage

```bash
# Получить все требования с покрытием
curl -X GET "https://xray.cloud.getxray.app/api/v2/graphql" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ getTests(jql: \"issue in requirements()\") { results { issueId jira(fields: [\"key\"]) } } }"
  }'
```

### 6.2. GraphQL — Traceability Matrix

```graphql
query Traceability($projectKey: String!) {
  getRequirements(projectKey: $projectKey) {
    results {
      issueId
      jira(fields: ["key", "summary", "status"])
      tests {
        results {
          issueId
          jira(fields: ["key", "summary"])
          status
          lastRun
        }
      }
      stories {
        results {
          issueId
          jira(fields: ["key", "summary", "sprint"])
        }
      }
    }
  }
}
```

### 6.3. GraphQL — Coverage Summary

```graphql
query Coverage {
  getCoverage(projectKey: "BANK") {
    requirementCoverage
    testCoverage
    automationCoverage
    uncoveredRequirements { issueId jira(fields: ["key"]) }
  }
}
```

### 6.4. Python-клиент для CI

```python
# scripts/xray_coverage.py
import os, sys, requests

XRAY_URL = "https://xray.cloud.getxray.app/api/v2/graphql"
TOKEN = os.getenv("XRAY_TOKEN")

QUERY = """
query {
  getCoverage(projectKey: "BANK") {
    requirementCoverage
    automationCoverage
    uncoveredRequirements { jira(fields: ["key"]) }
  }
}
"""

def main():
    r = requests.post(
        XRAY_URL,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
        json={"query": QUERY})
    r.raise_for_status()
    data = r.json()["data"]["getCoverage"]
    print(f"Requirement coverage: {data['requirementCoverage']}%")
    print(f"Automation coverage:  {data['automationCoverage']}%")
    if data["uncoveredRequirements"]:
        print("Uncovered:")
        for u in data["uncoveredRequirements"]:
            print(f"  {u['jira']['key']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## ЧАСТЬ 7. SQL — схема

### 7.1. DDL

```sql
-- Требования
CREATE TABLE requirements (
    id            VARCHAR(32) PRIMARY KEY,        -- BRQ-ORDER-001
    domain        VARCHAR(32) NOT NULL,            -- ORDER
    title         TEXT NOT NULL,
    priority      VARCHAR(16) NOT NULL,            -- Critical/High/Medium/Low
    owner         VARCHAR(64),
    status        VARCHAR(16) DEFAULT 'Active',    -- Active/Deprecated
    created_at    TIMESTAMP DEFAULT now()
);

-- Истории реализации
CREATE TABLE stories (
    id            VARCHAR(32) PRIMARY KEY,        -- STORY-2604
    requirement_id VARCHAR(32) REFERENCES requirements(id),
    sprint        VARCHAR(16),
    assignee      VARCHAR(64),
    status        VARCHAR(16),                     -- ToDo/InProgress/Done
    created_at    TIMESTAMP DEFAULT now()
);

-- Тест-кейсы
CREATE TABLE test_cases (
    id              VARCHAR(32) PRIMARY KEY,      -- TC-PORT-004
    title           TEXT NOT NULL,
    type            VARCHAR(32),                   -- Functional/API/Security/...
    priority        VARCHAR(16),
    requirement_id  VARCHAR(32) REFERENCES requirements(id),
    linked_issue    VARCHAR(32) REFERENCES stories(id),
    automation_status VARCHAR(16),                 -- Auto/Manual
    automation_script TEXT,
    environment     VARCHAR(64),
    owner           VARCHAR(64),
    sprint          VARCHAR(16),
    created_at      TIMESTAMP DEFAULT now()
);

-- Прогоны
CREATE TABLE test_runs (
    id            BIGSERIAL PRIMARY KEY,
    test_id       VARCHAR(32) REFERENCES test_cases(id),
    execution_id  VARCHAR(32),                     -- TestRail run / Xray execution
    status        VARCHAR(16) NOT NULL,            -- Passed/Failed/Blocked/Skipped
    environment   VARCHAR(64),
    run_date      TIMESTAMP DEFAULT now(),
    duration_ms   INT,
    error_message TEXT
);

-- Баги
CREATE TABLE bugs (
    id            VARCHAR(32) PRIMARY KEY,         -- BUG-4521
    test_id       VARCHAR(32) REFERENCES test_cases(id),
    requirement_id VARCHAR(32) REFERENCES requirements(id),
    linked_issue  VARCHAR(32) REFERENCES stories(id),
    severity      VARCHAR(16),
    status        VARCHAR(16),                     -- Open/Fixed/Closed
    created_at    TIMESTAMP DEFAULT now()
);

-- Индексы
CREATE INDEX idx_tc_req     ON test_cases(requirement_id);
CREATE INDEX idx_tc_story   ON test_cases(linked_issue);
CREATE INDEX idx_tr_test    ON test_runs(test_id);
CREATE INDEX idx_tr_date    ON test_runs(run_date);
CREATE INDEX idx_bug_test   ON bugs(test_id);
CREATE INDEX idx_bug_req    ON bugs(requirement_id);
```

### 7.2. Заполнение из CSV

```python
# scripts/load_csv_to_db.py
import csv, psycopg2

def load(conn, csv_path):
    with open(csv_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cur = conn.cursor()
            # requirement
            cur.execute("""
                INSERT INTO requirements (id, domain, title, priority, owner)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (r["RequirementID"], r["RequirementID"].split("-")[1],
                  r["Title"], r["Priority"], r["Owner"]))
            # story
            cur.execute("""
                INSERT INTO stories (id, requirement_id, sprint, status)
                VALUES (%s, %s, %s, 'Done')
                ON CONFLICT (id) DO NOTHING
            """, (r["LinkedIssue"], r["RequirementID"], r["Sprint"]))
            # test case
            cur.execute("""
                INSERT INTO test_cases
                  (id, title, type, priority, requirement_id, linked_issue,
                   automation_status, automation_script, environment, owner, sprint)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (id) DO NOTHING
            """, (r["ID"], r["Title"], r["Type"], r["Priority"],
                  r["RequirementID"], r["LinkedIssue"],
                  r["AutomationStatus"], r["AutomationScript"],
                  r["Environment"], r["Owner"], r["Sprint"]))
            conn.commit()
    print("Loaded")

if __name__ == "__main__":
    conn = psycopg2.connect("dbname=qa user=qa password=qa host=localhost")
    load(conn, "cases_100.csv")
```

---

## ЧАСТЬ 8. SQL — 20 запросов для аудита

### Q1. Requirement Coverage (общий)

```sql
SELECT
    COUNT(*) FILTER (WHERE tc_count > 0) AS covered,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE tc_count > 0) / COUNT(*), 2) AS coverage_pct
FROM (
    SELECT r.id, COUNT(tc.id) AS tc_count
    FROM requirements r
    LEFT JOIN test_cases tc ON tc.requirement_id = r.id
    GROUP BY r.id
) sub;
```

**Ожидаемо:** `100 / 100 / 100.00%`.

### Q2. Coverage по домену

```sql
SELECT
    r.domain,
    COUNT(DISTINCT r.id) AS req_total,
    COUNT(DISTINCT r.id) FILTER (WHERE tc.id IS NOT NULL) AS req_covered,
    ROUND(100.0 * COUNT(DISTINCT r.id) FILTER (WHERE tc.id IS NOT NULL)
          / COUNT(DISTINCT r.id), 2) AS coverage_pct
FROM requirements r
LEFT JOIN test_cases tc ON tc.requirement_id = r.id
GROUP BY r.domain
ORDER BY coverage_pct ASC, r.domain;
```

### Q3. Требования без тестов (пробелы)

```sql
SELECT r.id, r.domain, r.title, r.priority, r.owner
FROM requirements r
LEFT JOIN test_cases tc ON tc.requirement_id = r.id
WHERE tc.id IS NULL
ORDER BY
    CASE r.priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2
                    WHEN 'Medium' THEN 3 ELSE 4 END,
    r.id;
```

**Ожидаемо:** пусто (все покрыты). Если есть — gate блокирует релиз.

### Q4. Story Coverage (по спринту)

```sql
SELECT
    s.sprint,
    COUNT(DISTINCT s.id) AS stories_total,
    COUNT(DISTINCT s.id) FILTER (WHERE tc.id IS NOT NULL) AS stories_covered,
    ROUND(100.0 * COUNT(DISTINCT s.id) FILTER (WHERE tc.id IS NOT NULL)
          / COUNT(DISTINCT s.id), 2) AS coverage_pct
FROM stories s
LEFT JOIN test_cases tc ON tc.linked_issue = s.id
GROUP BY s.sprint
ORDER BY s.sprint;
```

### Q5. Истории без тестов

```sql
SELECT s.id, s.sprint, s.assignee, s.status, r.id AS requirement
FROM stories s
JOIN requirements r ON r.id = s.requirement_id
LEFT JOIN test_cases tc ON tc.linked_issue = s.id
WHERE tc.id IS NULL
ORDER BY s.sprint, s.id;
```

### Q6. Тесты без требования (orphans)

```sql
SELECT tc.id, tc.title, tc.type, tc.owner, tc.sprint
FROM test_cases tc
LEFT JOIN requirements r ON r.id = tc.requirement_id
WHERE r.id IS NULL OR tc.requirement_id IS NULL
ORDER BY tc.id;
```

### Q7. Тесты без истории (orphans LinkedIssue)

```sql
SELECT tc.id, tc.title, tc.requirement_id
FROM test_cases tc
LEFT JOIN stories s ON s.id = tc.linked_issue
WHERE s.id IS NULL OR tc.linked_issue IS NULL
ORDER BY tc.id;
```

### Q8. Automation Coverage по домену

```sql
SELECT
    r.domain,
    COUNT(tc.id) AS total,
    COUNT(tc.id) FILTER (WHERE tc.automation_status = 'Auto') AS auto,
    COUNT(tc.id) FILTER (WHERE tc.automation_status = 'Manual') AS manual,
    ROUND(100.0 * COUNT(tc.id) FILTER (WHERE tc.automation_status = 'Auto')
          / NULLIF(COUNT(tc.id), 0), 2) AS auto_pct
FROM test_cases tc
LEFT JOIN requirements r ON r.id = tc.requirement_id
GROUP BY r.domain
ORDER BY auto_pct ASC NULLS LAST;
```

**Ожидаемо:** FUT/BOND/STOCK — низкий %, API/SEC/UI — 100%.

### Q9. Test Effectiveness (баги, найденные тестом)

```sql
SELECT
    tc.id AS test_id,
    tc.title,
    COUNT(b.id) AS bugs_found,
    COUNT(b.id) FILTER (WHERE b.severity = 'Critical') AS critical_bugs
FROM test_cases tc
LEFT JOIN bugs b ON b.test_id = tc.id
GROUP BY tc.id, tc.title
HAVING COUNT(b.id) > 0
ORDER BY bugs_found DESC, critical_bugs DESC;
```

### Q10. Требования с наибольшим числом багов

```sql
SELECT
    r.id AS requirement,
    r.domain,
    COUNT(b.id) AS bugs,
    COUNT(b.id) FILTER (WHERE b.status = 'Open') AS open_bugs
FROM requirements r
JOIN bugs b ON b.requirement_id = r.id
GROUP BY r.id, r.domain
ORDER BY bugs DESC, open_bugs DESC;
```

### Q11. Flaky-тесты (за 30 дней)

```sql
SELECT
    tc.id,
    tc.title,
    COUNT(*) FILTER (WHERE tr.status = 'Passed') AS passed,
    COUNT(*) FILTER (WHERE tr.status = 'Failed') AS failed,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE tr.status = 'Failed')
          / NULLIF(COUNT(*), 0), 2) AS fail_rate_pct
FROM test_cases tc
JOIN test_runs tr ON tr.test_id = tc.id
WHERE tr.run_date > now() - interval '30 days'
GROUP BY tc.id, tc.title
HAVING COUNT(*) FILTER (WHERE tr.status = 'Passed') > 0
   AND COUNT(*) FILTER (WHERE tr.status = 'Failed') > 0
ORDER BY fail_rate_pct DESC;
```

### Q12. Статус критичных требований (release gate)

```sql
SELECT
    r.id AS requirement,
    r.priority,
    tc.id AS test_id,
    tc.title,
    last_run.status AS last_status,
    last_run.run_date
FROM requirements r
JOIN test_cases tc ON tc.requirement_id = r.id
LEFT JOIN LATERAL (
    SELECT status, run_date
    FROM test_runs
    WHERE test_id = tc.id
    ORDER BY run_date DESC
    LIMIT 1
) last_run ON TRUE
WHERE r.priority = 'Critical'
ORDER BY
    CASE last_run.status
        WHEN 'Failed' THEN 1
        WHEN 'Blocked' THEN 2
        WHEN 'Passed' THEN 3
        ELSE 4 END,
    r.id;
```

**Gate:** если хотя бы одна строка `last_status = 'Failed'` — релиз блокируется.

### Q13. Release Gate — сводка

```sql
WITH critical_status AS (
    SELECT
        r.id AS requirement,
        COALESCE((
            SELECT tr.status
            FROM test_runs tr
            WHERE tr.test_id = tc.id
            ORDER BY tr.run_date DESC
            LIMIT 1
        ), 'Untested') AS status
    FROM requirements r
    JOIN test_cases tc ON tc.requirement_id = r.id
    WHERE r.priority = 'Critical'
)
SELECT
    COUNT(*) FILTER (WHERE status = 'Passed')   AS passed,
    COUNT(*) FILTER (WHERE status = 'Failed')   AS failed,
    COUNT(*) FILTER (WHERE status = 'Blocked')  AS blocked,
    COUNT(*) FILTER (WHERE status = 'Untested') AS untested,
    CASE WHEN COUNT(*) FILTER (WHERE status IN ('Failed','Blocked','Untested')) = 0
         THEN 'RELEASE OK' ELSE 'RELEASE BLOCKED' END AS gate
FROM critical_status;
```

### Q14. Impact Analysis: тесты по требованию

```sql
SELECT tc.id, tc.title, tc.type, tc.automation_status, tc.owner
FROM test_cases tc
WHERE tc.requirement_id = 'BRQ-PORT-006'
ORDER BY tc.id;
```

**Использование:** при изменении требования — перезапустить только эти тесты.

### Q15. Impact Analysis: полная цепочка (BRQ → STORY → TC → Script)

```sql
SELECT
    r.id   AS requirement,
    r.title AS requirement_title,
    s.id   AS story,
    s.sprint,
    tc.id  AS test_id,
    tc.automation_status,
    tc.automation_script
FROM requirements r
JOIN stories s ON s.requirement_id = r.id
JOIN test_cases tc ON tc.linked_issue = s.id
WHERE r.id = 'BRQ-PORT-006'
ORDER BY s.id, tc.id;
```

### Q16. Дублирующее покрытие (≥3 тестов на BRQ)

```sql
SELECT
    tc.requirement_id,
    COUNT(*) AS tests_count,
    STRING_AGG(tc.id, ', ' ORDER BY tc.id) AS tests
FROM test_cases tc
GROUP BY tc.requirement_id
HAVING COUNT(*) >= 3
ORDER BY tests_count DESC;
```

**Зачем:** иногда дублирование избыточно (3+ теста на один BRQ), иногда оправдано (разные платформы). Помогает оптимизировать набор.

### Q17. Тренд Pass Rate по неделям

```sql
SELECT
    date_trunc('week', run_date) AS week,
    COUNT(*) AS total_runs,
    COUNT(*) FILTER (WHERE status = 'Passed') AS passed,
    COUNT(*) FILTER (WHERE status = 'Failed') AS failed,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'Passed')
          / NULLIF(COUNT(*), 0), 2) AS pass_rate_pct
FROM test_runs
GROUP BY week
ORDER BY week DESC
LIMIT 12;
```

### Q18. Непрогнанные тесты (Untested > 7 дней)

```sql
SELECT
    tc.id,
    tc.title,
    tc.requirement_id,
    tc.owner,
    MAX(tr.run_date) AS last_run
FROM test_cases tc
LEFT JOIN test_runs tr ON tr.test_id = tc.id
GROUP BY tc.id, tc.title, tc.requirement_id, tc.owner
HAVING MAX(tr.run_date) IS NULL
    OR MAX(tr.run_date) < now() - interval '7 days'
ORDER BY last_run NULLS FIRST, tc.id;
```

### Q19. Аудит регулятора: критичные BRQ + результат + история

```sql
SELECT
    r.id AS requirement,
    r.title,
    tc.id AS test_id,
    tc.title AS test_title,
    tc.automation_status,
    COALESCE((
        SELECT tr.status FROM test_runs tr
        WHERE tr.test_id = tc.id ORDER BY tr.run_date DESC LIMIT 1
    ), 'Untested') AS last_status,
    (SELECT MAX(tr.run_date) FROM test_runs tr WHERE tr.test_id = tc.id) AS last_run,
    (SELECT COUNT(*) FROM bugs b WHERE b.test_id = tc.id) AS bugs_found
FROM requirements r
JOIN test_cases tc ON tc.requirement_id = r.id
WHERE r.priority = 'Critical'
  AND r.domain IN ('ORDER','SEC','PORT','NFR')
ORDER BY r.id, tc.id;
```

**Приложение к аудиторскому отчёту:** доказывает, что критичные требования покрыты, прогнаны, багов нет (или есть с известным статусом).

### Q20. Полная матрица трассируемости (BRQ × STORY × TC × STATUS)

```sql
SELECT
    r.id   AS requirement,
    r.priority,
    s.id   AS story,
    s.sprint,
    tc.id  AS test_id,
    tc.title AS test_title,
    tc.automation_status,
    COALESCE((
        SELECT tr.status FROM test_runs tr
        WHERE tr.test_id = tc.id ORDER BY tr.run_date DESC LIMIT 1
    ), 'Untested') AS last_status,
    COALESCE((SELECT COUNT(*) FROM bugs b WHERE b.test_id = tc.id), 0) AS bugs
FROM requirements r
LEFT JOIN stories s     ON s.requirement_id = r.id
LEFT JOIN test_cases tc ON tc.requirement_id = r.id
                        AND tc.linked_issue = s.id
ORDER BY r.domain, r.id, s.id, tc.id;
```

---

## ЧАСТЬ 9. SQL — дашборд (views + materialized)

### V1. `v_requirement_coverage`

```sql
CREATE OR REPLACE VIEW v_requirement_coverage AS
SELECT
    r.id AS requirement_id,
    r.domain,
    r.priority,
    COUNT(tc.id) AS tests_total,
    COUNT(tc.id) FILTER (WHERE tc.automation_status = 'Auto') AS tests_auto,
    COUNT(tc.id) FILTER (WHERE tc.automation_status = 'Manual') AS tests_manual,
    CASE WHEN COUNT(tc.id) = 0 THEN 'UNCOVERED' ELSE 'COVERED' END AS coverage,
    ROUND(100.0 * COUNT(tc.id) FILTER (WHERE tc.automation_status = 'Auto')
          / NULLIF(COUNT(tc.id), 0), 2) AS auto_pct
FROM requirements r
LEFT JOIN test_cases tc ON tc.requirement_id = r.id
GROUP BY r.id, r.domain, r.priority;
```

### V2. `v_story_coverage`

```sql
CREATE OR REPLACE VIEW v_story_coverage AS
SELECT
    s.id AS story_id,
    s.sprint,
    s.status AS story_status,
    COUNT(tc.id) AS tests_total,
    CASE WHEN COUNT(tc.id) = 0 THEN 'UNCOVERED' ELSE 'COVERED' END AS coverage
FROM stories s
LEFT JOIN test_cases tc ON tc.linked_issue = s.id
GROUP BY s.id, s.sprint, s.status;
```

### V3. `v_last_status` (последний статус каждого теста)

```sql
CREATE OR REPLACE VIEW v_last_status AS
SELECT DISTINCT ON (tr.test_id)
    tr.test_id,
    tr.status,
    tr.run_date,
    tr.environment
FROM test_runs tr
ORDER BY tr.test_id, tr.run_date DESC;
```

### V4. `v_release_gate`

```sql
CREATE OR REPLACE VIEW v_release_gate AS
SELECT
    r.id AS requirement,
    r.priority,
    tc.id AS test_id,
    ls.status AS last_status,
    ls.run_date
FROM requirements r
JOIN test_cases tc ON tc.requirement_id = r.id
LEFT JOIN v_last_status ls ON ls.test_id = tc.id
WHERE r.priority = 'Critical';
```

### V5. Materialized view для дашборда

```sql
CREATE MATERIALIZED VIEW mv_qa_dashboard AS
SELECT
    r.domain,
    COUNT(DISTINCT r.id) AS requirements,
    COUNT(DISTINCT tc.id) AS tests,
    COUNT(DISTINCT tc.id) FILTER (WHERE tc.automation_status = 'Auto') AS auto_tests,
    ROUND(100.0 * COUNT(DISTINCT tc.id) FILTER (WHERE tc.automation_status = 'Auto')
          / NULLIF(COUNT(DISTINCT tc.id), 0), 2) AS auto_pct,
    COUNT(DISTINCT ls.test_id) FILTER (WHERE ls.status = 'Passed') AS passed,
    COUNT(DISTINCT ls.test_id) FILTER (WHERE ls.status = 'Failed') AS failed
FROM requirements r
LEFT JOIN test_cases tc ON tc.requirement_id = r.id
LEFT JOIN v_last_status ls ON ls.test_id = tc.id
GROUP BY r.domain;

-- Обновление раз в час
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_qa_dashboard;
```

### Grafana/Superset панели

| Панель | SQL-источник | Метрика |
|---|---|---|
| Requirement Coverage | `v_requirement_coverage` | `COUNT(*) FILTER (coverage='COVERED') / COUNT(*)` |
| Automation % | `mv_qa_dashboard` | `auto_pct` |
| Critical Pass Rate | `v_release_gate` | `COUNT(Passed) / COUNT(*)` |
| Flaky Tests | Q11 | список |
| Stories без тестов | `v_story_coverage` | `COUNT(*) WHERE coverage='UNCOVERED'` |
| Bugs по тестам | Q9 | top-10 |
| Pass Rate Trend | Q17 | line chart |

---

## ЧАСТЬ 10. CI/CD — интеграция

### 10.1. pytest-маркеры для трассируемости

```python
# tests/conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "requirement(brq): BRQ-* requirement ID")
    config.addinivalue_line("markers", "story(story): STORY-* linked issue")
    config.addinivalue_line("markers", "testid(tc): TC-* test case ID")

# tests/e2e/test_risk.py
@pytest.mark.requirement("BRQ-PORT-006")
@pytest.mark.story("STORY-2604")
@pytest.mark.testid("TC-PORT-004")
def test_stop_out(auth_page):
    ...
```

### 10.2. Прогон по требованию

```bash
pytest -m "requirement('BRQ-PORT-006')"
pytest -m "story('STORY-2604')"
pytest -m "testid('TC-PORT-004')"
```

### 10.3. Release Gate (GitHub Actions)

```yaml
# .github/workflows/release-gate.yml
name: Release Gate
on:
  pull_request:
    branches: [main]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install deps
        run: pip install pytest requests psycopg2-binary

      - name: Run critical tests
        run: |
          pytest \
            -m "requirement('BRQ-SEC-001') or requirement('BRQ-PORT-006') or requirement('BRQ-ORDER-010')" \
            --junitxml=artifacts/critical.xml

      - name: DB Coverage Audit
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: python scripts/audit_coverage.py

      - name: TestRail Coverage Gate
        env:
          TR_USER: ${{ secrets.TR_USER }}
          TR_KEY: ${{ secrets.TR_KEY }}
        run: python scripts/testrail_coverage.py

      - name: Upload artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: qa-artifacts
          path: artifacts/
```

### 10.4. `scripts/audit_coverage.py` — SQL-аудит в CI

```python
# scripts/audit_coverage.py
import os, sys, psycopg2

QUERIES = {
    "uncovered_requirements": """
        SELECT r.id FROM requirements r
        LEFT JOIN test_cases tc ON tc.requirement_id = r.id
        WHERE tc.id IS NULL
    """,
    "failed_critical": """
        SELECT r.id FROM requirements r
        JOIN test_cases tc ON tc.requirement_id = r.id
        LEFT JOIN v_last_status ls ON ls.test_id = tc.id
        WHERE r.priority = 'Critical' AND ls.status = 'Failed'
    """,
    "orphan_tests": """
        SELECT tc.id FROM test_cases tc
        LEFT JOIN requirements r ON r.id = tc.requirement_id
        WHERE r.id IS NULL
    """,
}

def main():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    failed = False
    for name, q in QUERIES.items():
        with conn.cursor() as cur:
            cur.execute(q)
            rows = [r[0] for r in cur.fetchall()]
        if rows:
            print(f"FAIL {name}: {rows}")
            failed = True
        else:
            print(f"OK {name}")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
```

### 10.5. `scripts/testrail_coverage.py` — TestRail gate

```python
# scripts/testrail_coverage.py
import os, sys, base64, requests

HOST = os.getenv("TR_HOST", "https://YOUR.testrail.io")
USER, KEY = os.getenv("TR_USER"), os.getenv("TR_KEY")
PROJECT = int(os.getenv("TR_PROJECT", "1"))

auth = base64.b64encode(f"{USER}:{KEY}".encode()).decode()
headers = {"Authorization": f"Basic {auth}"}

def get_cases():
    cases, offset = [], 0
    while True:
        r = requests.get(f"{HOST}/index.php?/api/v2/get_cases/{PROJECT}",
                         headers=headers, params={"limit": 250, "offset": offset})
        batch = r.json()
        if not batch:
            break
        cases.extend(batch if isinstance(batch, list) else batch.get("cases", []))
        offset += 250
    return cases

def main():
    cases = get_cases()
    missing_req = [c["id"] for c in cases if not c.get("custom_requirement_id")]
    missing_story = [c["id"] for c in cases if not c.get("custom_linked_issue")]
    auto = sum(1 for c in cases if c.get("custom_automation_status") == "Auto")
    pct = 100.0 * auto / len(cases) if cases else 0

    ok = True
    if missing_req:
        print(f"FAIL missing RequirementID: {missing_req}"); ok = False
    if missing_story:
        print(f"FAIL missing LinkedIssue: {missing_story}"); ok = False
    print(f"Automation coverage: {pct:.1f}% ({auto}/{len(cases)})")
    if pct < 60:
        print("FAIL automation below 60%"); ok = False
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
```

---

## ИТОГОВАЯ СВОДКА

### Что поставлено

| # | Блок | Артефакт |
|---|---|---|
| 1 | TestRail | 8 custom fields + настройка |
| 2 | TestRail | Traceability Report + API-генератор |
| 3 | TestRail | Requirement & Automation Coverage + gate |
| 4 | Xray | Issue types, links, custom fields, Requirement Status |
| 5 | Xray | Test Coverage, Traceability, Test Plans |
| 6 | Xray | REST + GraphQL + Python-клиент |
| 7 | SQL | DDL 5 таблиц + индексы + загрузчик CSV |
| 8 | SQL | **20 запросов** аудита |
| 9 | SQL | 5 views + materialized view + Grafana-панели |
| 10 | CI/CD | pytest-маркеры + 2 gate-скрипта + GitHub Actions |

### Ключевые метрики, которые теперь измеряются

| Метрика | Формула | Цель | Наш набор |
|---|---|---|---|
| Requirement Coverage | `BRQ с тестами / все BRQ` | 100% | **100%** |
| Story Coverage | `STORY с тестами / все STORY` | 100% | 100% |
| Automation Coverage | `Auto / все TC` | ≥80% | **60%** (→ Q2 80%) |
| Critical Pass Rate | `Passed Critical / все Critical` | 100% | gate |
| Flaky Rate | `flaky TC / все TC` | <5% | мониторинг |
| Test Effectiveness | `bugs / TC` | top-10 | мониторинг |
| Orphan Tests | `TC без BRQ/STORY` | 0 | gate |
| Untested >7d | `TC без прогона` | 0 | мониторинг |

### Три поля в действии — где что живёт

| Артефакт | `RequirementID` | `LinkedIssue` | `TestID` |
|---|---|---|---|
| CSV | колонка | колонка | `ID` |
| Step-by-step | — | — | `ID` (склейка) |
| Матрица | колонка 2 | колонка 3 | колонка 1 |
| TestRail | `custom_requirement_id` + `refs` | `custom_linked_issue` + `refs` | `title`/`id` |
| Xray | `Requirement` link | `implements` link | `Test` issue |
| SQL | `requirements.id` | `stories.id` | `test_cases.id` |
| pytest | `@pytest.mark.requirement` | `@pytest.mark.story` | `@pytest.mark.testid` |
| CI gate | `-m "requirement('BRQ-*')"` | `-m "story('STORY-*')"` | `-m "testid('TC-*')"` |

### Roadmap внедрения

| Неделя | Задача | Артефакт |
|---|---|---|
| 1 | TestRail custom fields + импорт 100 кейсов | Части 1–3 |
| 2 | SQL-схема + загрузка CSV + 20 запросов | Части 7–8 |
| 3 | Xray issue types + links + импорт | Части 4–6 |
| 4 | CI gate (pytest-маркеры + 2 скрипта) | Часть 10 |
| 5 | Grafana/Superset дашборд | Часть 9 |
| 6 | Довести Automation Coverage 60% → 80% | Q8 + roadmap |

---

**TestRail Traceability + Coverage, Xray Requirement/Story Coverage, 20 SQL-запросов, 5 views + materialized, 2 CI-gate скрипта, pytest-маркеры, GitHub Actions. Все 100 кейсов трассируются по цепочке `RequirementID → LinkedIssue → TestID → AutomationScript → BugID` с автоматическим gate на релиз.**
