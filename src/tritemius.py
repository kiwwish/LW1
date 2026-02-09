from alphabet import TelegraphAlphabet, CustomAlphabet


# Реализация шифра Тритемиуса
class TritemiusCipher:

    def __init__(self, shift: int = 8):
        self.shift = shift  # Фиксированный сдвиг Тритемиуса

    # Шифрование одного символа
    def encrypt_char(self, plain_char: str, alphabet: CustomAlphabet) -> str:
        """Шифрование символа с фиксированным сдвигом в пользовательском алфавите"""
        if not alphabet.standard_alphabet.is_valid_char(plain_char):
            return plain_char

        # Получаем значение символа в пользовательском алфавите
        char_val = alphabet.char_to_val.get(plain_char.upper())
        if char_val is None:
            return plain_char

        # Применяем сдвиг на 8 позиций
        encrypted_val = (char_val + self.shift) % 32
        return alphabet.val_to_char[encrypted_val]

    # Дешифрование одного символа
    def decrypt_char(self, cipher_char: str, alphabet: CustomAlphabet) -> str:
        """Дешифрование символа"""
        if not alphabet.standard_alphabet.is_valid_char(cipher_char):
            return cipher_char

        # Получаем значение символа в пользовательском алфавите
        char_val = alphabet.char_to_val.get(cipher_char.upper())
        if char_val is None:
            return cipher_char

        # Применяем обратный сдвиг на 8 позиций
        decrypted_val = (char_val - self.shift) % 32
        return alphabet.val_to_char[decrypted_val]


# Шифрование и дешифрование текстовых блоков
class TextCipher:

    def __init__(self, cipher: TritemiusCipher):
        self.cipher = cipher

    # Моноалфавитное шифрование (один символ ключа для всего текста)
    def encrypt_text(self, text: str, key_word: str) -> str:
        """
        Моноалфавитное шифрование Тритемиуса
        1. Создаем пользовательский алфавит на основе ключа
        2. Шифруем каждый символ со сдвигом 8 в этом алфавите
        """
        if not key_word:
            return text

        # Создаем пользовательский алфавит на основе ключа
        alphabet = CustomAlphabet(key_word)

        result = []
        for char in text.upper():
            if alphabet.standard_alphabet.is_valid_char(char):
                encrypted = self.cipher.encrypt_char(char, alphabet)
                result.append(encrypted)
            else:
                result.append(char)

        return ''.join(result)

    # Дешифрование моноалфавитного шифра
    def decrypt_text(self, text: str, key_word: str) -> str:
        """Дешифрование текста, зашифрованного методом Тритемиуса"""
        if not key_word:
            return text

        # Создаем пользовательский алфавит на основе ключа (должен быть тот же!)
        alphabet = CustomAlphabet(key_word)

        result = []
        for char in text.upper():
            if alphabet.standard_alphabet.is_valid_char(char):
                decrypted = self.cipher.decrypt_char(char, alphabet)
                result.append(decrypted)
            else:
                result.append(char)

        return ''.join(result)


# Дополнительные методы для работы с алфавитом
def get_custom_alphabet_string(key_word: str) -> str:
    """Получить строковое представление пользовательского алфавита"""
    alphabet = CustomAlphabet(key_word)
    return ', '.join(alphabet.custom_symbols)