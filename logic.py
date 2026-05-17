import random
import string
import pyperclip


def generate_password(length, use_upper, use_lower, use_digits, use_special):
    """
    Генерує пароль за заданими параметрами.

    :param length: довжина пароля (int)
    :param use_upper: включати великі літери (bool)
    :param use_lower: включати малі літери (bool)
    :param use_digits: включати цифри (bool)
    :param use_special: включати спецсимволи (bool)
    :return: згенерований пароль (str) або None якщо жоден тип не обрано
    """
    characters = ""

    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        return None

    password = "".join(random.choice(characters) for _ in range(length))
    return password


def check_strength(password):
    """
    Оцінює надійність пароля.

    Критерії (кожен дає +1 бал):
      - довжина >= 12
      - є великі літери
      - є малі літери
      - є цифри
      - є спецсимволи

    :return: tuple ("weak"|"medium"|"strong", int score 0-5)
    """
    if not password:
        return "weak", 0

    score = 0

    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        return "weak", score
    elif score <= 3:
        return "medium", score
    else:
        return "strong", score


def copy_to_clipboard(text):
    """
    Копіює текст у буфер обміну.

    :return: True якщо успішно, False якщо pyperclip недоступний
    """
    try:
        pyperclip.copy(text)
        return True
    except pyperclip.PyperclipException:
        return False


import json
import os
from datetime import datetime

PASSWORDS_FILE = "passwords.json"


def save_password(password, label=""):
    """
    Зберігає пароль у passwords.json.

    :param password: рядок пароля
    :param label: необов'язкова мітка (наприклад, "Gmail")
    :return: True якщо збережено успішно
    """
    entries = load_passwords()

    entry = {
        "password": password,
        "label": label,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    entries.append(entry)

    try:
        with open(PASSWORDS_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False


def load_passwords():
    """
    Читає список збережених паролів із passwords.json.

    :return: list of dict, або [] якщо файл не існує / пошкоджений
    """
    if not os.path.exists(PASSWORDS_FILE):
        return []

    try:
        with open(PASSWORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []