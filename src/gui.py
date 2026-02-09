"""
Графический интерфейс для криптосистемы Тритемиуса
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from sblocks import EnhancedCryptoSystem
from tritemius import get_custom_alphabet_string


class CryptoApp:
    """Главное окно приложения с 4 вкладками"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Криптосистема Тритемиуса")
        self.root.geometry("1000x800")

        # Создаем криптосистему
        self.system = EnhancedCryptoSystem()

        self.setup_ui()

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""

        # Создаем Notebook (вкладки)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Вкладка 1: Обычный шифр Тритемиуса
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Обычный шифр Тритемиуса")
        self._setup_tab1(tab1)

        # Вкладка 2: Полиалфавитный шифр (оставлен для совместимости)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Полиалфавитный шифр")
        self._setup_tab2(tab2)

        # Вкладка 3: S-блоки
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="S-блоки")
        self._setup_tab3(tab3)

        # Вкладка 4: Усиленные S-блоки
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="Усиленные S-блоки")
        self._setup_tab4(tab4)

        # Статус бар
        self.status_bar = ttk.Label(self.root, text="Готово", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # ===== ВКЛАДКА 1: Обычный шифр Тритемиуса =====
    def _setup_tab1(self, parent):
        """Настройка вкладки 1: Обычный шифр Тритемиуса"""

        # Левая часть: Шифрование
        left_frame = ttk.LabelFrame(parent, text="Шифрование", padding=10)
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        # Ключ
        ttk.Label(left_frame, text="Ключевое слово:").pack(anchor='w', pady=(0, 5))
        self.tab1_key = ttk.Entry(left_frame)
        self.tab1_key.pack(fill='x', pady=(0, 5))

        # Кнопка для просмотра алфавита
        ttk.Button(left_frame, text="ПОСМОТРЕТЬ АЛФАВИТ",
                  command=self.show_alphabet_tab1).pack(pady=(0, 10))

        # Исходный текст
        ttk.Label(left_frame, text="Исходный текст:").pack(anchor='w', pady=(0, 5))
        self.tab1_input = scrolledtext.ScrolledText(left_frame, height=8)
        self.tab1_input.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка шифрования
        ttk.Button(left_frame, text="ЗАШИФРОВАТЬ",
                  command=self.tab1_encrypt,
                  style='Accent.TButton').pack(pady=5)

        # Результат шифрования
        ttk.Label(left_frame, text="Результат шифрования:").pack(anchor='w', pady=(10, 5))
        self.tab1_result = scrolledtext.ScrolledText(left_frame, height=8)
        self.tab1_result.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка копирования
        ttk.Button(left_frame, text="КОПИРОВАТЬ РЕЗУЛЬТАТ",
                  command=self.tab1_copy_result).pack(pady=5)

        # Правая часть: Дешифрование
        right_frame = ttk.LabelFrame(parent, text="Дешифрование", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        # Зашифрованный текст
        ttk.Label(right_frame, text="Зашифрованный текст:").pack(anchor='w', pady=(0, 5))
        self.tab1_cipher_input = scrolledtext.ScrolledText(right_frame, height=8)
        self.tab1_cipher_input.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка дешифрования
        ttk.Button(right_frame, text="РАСШИФРОВАТЬ",
                  command=self.tab1_decrypt,
                  style='Accent.TButton').pack(pady=5)

        # Результат дешифрования
        ttk.Label(right_frame, text="Расшифрованный текст:").pack(anchor='w', pady=(10, 5))
        self.tab1_decrypt_result = scrolledtext.ScrolledText(right_frame, height=8)
        self.tab1_decrypt_result.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка копирования
        ttk.Button(right_frame, text="КОПИРОВАТЬ РЕЗУЛЬТАТ",
                  command=self.tab1_copy_decrypt_result).pack(pady=5)

    def show_alphabet_tab1(self):
        """Показать алфавит на основе ключа для вкладки 1"""
        key = self.tab1_key.get().strip()
        if not key:
            messagebox.showinfo("Алфавит", "Введите ключ для построения алфавита")
            return

        alphabet_str = get_custom_alphabet_string(key)
        messagebox.showinfo("Пользовательский алфавит",
                           f"Алфавит на основе ключа '{key}':\n\n{alphabet_str}")

    def tab1_encrypt(self):
        """Шифрование для вкладки 1"""
        try:
            key = self.tab1_key.get().strip()
            text = self.tab1_input.get("1.0", tk.END).strip()

            if not key:
                messagebox.showwarning("Ошибка", "Введите ключевое слово!")
                return

            if not text:
                messagebox.showwarning("Ошибка", "Введите текст для шифрования!")
                return

            result = self.system.encrypt_simple(text, key)
            self.tab1_result.delete("1.0", tk.END)
            self.tab1_result.insert("1.0", result)
            self.status_bar.config(text="Текст зашифрован (обычный шифр Тритемиуса)")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def tab1_decrypt(self):
        """Дешифрование для вкладки 1"""
        try:
            key = self.tab1_key.get().strip()
            text = self.tab1_cipher_input.get("1.0", tk.END).strip()

            if not key:
                messagebox.showwarning("Ошибка", "Введите ключевое слово!")
                return

            if not text:
                messagebox.showwarning("Ошибка", "Введите шифротекст!")
                return

            result = self.system.decrypt_simple(text, key)
            self.tab1_decrypt_result.delete("1.0", tk.END)
            self.tab1_decrypt_result.insert("1.0", result)
            self.status_bar.config(text="Текст расшифрован (обычный шифр Тритемиуса)")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def tab1_copy_result(self):
        """Копирование результата шифрования"""
        result = self.tab1_result.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_bar.config(text="Результат скопирован в буфер обмена")

    def tab1_copy_decrypt_result(self):
        """Копирование результата дешифрования"""
        result = self.tab1_decrypt_result.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_bar.config(text="Результат скопирован в буфер обмена")

    # ===== ВКЛАДКА 2: Полиалфавитный шифр =====
    def _setup_tab2(self, parent):
        """Настройка вкладки 2: Полиалфавитный шифр (оставлен для совместимости)"""

        # Левая часть: Шифрование
        left_frame = ttk.LabelFrame(parent, text="Шифрование", padding=10)
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        # Ключ
        ttk.Label(left_frame, text="Ключевое слово:").pack(anchor='w', pady=(0, 5))
        self.tab2_key = ttk.Entry(left_frame)
        self.tab2_key.pack(fill='x', pady=(0, 5))

        # Сдвиг
        ttk.Label(left_frame, text="Сдвиг (обычно 8):").pack(anchor='w', pady=(10, 5))
        self.tab2_shift = ttk.Spinbox(left_frame, from_=1, to=31, width=10)
        self.tab2_shift.set(8)
        self.tab2_shift.pack(fill='x', pady=(0, 10))

        # Исходный текст
        ttk.Label(left_frame, text="Исходный текст:").pack(anchor='w', pady=(0, 5))
        self.tab2_input = scrolledtext.ScrolledText(left_frame, height=8)
        self.tab2_input.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка шифрования
        ttk.Button(left_frame, text="ЗАШИФРОВАТЬ",
                  command=self.tab2_encrypt,
                  style='Accent.TButton').pack(pady=5)

        # Результат шифрования
        ttk.Label(left_frame, text="Результат шифрования:").pack(anchor='w', pady=(10, 5))
        self.tab2_result = scrolledtext.ScrolledText(left_frame, height=8)
        self.tab2_result.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка копирования
        ttk.Button(left_frame, text="КОПИРОВАТЬ РЕЗУЛЬТАТ",
                  command=self.tab2_copy_result).pack(pady=5)

        # Правая часть: Дешифрование
        right_frame = ttk.LabelFrame(parent, text="Дешифрование", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        # Зашифрованный текст
        ttk.Label(right_frame, text="Зашифрованный текст:").pack(anchor='w', pady=(0, 5))
        self.tab2_cipher_input = scrolledtext.ScrolledText(right_frame, height=8)
        self.tab2_cipher_input.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка дешифрования
        ttk.Button(right_frame, text="РАСШИФРОВАТЬ",
                  command=self.tab2_decrypt,
                  style='Accent.TButton').pack(pady=5)

        # Результат дешифрования
        ttk.Label(right_frame, text="Расшифрованный текст:").pack(anchor='w', pady=(10, 5))
        self.tab2_decrypt_result = scrolledtext.ScrolledText(right_frame, height=8)
        self.tab2_decrypt_result.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка копирования
        ttk.Button(right_frame, text="КОПИРОВАТЬ РЕЗУЛЬТАТ",
                  command=self.tab2_copy_decrypt_result).pack(pady=5)

    def tab2_encrypt(self):
        """Шифрование для вкладки 2"""
        try:
            key = self.tab2_key.get().strip()
            shift_text = self.tab2_shift.get().strip()
            shift = int(shift_text) if shift_text else 8
            text = self.tab2_input.get("1.0", tk.END).strip()

            if not key:
                messagebox.showwarning("Ошибка", "Введите ключевое слово!")
                return

            if not text:
                messagebox.showwarning("Ошибка", "Введите текст для шифрования!")
                return

            # Создаем новую систему с указанным сдвигом
            system = EnhancedCryptoSystem(shift=shift)
            result = system.encrypt_polyalphabetic(text, key, shift)
            self.tab2_result.delete("1.0", tk.END)
            self.tab2_result.insert("1.0", result)
            self.status_bar.config(text=f"Текст зашифрован (полиалфавитный, сдвиг={shift})")

        except ValueError:
            messagebox.showwarning("Ошибка", "Сдвиг должен быть числом от 1 до 31!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def tab2_decrypt(self):
        """Дешифрование для вкладки 2"""
        try:
            key = self.tab2_key.get().strip()
            shift_text = self.tab2_shift.get().strip()
            shift = int(shift_text) if shift_text else 8
            text = self.tab2_cipher_input.get("1.0", tk.END).strip()

            if not key:
                messagebox.showwarning("Ошибка", "Введите ключевое слово!")
                return

            if not text:
                messagebox.showwarning("Ошибка", "Введите шифротекст!")
                return

            # Создаем новую систему с указанным сдвигом
            system = EnhancedCryptoSystem(shift=shift)
            result = system.decrypt_polyalphabetic(text, key, shift)
            self.tab2_decrypt_result.delete("1.0", tk.END)
            self.tab2_decrypt_result.insert("1.0", result)
            self.status_bar.config(text=f"Текст расшифрован (полиалфавитный, сдвиг={shift})")

        except ValueError:
            messagebox.showwarning("Ошибка", "Сдвиг должен быть числом от 1 до 31!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def tab2_copy_result(self):
        """Копирование результата шифрования"""
        result = self.tab2_result.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_bar.config(text="Результат скопирован в буфер обмена")

    def tab2_copy_decrypt_result(self):
        """Копирование результата дешифрования"""
        result = self.tab2_decrypt_result.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_bar.config(text="Результат скопирован в буфер обмена")

    # ===== ВКЛАДКА 3: S-блоки =====
    def _setup_tab3(self, parent):
        """Настройка вкладки 3: S-блоки (по псевдокоду)"""

        # Верхняя часть: Прямой S-блок
        top_frame = ttk.LabelFrame(parent, text="Шифрование S-блоками", padding=10)
        top_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Ключ (16 символов)
        ttk.Label(top_frame, text="Ключ (ровно 16 символов):").pack(anchor='w', pady=(0, 5))
        self.tab3_key = ttk.Entry(top_frame)
        self.tab3_key.pack(fill='x', pady=(0, 10))

        # Исходный текст для S-блоков
        ttk.Label(top_frame, text="Текст (должен быть кратен 4 символам):").pack(anchor='w', pady=(0, 5))
        self.tab3_input = scrolledtext.ScrolledText(top_frame, height=6)
        self.tab3_input.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка для шифрования S-блоками
        ttk.Button(top_frame, text="ЗАШИФРОВАТЬ S-БЛОКАМИ",
                   command=self.tab3_encrypt_sblocks,
                   style='Accent.TButton').pack(pady=5)

        # Результат шифрования
        ttk.Label(top_frame, text="Результат шифрования:").pack(anchor='w', pady=(10, 5))
        self.tab3_result = scrolledtext.ScrolledText(top_frame, height=6)
        self.tab3_result.pack(fill='both', expand=True, pady=(0, 10))

        # Нижняя часть: Дешифрование S-блоков
        bottom_frame = ttk.LabelFrame(parent, text="Дешифрование S-блоков", padding=10)
        bottom_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Ключ для дешифрования
        ttk.Label(bottom_frame, text="Ключ (ровно 16 символов):").pack(anchor='w', pady=(0, 5))
        self.tab3_key2 = ttk.Entry(bottom_frame)
        self.tab3_key2.pack(fill='x', pady=(0, 10))

        # Зашифрованный текст для дешифрования
        ttk.Label(bottom_frame, text="Зашифрованный текст:").pack(anchor='w', pady=(0, 5))
        self.tab3_cipher_input = scrolledtext.ScrolledText(bottom_frame, height=6)
        self.tab3_cipher_input.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка для дешифрования S-блоками
        ttk.Button(bottom_frame, text="РАСШИФРОВАТЬ S-БЛОКАМИ",
                   command=self.tab3_decrypt_sblocks,
                   style='Accent.TButton').pack(pady=5)

        # Результат дешифрования
        ttk.Label(bottom_frame, text="Результат дешифрования:").pack(anchor='w', pady=(10, 5))
        self.tab3_decrypt_result = scrolledtext.ScrolledText(bottom_frame, height=6)
        self.tab3_decrypt_result.pack(fill='both', expand=True)

    def tab3_encrypt_sblocks(self):
        """Шифрование S-блоками (по псевдокоду)"""
        try:
            key = self.tab3_key.get().strip()
            text = self.tab3_input.get("1.0", tk.END).strip()

            if not key:
                messagebox.showwarning("Ошибка", "Введите ключ (16 символов)!")
                return

            if not text:
                messagebox.showwarning("Ошибка", "Введите текст для шифрования!")
                return

            # Проверяем длину ключа
            if len(key) != 16:
                messagebox.showwarning("Ошибка", "Ключ должен содержать ровно 16 символов!")
                return

            # Проверяем, что текст кратен 4
            if len(text) % 4 != 0:
                messagebox.showwarning("Ошибка", "Текст должен быть кратен 4 символам!")
                return

            result = self.system.encrypt_s_blocks(text, key)
            self.tab3_result.delete("1.0", tk.END)
            self.tab3_result.insert("1.0", result)
            self.status_bar.config(text="Текст зашифрован S-блоками")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def tab3_decrypt_sblocks(self):
        """Дешифрование S-блоками (по псевдокоду)"""
        try:
            key = self.tab3_key2.get().strip()
            text = self.tab3_cipher_input.get("1.0", tk.END).strip()

            if not key:
                messagebox.showwarning("Ошибка", "Введите ключ (16 символов)!")
                return

            if not text:
                messagebox.showwarning("Ошибка", "Введите шифротекст!")
                return

            # Проверяем длину ключа
            if len(key) != 16:
                messagebox.showwarning("Ошибка", "Ключ должен содержать ровно 16 символов!")
                return

            # Проверяем, что текст кратен 4
            if len(text) % 4 != 0:
                messagebox.showwarning("Ошибка", "Текст должен быть кратен 4 символам!")
                return

            result = self.system.decrypt_s_blocks(text, key)
            self.tab3_decrypt_result.delete("1.0", tk.END)
            self.tab3_decrypt_result.insert("1.0", result)
            self.status_bar.config(text="Текст расшифрован S-блоками")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    # ===== ВКЛАДКА 4: Усиленные S-блоки =====
    def _setup_tab4(self, parent):
        """Настройка вкладки 4: Усиленные S-блоки"""

        # Верхняя часть: Усиленный S-блок
        top_frame = ttk.LabelFrame(parent, text="Усиленный S-блок", padding=10)
        top_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Ключ
        ttk.Label(top_frame, text="Ключевое слово:").pack(anchor='w', pady=(0, 5))
        self.tab4_key = ttk.Entry(top_frame)
        self.tab4_key.pack(fill='x', pady=(0, 10))

        # Исходный текст для усиленного S-блока
        ttk.Label(top_frame, text="Исходный текст:").pack(anchor='w', pady=(0, 5))
        self.tab4_input = scrolledtext.ScrolledText(top_frame, height=6)
        self.tab4_input.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка для усиленного S-блока
        ttk.Button(top_frame, text="ЗАШИФРОВАТЬ С УСИЛЕННЫМИ S-БЛОКАМИ",
                  command=self.tab4_apply_enhanced_sbox,
                  style='Accent.TButton').pack(pady=5)

        # Результат усиленного S-блока
        ttk.Label(top_frame, text="Результат шифрования:").pack(anchor='w', pady=(10, 5))
        self.tab4_result = scrolledtext.ScrolledText(top_frame, height=6)
        self.tab4_result.pack(fill='both', expand=True, pady=(0, 10))

        # Нижняя часть: Дешифрование усиленного S-блока
        bottom_frame = ttk.LabelFrame(parent, text="Дешифрование усиленного S-блока", padding=10)
        bottom_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Ключ для дешифрования
        ttk.Label(bottom_frame, text="Ключевое слово:").pack(anchor='w', pady=(0, 5))
        self.tab4_key2 = ttk.Entry(bottom_frame)
        self.tab4_key2.pack(fill='x', pady=(0, 10))

        # Зашифрованный текст для дешифрования
        ttk.Label(bottom_frame, text="Зашифрованный текст:").pack(anchor='w', pady=(0, 5))
        self.tab4_cipher_input = scrolledtext.ScrolledText(bottom_frame, height=6)
        self.tab4_cipher_input.pack(fill='both', expand=True, pady=(0, 10))

        # Кнопка для дешифрования
        ttk.Button(bottom_frame, text="РАСШИФРОВАТЬ С УСИЛЕННЫМИ S-БЛОКАМИ",
                  command=self.tab4_apply_inverse_enhanced_sbox,
                  style='Accent.TButton').pack(pady=5)

        # Результат дешифрования
        ttk.Label(bottom_frame, text="Результат дешифрования:").pack(anchor='w', pady=(10, 5))
        self.tab4_decrypt_result = scrolledtext.ScrolledText(bottom_frame, height=6)
        self.tab4_decrypt_result.pack(fill='both', expand=True)

    def tab4_apply_enhanced_sbox(self):
        """Применение усиленного S-блока"""
        try:
            key = self.tab4_key.get().strip()
            text = self.tab4_input.get("1.0", tk.END).strip()

            if not text:
                messagebox.showwarning("Ошибка", "Введите текст!")
                return

            if not key:
                messagebox.showwarning("Ошибка", "Введите ключевое слово!")
                return

            # Полное шифрование с усиленными S-блоками
            result = self.system.encrypt_enhanced_sblocks(text, key)
            self.tab4_result.delete("1.0", tk.END)
            self.tab4_result.insert("1.0", result)
            self.status_bar.config(text="Текст зашифрован с усиленными S-блоками")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def tab4_apply_inverse_enhanced_sbox(self):
        """Применение обратного усиленного S-блока"""
        try:
            key = self.tab4_key2.get().strip()
            text = self.tab4_cipher_input.get("1.0", tk.END).strip()

            if not text:
                messagebox.showwarning("Ошибка", "Введите зашифрованный текст!")
                return

            if not key:
                messagebox.showwarning("Ошибка", "Введите ключевое слово!")
                return

            # Полное дешифрование с усиленными S-блоками
            result = self.system.decrypt_enhanced_sblocks(text, key)
            self.tab4_decrypt_result.delete("1.0", tk.END)
            self.tab4_decrypt_result.insert("1.0", result)
            self.status_bar.config(text="Текст расшифрован с усиленными S-блоками")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def run(self):
        """Запуск приложения"""
        # Настройка стилей
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'), foreground='blue')

        self.root.mainloop()


# Точка входа в приложение
if __name__ == "__main__":
    app = CryptoApp()
    app.run()