import customtkinter as ctk
from PIL import Image, ImageTk
import pyjokes
import os
import random
import tkinter as tk

class GreetingWindow:
    def __init__(self, root, on_continue):
        self.root = root
        self.root.title("Welcome to Joke & Meme Generator")
        self.root.geometry("1280x960")
        
        # Сохраняем функцию для продолжения
        self.on_continue = on_continue
        
        # Заголовок приветственного окна
        greeting_label = ctk.CTkLabel(root, text="Welcome to Joke & Meme Generator!", font=("Comic Sans MS", 28, "bold"))
        greeting_label.place(relx=0.5, rely=0.2, anchor="center")
        
        # Предисловие в правом верхнем углу
        intro_text = ("Шутки – это мост между людьми. Они позволяют нам смеяться над собой, преодолевать барьеры и находить общий "
                      "язык даже в самых сложных ситуациях. Шутки могут быть лекарством для души и способом сделать мир немного светлее.")
        self.intro_label = ctk.CTkLabel(root, text=intro_text, font=("Comic Sans MS", 10), wraplength=400, anchor="ne", width=400)
        self.intro_label.place(x=880, y=30)
        
        # Кнопка "Продолжить", которая откроет главное окно
        continue_button = ctk.CTkButton(root, text="Continue", font=("Comic Sans MS", 14), command=self.on_continue)
        continue_button.place(relx=0.5, rely=0.5, anchor="center")

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke & Meme Generator")
        self.root.geometry("1280x960")
        
        # Устанавливаем цветовую тему
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Задний фон
        self.set_background("back.png")
        
        # Заголовок
        title_label = ctk.CTkLabel(root, text="Joke & Meme Generator", font=("Comic Sans MS", 28, "bold"))
        title_label.place(relx=0.5, rely=0.05, anchor="n")
        
        # Поле для шуток
        self.text_widget = ctk.CTkTextbox(root, width=600, height=300, font=("Comic Sans MS", 14), wrap="word", bg_color="#FFB6C1")
        self.text_widget.place(x=50, y=150)

        # Кнопки управления
        self.buttons = [
            ("Neutral", lambda: self.show_joke("neutral"), "#FFD700"),
            ("Chuck Norris", lambda: self.show_joke("chuck"), "#228B22"),
            ("All", lambda: self.show_joke("all"), "#9370DB"),
            ("Show Meme", self.show_meme, "#FFA500")
        ]

        for i, (text, command, color) in enumerate(self.buttons):
            btn = ctk.CTkButton(
                root, 
                text=text, 
                command=command, 
                font=("Comic Sans MS", 12, "bold"),
                text_color="black", 
                width=120, 
                height=40, 
                fg_color=color,  
                hover_color=self.lighten_color(color),  
                border_width=0  
            )
            btn.place(x=50 + i * 150, y=500)

        # Поле для мемов
        self.image_label = ctk.CTkLabel(root, text="", corner_radius=15, fg_color="white", width=500, height=500)
        self.image_label.place(x=700, y=150)

    def set_background(self, image_path):
        """Добавляет картинку на фон"""
        canvas = tk.Canvas(self.root, width=1280, height=960)
        canvas.place(x=0, y=0)

        image = Image.open(image_path)
        image = image.resize((1280, 960), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def show_joke(self, category):
        """Отображает шутку в текстовом поле"""
        try:
            joke = pyjokes.get_joke(category=category, language="en")
        except ValueError:
            joke = "Invalid category selected."

        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("end", joke)

    def show_meme(self):
        """Показывает случайный мем"""
        meme_folder = "memes"
        try:
            meme_files = [file for file in os.listdir(meme_folder) if file.endswith(('.png', '.jpg', '.jpeg'))]
            if not meme_files:
                raise FileNotFoundError("No meme images found in the folder.")

            random_meme = random.choice(meme_files)
            image_path = os.path.join(meme_folder, random_meme)

            image = Image.open(image_path)
            image = image.resize((500, 500), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            self.image_label.configure(image=photo)
            self.image_label.image = photo
        except Exception as e:
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("end", f"Error: {e}")

    def lighten_color(self, hex_color):
        """Осветляет указанный цвет (для hover-эффекта)"""
        rgb = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
        light_rgb = [min(255, int(c + (255 - c) * 0.5)) for c in rgb]
        return f"#{light_rgb[0]:02x}{light_rgb[1]:02x}{light_rgb[2]:02x}"

def run_app():
    """Запуск основного приложения"""
    try:
        greeting_app.destroy()  # Закрываем окно приветствия
    except Exception as e:
        print(f"Error closing greeting window: {e}")
    app = ctk.CTk()  # Открываем главное окно
    JokeApp(app)
    app.mainloop()

if __name__ == "__main__":
    # Создаем окно приветствия и передаем callback для продолжения
    greeting_app = ctk.CTk()
    GreetingWindow(greeting_app, on_continue=run_app)
    greeting_app.mainloop()
