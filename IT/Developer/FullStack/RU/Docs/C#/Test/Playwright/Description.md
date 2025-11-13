# Playwright - Описание и сценарии использования

## Что такое Playwright?

**Playwright** - это современный фреймворк для автоматизации тестирования веб-приложений, разработанный Microsoft. Поддерживает Chromium, Firefox и WebKit через единый API.

## Ключевые особенности

- **Кросс-браузерное тестирование** (Chrome, Firefox, Safari, Edge)
- **Кросс-платформенность** (Windows, Linux, macOS)
- **Автоматическое ожидание** элементов
- **Поддержка мобильных устройств** (эмуляция)
- **Скриншоты и видео** запись тестов
- **Сетевое перехватывание** (mock, intercept)
- **Параллельное выполнение** тестов

## Установка

```bash
# Инициализация проекта
npm init playwright@latest

# Или установка в существующий проект
npm install @playwright/test

# Установка браузеров
npx playwright install
```

## Базовые сценарии использования

### 1. Простой E2E тест

```javascript
import { test, expect } from '@playwright/test';

test('basic test', async ({ page }) => {
  // Навигация на сайт
  await page.goto('https://example.com');
  
  // Проверка заголовка
  await expect(page).toHaveTitle('Example Domain');
  
  // Клик по элементу
  await page.click('text=More information...');
  
  // Проверка URL
  await expect(page).toHaveURL(/iana/);
});
```

### 2. Тестирование авторизации

```javascript
import { test, expect } from '@playwright/test';

test('user login', async ({ page }) => {
  await page.goto('https://demo.app.com/login');
  
  // Заполнение формы
  await page.fill('#username', 'testuser');
  await page.fill('#password', 'password123');
  
  // Клик по кнопке входа
  await page.click('button[type="submit"]');
  
  // Проверка успешного входа
  await expect(page.locator('.user-profile')).toBeVisible();
  await expect(page).toHaveURL(/dashboard/);
});
```

### 3. Тестирование интернет-магазина

```javascript
import { test, expect } from '@playwright/test';

test('complete purchase flow', async ({ page }) => {
  await page.goto('https://shop.example.com');
  
  // Поиск товара
  await page.fill('.search-input', 'laptop');
  await page.click('.search-button');
  
  // Выбор товара
  await page.click('.product-item:first-child');
  await page.click('.add-to-cart');
  
  // Переход в корзину
  await page.click('.cart-icon');
  
  // Оформление заказа
  await page.click('.checkout-button');
  await page.fill('#email', 'test@example.com');
  await page.fill('#address', 'Test Address 123');
  
  // Завершение покупки
  await page.click('.place-order');
  
  // Проверка подтверждения
  await expect(page.locator('.order-confirmation')).toBeVisible();
});
```

## Продвинутые сценарии

### 4. Тестирование с моками API

```javascript
import { test, expect } from '@playwright/test';

test('mock api response', async ({ page }) => {
  // Mock API response
  await page.route('**/api/users', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Mock User 1' },
        { id: 2, name: 'Mock User 2' }
      ])
    });
  });

  await page.goto('https://app.example.com/users');
  
  // Проверка моковых данных
  await expect(page.locator('.user-item')).toHaveCount(2);
});
```

### 5. Тестирование загрузки файлов

```javascript
import { test, expect } from '@playwright/test';

test('file upload', async ({ page }) => {
  await page.goto('https://app.example.com/upload');
  
  // Загрузка файла
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles('./test-data/sample.pdf');
  
  await page.click('#upload-button');
  
  // Проверка успешной загрузки
  await expect(page.locator('.upload-success')).toBeVisible();
});
```

### 6. Параллельное тестирование

```javascript
import { test, expect } from '@playwright/test';

test.describe('parallel tests', () => {
  test('test on chrome', async ({ browser }) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto('https://example.com');
    // ... тест
  });

  test('test on firefox', async ({ browser }) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto('https://example.com');
    // ... тест
  });
});
```

## Сценарии использования в реальных проектах

### 7. Тестирование Single Page Application (SPA)

```javascript
import { test, expect } from '@playwright/test';

test('SPA navigation', async ({ page }) => {
  await page.goto('https://spa.example.com');
  
  // Навигация без перезагрузки страницы
  await page.click('nav >> text=Dashboard');
  await expect(page.locator('.dashboard-content')).toBeVisible();
  
  await page.click('nav >> text=Settings');
  await expect(page.locator('.settings-form')).toBeVisible();
  
  // Проверка что страница не перезагружалась
  await expect(page).toHaveURL('https://spa.example.com/#/settings');
});
```

### 8. Тестирование PWA (Progressive Web App)

```javascript
import { test, expect } from '@playwright/test';

test('PWA features', async ({ page }) => {
  await page.goto('https://pwa.example.com');
  
  // Проверка Service Worker
  const swState = await page.evaluate(() => 
    navigator.serviceWorker?.ready
  );
  expect(swState).toBeTruthy();
  
  // Проверка оффлайн режима
  await page.context().setOffline(true);
  await page.reload();
  await expect(page.locator('.offline-message')).toBeVisible();
});
```

### 9. Тестирование доступности (a11y)

```javascript
import { test, expect } from '@playwright/test';
import { injectAxe, checkA11y } from 'axe-playwright';

test('accessibility test', async ({ page }) => {
  await page.goto('https://example.com');
  
  // Инициализация axe
  await injectAxe(page);
  
  // Проверка доступности
  await checkA11y(page, null, {
    detailedReport: true,
    detailedReportOptions: { html: true }
  });
});
```

### 10. Визуальное регрессионное тестирование

```javascript
import { test, expect } from '@playwright/test';

test('visual regression', async ({ page }) => {
  await page.goto('https://example.com');
  
  // Сравнение скриншотов
  await expect(page).toHaveScreenshot('homepage.png', {
    threshold: 0.1, // допуск 10%
    maxDiffPixels: 100
  });
});
```

## Конфигурация Playwright

### playwright.config.js

```javascript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  timeout: 30000,
  retries: 1,
  
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile',
      use: { ...devices['iPhone 12'] },
    },
  ],

  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results.json' }]
  ],
});
```

## Интеграция с CI/CD

### GitHub Actions

```yaml
name: Playwright Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright
        run: npx playwright install
      
      - name: Run tests
        run: npx playwright test
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## Продвинутые техники

### 11. Тестирование безопасности

```javascript
test('XSS vulnerability test', async ({ page }) => {
  await page.goto('https://app.example.com/search');
  
  // Попытка XSS инъекции
  const xssPayload = '<script>alert("XSS")</script>';
  await page.fill('#search', xssPayload);
  await page.click('#search-button');
  
  // Проверка что скрипт не выполнился
  const alertCount = await page.evaluate(() => window.alerts);
  expect(alertCount).toBeUndefined();
});
```

### 12. Performance testing

```javascript
test('performance metrics', async ({ page }) => {
  await page.goto('https://example.com');
  
  // Измерение метрик производительности
  const performanceTiming = await page.evaluate(() => 
    JSON.stringify(performance.timing)
  );
  
  const metrics = JSON.parse(performanceTiming);
  const loadTime = metrics.loadEventEnd - metrics.navigationStart;
  
  expect(loadTime).toBeLessThan(3000); // Загрузка менее 3 секунд
});
```

### 13. Тестирование WebSocket

```javascript
test('websocket communication', async ({ page }) => {
  await page.goto('https://realtime.example.com');
  
  // Ожидание WebSocket сообщения
  const wsMessage = await page.waitForEvent('websocket', {
    timeout: 5000,
    predicate: ws => ws.url().includes('/realtime')
  });
  
  expect(wsMessage).toBeTruthy();
});
```

## Лучшие практики

1. **Используйте Page Object Model**
2. **Избегайте sleep() - используйте встроенные ожидания**
3. **Параллелизуйте тесты для скорости**
4. **Используйте data-testid атрибуты**
5. **Регулярно обновляйте браузеры**
6. **Интегрируйте в процесс разработки**

## Преимущества Playwright

1. **Единый API** для всех браузеров
2. **Надежные автоматические ожидания**
3. **Отличная документация** и сообщество
4. **Поддержка мобильных устройств**
5. **Мощные возможности отладки**
6. **Интеграция с популярными фреймворками**