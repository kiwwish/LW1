from alphabet import TelegraphAlphabet
from tritemius import PolyAlphabeticCipher, TritemiusCipher


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
        self.cipher = TritemiusCipher(self.alphabet, shift=shift)
        self.poly_cipher = PolyAlphabeticCipher(self.alphabet, self.cipher)
        self.sblock = SBlock(self.alphabet)

    # Метод для обычного шифра Тритемиуса (без ключа, только позиционный сдвиг)
    def encrypt_simple(self, text: str, key_word: str) -> str:
        """
        Обычное шифрование Тритемиуса
        (ключ игнорируется, используется только позиционный сдвиг)
        """
        result = []

        for i, char in enumerate(text.upper()):
            if self.alphabet.is_valid_char(char):
                # В оригинале Тритемиуса: сдвиг = позиция * 8
                encrypted = self.cipher.encrypt_char(char, i)
                result.append(encrypted)
            else:
                result.append(char)

        return ''.join(result)

    def decrypt_simple(self, text: str, key_word: str) -> str:
        """Дешифрование обычного шифра Тритемиуса"""
        result = []

        for i, char in enumerate(text.upper()):
            if self.alphabet.is_valid_char(char):
                decrypted = self.cipher.decrypt_char(char, i)
                result.append(decrypted)
            else:
                result.append(char)

        return ''.join(result)

    # Метод для полиалфавитного шифра Тритемиуса
    def encrypt_polyalphabetic(self, text: str, key_word: str, shift: int = 8) -> str:
        """
        Полиалфавитное шифрование Тритемиуса
        сдвиг = позиция * базовый_сдвиг + значение_символа_ключа
        """
        return self.poly_cipher.encrypt_text_polyalphabetic(text, key_word)

    def decrypt_polyalphabetic(self, text: str, key_word: str, shift: int = 8) -> str:
        """Дешифрование полиалфавитного шифра Тритемиуса"""
        return self.poly_cipher.decrypt_text_polyalphabetic(text, key_word)

    # Остальные методы остаются без изменений...
    # (encrypt_with_sblocks, decrypt_with_sblocks и т.д.)