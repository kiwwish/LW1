from alphabet import TelegraphAlphabet, CustomAlphabet
from tritemius import TritemiusCipher, TextCipher


class SBlock:
    """S-блоки для преобразования блоков по 4 символа"""

    def __init__(self, alphabet: TelegraphAlphabet):
        self.alphabet = alphabet
        # Создаем S-бокс (таблицу замены)
        self.sbox = self._create_sbox()
        self.inv_sbox = {v: k for k, v in self.sbox.items()}

    def _create_sbox(self):
        """Создание S-бокса (нелинейное преобразование)"""
        sbox = {}
        # Пример: циклический сдвиг на позицию + умножение
        for i in range(32):
            # Нелинейное преобразование: (value * 7 + 3) % 32
            new_val = (i * 7 + 3) % 32
            sbox[self.alphabet.get_char(i)] = self.alphabet.get_char(new_val)
        return sbox

    def apply_sbox(self, block: str) -> str:
        """Применение S-блока к блоку из 4 символов"""
        if len(block) != 4:
            raise ValueError(f"Блок должен содержать 4 символа, получено {len(block)}")

        result = []
        for i, char in enumerate(block):
            if self.alphabet.is_valid_char(char):
                # Разное преобразование в зависимости от позиции
                transformed = self._sbox_transform(char, i)
                result.append(transformed)
            else:
                result.append(char)

        return ''.join(result)

    def _sbox_transform(self, char: str, position: int) -> str:
        """Преобразование символа с учетом позиции в блоке"""
        # Базовое преобразование из S-бокса
        base = self.sbox.get(char, char)

        # Дополнительный сдвиг в зависимости от позиции
        val = self.alphabet.get_value(base)
        shift = (position * 5) % 32  # Разный сдвиг для каждой позиции
        new_val = (val + shift) % 32

        return self.alphabet.get_char(new_val)

    def apply_inverse_sbox(self, block: str) -> str:
        """Обратное преобразование S-блока"""
        if len(block) != 4:
            raise ValueError(f"Блок должен содержать 4 символа, получено {len(block)}")

        result = []
        for i, char in enumerate(block):
            if self.alphabet.is_valid_char(char):
                # Сначала убираем позиционный сдвиг
                val = self.alphabet.get_value(char)
                shift = (i * 5) % 32
                base_val = (val - shift) % 32
                base_char = self.alphabet.get_char(base_val)

                # Затем обратное преобразование S-бокса
                original = self.inv_sbox.get(base_char, base_char)
                result.append(original)
            else:
                result.append(char)

        return ''.join(result)


class EnhancedCryptoSystem:
    """Усиленная криптосистема с S-блоками"""

    def __init__(self, shift: int = 8):
        self.alphabet = TelegraphAlphabet()
        self.cipher = TritemiusCipher(shift=shift)
        self.text_cipher = TextCipher(self.cipher)
        self.sblock = SBlock(self.alphabet)

    # Метод для обычного шифра Тритемиуса
    def encrypt_simple(self, text: str, key_word: str) -> str:
        """
        Обычное шифрование Тритемиуса
        """
        return self.text_cipher.encrypt_text(text, key_word)

    def decrypt_simple(self, text: str, key_word: str) -> str:
        """Дешифрование обычного шифра Тритемиуса"""
        return self.text_cipher.decrypt_text(text, key_word)

    # Метод для шифрования с усиленными S-блоками
    def encrypt_enhanced_sblocks(self, text: str, key_word: str) -> str:
        """
        Усиленное шифрование с S-блоками

        Шаги:
        1. Шифруем обычным шифром Тритемиуса
        2. Разбиваем на блоки по 4 символа
        3. Применяем S-блок к каждому блоку
        """
        if not key_word:
            return text

        # Сначала шифруем обычным шифром Тритемиуса
        encrypted = self.encrypt_simple(text, key_word)

        # Дополняем текст до кратности 4 символом '_'
        while len(encrypted) % 4 != 0:
            encrypted += '_'

        # Применяем S-блоки
        result_blocks = []
        for i in range(0, len(encrypted), 4):
            block = encrypted[i:i + 4]
            sbox_block = self.sblock.apply_sbox(block)
            result_blocks.append(sbox_block)

        return ''.join(result_blocks)

    # Метод для дешифрования с усиленными S-блоками
    def decrypt_enhanced_sblocks(self, text: str, key_word: str) -> str:
        """
        Дешифрование усиленного шифрования с S-блоками

        Шаги:
        1. Применяем обратный S-блок
        2. Дешифруем обычным шифром Тритемиуса
        """
        if not key_word:
            return text

        # Проверяем, что текст кратен 4
        if len(text) % 4 != 0:
            # Дополняем до кратности 4
            padded_text = text
            while len(padded_text) % 4 != 0:
                padded_text += '_'
        else:
            padded_text = text

        # Применяем обратный S-блок
        decrypted_blocks = []
        for i in range(0, len(padded_text), 4):
            block = padded_text[i:i + 4]
            sbox_block = self.sblock.apply_inverse_sbox(block)
            decrypted_blocks.append(sbox_block)

        decrypted = ''.join(decrypted_blocks)

        # Убираем возможное дополнение
        decrypted = decrypted.rstrip('_')

        # Дешифруем обычным шифром Тритемиуса
        return self.decrypt_simple(decrypted, key_word)

    # Метод для полиалфавитного шифра (оставлен для совместимости)
    def encrypt_polyalphabetic(self, text: str, key_word: str, shift: int = 8) -> str:
        """Полиалфавитное шифрование (для совместимости с GUI)"""
        # В данном случае просто используем обычное шифрование
        # так как в классическом шифре Тритемиуса нет полиалфавитного варианта
        return self.encrypt_simple(text, key_word)

    def decrypt_polyalphabetic(self, text: str, key_word: str, shift: int = 8) -> str:
        """Дешифрование полиалфавитного шифра (для совместимости с GUI)"""
        return self.decrypt_simple(text, key_word)