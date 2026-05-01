# Password Generator — CustomTkinter

Навчальний проєкт на Python + CustomTkinter для 3 уроків по 1.5 години.

---

## Функціональність

### Урок 1 — Основний інтерфейс
- Поле виводу згенерованого пароля
- Слайдер довжини пароля (8–64 символи)
- Кнопка «Згенерувати»
- Чекбокси вибору символів:
  - великі літери (A–Z)
  - малі літери (a–z)
  - цифри (0–9)
  - спецсимволи (!@#$...)

### Урок 2 — Логіка і зручність
- Копіювання пароля в буфер обміну (`pyperclip`)
- Індикатор надійності пароля: слабкий / середній / сильний
- Валідація: хоча б один тип символів має бути обраний

### Урок 3 — Полірування
- Перемикач темної/світлої теми (вбудований у CTk)
- Збереження паролів у файл (`passwords.json`)
- Анімація при генерації (зміна кольору або fade-ефект)

---

## Архітектура

Проєкт розділено на **2 файли**. Це навчає розділяти логіку і GUI з самого початку.

<img width="196" height="150" alt="password_gen_architecture" src="https://github.com/user-attachments/assets/9bb37832-1b08-452d-80d9-c5e65a423ca1" />


```
password_generator/
├── main.py          # GUI + запуск
├── logic.py         # чиста логіка, без GUI
└── passwords.json   # створюється автоматично при першому збереженні
```

### logic.py — чиста логіка

Не містить жодного GUI-коду. Функції можна тестувати окремо в терміналі.

| Функція | Що робить |
|---|---|
| `generate_password()` | генерує пароль через `random`, `string`, `secrets` |
| `check_strength()` | повертає `"weak"` / `"medium"` / `"strong"` |
| `save_password()` | зберігає пароль у `passwords.json` |
| `load_passwords()` | читає список збережених паролів |
| `copy_to_clipboard()` | копіює рядок через `pyperclip` |

### main.py — GUI

Клас `App` наслідує `customtkinter.CTk`. Кожна дія користувача — окремий метод.

| Метод | Що робить |
|---|---|
| `__init__()` | налаштовує вікно, викликає `setup_ui()` |
| `setup_ui()` | створює всі віджети, layout, grid |
| `on_generate()` | викликає `logic.generate_password()`, оновлює UI |
| `on_copy()` | викликає `logic.copy_to_clipboard()` |
| `toggle_theme()` | перемикає dark / light через `ctk.set_appearance_mode()` |

Точка входу:

```python
if __name__ == "__main__":
    App().mainloop()
```

---

## Залежності

```
customtkinter
pyperclip
```

Встановлення:

```bash
pip install customtkinter pyperclip
```

---

## Розподіл по уроках

| Урок | Файли | Теми |
|---|---|---|
| 1 | `logic.py` + базовий `main.py` | вікно, віджети, слайдер, чекбокси, `setup_ui()` |
| 2 | `main.py` | `on_generate()`, `on_copy()`, індикатор надійності, валідація |
| 3 | `main.py` + `logic.py` | тема, збереження в JSON, анімація |
