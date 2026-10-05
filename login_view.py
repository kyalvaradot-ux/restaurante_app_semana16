import tkinter as tk
from tkinter import ttk, messagebox


class LoginView(tk.Frame):
    def __init__(self, master, servicio, on_login):
        super().__init__(master, bg="#f5f7fb")
        self.servicio = servicio
        self.on_login = on_login
        self.pack(fill="both", expand=True)
        self._crear_interfaz()

    def _crear_interfaz(self):
        panel = tk.Frame(self, bg="white", padx=45, pady=35)
        panel.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(panel, text="RESTAURANTE APP", font=("Segoe UI", 22, "bold"), bg="white").pack(pady=(0, 8))
        tk.Label(panel, text="Inicio de sesión", font=("Segoe UI", 11), bg="white").pack(pady=(0, 22))
        tk.Label(panel, text="Usuario", bg="white", anchor="w").pack(fill="x")
        self.usuario = ttk.Entry(panel, width=35)
        self.usuario.pack(pady=(4, 12))
        tk.Label(panel, text="Contraseña", bg="white", anchor="w").pack(fill="x")
        self.contrasena = ttk.Entry(panel, width=35, show="*")
        self.contrasena.pack(pady=(4, 18))
        ttk.Button(panel, text="Ingresar", command=self.iniciar).pack(fill="x")
        tk.Label(panel, text="Administrador inicial: admin / admin123", fg="#666", bg="white").pack(pady=(15, 0))
        self.contrasena.bind("<Return>", lambda event: self.iniciar())
        self.usuario.focus_set()

    def iniciar(self):
        usuario = self.servicio.autenticar(self.usuario.get().strip(), self.contrasena.get())
        if usuario:
            self.on_login(usuario)
        else:
            messagebox.showerror("Acceso", "Usuario o contraseña incorrectos.")
