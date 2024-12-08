import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyjokes
import random
import os


class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke Generator")

        title_label = ttk.Label(root, text="Joke Generator", font=("Arial", 16))
        title_label.pack(pady=10)

        self.text_widget = tk.Text(root, width=50, height=10, wrap=tk.WORD, font=("Arial", 12))
        self.text_widget.pack(pady=10)

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        neutral_button = ttk.Button(button_frame, text="Neutral", command=lambda: self.show_joke("neutral"))
        neutral_button.grid(row=0, column=0, padx=5)

        chuck_button = ttk.Button(button_frame, text="Chuck Norris", command=lambda: self.show_joke("chuck"))
        chuck_button.grid(row=0, column=1, padx=5)

        all_button = ttk.Button(button_frame, text="All", command=lambda: self.show_joke("all"))
        all_button.grid(row=0, column=2, padx=5)

        meme_button = ttk.Button(button_frame, text="Meme", command=self.show_meme)
        meme_button.grid(row=0, column=3, padx=5)

        self.image_label = ttk.Label(root)
        self.image_label.pack(pady=10)

    def show_joke(self, category):
        try:
            joke = pyjokes.get_joke(category=category, language="en")
        except ValueError:
            joke = "Invalid category selected."

        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, joke)

    def show_meme(self):
        
        meme_folder = "memes"  
        try:
            meme_files = [file for file in os.listdir(meme_folder) if file.endswith(('.png', '.jpg', '.jpeg'))]
            if not meme_files:
                raise FileNotFoundError("No meme images found in the folder.")

            random_meme = random.choice(meme_files)
            image_path = os.path.join(meme_folder, random_meme)

            
            image = Image.open(image_path)
            image = image.resize((400, 400), Image.Resampling.LANCZOS)  
            photo = ImageTk.PhotoImage(image)

            self.image_label.configure(image=photo)
            self.image_label.image = photo
        except Exception as e:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()
