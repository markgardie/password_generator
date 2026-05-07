import customtkinter as ctk
from logic import generate_password

# Налаштування зовнішнього вигляду за замовчуванням
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        self.title("Генератор паролю")
        self.geometry("480x420")
        self.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        pass

    # --- Обробники подій ---

    def on_slider_change(self, value):
        pass

    def on_generate(self):
        pass


if __name__ == "__main__":
    App().mainloop()