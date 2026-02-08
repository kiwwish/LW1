
import sys
import os

# Добавляем папку src в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def main():
    """Запуск графического интерфейса"""
    try:
        from gui import CryptoApp

        print("Запуск криптосистемы Тритемиуса...")
        app = CryptoApp()
        app.run()

    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("\nУбедитесь, что у вас есть следующие файлы:")
        print("1. src/alphabet.py")
        print("2. src/tritemius.py")
        print("3. src/sblocks.py (обновленный)")
        print("4. src/gui.py")
        print("\nИ что в папке src есть файл __init__.py")
        input("\nНажмите Enter для выхода...")


if __name__ == "__main__":
    main()