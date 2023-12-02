import tkinter as tk
from tkinter import scrolledtext
import time
import threading
import random
import requests
import json
import codecs

def remove_unicode_escapes(text):
    if text is not None:
        text = codecs.escape_decode(text.encode('utf-8'))[0].decode('utf-8')
    return text

class TypeSpeedGUI:

    def __init__(self, news_texts):
        self.root = tk.Tk()
        self.root.title("Type-A-Ware")
        self.root.geometry("800x400")
        self.root.configure(bg='#2c3e50')  

        self.texts = news_texts

        self.frame = tk.Frame(self.root, padx=20, pady=20, bg='#2c3e50')  
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.sample_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=70, height=5, font=("Poppins", 14), bg='#34495e', fg='#ecf0f1')  
        self.sample_text.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        self.input_entry = tk.Entry(self.frame, width=30, font=("Poppins", 24), bg='#34495e', fg='#ecf0f1')  
        self.input_entry.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")
        self.input_entry.bind("<KeyRelease>", self.start)

        self.speed_label = tk.Label(self.frame, text='Speed: 0.00 WPM', font=("Poppins", 18), fg='#ecf0f1', bg='#2c3e50')  
        self.speed_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset, bg='#3498db', fg='#ecf0f1')  
        self.reset_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)

        self.counter = 0
        self.running = False

        self.set_sample_text()
        self.root.mainloop()

    def set_sample_text(self):
        random_text = random.choice(self.texts)
        self.sample_text.delete(1.0, tk.END)
        self.sample_text.insert(tk.END, random_text)

    def start(self, event):
        if not self.running:
            if event.keysym not in ['Shift_L', 'Control_L', 'Alt_L']:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.sample_text.get("1.0", tk.END).startswith(self.input_entry.get()):
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")

        if self.input_entry.get() == self.sample_text.get("1.0", tk.END).strip():
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

def fetch_and_save_news(api_key, country="us", category="business"):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": country,
        "category": category,
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        content = response.json()
        articles = content['articles']
        descriptions = [article['description'] for article in articles]
        cleaned_descriptions = [description for description in descriptions if description is not None and description != "null"]
        cleaned_descriptions = [description for description in cleaned_descriptions if "<a href" not in description]
        cleaned_descriptions = [remove_unicode_escapes(description) for description in cleaned_descriptions]

        final_descriptions = "|".join(cleaned_descriptions)
        with open('news_data.txt', 'w') as file:
            file.write(final_descriptions)
        return cleaned_descriptions
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

api_key = config['api_key']
news_texts = fetch_and_save_news(api_key)
TypeSpeedGUI(news_texts)
