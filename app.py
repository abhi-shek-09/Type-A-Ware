import tkinter as tk
from tkinter import scrolledtext
import time
import threading
import random

class TypeSpeedGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Type-A-Ware")
        self.root.geometry("800x400")
        self.texts = open('news_data.txt', 'r').read().split('|')

        self.frame = tk.Frame(self.root, padx=20, pady=20)

        self.sample_label = tk.Label(self.frame, text="", font=("Poppins", 18), wraplength=600, justify='left')
        self.sample_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.sample_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=50, height=5, font=("Poppins", 14))
        self.sample_text.grid(row=1, column=0, columnspan=2, pady=10)

        self.input_entry = tk.Entry(self.frame, width=40, font=("Poppins", 24))
        self.input_entry.grid(row=2, column=0, columnspan=2, pady=10)
        self.input_entry.bind("<KeyRelease>", self.start)

        self.speed_label = tk.Label(self.frame, text='Speed: 0.00 WPM', font=("Poppins", 18))
        self.speed_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.frame.pack(expand=True, fill="both")

        self.counter = 0
        self.running = False

        self.set_sample_text()
        self.root.mainloop()

    def set_sample_text(self):
        random_text = random.choice(self.texts)
        self.sample_label.config(text=random_text)
        self.sample_text.delete(1.0, tk.END)
        self.sample_text.insert(tk.END, random_text)

    def start(self, event):
        if not self.running:
            if event.keysym not in ['Shift_L', 'Control_L', 'Alt_L']:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.sample_label.cget('text').startswith(self.input_entry.get()):
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")

        if self.input_entry.get() == self.sample_label.cget('text'):
            self.running = False
            self.input_entry.config(fg="green")

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            wpm = (len(self.input_entry.get().split(' ')) / self.counter) * 60
            self.speed_label.config(text=f"Speed: {wpm:.2f} WPM")

    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_label.config(text="Speed: 0.00 WPM")
        self.set_sample_text()
        self.input_entry.delete(0, tk.END)

TypeSpeedGUI()
