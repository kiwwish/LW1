import re

class TelegraphAlphabet:

    # Определение русского телеграфного алфавита
    def __init__(self):
        # 32 символа русского алфавита (без Ё и Ъ) и пробел
        self.symbols = [
            'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З',
            'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П',
            'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч',
            'Ш', 'Щ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', '_'
        ]

        # Создаем словари для быстрого доступа
        self.char_to_val = {char: idx for idx, char in enumerate(self.symbols)}
        self.val_to_char = {idx: char for idx, char in enumerate(self.symbols)}

    # Получение символа по значению (0-31)
    def get_char(self, value: int) -> str:
        return self.val_to_char.get(value % 32, '?')

    # Получние значения по символу
    def get_value(self, char: str) -> int:
        return self.char_to_val.get(char.upper(), 0)

    # Суммирование символов по модулю 32
    def add(self, char1: str, char2: str) -> str:
        val1 = self.get_value(char1)
        val2 = self.get_value(char2)
        result = (val1 + val2) % 32
        return self.get_char(result)

    # Вычитание символов по модулю 32
    def subtract(self, char1: str, char2: str) -> str:
        val1 = self.get_value(char1)
        val2 = self.get_value(char2)
        result = (val1 - val2) % 32
        return self.get_char(result)

    # Проверка на пренадлежность к алфавиту
    def is_valid_char(self, char: str) -> bool:
        return char.upper() in self.char_to_val