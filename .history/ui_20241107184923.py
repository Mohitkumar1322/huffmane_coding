# ui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from huffman_code import HuffmanCode

class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Compression Tool")
        
        self.select_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=10)
        
        self.compress_button = tk.Button(root, text="Compress", command=self.compress_file, state=tk.DISABLED)
        self.compress_button.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Select a file to start.")
        self.status_label.pack(pady=10)

    def select_file(self):
        self.filepath = filedialog.askopenfilename()
        if self.filepath:
            self.status_label.config(text=f"Selected File: {self.filepath}")
            self.compress_button.config(state=tk.NORMAL)
    
    def compress_file(self):
        huffman = HuffmanCode(self.filepath)
        output_path = huffman.compression()
        messagebox.showinfo("Compression Complete", f"File compressed:\n{output_path}")
        self.status_label.config(text="Compression completed successfully!")

root = tk.Tk()
app = HuffmanApp(root)
root.mainloop()
