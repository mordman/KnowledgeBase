#!/usr/bin/env python3
"""Тест применения шаблонов."""

from config.settings_manager import load_settings, apply_template, save_settings, get_default_settings

def test_templates():
    """Проверяет работу шаблонов."""
    print("🧪 Тестирование шаблонов...\n")
    
    settings = load_settings()
    print(f"✅ Настройки загружены")
    print(f"   Текущий шаблон: {settings.get('current_template', 'N/A')}")
    print(f"   Доступно шаблонов: {len(settings.get('templates', {}))}\n")
    
    # Тест применения каждого шаблона
    for key in ['mini', 'standard', 'large', 'dark', 'light']:
        test_settings = load_settings()
        result = apply_template(test_settings, key)
        print(f"{'✅' if result else '❌'} Шаблон '{key}': {'применён' if result else 'ошибка'}")
        
        if result:
            print(f"   cell_width: {test_settings.get('cell_width')}")
            print(f"   cell_height: {test_settings.get('cell_height')}")
    
    print("\n🎉 Тест завершён!")

if __name__ == "__main__":
    test_templates()