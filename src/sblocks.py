from alphabet import TelegraphAlphabet, CustomAlphabet
from tritemius import TritemiusCipher, TextCipher, PolyTritemiusCipher


class SBlock:
    """S-блоки для шифра Тритимуса (по псевдокоду)"""

    def __init__(self):
        self.alphabet = TelegraphAlphabet()
        self.poly_cipher = PolyTritemiusCipher(shift=8)  # Для полиалфавитного шифра

    def encrypt_s_block(self, block: str, key: str) -> str:
        """
        S-блок шифрование по алгоритму fru_S_Trithemus

        Args:
            block: блок из 4 символов
            key: ключ из 16 символов

        Returns:
            Зашифрованный блок или "input_error"
        """
        if len(block) != 4:
            return "input_error: блок должен содержать 4 символа"

        if len(key) != 16:
            return "input_error: ключ должен содержать 16 символов"

        # Просто используем полиалфавитный шифр
        return self.poly_cipher.encrypt(block, key)

    def decrypt_s_block(self, block: str, key: str) -> str:
        """
        Расшифровка S-блока

        Args:
            block: зашифрованный блок из 4 символов
            key: ключ из 16 символов

        Returns:
            Расшифрованный блок или "input_error"
        """
        if len(block) != 4:
            return "input_error: блок должен содержать 4 символа"

        if len(key) != 16:
            return "input_error: ключ должен содержать 16 символов"

        # Используем полиалфавитный дешифратор
        return self.poly_cipher.decrypt(block, key)


class EnhancedCryptoSystem:
    """Усиленная криптосистема с S-блоками"""

    def __init__(self, shift: int = 8):
        self.alphabet = TelegraphAlphabet()
        self.cipher = TritemiusCipher(shift=shift)
        self.poly_cipher = PolyTritemiusCipher(shift=8)
        self.text_cipher = TextCipher(self.cipher)
        self.sblock = SBlock()  # Используем новый SBlock

    # ... остальные методы без изменений (encrypt_simple, decrypt_simple и т.д.) ...

    # Новые методы для S-блоков (по псевдокоду)
    def encrypt_s_blocks(self, text: str, key: str) -> str:
        """
        Шифрование текста с использованием S-блоков

        Args:
            text: исходный текст (должен быть кратен 4)
            key: ключ из 16 символов

        Returns:
            Зашифрованный текст или сообщение об ошибке
        """
        if len(key) != 16:
            return "Ошибка: ключ должен содержать ровно 16 символов"

        # Проверяем, что текст кратен 4
        if len(text) % 4 != 0:
            return "Ошибка: текст должен быть кратен 4 символам"

        result_blocks = []
        for i in range(0, len(text), 4):
            block = text[i:i + 4]
            encrypted_block = self.sblock.encrypt_s_block(block, key)
            result_blocks.append(encrypted_block)

        return ''.join(result_blocks)

    def decrypt_s_blocks(self, text: str, key: str) -> str:
        """
        Расшифровка текста с использованием S-блоков

        Args:
            text: зашифрованный текст (должен быть кратен 4)
            key: ключ из 16 символов

        Returns:
            Расшифрованный текст или сообщение об ошибке
        """
        if len(key) != 16:
            return "Ошибка: ключ должен содержать ровно 16 символов"

        # Проверяем, что текст кратен 4
        if len(text) % 4 != 0:
            return "Ошибка: текст должен быть кратен 4 символам"

        result_blocks = []
        for i in range(0, len(text), 4):
            block = text[i:i + 4]
            decrypted_block = self.sblock.decrypt_s_block(block, key)
            result_blocks.append(decrypted_block)

        return ''.join(result_blocks)