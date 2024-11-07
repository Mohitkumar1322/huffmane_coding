# main.py

import ui  # Import the ui module to start the GUI

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    app = ui.HuffmanApp(root)
    root.mainloop()
