"""
Тестирование правильного алгоритма Тритемиуса
"""

import sys
import os

sys.path.append('src')

from alphabet import TelegraphAlphabet

def test_alphabet_creation():
    """Тестирование создания переставленного алфавита"""
    print("="*60)
    print("ТЕСТ СОЗДАНИЯ ПЕРЕСТАВЛЕННОГО АЛФАВИТА")
    print("="*60)

    alphabet = TelegraphAlphabet()

    # Тест 1: Ключ "ВЫСОКОПРЕВОСХОДИТЕЛЬСТВО"
    print("\n1. Ключ: 'ВЫСОКОПРЕВОСХОДИТЕЛЬСТВО'")
    key1 = "ВЫСОКОПРЕВОСХОДИТЕЛЬСТВО"

    # Убираем повторения вручную
    unique1 = []
    for char in key1.upper():
        if char in alphabet.symbols and char not in unique1:
            unique1.append(char)

    print(f"   Уникальные буквы ключа: {''.join(unique1)}")
    print(f"   Последняя уникальная буква: '{unique1[-1]}'")

    permuted1 = alphabet.create_permuted_alphabet(key1)

    print(f"   Длина алфавита: {len(permuted1)}")
    print(f"   Первые 16 символов: {''.join(permuted1[:16])}")
    print(f"   Последние 16 символов: {''.join(permuted1[16:])}")

    # Тест 2: Ключ "МАМА"
    print("\n2. Ключ: 'МАМА'")
    key2 = "МАМА"

    unique2 = []
    for char in key2.upper():
        if char in alphabet.symbols and char not in unique2:
            unique2.append(char)

    print(f"   Уникальные буквы ключа: {''.join(unique2)}")
    print(f"   Последняя уникальная буква: '{unique2[-1]}'")

    permuted2 = alphabet.create_permuted_alphabet(key2)

    print(f"   Длина алфавита: {len(permuted2)}")
    print(f"   Первые 16 символов: {''.join(permuted2[:16])}")

    # Проверяем сдвиг после 'А'
    last_char_index = permuted2.index(unique2[-1])
    print(f"   Позиция '{unique2[-1]}': {last_char_index}")
    print(f"   Символы после '{unique2[-1]}': {''.join(permuted2[last_char_index+1:last_char_index+9])}")

    # По вашей логике: М→З
    print(f"\n   Проверка М→З:")
    print(f"   'М' в исходном алфавите: индекс {alphabet.get_value('М')}")
    print(f"   В переставленном на этой позиции: '{permuted2[alphabet.get_value('М')]}'")
    print(f"   После сдвига +8: нужно проверить...")

def test_tritemius_encryption():
    """Тестирование шифрования Тритемиуса"""
    print("\n" + "="*60)
    print("ТЕСТ ШИФРОВАНИЯ ТРИТЕМИУСА")
    print("="*60)

    alphabet = TelegraphAlphabet()

    # Тест с ключом "ВЫСОКОПРЕВОСХОДИТЕЛЬСТВО"
    key = "ВЫСОКОПРЕВОСХОДИТЕЛЬСТВО"
    text = "СЫЗРАНЬ"

    print(f"Ключ: {key}")
    print(f"Текст: {text}")

    # Создаем переставленный алфавит
    permuted = alphabet.create_permuted_alphabet(key)

    print(f"\nПереставленный алфавит:")
    for i in range(0, 32, 8):
        chars = permuted[i:i+8]
        indices = list(range(i, i+len(chars)))
        print(f"  {''.join(chars)}")
        print(f"  {' '.join([f'{idx:2d}' for idx in indices])}")
        print()

    # Находим последнюю уникальную букву ключа
    unique_chars = []
    for char in key.upper():
        if char in alphabet.symbols and char not in unique_chars:
            unique_chars.append(char)

    last_key_char = unique_chars[-1]
    print(f"Последняя уникальная буква ключа: '{last_key_char}'")

    # Алгоритм шифрования:
    # 1. Берем символ текста
    # 2. Находим его индекс в исходном алфавите
    # 3. Берем символ из переставленного алфавита на этой позиции
    # 4. Сдвигаем этого символ на 8 позиций в переставленном алфавите

    print(f"\nШифрование '{text}':")
    result = []

    for char in text:
        # 1. Индекс в исходном алфавите
        orig_idx = alphabet.get_value(char)

        # 2. Символ в переставленном алфавите на этой позиции
        permuted_char = permuted[orig_idx]

        # 3. Индекс этого символа в переставленном алфавите
        permuted_idx = permuted.index(permuted_char)

        # 4. Сдвиг на 8 позиций
        encrypted_idx = (permuted_idx + 8) % 32
        encrypted_char = permuted[encrypted_idx]

        result.append(encrypted_char)

        print(f"  {char}({orig_idx:2d}) → '{permuted_char}'({permuted_idx:2d}) "
              f"+8 → '{encrypted_char}'({encrypted_idx:2d})")

    encrypted = ''.join(result)
    print(f"\nРезультат: {encrypted}")
    print(f"Ожидаемый: ИДШАУЮН")

    # Дешифрование
    print(f"\nДешифрование '{encrypted}':")
    decrypted = []

    for char in encrypted:
        # 1. Индекс в переставленном алфавите
        enc_idx = permuted.index(char)

        # 2. Убираем сдвиг
        permuted_idx = (enc_idx - 8) % 32
        permuted_char = permuted[permuted_idx]

        # 3. Находим какой исходный символ был на этой позиции
        orig_idx = permuted.index(permuted_char)  # Это и есть исходный индекс!
        orig_char = alphabet.get_char(orig_idx)

        decrypted.append(orig_char)

        print(f"  {char}({enc_idx:2d}) -8 → '{permuted_char}'({permuted_idx:2d}) "
              f"→ {orig_char}({orig_idx:2d})")

    decrypted_text = ''.join(decrypted)
    print(f"\nДешифрованный текст: {decrypted_text}")

    if decrypted_text == text:
        print("✓ Дешифрование работает!")
    else:
        print("✗ Ошибка дешифрования!")

def test_simple_case():
    """Простой тест с ключом МАМА"""
    print("\n" + "="*60)
    print("ПРОСТОЙ ТЕСТ: КЛЮЧ 'МАМА', ПРОВЕРКА М→З")
    print("="*60)

    alphabet = TelegraphAlphabet()
    key = "МАМА"

    print(f"Ключ: {key}")

    # Уникальные буквы
    unique = []
    for char in key.upper():
        if char in alphabet.symbols and char not in unique:
            unique.append(char)

    print(f"Уникальные буквы: {''.join(unique)}")
    print(f"Последняя уникальная буква: '{unique[-1]}'")

    # Переставленный алфавит
    permuted = alphabet.create_permuted_alphabet(key)

    print(f"\nПереставленный алфавит:")
    for i in range(0, 32, 8):
        print(f"  {''.join(permuted[i:i+8])}")

    # Проверяем М→З
    print(f"\nПроверка М→З:")

    # Исходный индекс 'М'
    m_index = alphabet.get_value('М')
    print(f"  'М' имеет индекс {m_index} в исходном алфавите")

    # Символ на этой позиции в переставленном алфавите
    char_at_m_pos = permuted[m_index]
    print(f"  На позиции {m_index} в переставленном алфавите: '{char_at_m_pos}'")

    # Индекс этого символа в переставленном алфавите
    char_index = permuted.index(char_at_m_pos)
    print(f"  '{char_at_m_pos}' имеет индекс {char_index} в переставленном алфавите")

    # Сдвиг на 8
    shifted_index = (char_index + 8) % 32
    shifted_char = permuted[shifted_index]
    print(f"  +8 → индекс {shifted_index} → символ '{shifted_char}'")

    if shifted_char == 'З':
        print("  ✓ М→З подтверждено!")
    else:
        print(f"  ✗ Ожидалось 'З', получилось '{shifted_char}'")

if __name__ == "__main__":
    test_alphabet_creation()
    test_tritemius_encryption()
    test_simple_case()

    input("\nНажмите Enter для выхода...")
