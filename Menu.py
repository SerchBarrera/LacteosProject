from customtkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import json
from fpdf import FPDF
import pandas as pd

from Reporte import Reportes
from Inventario import Inventario
from Pedido import Pedidos
from Empresas import Empresas

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x700")  # Aumentar el tamaño de la ventana
        self.root.resizable(0, 0)
        self.root.title("Menú Principal")

        set_appearance_mode("light")

        sidebar_frame = CTkFrame(master=self.root, fg_color="#2A8C55", width=176, height=700, corner_radius=0)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")

        logo_img_data = Image.open(
            "C:\\Users\\sbarr\\PycharmProjects\\ProjectCompleto_V1\\ProjectCompleto_V1\\imagenes\\logo.jpg")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

        CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        reportes_img_data = Image.open(
            "C:\\Users\\sbarr\\PycharmProjects\\ProjectCompleto_V1\\ProjectCompleto_V1\\imagenes\\analytics_icon.png")
        reportes_img = CTkImage(dark_image=reportes_img_data, light_image=reportes_img_data)
        CTkButton(master=sidebar_frame, image=reportes_img, text="Reportes", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w",
                  command=lambda: self.show_view("Reportes")).pack(anchor="center", ipady=5,
                                                                   pady=(60, 0))

        package_img_data = Image.open(
            "C:\\Users\\sbarr\\PycharmProjects\\ProjectCompleto_V1\\ProjectCompleto_V1\\imagenes\\package_icon_white.png")
        package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)
        CTkButton(master=sidebar_frame, image=package_img, text="Pedidos", fg_color="transparent",
                  font=("Arial Bold", 14),
                  hover_color="#207244", anchor="w", command=lambda: self.show_view("Pedidos")).pack(anchor="center",
                                                                                                    ipady=5,
                                                                                                    pady=(16, 0))

        returns_img_data = Image.open(
            "C:\\Users\\sbarr\\PycharmProjects\\ProjectCompleto_V1\\ProjectCompleto_V1\\imagenes\\inventory_icon_white.png")
        returns_img = CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
        CTkButton(master=sidebar_frame, image=returns_img, text="Inventario", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w",
                  command=lambda: self.show_view("Inventario")).pack(anchor="center", ipady=5,
                                                                  pady=(16, 0))

        settings_img_data = Image.open(
            "C:\\Users\\sbarr\\PycharmProjects\\ProjectCompleto_V1\\ProjectCompleto_V1\\imagenes\\store_icon_white.png")
        settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
        CTkButton(master=sidebar_frame, image=settings_img, text="Empresas", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w",
                  command=lambda: self.show_view("Empresas")).pack(anchor="center", ipady=5,
                                                                   pady=(16, 0))

        person_img_data = Image.open(
            "C:\\Users\\sbarr\\PycharmProjects\\ProjectCompleto_V1\\ProjectCompleto_V1\\imagenes\\person_icon.png")
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
        CTkButton(master=sidebar_frame, image=person_img, text="Cerrar Sesion", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w",
                  command=self.cerrar_sesion).pack(anchor="center", ipady=5,
                                                    pady=(160, 0))

        self.main_view = CTkFrame(master=self.root, fg_color="#fff", width=824, height=700, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")

        self.welcome_label = CTkLabel(master=self.main_view, text="Bienvenido, Administrador", font=("Arial Black", 25),
                                      text_color="#2A8C55")
        self.welcome_label.pack(expand=True)

        self.reportes = Reportes(self.main_view)
        self.inventario = Inventario(self.main_view)
        self.pedidos = Pedidos(self.main_view)
        self.empresas = Empresas(self.main_view)

    def show_view(self, view_name):
        for widget in self.main_view.winfo_children():
            widget.destroy()

        if view_name == "Reportes":
            self.reportes.show_reportes_view()
        elif view_name == "Pedidos":
            self.pedidos.show_orders_view()
        elif view_name == "Inventario":
            self.inventario.show_inventory_view()
        elif view_name == "Empresas":
            self.empresas.show_empresas_view()

    def cerrar_sesion(self):
        respuesta = messagebox.askquestion("Cerrar Sesión", "¿Estás seguro que quieres salir?")
        if respuesta == 'yes':
            self.root.destroy()
            import subprocess
            subprocess.Popen(["python", "C:\\Users\\sbarr\\PycharmProjects\\ProjectCompleto_V1\\ProjectCompleto_V1\\IniciarSesion.py"])

if __name__ == "__main__":
    app = CTk()
    MenuApp(app)
    app.mainloop()
