from .alphabet import TelegraphAlphabet
from .tritemius import PolyAlphabeticCipher, TritemiusCipher


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

    def __init__(self):
        self.alphabet = TelegraphAlphabet()
        self.cipher = TritemiusCipher(self.alphabet)
        self.poly_cipher = PolyAlphabeticCipher(self.alphabet, self.cipher)
        self.sblock = SBlock(self.alphabet)

    def encrypt_with_sblocks(self, text: str, key_word: str) -> str:
        """
        Полное шифрование: Тритемиус → S-блоки
        """
        # 1. Полиалфавитное шифрование Тритемиуса
        poly_encrypted = self.poly_cipher.encrypt_text_polyalphabetic(text, key_word)

        # 2. Разбивка на блоки по 4 символа
        # Добавляем padding, если нужно
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

    def _pad_text(self, text: str) -> str:
        """Добавление padding для выравнивания по 4 символа"""
        remainder = len(text) % 4
        if remainder == 0:
            return text

        padding_needed = 4 - remainder
        # Используем 'А' для padding (можно любой символ из алфавита)
        return text + 'А' * padding_needed

    def _unpad_text(self, text: str) -> str:
        """Удаление padding"""
        # В простейшем случае - убираем 'А' в конце
        # В реальной системе нужно хранить длину исходного текста
        return text.rstrip('А')

    def analyze_properties(self):
        """Анализ свойств криптосистемы (Задача 6)"""
        print("\n" + "=" * 60)
        print("АНАЛИЗ СВОЙСТВ КРИПТОСИСТЕМЫ")
        print("=" * 60)

        # 1. Влияние позиции символа в блоке
        print("\n1. Влияние позиции символа на отображение:")
        test_char = 'А'
        for pos in range(4):
            block = 'А' * 4
            block_list = list(block)
            block_list[pos] = test_char
            test_block = ''.join(block_list)

            encrypted = self.sblock.apply_sbox(test_block)
            print(f"   Блок '{test_block}' → '{encrypted}'")
            print(f"   Символ на позиции {pos}: {test_char} → {encrypted[pos]}")

        # 2. Порядок применения ключей
        print("\n2. Порядок применения ключей:")
        text = "ТЕКСТ"
        key1 = "ПЕРВЫЙ"
        key2 = "ВТОРОЙ"

        # Шифруем ключом1, потом ключом2
        enc1 = self.poly_cipher.encrypt_text_polyalphabetic(text, key1)
        enc2 = self.poly_cipher.encrypt_text_polyalphabetic(enc1, key2)

        # Дешифруем в обратном порядке
        dec1 = self.poly_cipher.decrypt_text_polyalphabetic(enc2, key2)
        dec2 = self.poly_cipher.decrypt_text_polyalphabetic(dec1, key1)

        print(f"   Исходный: {text}")
        print(f"   Ключ1 → Ключ2: {enc2}")
        print(f"   Дешифровка (ключ2 → ключ1): {dec2}")
        print(f"   Совпадение с исходным: {'✓' if dec2 == text else '✗'}")

        # 3. Эффект лавины (изменение одного символа)
        print("\n3. Эффект лавины (avalanche effect):")
        text1 = "АБВГДЕЖЗ"
        text2 = "АБВГДЕЖИ"  # Изменили последний символ

        key = "КЛЮЧИК"
        enc1 = self.encrypt_with_sblocks(text1, key)
        enc2 = self.encrypt_with_sblocks(text2, key)

        # Считаем разницу
        diff_count = sum(1 for a, b in zip(enc1, enc2) if a != b)
        total_len = len(enc1)

        print(f"   Текст1: {text1}")
        print(f"   Текст2: {text2}")
        print(f"   Шифротекст1: {enc1}")
        print(f"   Шифротекст2: {enc2}")
        print(f"   Изменилось символов: {diff_count}/{total_len}")
        print(f"   Процент изменения: {diff_count / total_len * 100:.1f}%")

        if diff_count > 1:
            print("   ✓ Эффект лавины присутствует!")
        else:
            print("   ✗ Эффект лавины слабый")

