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

    def apply_sbox_with_key(self, block: str, key_word: str) -> str:
        """Применение S-блока с ключом"""
        if len(block) != 4:
            raise ValueError(f"Блок должен содержать 4 символа, получено {len(block)}")

        result = []
        key_length = len(key_word)

        for i, char in enumerate(block):
            if self.alphabet.is_valid_char(char):
                # Получаем значение символа ключа для этой позиции
                if key_word:
                    key_char = key_word[i % key_length]
                    key_val = self.alphabet.get_value(key_char)
                else:
                    key_val = 0

                # Применяем S-бокс
                transformed = self._sbox_transform(char, i)

                # Добавляем влияние ключа
                val = self.alphabet.get_value(transformed)
                new_val = (val + key_val) % 32
                result.append(self.alphabet.get_char(new_val))
            else:
                result.append(char)

        return ''.join(result)

    def apply_inverse_sbox_with_key(self, block: str, key_word: str) -> str:
        """Обратное преобразование S-блока с ключом"""
        if len(block) != 4:
            raise ValueError(f"Блок должен содержать 4 символа, получено {len(block)}")

        result = []
        key_length = len(key_word)

        for i, char in enumerate(block):
            if self.alphabet.is_valid_char(char):
                # Получаем значение символа ключа
                if key_word:
                    key_char = key_word[i % key_length]
                    key_val = self.alphabet.get_value(key_char)
                else:
                    key_val = 0

                # Убираем влияние ключа
                val = self.alphabet.get_value(char)
                base_val = (val - key_val) % 32
                base_char = self.alphabet.get_char(base_val)

                # Убираем позиционный сдвиг
                shift = (i * 5) % 32
                sbox_val = (self.alphabet.get_value(base_char) - shift) % 32
                sbox_char = self.alphabet.get_char(sbox_val)

                # Обратное преобразование S-бокса
                original = self.inv_sbox.get(sbox_char, sbox_char)
                result.append(original)
            else:
                result.append(char)

        return ''.join(result)


class EnhancedCryptoSystem:
    """Усиленная криптосистема с S-блоками"""

    def __init__(self):
        self.alphabet = TelegraphAlphabet()
        self.cipher = TritemiusCipher(self.alphabet)
        self.poly_cipher = PolyAlphabeticCipher(self.alphabet, self.cipher)
        self.sblock = SBlock(self.alphabet)

    # Метод для обычного шифра Тритемиуса
    def encrypt_simple(self, text: str, key_word: str) -> str:
        """Обычное шифрование Тритемиуса (моноалфавитное)"""
        if not key_word:
            return text

        key_char = key_word[0].upper()
        result = []

        for char in text.upper():
            if self.alphabet.is_valid_char(char):
                encrypted = self.cipher.encrypt_char(char, key_char)
                result.append(encrypted)
            else:
                result.append(char)

        return ''.join(result)

    def decrypt_simple(self, text: str, key_word: str) -> str:
        """Дешифрование обычного шифра Тритемиуса"""
        key_char = key_word[0].upper() if key_word else 'А'
        result = []

        for char in text.upper():
            if self.alphabet.is_valid_char(char):
                decrypted = self.cipher.decrypt_char(char, key_char)
                result.append(decrypted)
            else:
                result.append(char)

        return ''.join(result)

    # Метод для полиалфавитного шифра Тритемиуса
    def encrypt_polyalphabetic(self, text: str, key_word: str, shift: int = 0) -> str:
        """Полиалфавитное шифрование Тритемиуса с дополнительным сдвигом"""
        # Сначала полиалфавитное шифрование
        encrypted = self.poly_cipher.encrypt_text_polyalphabetic(text, key_word)

        # Затем применяем дополнительный сдвиг
        if shift != 0:
            shifted_chars = []
            for char in encrypted:
                if self.alphabet.is_valid_char(char):
                    val = self.alphabet.get_value(char)
                    new_val = (val + shift) % 32
                    shifted_chars.append(self.alphabet.get_char(new_val))
                else:
                    shifted_chars.append(char)
            encrypted = ''.join(shifted_chars)

        return encrypted

    def decrypt_polyalphabetic(self, text: str, key_word: str, shift: int = 0) -> str:
        """Дешифрование полиалфавитного шифра Тритемиуса"""
        # Сначала убираем дополнительный сдвиг
        if shift != 0:
            unshifted_chars = []
            for char in text:
                if self.alphabet.is_valid_char(char):
                    val = self.alphabet.get_value(char)
                    new_val = (val - shift) % 32
                    unshifted_chars.append(self.alphabet.get_char(new_val))
                else:
                    unshifted_chars.append(char)
            text = ''.join(unshifted_chars)

        # Затем полиалфавитное дешифрование
        return self.poly_cipher.decrypt_text_polyalphabetic(text, key_word)

    # Метод для S-блоков
    def encrypt_with_sblocks(self, text: str, key_word: str) -> str:
        """
        Полное шифрование: Тритемиус → S-блоки
        """
        # 1. Полиалфавитное шифрование Тритемиуса
        poly_encrypted = self.poly_cipher.encrypt_text_polyalphabetic(text, key_word)

        # 2. Разбивка на блоки по 4 символа
        padded_text = self._pad_text(poly_encrypted)

        # 3. Применение S-блоков к каждому блоку
        result_blocks = []
        for i in range(0, len(padded_text), 4):
            block = padded_text[i:i + 4]
            sbox_block = self.sblock.apply_sbox(block)
            result_blocks.append(sbox_block)

        return ''.join(result_blocks)

    def decrypt_with_sblocks(self, text: str, key_word: str) -> str:
        """Полное дешифрование"""
        # 1. Обратное преобразование S-блоков
        result_blocks = []
        for i in range(0, len(text), 4):
            block = text[i:i + 4]
            sbox_block = self.sblock.apply_inverse_sbox(block)
            result_blocks.append(sbox_block)

        sbox_decrypted = ''.join(result_blocks)

        # 2. Убираем padding
        unpadded = self._unpad_text(sbox_decrypted)

        # 3. Дешифрование Тритемиуса
        return self.poly_cipher.decrypt_text_polyalphabetic(unpadded, key_word)

    # Метод для усиленных S-блоков
    def encrypt_enhanced_sblocks(self, text: str, key_word: str) -> str:
        """Шифрование с усиленными S-блоками"""
        # 1. Полиалфавитное шифрование
        poly_encrypted = self.poly_cipher.encrypt_text_polyalphabetic(text, key_word)

        # 2. Разбивка на блоки
        padded_text = self._pad_text(poly_encrypted)

        # 3. Применение усиленных S-блоков
        result_blocks = []
        for i in range(0, len(padded_text), 4):
            block = padded_text[i:i + 4]
            sbox_block = self.sblock.apply_sbox_with_key(block, key_word)
            result_blocks.append(sbox_block)

        return ''.join(result_blocks)

    def decrypt_enhanced_sblocks(self, text: str, key_word: str) -> str:
        """Дешифрование с усиленными S-блоками"""
        # 1. Обратное преобразование усиленных S-блоков
        result_blocks = []
        for i in range(0, len(text), 4):
            block = text[i:i + 4]
            sbox_block = self.sblock.apply_inverse_sbox_with_key(block, key_word)
            result_blocks.append(sbox_block)

        sbox_decrypted = ''.join(result_blocks)

        # 2. Убираем padding
        unpadded = self._unpad_text(sbox_decrypted)

        # 3. Дешифрование Тритемиуса
        return self.poly_cipher.decrypt_text_polyalphabetic(unpadded, key_word)

    def _pad_text(self, text: str) -> str:
        """Добавление padding для выравнивания по 4 символа"""
        remainder = len(text) % 4
        if remainder == 0:
            return text

        padding_needed = 4 - remainder
        return text + 'А' * padding_needed

    def _unpad_text(self, text: str) -> str:
        """Удаление padding"""
        return text.rstrip('А')