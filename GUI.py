import tkinter as tk
from tkinter import ttk
import pyjokes


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


    def show_joke(self, category):
        try:
            joke = pyjokes.get_joke(category=category,language="ru")
        except ValueError:
            joke = "Invalid category selected."

        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, joke)


if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()
