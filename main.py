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
