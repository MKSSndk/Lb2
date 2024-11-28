import re
import requests
import unittest

ROMAN_REGEX = r'^(M{0,3})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'


def is_valid_roman(roman: str) -> bool:
    return bool(re.match(ROMAN_REGEX, roman.upper()))


def find_roman_numerals(text: str) -> list:
    pattern = re.compile(r'\b(M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?)\b', re.IGNORECASE)
    return [match.group(0) for match in pattern.finditer(text) if match.group(0)]


def read_from_url(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise ValueError(f"Ошибка загрузки URL: {e}")


def read_from_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise ValueError("Файл не найден. Проверьте путь.")
    except IOError as e:
        raise ValueError(f"Ошибка чтения файла: {e}")

def main():
    while True:
        print("\nВыберите опцию:")
        print("1. Ввод числа вручную")
        print("2. Проверка текста с веб-страницы")
        print("3. Проверка текста из файла")
        print("4. Запуск тестов")
        print("5. Выход")

        option = input("Введите номер опции: ").strip()

        if option == "1":
            user_input = input("Введите строку с римскими числами: ").strip()
            if is_valid_roman(user_input):
                print(f"'{user_input}' является корректным римским числом.")
            else:
                print(f"'{user_input}' не является корректным римским числом.")
        elif option == "2":
            url = input("Введите URL веб-страницы: ").strip()
            try:
                text = read_from_url(url)
                numerals = find_roman_numerals(text)
                if numerals:
                    print(f"Найдено римских чисел: {len(numerals)}")
                    print(numerals)
                else:
                    print("Римских чисел не найдено.")
            except ValueError as e:
                print(e)
        elif option == "3":
            file_path = input("Введите путь к файлу: ").strip()
            try:
                text = read_from_file(file_path)
                numerals = find_roman_numerals(text)
                if numerals:
                    print(f"Найдено римских чисел: {len(numerals)}")
                    print(numerals)
                else:
                    print("Римских чисел не найдено.")
            except ValueError as e:
                print(e)
        elif option == "4":
            print("Запуск тестов...")
            unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestRomanNumerals))
        elif option == "5":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор опции. Попробуйте снова.")

# Unit-тесты
class TestRomanNumerals(unittest.TestCase):
    def test_valid_roman_numerals(self):
        self.assertTrue(is_valid_roman("X"))
        self.assertTrue(is_valid_roman("XL"))
        self.assertTrue(is_valid_roman("MMM"))
        self.assertTrue(is_valid_roman("IV"))
        self.assertTrue(is_valid_roman("CMXCIX"))

    def test_invalid_roman_numerals(self):
        self.assertFalse(is_valid_roman("IIII"))
        self.assertFalse(is_valid_roman("MMMM"))
        self.assertFalse(is_valid_roman("VV"))
        self.assertFalse(is_valid_roman("XCXC"))
        self.assertFalse(is_valid_roman("123"))

    def test_find_roman_numerals(self):
        text = "Римские числа: I, II, III, IV, IX, XX, XL, XC, CD, CM, и MMM."
        expected = ["I", "II", "III", "IV", "IX", "XX", "XL", "XC", "CD", "CM", "MMM"]
        self.assertEqual(find_roman_numerals(text), expected)


if __name__ == "__main__":
    main()