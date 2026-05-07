import random
import string

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
