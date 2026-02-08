from src.alphabet import TelegraphAlphabet

# Реализация шифра Тритемиуса
class TritemiusCipher:

    def __init__(self, alphabet: TelegraphAlphabet):
        self.alphabet = alphabet

    # Шифрование одного символа

    def encrypt_char(self, plain_char: str, key_char: str) -> str:
        if not self.alphabet.is_valid_char(plain_char):
            return plain_char  # Возвращаем как есть, если не в алфавите
        return self.alphabet.add(plain_char, key_char)

    # Дешифрование одного символа
    def decrypt_char(self, cipher_char: str, key_char: str) -> str:
        if not self.alphabet.is_valid_char(cipher_char):
            return cipher_char
        return self.alphabet.subtract(cipher_char, key_char)


# Шифрование и дешифрование текстовых блоков
class TextCipher:

    def __init__(self, alphabet: TelegraphAlphabet, cipher: TritemiusCipher):
        self.alphabet = alphabet
        self.cipher = cipher

    # Моноалфавитное шифрование (один символ ключа для всего текста)
    def encrypt_text_monoalphabetic(self, text: str, key_word: str) -> str:

        if not key_word:
            return text

        key_char = key_word[0].upper()  # Берем первый символ ключа
        result = []

        for char in text.upper():
            if self.alphabet.is_valid_char(char):
                encrypted = self.cipher.encrypt_char(char, key_char)
                result.append(encrypted)
            else:
                result.append(char)

        return ''.join(result)

    # Дешифрование моноалфавитного шифра
    def decrypt_text_monoalphabetic(self, text: str, key_word: str) -> str:
        key_char = key_word[0].upper() if key_word else 'А'
        result = []

        for char in text.upper():
            if self.alphabet.is_valid_char(char):
                decrypted = self.cipher.decrypt_char(char, key_char)
                result.append(decrypted)
            else:
                result.append(char)

        return ''.join(result)

    # Полиалфавитная модификация шифра Тритемиуса
class PolyAlphabeticCipher(TextCipher):

    #  Полиалфавитное шифрование - ключ циклически повторяется
    def encrypt_text_polyalphabetic(self, text: str, key_word: str) -> str:
        if not key_word:
            return text

        key_word = key_word.upper()
        result = []
        key_length = len(key_word)

        for i, char in enumerate(text.upper()):
            if self.alphabet.is_valid_char(char):
                key_index = i % key_length
                key_char = key_word[key_index]
                encrypted = self.cipher.encrypt_char(char, key_char)
                result.append(encrypted)
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
                decrypted = self.cipher.decrypt_char(char, key_char)
                result.append(decrypted)
            else:
                result.append(char)

        return ''.join(result)
