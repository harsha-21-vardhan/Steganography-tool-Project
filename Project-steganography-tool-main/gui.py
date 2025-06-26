import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from steg_utils import encode_text, decode_text, encode_file, decode_file, encrypt_message, decrypt_message

class StegoGUI:
    def __init__(self, root):
        self.root = root = TkinterDnD.Tk()
        root.title("Steganography Tool")
        root.geometry("500x400")

        self.image_path = None
        self.output_path = "output.png"

        self.label = tk.Label(root, text="Drag & Drop Image Here", width=60, height=4, relief="groove")
        self.label.pack(pady=10)
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.drop_image)

        self.message_entry = tk.Text(root, height=6, width=50)
        self.message_entry.pack(pady=10)

        self.encode_btn = tk.Button(root, text="Hide Message", command=self.hide_message)
        self.encode_btn.pack(pady=5)

        self.decode_btn = tk.Button(root, text="Extract Message", command=self.extract_message)
        self.decode_btn.pack(pady=5)

        self.encode_file_btn = tk.Button(root, text="Hide File", command=self.hide_file)
        self.encode_file_btn.pack(pady=5)

        self.decode_file_btn = tk.Button(root, text="Extract File", command=self.extract_file)
        self.decode_file_btn.pack(pady=5)

    def drop_image(self, event):
        self.image_path = event.data.strip('{}')
        self.label.config(text=os.path.basename(self.image_path))

    def hide_message(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Drop an image first.")
            return
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Empty Message", "Enter a message to hide.")
            return
        password = simpledialog.askstring("Password", "Enter password to encrypt:", show='*')
        if not password:
            return
        try:
            encrypted_msg = encrypt_message(message, password)
            encode_text(self.image_path, encrypted_msg, self.output_path)
            messagebox.showinfo("Success", f"Message hidden in {self.output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_message(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Drop an image first.")
            return
        password = simpledialog.askstring("Password", "Enter password to decrypt:", show='*')
        if not password:
            return
        try:
            encrypted_msg = decode_text(self.image_path)
            message = decrypt_message(encrypted_msg, password)
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.insert(tk.END, message)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hide_file(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Drop an image first.")
            return
        file_path = filedialog.askopenfilename(title="Select file to hide")
        if not file_path:
            return
        try:
            encode_file(self.image_path, file_path, self.output_path)
            messagebox.showinfo("Success", f"File hidden in {self.output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_file(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Drop an image first.")
            return
        save_path = filedialog.asksaveasfilename(title="Save extracted file as", defaultextension=".bin")
        if not save_path:
            return
        try:
            decode_file(self.image_path, save_path)
            messagebox.showinfo("Success", f"File extracted to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))