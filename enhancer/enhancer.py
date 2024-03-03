import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
import threading
import os

class PhotoEnhancerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Enhancer")

        # Interfaccia per caricare l'immagine
        self.load_button = tk.Button(root, text="Carica Immagine", command=self.load_image)
        self.load_button.pack()

        # Opzioni di risoluzione
        self.resolution_var = tk.StringVar()
        self.resolutions = ['5500x5500', '4500x4500', '2000x2000', '3000x3000']
        self.resolution_menu = ttk.Combobox(root, textvariable=self.resolution_var, values=self.resolutions)
        self.resolution_menu.pack()

        # Pulsante per avviare il miglioramento
        self.start_button = tk.Button(root, text="Avvia Miglioramento", command=self.start_enhancing)
        self.start_button.pack()

        # Barra di progresso
        self.progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
        self.progress.pack()

        # Stato
        self.status_label = tk.Label(root, text="Stato: In attesa")
        self.status_label.pack()

        self.file_path = None

    def load_image(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.image = Image.open(self.file_path)
            self.update_status("Immagine caricata")

    def start_enhancing(self):
        selected_resolution = self.resolution_var.get()
        if selected_resolution and self.file_path:
            width, height = map(int, selected_resolution.split('x'))
            threading.Thread(target=self.enhance_image, args=(width, height), daemon=True).start()

    def enhance_image(self, width, height):
        self.update_status("In corso")
        self.progress['maximum'] = 100
        for i in range(101):
            self.progress['value'] = i
            self.root.update_idletasks()

        enhanced_img = self.image.resize((width, height), Image.LANCZOS)
        save_path = os.path.join(os.path.dirname(__file__), f"enhanced_{os.path.basename(self.file_path)}")
        enhanced_img.save(save_path)
        self.update_status("Fatto - Immagine salvata")

    def update_status(self, status):
        self.status_label.configure(text=f"Stato: {status}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoEnhancerApp(root)
    root.mainloop()
