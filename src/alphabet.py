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


class PolyAlphabet:
    """Алфавит для полиалфавитного шифра Тритемиуса (с заменой дубликатов)"""

    def __init__(self, key, standard_alphabet=None):
        """
        Инициализация полиалфавита

        Args:
            key (str): Ключевое слово
            standard_alphabet: Базовый алфавит (по умолчанию TelegraphAlphabet)
        """
        if standard_alphabet is None:
            standard_alphabet = TelegraphAlphabet()

        self.standard_alphabet = standard_alphabet
        self.key = key.upper()
        self.custom_symbols = self._build_poly_alphabet()
        self.char_to_val = {char: idx for idx, char in enumerate(self.custom_symbols)}
        self.val_to_char = {idx: char for idx, char in enumerate(self.custom_symbols)}

    def _build_poly_alphabet(self):
        """Построение алфавита по алгоритму Thrithemus_table"""
        out = []

        for i in range(len(self.key)):
            tmp = self.key[i]
            # Пока символ уже есть в out, увеличиваем его на 1
            while self._char_in_list(tmp, out):
                # Получаем следующий символ по стандартному алфавиту
                val = self.standard_alphabet.get_value(tmp)
                next_val = (val + 1) % 32
                tmp = self.standard_alphabet.get_char(next_val)

            # Добавляем символ, только если алфавит ещё не заполнен
            if len(out) < 32:
                out.append(tmp)

        # Добавляем остальные символы стандартного алфавита
        for i in range(32):
            char = self.standard_alphabet.get_char(i)
            if not self._char_in_list(char, out):
                out.append(char)

        return out

    def _char_in_list(self, char, char_list):
        """Проверка, есть ли символ в списке"""
        return char in char_list

    def shift_table(self, table, sym_in, bias_in):
        """
        Реализация shift_Trithemus

        Args:
            table: текущая таблица (список символов)
            sym_in: символ, который должен стать первым
            bias_in: смещение для разделения таблицы

        Returns:
            Новая таблица
        """
        s = sym_in
        str_part = table[bias_in:]  # часть с bias_in до конца
        rem_part = table[:bias_in]  # первые bias_in символов

        # Пока s находится в rem_part, увеличиваем s
        while s in rem_part:
            val = self.standard_alphabet.get_value(s)
            next_val = (val + 1) % 32
            s = self.standard_alphabet.get_char(next_val)

        # Находим позицию s в str_part
        if s not in str_part:
            # Если s нет в str_part, ищем первый доступный символ
            for char in str_part:
                if char not in rem_part:
                    s = char
                    break

        x = str_part.index(s)

        # Удаляем s из str_part
        str_part = str_part[:x] + str_part[x + 1:]

        # Собираем новую таблицу
        new_table = [s] + rem_part + str_part
        return new_table