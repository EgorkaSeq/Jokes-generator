import customtkinter as ctk
from PIL import Image, ImageTk
import os
import random
import pyjokes
import tkinter as tk
from tkinter import messagebox
import pygame


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke & Meme Generator")
        self.root.geometry("1280x960")

        # Инициализация музыки
        pygame.mixer.init()
        try:
            pygame.mixer.music.load("pythonproject.mp3")
            pygame.mixer.music.play(-1)
        except FileNotFoundError:
            print("Warning: Music file 'pythonproject.mp3' not found.")
        
        # Главный фрейм
        self.main_frame = ctk.CTkFrame(self.root, width=1280, height=960)
        self.main_frame.pack(fill="both", expand=True)

        # Загрузка мемов
        self.available_memes = []
        self.used_memes = []
        self.load_memes()

        # Создание экранов
        self.greeting_frame = self.create_greeting_frame()
        self.game_frame = self.create_game_frame()

        # Отображение приветственного экрана
        self.show_frame(self.greeting_frame)

    def create_greeting_frame(self):
        """Создает приветственное окно."""
        frame = ctk.CTkFrame(self.main_frame, width=1280, height=960)
        self.set_background(frame, "welcome.jpg")

        # Приветствие
        ctk.CTkLabel(frame, text="Welcome to Joke & Meme Generator!",
                     font=("Comic Sans MS", 28, "bold")).place(relx=0.5, rely=0.2, anchor="center")

        intro_text = (
            "Шутки – это мост между людьми. Они позволяют нам смеяться над собой, преодолевать барьеры и находить общий "
            "язык даже в самых сложных ситуациях. Шутки могут быть лекарством для души и способом сделать мир немного светлее."
        )
        ctk.CTkLabel(frame, text=intro_text, font=("Comic Sans MS", 10), wraplength=400).place(x=880, y=30)

        # Кнопка продолжения
        ctk.CTkButton(frame, text="Continue", font=("Comic Sans MS", 14),
                      command=lambda: self.show_frame(self.game_frame)).place(relx=0.5, rely=0.5, anchor="center")

        # Ползунок громкости
        volume_slider = ctk.CTkSlider(frame, from_=0, to=1, command=self.set_volume, width=400)
        volume_slider.place(relx=0.5, rely=0.65, anchor="center")
        volume_slider.set(0.3)
        ctk.CTkLabel(frame, text="Volume", font=("Comic Sans MS", 14)).place(relx=0.5, rely=0.6, anchor="center")

        # Кнопка выхода
        ctk.CTkButton(frame, text="Exit", font=("Comic Sans MS", 14), fg_color="#FF6347",
                      command=self.exit_app).place(relx=0.5, rely=0.75, anchor="center")

        return frame

    def create_game_frame(self):
        """Создает основное окно с шутками и мемами."""
        frame = ctk.CTkFrame(self.main_frame, width=1280, height=960)
        self.set_background(frame, "back.png")

        # Заголовок
        ctk.CTkLabel(frame, text="Joke & Meme Generator", font=("Comic Sans MS", 28, "bold")).place(relx=0.5, rely=0.05, anchor="n")

        # Поле для шуток
        self.text_widget = ctk.CTkTextbox(
            frame, width=600, height=300, font=("Comic Sans MS", 16),
            wrap="word", fg_color="white", text_color="black"
        )
        self.text_widget.place(x=50, y=150)

        # Кнопки управления
        buttons = [
            ("Chuck Norris", lambda: self.show_joke("chuck"), "#228B22"),
            ("All", lambda: self.show_joke("all"), "#9370DB"),
            ("Neutral", lambda: self.show_joke("neutral"), "#FF4500"),
            ("Show Meme", self.show_meme, "#FFA500")
        ]
        for i, (text, command, color) in enumerate(buttons):
            ctk.CTkButton(frame, text=text, command=command, font=("Comic Sans MS", 12, "bold"), fg_color=color).place(x=50 + i * 150, y=500)

        # Поле для мемов
        self.image_label = ctk.CTkLabel(frame, text="", corner_radius=15, width=500, height=500)
        self.image_label.place(x=700, y=150)

        # Кнопка назад и выхода
        ctk.CTkButton(frame, text="Back", font=("Comic Sans MS", 12, "bold"),
                      command=lambda: self.show_frame(self.greeting_frame)).place(x=50, y=650)
        ctk.CTkButton(frame, text="Exit", font=("Comic Sans MS", 12, "bold"),
                      command=self.exit_app).place(x=200, y=650)

        return frame

    def load_memes(self):
        """Загружает список всех мемов из папки."""
        meme_folder = "memes"
        try:
            self.available_memes = [
                os.path.join(meme_folder, file) for file in os.listdir(meme_folder)
                if file.lower().endswith(('.png', '.jpg', '.jpeg'))
            ]
        except FileNotFoundError:
            print(f"Error: Folder '{meme_folder}' not found.")
        except Exception as e:
            print(f"Error loading memes: {e}")

    def show_meme(self):
        """Показывает случайный мем, исключая уже показанные."""
        if not self.available_memes:
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("end", "All memes have been shown! Restart the app to reset.")
            return

        meme_path = random.choice(self.available_memes)
        self.available_memes.remove(meme_path)
        self.used_memes.append(meme_path)

        try:
            image = Image.open(meme_path)
            image = image.resize((500, 500), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        except Exception as e:
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("end", f"Error displaying meme: {e}")

    def show_joke(self, category):
        """Отображает шутку в текстовом поле."""
        try:
            joke = pyjokes.get_joke(category=category, language="en")
        except ValueError:
            joke = "Invalid category selected."
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("end", joke)

    def set_background(self, frame, image_path):
        """Устанавливает фон для фрейма."""
        canvas = tk.Canvas(frame, width=1280, height=960)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open(image_path)
            image = image.resize((1280, 960), Image.Resampling.LANCZOS)
            bg_image = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, image=bg_image, anchor="nw")
            frame.bg_image = bg_image
        except Exception as e:
            print(f"Error loading background: {e}")

    def show_frame(self, frame):
        """Отображает указанный фрейм."""
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()
        frame.pack(fill="both", expand=True)

    def set_volume(self, value):
        """Устанавливает громкость музыки."""
        pygame.mixer.music.set_volume(float(value))

    def exit_app(self):
        """Закрывает приложение."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
