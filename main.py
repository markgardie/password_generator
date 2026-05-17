import customtkinter as ctk
from logic import (
    generate_password,
    check_strength,
    copy_to_clipboard,
    save_password,
    load_passwords,
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

STRENGTH_CONFIG = {
    "weak":   {"label": "Слабкий",  "color": "#e05555", "progress": 0.33},
    "medium": {"label": "Середній", "color": "#e09a00", "progress": 0.66},
    "strong": {"label": "Надійний", "color": "#3dba6f", "progress": 1.0},
}

# Кількість кроків анімації при генерації пароля
ANIMATION_STEPS = 8
ANIMATION_DELAY = 40  # мс між кроками


class HistoryWindow(ctk.CTkToplevel):
    """Окреме вікно зі збереженими паролями."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Збережені паролі")
        self.geometry("420x380")
        self.resizable(False, False)
        # Вікно завжди поверх головного
        self.after(100, self.lift)

        self._build_ui()
        self._load()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text="Збережені паролі",
            font=ctk.CTkFont(size=17, weight="bold"),
        ).grid(row=0, column=0, padx=20, pady=(20, 10))

        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="")
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

    def _load(self):
        entries = load_passwords()

        if not entries:
            ctk.CTkLabel(
                self.scroll_frame,
                text="Поки що нічого не збережено",
                text_color="gray",
            ).grid(row=0, column=0, pady=20)
            return

        # Виводимо у зворотному порядку — нові зверху
        for i, entry in enumerate(reversed(entries)):
            row_frame = ctk.CTkFrame(self.scroll_frame)
            row_frame.grid(row=i, column=0, sticky="ew", pady=(0, 8))
            row_frame.grid_columnconfigure(1, weight=1)

            # Мітка / дата
            meta = entry.get("label") or entry.get("created_at", "")
            ctk.CTkLabel(
                row_frame,
                text=meta,
                font=ctk.CTkFont(size=11),
                text_color="gray",
            ).grid(row=0, column=0, columnspan=3, padx=12, pady=(8, 2), sticky="w")

            # Пароль
            ctk.CTkLabel(
                row_frame,
                text=entry["password"],
                font=ctk.CTkFont(size=13, family="Courier"),
            ).grid(row=1, column=0, padx=12, pady=(0, 8), sticky="w")

            # Кнопка копіювання
            pw = entry["password"]
            ctk.CTkButton(
                row_frame,
                text="📋",
                width=36,
                height=28,
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                border_width=1,
                command=lambda p=pw: copy_to_clipboard(p),
            ).grid(row=1, column=2, padx=(0, 10), pady=(0, 8))


class App(ctk.CTk):

    def __init__(self):
        self.title("Генератор паролю")
        self.geometry("480x420")
        self.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # --- Заголовок ---
        ctk.CTkLabel(
            self,
            text="Password Generator",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(row=0, column=0, padx=24, pady=(24, 4))

        ctk.CTkLabel(
            self,
            text="Налаштуй та згенеруй надійний пароль",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).grid(row=1, column=0, padx=24, pady=(0, 16))

        # --- Поле виводу пароля + кнопка копіювання ---
        password_frame = ctk.CTkFrame(self, fg_color="transparent")
        password_frame.grid(row=2, column=0, padx=24, pady=(0, 8), sticky="ew")
        password_frame.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Тут з'явиться пароль...",
            font=ctk.CTkFont(size=15, family="Courier"),
            height=48,
            justify="center",
        )
        self.password_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.copy_btn = ctk.CTkButton(
            password_frame,
            text="📋",
            width=48,
            height=48,
            font=ctk.CTkFont(size=18),
            command=self.on_copy,
            fg_color="transparent",
            border_width=1,
        )
        self.copy_btn.grid(row=0, column=1)

        # --- Індикатор надійності ---
        strength_frame = ctk.CTkFrame(self, fg_color="transparent")
        strength_frame.grid(row=3, column=0, padx=24, pady=(0, 12), sticky="ew")
        strength_frame.grid_columnconfigure(0, weight=1)

        self.strength_bar = ctk.CTkProgressBar(strength_frame, height=8)
        self.strength_bar.set(0)
        self.strength_bar.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.strength_label = ctk.CTkLabel(
            strength_frame,
            text="—",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=64,
            anchor="e",
        )
        self.strength_label.grid(row=0, column=1)

        # --- Слайдер довжини ---
        length_frame = ctk.CTkFrame(self, fg_color="transparent")
        length_frame.grid(row=4, column=0, padx=24, pady=(0, 8), sticky="ew")
        length_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            length_frame,
            text="Довжина:",
            font=ctk.CTkFont(size=13),
        ).grid(row=0, column=0, padx=(0, 8))

        self.length_var = ctk.IntVar(value=16)

        self.length_label = ctk.CTkLabel(
            length_frame,
            text="16",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=28,
        )
        self.length_label.grid(row=0, column=2, padx=(8, 0))

        self.length_slider = ctk.CTkSlider(
            length_frame,
            from_=8,
            to=64,
            number_of_steps=56,
            variable=self.length_var,
            command=self.on_slider_change,
        )
        self.length_slider.grid(row=0, column=1, sticky="ew")

        # --- Чекбокси символів ---
        checkboxes_frame = ctk.CTkFrame(self)
        checkboxes_frame.grid(row=5, column=0, padx=24, pady=(0, 16), sticky="ew")
        checkboxes_frame.grid_columnconfigure((0, 1), weight=1)

        self.use_upper = ctk.BooleanVar(value=True)
        self.use_lower = ctk.BooleanVar(value=True)
        self.use_digits = ctk.BooleanVar(value=True)
        self.use_special = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(
            checkboxes_frame, text="Великі літери  (A–Z)", variable=self.use_upper
        ).grid(row=0, column=0, padx=16, pady=(12, 6), sticky="w")

        ctk.CTkCheckBox(
            checkboxes_frame, text="Малі літери  (a–z)", variable=self.use_lower
        ).grid(row=1, column=0, padx=16, pady=(0, 12), sticky="w")

        ctk.CTkCheckBox(
            checkboxes_frame, text="Цифри  (0–9)", variable=self.use_digits
        ).grid(row=0, column=1, padx=16, pady=(12, 6), sticky="w")

        ctk.CTkCheckBox(
            checkboxes_frame, text="Спецсимволи  (!@#...)", variable=self.use_special
        ).grid(row=1, column=1, padx=16, pady=(0, 12), sticky="w")

        # --- Кнопка генерації ---
        self.generate_btn = ctk.CTkButton(
            self,
            text="Згенерувати",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=44,
            command=self.on_generate,
        )
        self.generate_btn.grid(row=6, column=0, padx=24, pady=(0, 8), sticky="ew")

        # --- Повідомлення (помилка або підтвердження копіювання) ---
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
        )
        self.status_label.grid(row=7, column=0, padx=24, pady=(0, 16))



    # --- Обробники подій ---

    def on_slider_change(self, value):
        pass

    def on_generate(self):
        pass

    
    def on_save(self):
        password = self.password_entry.get()
        if not password:
            self._set_status("Спочатку згенеруй пароль!", color="#e05555")
            return
        
        if save_password(password):
            self._set_status("✓ Збережено!", color="#3dba6f")
            self.after(2000, lambda: self._set_status(""))
        else:
            self._set_status("Помилка збереження", color="#e05555")

    def open_history(self):
        # Якщо вікно вже відкрите — просто підняти його вперед
        if self._history_window is not None and self._history_window.winfo_exists():
            self._history_window.lift()
            return
        self._history_window = HistoryWindow(self)

    def toggle_theme(self):
        current = ctk.get_appearance_mode()

        if current == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="🌙")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="")

    # ------------------------------------------------------------------ #
    #  Анімація                                                            #
    # ------------------------------------------------------------------ #

    def _animate_password(self, final_password, step=0):
        """
        Показує випадкові символи перед фінальним паролем —
        ефект «матриці». Рекурсивно викликає себе через after().
        """
        import random
        import string

        if step < ANIMATION_STEPS:
            chars = string.ascii_letters + string.digits
            fake = "".join(random.choice(chars) for _ in final_password)
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, fake)
            self.after(
                ANIMATION_DELAY,
                self._animate_password(final_password, step + 1)
            )
        else:
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, final_password)
            level, _ = check_strength(final_password)
            self._update_strength(level)



    # ------------------------------------------------------------------ #
    #  Допоміжні методи                                                   #
    # ------------------------------------------------------------------ #

    def _update_strength(self, level):
        config = STRENGTH_CONFIG[level]
        self.strength_bar.set(config["progress"])
        self.strength_bar.configure(progress_color=config["color"])
        self.strength_label.configure(text=config["label"], text_color=config["color"])

    def _reset_strength(self):
        self.strength_bar.set(0)
        self.strength_bar.configure(progress_color="gray")
        self.strength_label.configure(text="—", text_color="gray")

    def _set_status(self, text, color="gray"):
        self.status_label.configure(text=text, text_color=color)



if __name__ == "__main__":
    App().mainloop()