from alphabet import TelegraphAlphabet


# Реализация шифра Тритемиуса
class TritemiusCipher:

    def __init__(self, alphabet: TelegraphAlphabet, shift: int = 8):
        self.alphabet = alphabet
        self.shift = shift  # Фиксированный сдвиг Тритемиуса

    # Шифрование одного символа с учетом позиции
    def encrypt_char(self, plain_char: str, position: int) -> str:
        """Шифрование символа с фиксированным сдвигом по позиции"""
        if not self.alphabet.is_valid_char(plain_char):
            return plain_char

        # Сдвиг = базовый сдвиг Тритемиуса (8) * позиция
        # Или просто позиция, если сдвиг = 1
        shift_value = position * self.shift
        char_val = self.alphabet.get_value(plain_char)
        encrypted_val = (char_val + shift_value) % 32
        return self.alphabet.get_char(encrypted_val)

    # Дешифрование одного символа
    def decrypt_char(self, cipher_char: str, position: int) -> str:
        """Дешифрование символа"""
        if not self.alphabet.is_valid_char(cipher_char):
            return cipher_char

        shift_value = position * self.shift
        char_val = self.alphabet.get_value(cipher_char)
        decrypted_val = (char_val - shift_value) % 32
        return self.alphabet.get_char(decrypted_val)


# Шифрование и дешифрование текстовых блоков
class TextCipher:

    def __init__(self, alphabet: TelegraphAlphabet, cipher: TritemiusCipher):
        self.alphabet = alphabet
        self.cipher = cipher

    # Моноалфавитное шифрование (один символ ключа для всего текста)
    def encrypt_text_monoalphabetic(self, text: str, key_word: str) -> str:
        """
        Моноалфавитное шифрование Тритемиуса
        В оригинале Тритемиуса ключ не используется для определения сдвига,
        но для совместимости оставим
        """
        result = []

        for i, char in enumerate(text.upper()):
            if self.alphabet.is_valid_char(char):
                encrypted = self.cipher.encrypt_char(char, i)
                result.append(encrypted)
            else:
                result.append(char)

        return ''.join(result)

    # Дешифрование моноалфавитного шифра
    def decrypt_text_monoalphabetic(self, text: str, key_word: str) -> str:
        result = []

        for i, char in enumerate(text.upper()):
            if self.alphabet.is_valid_char(char):
                decrypted = self.cipher.decrypt_char(char, i)
                result.append(decrypted)
            else:
                result.append(char)

        return ''.join(result)

    # Полиалфавитная модификация шифра Тритемиуса


class PolyAlphabeticCipher(TextCipher):

    #  Полиалфавитное шифрование - ключ циклически повторяется
    def encrypt_text_polyalphabetic(self, text: str, key_word: str) -> str:
        """
        Полиалфавитный вариант Тритемиуса
        Здесь ключ уже влияет на сдвиг
        """
        if not key_word:
            return text

        key_word = key_word.upper()
        result = []
        key_length = len(key_word)

        for i, char in enumerate(text.upper()):
            if self.alphabet.is_valid_char(char):
                # Получаем значение символа ключа
                key_index = i % key_length
                key_char = key_word[key_index]
                key_val = self.alphabet.get_value(key_char)

                # Сдвиг = позиция * базовый сдвиг + значение ключа
                shift_value = (i * self.cipher.shift + key_val) % 32

                char_val = self.alphabet.get_value(char)
                encrypted_val = (char_val + shift_value) % 32
                encrypted_char = self.alphabet.get_char(encrypted_val)
                result.append(encrypted_char)
            else:
                result.append(char)

        return ''.join(result)

    # Дешифрование полиалфавитного шифра
    def decrypt_text_polyalphabetic(self, text: str, key_word: str) -> str:
        key_word = key_word.upper()
        result = []
        key_length = len(key_word)

        for i, char in enumerate(text.upper()):
            if self.alphabet.is_valid_char(char):
                key_index = i % key_length
                key_char = key_word[key_index]
                key_val = self.alphabet.get_value(key_char)

                shift_value = (i * self.cipher.shift + key_val) % 32

                char_val = self.alphabet.get_value(char)
                decrypted_val = (char_val - shift_value) % 32
                decrypted_char = self.alphabet.get_char(decrypted_val)
                result.append(decrypted_char)
            else:
                result.append(char)

        return ''.join(result)