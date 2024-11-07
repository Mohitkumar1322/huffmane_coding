import tkinter as tk
from tkinter import filedialog, messagebox
from huffman_code import HuffmanCode

# Define the main application window class
class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Coding Compressor")
        self.root.geometry("500x400")  # Set the window size
        self.root.configure(bg='#2C3E50')  # Dark background color

        # Create a header label
        self.header_label = tk.Label(root, text="Huffman Coding Compression", font=("Arial", 16, "bold"), fg="white", bg="#2C3E50")
        self.header_label.pack(pady=20)

        # Create a label for showing status
        self.status_label = tk.Label(root, text="Choose a file to compress", font=("Arial", 12), fg="white", bg="#2C3E50")
        self.status_label.pack(pady=10)

        # Create a button to choose the file
        self.browse_button = tk.Button(root, text="Browse File", font=("Arial", 12), command=self.browse_file, relief="raised", bg="#16A085", fg="white")
        self.browse_button.pack(pady=10)

        # Create a button to start the compression process
        self.compress_button = tk.Button(root, text="Start Compression", font=("Arial", 12), command=self.start_compression, state=tk.DISABLED, relief="raised", bg="#2980B9", fg="white")
        self.compress_button.pack(pady=10)

        # Create a label for showing the file path
        self.filepath_label = tk.Label(root, text="", font=("Arial", 10), fg="white", bg="#2C3E50")
        self.filepath_label.pack(pady=10)

    # Function to browse for the file to be compressed
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            self.filepath_label.config(text=f"File selected: {file_path}")
            self.selected_file = file_path
            self.compress_button.config(state=tk.NORMAL)  # Enable the compression button

    # Function to start the compression
    def start_compression(self):
        if hasattr(self, 'selected_file'):
            self.status_label.config(text="Compression in progress...", fg="#F39C12")
            self.root.update()

            huffman = HuffmanCode(self.selected_file)
            output_file = huffman.compression()

            self.status_label.config(text=f"Compression successful! Saved to {output_file}", fg="#2ECC71")
            messagebox.showinfo("Success", f"File compressed and saved to {output_file}")
        else:
            messagebox.showerror("Error", "No file selected. Please select a file first.")

# Create the main window instance
root = tk.Tk()
app = HuffmanApp(root)

# Start the Tkinter event loop
root.mainloop()
