Ниже — объединённая схема, которая связывает **TestRail (Traceability)** и **Xray (Coverage)** с автотестами на **Playwright** и **Selenium** в единый контур. Ключевая идея: оба фреймворка генерируют стандартный **JUnit XML**, который затем загружается в TestRail через **TRCLI** и в Xray через **специализированные репортеры / REST API**. Это позволяет не дублировать разметку тестов и сохранить сквозную трассируемость `RequirementID → LinkedIssue → TestID`.

---

## 1. Архитектура: один прогон → два пункта назначения

```
┌─────────────────┐     ┌─────────────────┐
│   Playwright    │     │    Selenium     │
│  (pytest / JS)  │     │ (pytest / Java) │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └──────────┬────────────┘
                    │ JUnit XML (+ маркеры TestID / RequirementID)
                    ▼
         ┌─────────────────────┐
         │   Единый артефакт   │
         │   junit-results.xml │
         └──────────┬──────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│   TestRail    │       │     Xray      │
│   (TRCLI)     │       │ (Reporter /   │
│               │       │  REST / GraphQL)│
└───────┬───────┘       └───────┬───────┘
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│  Traceability │       │   Coverage    │
│  Report       │       │   (Requirement│
│  (BRQ→TC→Run) │       │    Status)    │
└───────────────┘       └───────────────┘
```

---

## 2. TestRail: Traceability через TRCLI

TestRail с версии 10.2.0 усилил поддержку трассируемости и интеграции с Selenium/Playwright. Основной инструмент — **TestRail CLI (TRCLI)**, который парсит JUnit XML и создаёт прогоны с привязкой к кейсам.

### 2.1. Подготовка TestRail

Создайте кастомные поля (если ещё не сделано):

| Поле | Тип | Назначение |
|---|---|---|
| `custom_requirement_id` | String | BRQ-* |
| `custom_linked_issue` | String | STORY-* |
| `custom_automation_status` | Dropdown | Auto / Manual |
| `custom_automation_script` | String | путь к тесту |

### 2.2. Playwright → TestRail

**Шаг 1. Генерация JUnit XML.** В `playwright.config.ts` (или через CLI):

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: [
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
});
```

Или без изменения конфига:
```bash
npx playwright test --reporter=junit
# результат: test-results/junit.xml
```

**Шаг 2. Загрузка через TRCLI.**

```bash
pip install trcli

trcli -y \
  -h https://YOUR.testrail.io/ \
  --project "Exchange QA" \
  --username "$TR_USERNAME" \
  --password "$TR_API_TOKEN" \
  parse_junit \
  -f test-results/junit.xml \
  --title "Playwright run $(date +%F-%H%M)" \
  --run-description "CI: $CI_PIPELINE_URL" \
  --close-run
```

TRCLI автоматически сопоставляет `testcase` из JUnit с кейсами TestRail. Для точной привязки к `TC-*` используйте опцию `--case-matcher` или добавьте в JUnit атрибут `classname`, равный TestID.

**Шаг 3. Traceability-отчёт.** В TestRail: `Reports → Traceability`, группировка по `custom_requirement_id`. Покрытие считается по наличию кейсов с данным BRQ.

### 2.3. Selenium → TestRail

**Для Python/pytest (Selenium):**

```bash
pytest tests/selenium/ \
  --junitxml=test-results/selenium-junit.xml
```

Затем тот же TRCLI:
```bash
trcli parse_junit -f test-results/selenium-junit.xml \
  --title "Selenium run" --close-run ...
```

**Для Java (JUnit5 + Selenium):** Maven Surefire генерирует JUnit XML в `target/surefire-reports/`. TRCLI парсит его напрямую.

### 2.4. Альтернатива: нативные репортеры

Если не хотите использовать TRCLI, есть готовые пакеты:
- `playwright-testrail-reporter` (npm) — автоматически создаёт прогон и обновляет результаты.
- `pytest-testrail2` / `pytest-testrail-reporter` (Python) — загружают результаты из pytest напрямую.

---

## 3. Xray: Coverage через репортеры и GraphQL

Xray строит покрытие требований на основе связей `Test → Requirement` и результатов прогонов. Для Playwright и Selenium есть официальные и community-репортеры.

### 3.1. Playwright → Xray

**Официальный репортер `@xray-app/playwright-junit-reporter`:**

```bash
npm install --save-dev @xray-app/playwright-junit-reporter
```

```typescript
// playwright.config.ts
export default defineConfig({
  reporter: [
    ['@xray-app/playwright-junit-reporter', { outputFile: 'xray-results.xml' }],
  ],
});
```

Репортер встраивает аннотации в JUnit XML так, чтобы Xray мог связать тест с существующим Test issue. В тестах укажите `test_key`:

```typescript
test('stop-out < 5s', async ({ page }) => {
  test.info().annotations.push({ type: 'test_key', description: 'TC-PORT-004' });
  // ...
});
```

Затем загрузите XML в Xray:

```bash
curl -X POST "https://xray.cloud.getxray.app/api/v2/import/execution/junit?projectKey=EXCH&testPlanKey=PLAN-123" \
  -H "Authorization: Bearer $XRAY_TOKEN" \
  -H "Content-Type: application/xml" \
  --data-binary @xray-results.xml
```

**Альтернатива: `playwright-xray` (community).** Поддерживает автоматическую привязку к Test Plan через GraphQL.

### 3.2. Selenium → Xray

**Python/pytest:** используйте `pytest-xray-reporter` для генерации Xray JSON или стандартный JUnit XML.

```bash
pip install pytest-xray-reporter

pytest tests/selenium/ --xray-output=results.json
```

Затем импорт JSON через REST:
```bash
curl -X POST "https://xray.cloud.getxray.app/api/v2/import/execution" \
  -H "Authorization: Bearer $XRAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @results.json
```

**Java (JUnit/Surefire):** Xray принимает стандартный JUnit XML через endpoint `import/execution/junit`. Убедитесь, что в отчёте есть `classname`, соответствующий Test Key (TC-*).

### 3.3. Проверка Coverage в Xray

После импорта Xray автоматически обновляет **Requirement Status**:
- `OK` — все связанные тесты прошли.
- `NOK` — есть упавшие.
- `UNCOVERED` — нет тестов.

Отчёт: `Xray → Reports → Test Coverage by Requirement`. Для программного доступа используйте GraphQL:

```graphql
query {
  getCoverage(projectKey: "EXCH") {
    requirementCoverage
    automationCoverage
    uncoveredRequirements { jira(fields: ["key"]) }
  }
}
```

Xray предоставляет полный GraphQL API для запроса покрытия и пробелов.

---

## 4. Единый контракт маркеров для обоих фреймворков

Чтобы один и тот же тест мог уйти и в TestRail, и в Xray, используйте одинаковые идентификаторы в коде.

### Playwright (TypeScript)

```typescript
test('TC-PORT-004 | stop-out <5s', async ({ page }) => {
  test.info().annotations.push(
    { type: 'test_key', description: 'TC-PORT-004' },
    { type: 'requirement', description: 'BRQ-PORT-006' },
    { type: 'story', description: 'STORY-2604' },
  );
  // ... тест
});
```

### Selenium (Python/pytest)

```python
import pytest

@pytest.mark.testid("TC-PORT-004")
@pytest.mark.requirement("BRQ-PORT-006")
@pytest.mark.story("STORY-2604")
def test_stop_out(driver):
    ...
```

Оба варианта генерируют JUnit XML с нужными атрибутами. TRCLI использует `classname` (TestID), а Xray-репортер — аннотацию `test_key`.

---

## 5. CI/CD-пайплайн: Playwright + Selenium → TestRail + Xray

```yaml
# .github/workflows/qa-traceability.yml
name: QA Traceability
on: [push, pull_request]

jobs:
  playwright:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test --reporter=junit
        # output: test-results/junit.xml
      - name: Upload to TestRail (TRCLI)
        run: |
          pip install trcli
          trcli parse_junit -f test-results/junit.xml \
            --host ${{ secrets.TR_HOST }} \
            --project "Exchange QA" \
            --username ${{ secrets.TR_USER }} \
            --password ${{ secrets.TR_KEY }} \
            --title "Playwright CI" --close-run
      - name: Upload to Xray
        run: |
          curl -X POST "$XRAY_URL/import/execution/junit?projectKey=EXCH" \
            -H "Authorization: Bearer ${{ secrets.XRAY_TOKEN }}" \
            -H "Content-Type: application/xml" \
            --data-binary @test-results/junit.xml

  selenium:
    runs-on: ubuntu-latest
    needs: playwright
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest tests/selenium --junitxml=selenium-junit.xml
      - name: Upload to TestRail
        run: trcli parse_junit -f selenium-junit.xml ... --close-run
      - name: Upload to Xray
        run: |
          pytest tests/selenium --xray-output=xray.json
          curl -X POST "$XRAY_URL/import/execution" \
            -H "Authorization: Bearer ${{ secrets.XRAY_TOKEN }}" \
            -H "Content-Type: application/json" -d @xray.json
```

---

## 6. Что получается на выходе

| Инструмент | Артефакт | Что даёт |
|---|---|---|
| **TestRail** | Traceability Report | Связь `RequirementID → TestID → Run`, покрытие требований |
| **TestRail** | Coverage (Jira) | Проверка покрытия Epic/Sprint/Fix Version |
| **Xray** | Requirement Status | Авто-обновление `OK/NOK/UNCOVERED` |
| **Xray** | Test Coverage Report | Покрытие по требованиям и автоматизации |
| **Playwright** | JUnit XML + аннотации | Единый артефакт для обоих TMS |
| **Selenium** | JUnit XML / Xray JSON | То же |

---

## 7. Итог

- **TestRail** получает **JUnit XML** от Playwright и Selenium через **TRCLI** и строит **Traceability** на кастомных полях `RequirementID` / `LinkedIssue` / `TestID`.
- **Xray** получает результаты через **официальный Playwright-репортер**, **pytest-xray-reporter** или **JUnit XML** и автоматически рассчитывает **Coverage** (Requirement Status + отчёты).
- **Оба фреймворка** используют единый контракт маркеров, поэтому один прогон закрывает и трассируемость в TestRail, и покрытие в Xray.
- **CI/CD** оркестрирует загрузку в оба инструмента параллельно, не дублируя тестовый код.
