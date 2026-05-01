import customtkinter as ctk
from logic import generate_password

# Налаштування зовнішнього вигляду за замовчуванням
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.geometry("480x420")
        self.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        # Відступи для всього вмісту
        self.grid_columnconfigure(0, weight=1)

        # --- Заголовок ---
        title_label = ctk.CTkLabel(
            self,
            text="Password Generator",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        title_label.grid(row=0, column=0, padx=24, pady=(24, 4))

        subtitle_label = ctk.CTkLabel(
            self,
            text="Налаштуй та згенеруй надійний пароль",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        )
        subtitle_label.grid(row=1, column=0, padx=24, pady=(0, 16))

        # --- Поле виводу пароля ---
        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Тут з'явиться пароль...",
            font=ctk.CTkFont(size=15, family="Courier"),
            height=48,
            justify="center",
        )
        self.password_entry.grid(row=2, column=0, padx=24, pady=(0, 16), sticky="ew")

        # --- Слайдер довжини ---
        length_frame = ctk.CTkFrame(self, fg_color="transparent")
        length_frame.grid(row=3, column=0, padx=24, pady=(0, 8), sticky="ew")
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
        checkboxes_frame.grid(row=4, column=0, padx=24, pady=(0, 16), sticky="ew")
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
        self.generate_btn.grid(row=5, column=0, padx=24, pady=(0, 8), sticky="ew")

        # --- Повідомлення про помилку ---
        self.error_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#e05555",
        )
        self.error_label.grid(row=6, column=0, padx=24, pady=(0, 16))

    # --- Обробники подій ---

    def on_slider_change(self, value):
        """Оновлює лейбл поруч зі слайдером."""
        self.length_label.configure(text=str(int(value)))

    def on_generate(self):
        """Генерує пароль і виводить у поле."""
        password = generate_password(
            length=self.length_var.get(),
            use_upper=self.use_upper.get(),
            use_lower=self.use_lower.get(),
            use_digits=self.use_digits.get(),
            use_special=self.use_special.get(),
        )

        if password is None:
            self.error_label.configure(text="Оберіть хоча б один тип символів!")
            self.password_entry.delete(0, "end")
            return

        self.error_label.configure(text="")
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)


if __name__ == "__main__":
    App().mainloop()