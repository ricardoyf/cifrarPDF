import os
import tkinter as tk
from tkinter import filedialog, messagebox

import pikepdf
from tkinterdnd2 import DND_FILES, TkinterDnD

APP_TITLE = "PDF Cifrador"


def clean_drop_path(data: str) -> str:
    data = data.strip()
    if data.startswith("{") and data.endswith("}"):
        data = data[1:-1]
    return data


class PdfEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("560x430")
        self.root.resizable(False, False)
        self.pdf_path = tk.StringVar()

        tk.Label(root, text="Cifrar PDF con contraseña", font=("Segoe UI", 18, "bold")).pack(pady=(24, 8))
        tk.Label(root, text="El PDF se cifra localmente en este ordenador con AES-256.", font=("Segoe UI", 10)).pack(pady=(0, 14))

        self.drop_zone = tk.Label(
            root,
            text="Arrastra aquí un PDF\n\no haz clic para seleccionarlo",
            relief="groove",
            borderwidth=2,
            width=52,
            height=6,
            font=("Segoe UI", 11),
            cursor="hand2",
        )
        self.drop_zone.pack(pady=8)
        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind("<<Drop>>", self.on_drop)
        self.drop_zone.bind("<Button-1>", self.select_pdf)

        self.file_label = tk.Label(root, text="Ningún archivo seleccionado", font=("Segoe UI", 9))
        self.file_label.pack(pady=(4, 14))

        form = tk.Frame(root)
        form.pack()
        tk.Label(form, text="Contraseña:", width=20, anchor="e", font=("Segoe UI", 10)).grid(row=0, column=0, padx=6, pady=6)
        self.password1 = tk.Entry(form, show="●", width=28, font=("Segoe UI", 10))
        self.password1.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(form, text="Repetir contraseña:", width=20, anchor="e", font=("Segoe UI", 10)).grid(row=1, column=0, padx=6, pady=6)
        self.password2 = tk.Entry(form, show="●", width=28, font=("Segoe UI", 10))
        self.password2.grid(row=1, column=1, padx=6, pady=6)

        self.encrypt_button = tk.Button(root, text="Cifrar PDF", command=self.encrypt_pdf, width=22, height=2, font=("Segoe UI", 11, "bold"))
        self.encrypt_button.pack(pady=22)
        self.status = tk.Label(root, text="", font=("Segoe UI", 9))
        self.status.pack()

    def set_pdf(self, path):
        if not path:
            return
        path = os.path.abspath(path)
        if not os.path.isfile(path) or not path.lower().endswith(".pdf"):
            messagebox.showerror(APP_TITLE, "Selecciona un archivo PDF válido.")
            return
        self.pdf_path.set(path)
        self.file_label.config(text=os.path.basename(path))
        self.status.config(text="PDF preparado para cifrar")
        self.password1.focus_set()

    def on_drop(self, event):
        path = clean_drop_path(event.data)
        try:
            paths = self.root.tk.splitlist(event.data)
            if paths:
                path = paths[0]
        except Exception:
            pass
        self.set_pdf(path)

    def select_pdf(self, _event=None):
        path = filedialog.askopenfilename(title="Seleccionar PDF", filetypes=[("Archivos PDF", "*.pdf")])
        self.set_pdf(path)

    def encrypt_pdf(self):
        source = self.pdf_path.get()
        if not source:
            messagebox.showwarning(APP_TITLE, "Arrastra o selecciona primero un PDF.")
            return

        password_a = self.password1.get()
        password_b = self.password2.get()
        if not password_a:
            messagebox.showwarning(APP_TITLE, "Introduce una contraseña.")
            return
        if password_a != password_b:
            messagebox.showerror(APP_TITLE, "Las dos contraseñas no coinciden.")
            return

        folder = os.path.dirname(source)
        stem = os.path.splitext(os.path.basename(source))[0]
        destination = filedialog.asksaveasfilename(
            title="Guardar PDF cifrado",
            initialdir=folder,
            initialfile=f"{stem}_cifrado.pdf",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
        )
        if not destination:
            return
        if os.path.abspath(destination).lower() == os.path.abspath(source).lower():
            messagebox.showerror(APP_TITLE, "El archivo cifrado debe guardarse con otro nombre.")
            return

        self.encrypt_button.config(state="disabled")
        self.status.config(text="Cifrando…")
        self.root.update_idletasks()

        try:
            with pikepdf.open(source) as pdf:
                encryption = pikepdf.Encryption(
                    owner=password_a,
                    user=password_a,
                    R=6,
                    aes=True,
                    metadata=True,
                )
                pdf.save(destination, encryption=encryption)

            with pikepdf.open(destination, password=password_a):
                pass

            self.password1.delete(0, tk.END)
            self.password2.delete(0, tk.END)
            self.status.config(text="PDF cifrado correctamente")
            messagebox.showinfo(APP_TITLE, f"PDF cifrado correctamente con AES-256.\n\nGuardado en:\n{destination}")
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"No se ha podido cifrar el PDF.\n\n{exc}")
            self.status.config(text="Error al cifrar")
        finally:
            self.encrypt_button.config(state="normal")


def main():
    root = TkinterDnD.Tk()
    PdfEncryptorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
