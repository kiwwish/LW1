import re


class TelegraphAlphabet:

    def __init__(self):
        # Алфавит из методички: 31 буква + '_'
        self.symbols = [
            'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З',
            'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П',
            'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч',
            'Ш', 'Щ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', '_'
        ]

        # Создаем словари для быстрого доступа
        self.char_to_val = {char: idx for idx, char in enumerate(self.symbols)}
        self.val_to_char = {idx: char for idx, char in enumerate(self.symbols)}

    def get_char(self, value: int) -> str:
        """Получить символ по значению (0-31)"""
        return self.val_to_char.get(value % 32, '?')

    def get_value(self, char: str) -> int:
        """Получить значение по символу"""
        return self.char_to_val.get(char.upper(), 0)

    def add(self, char1: str, char2: str) -> str:
        """Суммирование символов по модулю 32"""
        val1 = self.get_value(char1)
        val2 = self.get_value(char2)
        result = (val1 + val2) % 32
        return self.get_char(result)

    def subtract(self, char1: str, char2: str) -> str:
        """Вычитание символов по модулю 32"""
        val1 = self.get_value(char1)
        val2 = self.get_value(char2)
        result = (val1 - val2) % 32
        return self.get_char(result)

    def is_valid_char(self, char: str) -> bool:
        """Проверка, является ли символ допустимым"""
        return char.upper() in self.char_to_val

    def get_all_symbols(self):
        """Получить все символы алфавита"""
        return self.symbols


class CustomAlphabet:
    """Класс для создания пользовательского алфавита на основе ключа"""

    def __init__(self, key):
        """
        Инициализация пользовательского алфавита

        Args:
            key (str): Ключевое слово для построения алфавита
        """
        self.key = key.upper()
        self.standard_alphabet = TelegraphAlphabet()
        self.custom_symbols = self._build_custom_alphabet()
        self.char_to_val = {char: idx for idx, char in enumerate(self.custom_symbols)}
        self.val_to_char = {idx: char for idx, char in enumerate(self.custom_symbols)}

    def _prepare_key(self):
        """Подготовка ключа: удаление дубликатов с сохранением порядка"""
        seen = set()
        unique_key = []
        for char in self.key:
            if char not in seen and self.standard_alphabet.is_valid_char(char):
                seen.add(char)
                unique_key.append(char)
        return ''.join(unique_key)

    def _build_custom_alphabet(self):
        """Построение нового алфавита по ключу"""
        unique_key = self._prepare_key()
        custom_alpha = list(unique_key)

        # Добавляем буквы из стандартного алфавита, которых нет в ключе
        for char in self.standard_alphabet.get_all_symbols():
            if char not in custom_alpha:
                custom_alpha.append(char)

        return custom_alpha



