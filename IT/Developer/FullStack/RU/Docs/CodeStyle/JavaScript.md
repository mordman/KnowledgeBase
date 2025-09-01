Вот основные рекомендации по **CodeStyle для JavaScript**, основанные на популярных стандартах, таких как **Airbnb JavaScript Style Guide**, **Google JavaScript Style Guide** и **StandardJS**. Эти правила помогут сделать ваш код более читаемым, единообразным и поддерживаемым.

---

## **1. Отступы**
- Используйте **2 пробела** для каждого уровня отступа.
- Не используйте табуляцию.
- Пример:
  ```javascript
  function greet(name) {
    return `Hello, ${name}!`;
  }
  ```

---

## **2. Длина строки**
- Ограничивайте длину строки **80–100 символами**.
- Переносите длинные строки с помощью отступов:
  ```javascript
  // Плохо
  const result = someVeryLongFunctionCallWithManyParameters(param1, param2, param3, param4, param5);

  // Хорошо
  const result = someVeryLongFunctionCallWithManyParameters(
    param1,
    param2,
    param3,
    param4,
    param5
  );
  ```

---

## **3. Точка с запятой**
- **Рекомендуется** использовать точки с запятой в конце выражений (хотя в современном JavaScript они не всегда обязательны благодаря **ASI — Automatic Semicolon Insertion**).
- Пример:
  ```javascript
  const name = 'Alice';
  console.log(name);
  ```

---

## **4. Пустые строки**
- Используйте **1 пустую строку** между логическими блоками кода (например, между функциями, циклами или большими блоками логики).
- Пример:
  ```javascript
  function firstFunction() {
    // ...
  }

  function secondFunction() {
    // ...
  }
  ```

---

## **5. Импорты**
- Группируйте импорты в следующем порядке:
  1. Внешние библиотеки (например, `react`, `lodash`).
  2. Локальные импорты (из вашего проекта).
- Используйте **абсолютные пути** (например, `@/components/Button`) или **относительные пути** (например, `../utils/helper`).
- Пример:
  ```javascript
  import React from 'react';
  import { debounce } from 'lodash';

  import { Button } from '@/components/Button';
  import { fetchData } from '../api/data';
  ```

---

## **6. Пробелы**
- **Операторы:** Окружайте операторы пробелами:
  ```javascript
  const sum = a + b; // Хорошо
  const sum=a+b;     // Плохо
  ```
- **Запятые:** Ставьте пробел после запятой, но не перед ней:
  ```javascript
  const colors = ['red', 'green', 'blue']; // Хорошо
  const colors = ['red','green','blue'];   // Плохо
  ```
- **После двоеточия в объектах:** Ставьте пробел после двоеточия:
  ```javascript
  const user = { name: 'Alice', age: 25 }; // Хорошо
  ```

---

## **7. Именование**
- **Переменные и функции:** Используйте **camelCase**:
  ```javascript
  const userName = 'Alice';
  function calculateTotal() { ... }
  ```
- **Константы:** Используйте **ВЕРХНИЙ РЕГИСТР** с подчёркиваниями:
  ```javascript
  const MAX_COUNT = 100;
  ```
- **Классы:** Используйте **PascalCase**:
  ```javascript
  class User { ... }
  ```
- **Приватные переменные и методы:** Используйте префикс `_` (неофициально, но распространено):
  ```javascript
  this._secretKey = '12345';
  ```

---

## **8. Объявление переменных**
- Используйте `const` по умолчанию. Используйте `let`, только если переменная будет изменяться.
- Избегайте использования `var`.
- Пример:
  ```javascript
  const name = 'Alice'; // Если значение не меняется
  let count = 0;        // Если значение будет изменяться
  ```

---

## **9. Комментарии**
- Используйте **JSDoc** для документирования функций и модулей:
  ```javascript
  /**
   * Возвращает сумму двух чисел.
   * @param {number} a Первое число.
   * @param {number} b Второе число.
   * @returns {number} Сумма чисел.
   */
  function add(a, b) {
    return a + b;
  }
  ```
- Избегайте избыточных комментариев. Код должен быть самодокументируемым.

---

## **10. Строки**
- Используйте **обратные кавычки** (`` ` ``) для шаблонных строк:
  ```javascript
  const greeting = `Hello, ${name}!`;
  ```

---

## **11. Условные операторы**
- Ставьте пробелы вокруг операторов сравнения:
  ```javascript
  if (age >= 18) { ... } // Хорошо
  ```
- Избегайте лишних скобок в условиях:
  ```javascript
  if ((age >= 18)) { ... } // Плохо
  ```

---

## **12. Работа с объектами и массивами**
- Используйте короткий синтаксис для объявления объектов и массивов:
  ```javascript
  const user = { name, age }; // Если ключи совпадают с именами переменных
  const colors = ['red', 'green', 'blue'];
  ```
- Для копирования объектов используйте **spread-оператор**:
  ```javascript
  const newUser = { ...user, status: 'active' };
  ```

---

## **13. Асинхронный код**
- Используйте `async/await` вместо цепочек `.then()` для улучшения читаемости:
  ```javascript
  async function fetchData() {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    return data;
  }
  ```

---

## **14. Обработка ошибок**
- Используйте `try/catch` для обработки ошибок в асинхронном коде:
  ```javascript
  async function fetchData() {
    try {
      const response = await fetch('https://api.example.com/data');
      return await response.json();
    } catch (error) {
      console.error('Ошибка при загрузке данных:', error);
    }
  }
  ```

---

## **15. Пример кода в стиле JavaScript**
```javascript
/**
 * Класс для работы с пользователями.
 */
class User {
  constructor(name, age) {
    this.name = name;
    this.age = age;
    this._secretKey = '12345';
  }

  /**
   * Возвращает приветственное сообщение.
   * @returns {string}
   */
  greet() {
    return `Hello, ${this.name}!`;
  }
}

/**
 * Возвращает сумму всех чисел в массиве.
 * @param {number[]} numbers Массив чисел.
 * @returns {number} Сумма чисел.
 */
function calculateSum(numbers) {
  return numbers.reduce((sum, num) => sum + num, 0);
}

// Пример использования
const user = new User('Alice', 25);
console.log(user.greet());

const numbers = [1, 2, 3, 4, 5];
console.log(calculateSum(numbers));
```

---

### **Инструменты для проверки стиля**
- **ESLint** — гибкий инструмент для анализа кода.
- **Prettier** — автоматический форматтер кода.
- **StandardJS** — строгий стиль с минимальной настройкой.