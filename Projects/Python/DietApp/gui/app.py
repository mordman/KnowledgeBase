import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from typing import Dict
from data.loader import DataLoader
from solver.factory import SolverFactory
from solver.pulp_solver import PULP_AVAILABLE
from models.dish import DietTarget, DietTolerance, MealStructure
import json


class DietApp:
    """Основной класс приложения"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Оптимальная Диета (Python Solver)")
        self.root.geometry("1200x800")
        
        self.data_loader = DataLoader()
        self.solver = None
        self.dishes = []
        self.prefer_pulp = tk.BooleanVar(value=True)

        self._create_widgets()
        self._load_sample_data()
        self._update_solver_status()

    def _create_widgets(self):
        """Создает все виджеты интерфейса"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Левая колонка - Параметры
        self._create_parameters_frame(main_frame)
        
        # Правая колонка - Данные и Результат
        self._create_data_frame(main_frame)

    def _create_parameters_frame(self, parent):
        """Создает панель параметров"""
        left_frame = ttk.LabelFrame(parent, text="Параметры и Цели", padding=10)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Статус решателя
        status_frame = ttk.LabelFrame(left_frame, text="Метод решения", padding=5)
        status_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        self.lbl_solver_status = ttk.Label(status_frame, text="", foreground="green")
        self.lbl_solver_status.grid(row=0, column=0, columnspan=4, sticky=tk.W)
        
        self.chk_prefer_pulp = ttk.Checkbutton(
            status_frame, 
            text="Использовать PuLP (если доступен)",
            variable=self.prefer_pulp,
            command=self._update_solver_status
        )
        self.chk_prefer_pulp.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=5)
        
        # Поля ввода целей
        self.targets_entries: Dict[str, ttk.Entry] = {}
        self.tolerances_entries: Dict[str, ttk.Entry] = {}
        self.percentages_entries: Dict[str, ttk.Entry] = {}
        self.percentages_vars: Dict[str, tk.StringVar] = {}

        fields = [
            ("Ккал", "calories", "2000"),
            ("Белки (г)", "proteins", "100"),
            ("Жиры (г)", "fats", "80"),
            ("Углеводы (г)", "carbs", "250"),
            ("Цена (руб)", "price", "500")
        ]

        row = 2
        for label, key, default in fields:
            ttk.Label(left_frame, text=label).grid(row=row, column=0, sticky=tk.W, pady=2)

            # Цель
            ent_target = ttk.Entry(left_frame, width=10)
            ent_target.grid(row=row, column=1, padx=5, pady=2)
            ent_target.insert(0, default)
            self.targets_entries[key] = ent_target

            # Отклонение %
            ttk.Label(left_frame, text="±%").grid(row=row, column=2, sticky=tk.W)
            ent_tol = ttk.Entry(left_frame, width=5)
            ent_tol.grid(row=row, column=3, padx=5, pady=2)
            ent_tol.insert(0, "10")
            self.tolerances_entries[key] = ent_tol

            # Поле процента для БЖУ (не для калорий и цены)
            if key in ['proteins', 'fats', 'carbs']:
                ttk.Label(left_frame, text="% от ккал").grid(row=row, column=4, sticky=tk.W, padx=(10, 0))
                
                # Используем StringVar для отслеживания изменений
                pct_var = tk.StringVar(value="")
                self.percentages_vars[key] = pct_var
                
                ent_pct = ttk.Entry(left_frame, width=5, textvariable=pct_var)
                ent_pct.grid(row=row, column=5, padx=5, pady=2)
                self.percentages_entries[key] = ent_pct
                
                # Привязываем событие для динамического обновления суммы
                pct_var.trace_add('write', self._on_percentage_change)

            row += 1

        # Сумма процентов БЖУ
        sum_frame = ttk.LabelFrame(left_frame, text="Сумма процентов БЖУ", padding=5)
        sum_frame.grid(row=row, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=10)
        
        self.lbl_sum_pct = ttk.Label(sum_frame, text="0%", font=("Arial", 14, "bold"), foreground="green")
        self.lbl_sum_pct.grid(row=0, column=0, padx=10)
        
        self.lbl_sum_pct_bar = ttk.Label(sum_frame, text="", font=("Arial", 10))
        self.lbl_sum_pct_bar.grid(row=0, column=1, padx=10)

        # Структура питания
        struct_frame = ttk.LabelFrame(left_frame, text="Структура питания", padding=5)
        struct_frame.grid(row=row, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(struct_frame, text="Приемов пищи:").grid(row=0, column=0, padx=5)
        self.ent_meals = ttk.Entry(struct_frame, width=5)
        self.ent_meals.grid(row=0, column=1)
        self.ent_meals.insert(0, "3")

        ttk.Label(struct_frame, text="Блюд (мин):").grid(row=0, column=2, padx=10)
        self.ent_min_dishes = ttk.Entry(struct_frame, width=5)
        self.ent_min_dishes.grid(row=0, column=3)
        self.ent_min_dishes.insert(0, "1")

        ttk.Label(struct_frame, text="Блюд (макс):").grid(row=0, column=4, padx=10)
        self.ent_max_dishes = ttk.Entry(struct_frame, width=5)
        self.ent_max_dishes.grid(row=0, column=5)
        self.ent_max_dishes.insert(0, "2")

        # Кнопка расчета
        btn_calc = ttk.Button(left_frame, text="🔢 Рассчитать диету", 
                              command=self.run_calculation)
        btn_calc.grid(row=row+1, column=0, columnspan=4, pady=20, sticky=(tk.W, tk.E))
        
        # Кнопка очистки
        btn_clear = ttk.Button(left_frame, text="🗑 Очистить результат", 
                               command=self.clear_output)
        btn_clear.grid(row=row+2, column=0, columnspan=4, pady=5, sticky=(tk.W, tk.E))

    def _create_data_frame(self, parent):
        """Создает панель данных и результатов"""
        right_frame = ttk.LabelFrame(parent, text="Данные и Результат", padding=10)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(3, weight=1)

        ttk.Label(right_frame, text="📋 JSON список блюд:").grid(row=0, column=0, sticky=tk.W)
        
        self.txt_input = scrolledtext.ScrolledText(right_frame, height=10, width=60)
        self.txt_input.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Кнопки для работы с JSON
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(btn_frame, text="📥 Загрузить пример", 
                   command=self._load_sample_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✓ Проверить JSON", 
                   command=self._validate_json).pack(side=tk.LEFT, padx=5)

        ttk.Label(right_frame, text="📊 Результат (JSON):").grid(row=3, column=0, sticky=tk.W, pady=(10,0))
        self.txt_output = scrolledtext.ScrolledText(right_frame, height=10, width=60)
        self.txt_output.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Кнопка экспорта
        btn_export = ttk.Button(right_frame, text="💾 Сохранить в файл", 
                                command=self.export_result)
        btn_export.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)

    def _update_solver_status(self):
        """Обновляет статус решателя в интерфейсе"""
        if PULP_AVAILABLE:
            if self.prefer_pulp.get():
                status = "✅ PuLP доступен (будет использован)"
                self.lbl_solver_status.config(foreground="green")
            else:
                status = "⚠️ PuLP доступен (используется эвристика)"
                self.lbl_solver_status.config(foreground="orange")
        else:
            status = "❌ PuLP не установлен (используется эвристика)"
            self.lbl_solver_status.config(foreground="red")

        self.lbl_solver_status.config(text=status)

    def _on_percentage_change(self, *args):
        """Обработчик изменения процентов - обновляет сумму и валидирует"""
        total = 0
        for key in ['proteins', 'fats', 'carbs']:
            if key in self.percentages_vars:
                val = self.percentages_vars[key].get().strip()
                if val:
                    try:
                        total += float(val)
                    except ValueError:
                        pass

        # Обновляем отображение суммы
        self.lbl_sum_pct.config(text=f"{total:.1f}%")

        # Визуальная индикация
        if total > 100:
            self.lbl_sum_pct.config(foreground="red")
            self.lbl_sum_pct_bar.config(text="❌ Превышено 100%!", foreground="red")
        elif total == 100:
            self.lbl_sum_pct.config(foreground="green")
            self.lbl_sum_pct_bar.config(text="✅ Идеально!", foreground="green")
        elif total > 0:
            self.lbl_sum_pct.config(foreground="orange")
            remaining = 100 - total
            self.lbl_sum_pct_bar.config(text=f"Осталось: {remaining:.1f}%", foreground="orange")
        else:
            self.lbl_sum_pct.config(foreground="gray")
            self.lbl_sum_pct_bar.config(text="Не указано", foreground="gray")

    def _validate_percentages(self) -> bool:
        """Проверяет, что сумма процентов не превышает 100%"""
        total = 0
        for key in ['proteins', 'fats', 'carbs']:
            if key in self.percentages_entries:
                val = self.percentages_entries[key].get().strip()
                if val:
                    try:
                        total += float(val)
                    except ValueError:
                        messagebox.showerror("Ошибка ввода", f"Некорректное значение процента для {key}")
                        return False

        if total > 100:
            messagebox.showerror("Ошибка валидации", 
                f"Сумма процентов БЖУ не может превышать 100%!\n"
                f"Текущая сумма: {total:.1f}%")
            return False

        if total > 0 and total < 50:
            # Предупреждение, но не ошибка
            result = messagebox.askyesno("Предупреждение",
                f"Сумма процентов БЖУ составляет только {total:.1f}%.\n"
                f"Обычно рекомендуется 100%. Продолжить?")
            return result

        return True

    def _load_sample_data(self):
        """Загружает пример данных в поле ввода"""
        self.txt_input.delete("1.0", tk.END)
        self.txt_input.insert(tk.END, self.data_loader.get_sample_json())

    def _validate_json(self):
        """Проверяет корректность JSON"""
        json_data = self.txt_input.get("1.0", tk.END)
        dishes, error = self.data_loader.load_dishes_from_json(json_data)
        
        if error:
            messagebox.showerror("Ошибка JSON", error)
        else:
            messagebox.showinfo("OK", f"Загружено {len(dishes)} блюд")

    def clear_output(self):
        """Очищает поле результата"""
        self.txt_output.delete("1.0", tk.END)

    def export_result(self):
        """Экспортирует результат в JSON файл"""
        result_text = self.txt_output.get("1.0", tk.END).strip()
        if not result_text:
            messagebox.showwarning("Нет данных", "Сначала рассчитайте диету")
            return
        
        try:
            json.loads(result_text)
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Сохранить результат диеты"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result_text)
                messagebox.showinfo("Успех", f"Результат сохранен в:\n{file_path}")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Некорректный JSON для сохранения")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def _collect_parameters(self):
        """Собирает параметры из интерфейса"""
        try:
            targets = {k: float(v.get()) for k, v in self.targets_entries.items()}
            tolerances = {k: float(v.get()) for k, v in self.tolerances_entries.items()}
            num_meals = int(self.ent_meals.get())
            min_d = int(self.ent_min_dishes.get())
            max_d = int(self.ent_max_dishes.get())

            # Проверяем валидность процентов
            if not self._validate_percentages():
                return None

            # Считываем проценты для БЖУ
            percentages = {}
            for key in ['proteins', 'fats', 'carbs']:
                if key in self.percentages_entries:
                    pct_val = self.percentages_entries[key].get().strip()
                    percentages[f'{key}_pct'] = float(pct_val) if pct_val else 0.0
                else:
                    percentages[f'{key}_pct'] = 0.0

            if min_d > max_d:
                raise ValueError("Мин блюд не может быть больше макс")

            if num_meals < 1:
                raise ValueError("Количество приемов пищи должно быть >= 1")

            # Создаем объект цели с процентами
            target_params = {**targets, **percentages}
            target = DietTarget(**target_params)

            # Если проценты указаны, пересчитываем граммы
            if target.proteins_pct > 0 or target.fats_pct > 0 or target.carbs_pct > 0:
                target = target.resolve_macros()

            return (
                target,
                DietTolerance(**tolerances),
                MealStructure(num_meals, min_d, max_d)
            )

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return None

    def run_calculation(self):
        """Запускает расчет диеты"""
        # Сбор параметров
        params = self._collect_parameters()
        if not params:
            return
        
        target, tolerance, structure = params

        # Загрузка блюд
        json_data = self.txt_input.get("1.0", tk.END)
        dishes, error = self.data_loader.load_dishes_from_json(json_data)
        
        if error:
            messagebox.showerror("Ошибка данных", error)
            return
        
        self.dishes = dishes

        # Создание решателя через фабрику
        self.solver = SolverFactory.create(self.dishes, self.prefer_pulp.get())
        method_name = SolverFactory.get_method_name()

        # Запуск расчета
        try:
            self.root.config(cursor="watch")
            self.root.update()
            
            result = self.solver.solve(target, tolerance, structure)
            
            # Вывод результата
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert(tk.END, json.dumps(result, ensure_ascii=False, indent=2))
            
            if result.get('status') == 'success':
                method_used = result.get('method', 'Unknown')
                messagebox.showinfo("Готово", 
                    f"Диета рассчитана!\n"
                    f"Метод: {method_used}\n"
                    f"Общая цена: {result.get('total_price', 0)} руб.\n"
                    f"Общий вес: {result.get('total_weight', 0)} г")
            else:
                messagebox.showwarning("Внимание", result.get('message', 'Ошибка расчета'))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        finally:
            self.root.config(cursor="")