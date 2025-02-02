from customtkinter import *
import tkinter as tk
from tkinter import messagebox
import json

class Empresas:
    def __init__(self, parent):
        self.parent = parent
        self.empresas = []

    def show_empresas_view(self):
        title_frame = CTkFrame(master=self.parent, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Empresas", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")
        button_frame = CTkFrame(master=self.parent, fg_color="transparent")
        button_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        CTkButton(master=button_frame, text="Ver Empresas", font=("Arial", 12), command=self.load_empresas_table, fg_color="#2A8C55", hover_color="#66d681").pack(
            side="left", padx=(0, 10))
        CTkButton(master=button_frame, text="Añadir Empresa", font=("Arial", 12), command=self.add_empresa, fg_color="#2A8C55", hover_color="#66d681").pack(
            side="left", padx=(0, 10))
        CTkButton(master=button_frame, text="Actualizar Empresa", font=("Arial", 12), command=self.update_empresa, fg_color="#2A8C55", hover_color="#66d681").pack(
            side="left", padx=(0, 10))
        CTkButton(master=button_frame, text="Eliminar Empresa", font=("Arial", 12), command=self.delete_empresa, fg_color="#2A8C55", hover_color="#66d681").pack(
            side="left", padx=(0, 10))

        self.table_frame = CTkFrame(master=self.parent, fg_color="transparent")
        self.table_frame.pack(anchor="n", fill="both", expand=True, padx=27, pady=(10, 0))

    def load_empresas_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        try:
            with open('imagenes/empresas.json', 'r') as f:
                self.empresas = json.load(f)

            columns = ["ID Empresa", "Empresa", "Calle", "Codigo Postal", "Numero de Contacto"]
            rows = [list(item.values()) for item in self.empresas]

            table = CTkScrollableFrame(master=self.table_frame, fg_color="transparent")
            table.pack(expand=True, fill="both")

            for col, column_name in enumerate(columns):
                CTkLabel(master=table, text=column_name, font=("Arial", 12, "bold"), fg_color="#2A8C55",
                         text_color="#fff").grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

            for row, data_row in enumerate(rows, start=1):
                bg_color = "#f0f0f0" if row % 2 == 0 else "#e0e0e0"
                for col, value in enumerate(data_row):
                    CTkLabel(master=table, text=value, font=("Arial", 12), fg_color=bg_color).grid(row=row,
                                                                                                   column=col,
                                                                                                   padx=10, pady=5,
                                                                                                   sticky="nsew")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla de empresas: {e}")

    def add_empresa(self):
        add_empresa_window = tk.Toplevel(self.parent)
        add_empresa_window.title("Añadir Empresa")
        add_empresa_window.geometry("400x600")

        CTkLabel(master=add_empresa_window, text="Nombre de la Empresa").pack(pady=10)
        nombre_entry = CTkEntry(master=add_empresa_window)
        nombre_entry.pack()

        CTkLabel(master=add_empresa_window, text="Calle").pack(pady=10)
        calle_entry = CTkEntry(master=add_empresa_window)
        calle_entry.pack()

        CTkLabel(master=add_empresa_window, text="Codigo Postal").pack(pady=10)
        cp_entry = CTkEntry(master=add_empresa_window)
        cp_entry.pack()

        CTkLabel(master=add_empresa_window, text="Numero de Contacto").pack(pady=10)
        contacto_entry = CTkEntry(master=add_empresa_window)
        contacto_entry.pack()

        def save_empresa():
            nombre = nombre_entry.get()
            calle = calle_entry.get()
            cp = cp_entry.get()
            contacto = contacto_entry.get()

            if not nombre or not calle or not cp or not contacto:
                messagebox.showerror("Error", "No se aceptan campos vacíos.")
                return

            try:
                cp_num = int(cp)
                if cp_num <= 0 or len(cp) != 5:
                    messagebox.showerror("Error", "El código postal debe ser un número positivo de 5 dígitos.")
                    return
            except ValueError:
                messagebox.showerror("Error", "El código postal debe ser un número.")
                return

            try:
                contacto_num = int(contacto)
                if contacto_num <= 0 or len(contacto) != 10:
                    messagebox.showerror("Error", "El número de contacto debe ser un número positivo de 10 dígitos.")
                    return
            except ValueError:
                messagebox.showerror("Error", "El número de contacto debe ser un número.")
                return

            if not self.empresas:
                id_empresa = 1
            else:
                id_empresa = max(item["ID Empresa"] for item in self.empresas) + 1

            new_empresa = {
                "ID Empresa": id_empresa,
                "Empresa": nombre,
                "Calle": calle,
                "Codigo Postal": cp,
                "Numero de Contacto": contacto
            }

            self.empresas.append(new_empresa)
            with open('imagenes/empresas.json', 'w') as f:
                json.dump(self.empresas, f)

            messagebox.showinfo("Éxito", f"Se agregó la empresa {nombre} correctamente.")
            add_empresa_window.destroy()
            self.load_empresas_table()

        CTkButton(master=add_empresa_window, text="Guardar", command=save_empresa, fg_color="#2A8C55", hover_color="#66d681").pack(pady=20)

    def update_empresa(self):
        update_empresa_window = tk.Toplevel(self.parent)
        update_empresa_window.title("Actualizar Empresa")
        update_empresa_window.geometry("400x600")

        CTkLabel(master=update_empresa_window, text="Seleccionar ID Empresa").pack(pady=10)
        id_empresa_var = tk.StringVar()
        id_empresa_dropdown = CTkComboBox(master=update_empresa_window, values=[str(item["ID Empresa"]) for item in self.empresas], variable=id_empresa_var)
        id_empresa_dropdown.pack()

        def load_empresa_info(*args):
            id_empresa = int(id_empresa_var.get())
            empresa = next(item for item in self.empresas if item["ID Empresa"] == id_empresa)
            nombre_entry.delete(0, tk.END)
            nombre_entry.insert(0, empresa["Empresa"])
            calle_entry.delete(0, tk.END)
            calle_entry.insert(0, empresa["Calle"])
            cp_entry.delete(0, tk.END)
            cp_entry.insert(0, empresa.get("Codigo Postal", ""))
            contacto_entry.delete(0, tk.END)
            contacto_entry.insert(0, empresa["Numero de Contacto"])

        id_empresa_var.trace("w", load_empresa_info)

        CTkLabel(master=update_empresa_window, text="Nombre de la Empresa").pack(pady=10)
        nombre_entry = CTkEntry(master=update_empresa_window)
        nombre_entry.pack()

        CTkLabel(master=update_empresa_window, text="Calle").pack(pady=10)
        calle_entry = CTkEntry(master=update_empresa_window)
        calle_entry.pack()

        CTkLabel(master=update_empresa_window, text="Codigo Postal").pack(pady=10)
        cp_entry = CTkEntry(master=update_empresa_window)
        cp_entry.pack()

        CTkLabel(master=update_empresa_window, text="Numero de Contacto").pack(pady=10)
        contacto_entry = CTkEntry(master=update_empresa_window)
        contacto_entry.pack()

        def save_updated_empresa():
            id_empresa = int(id_empresa_var.get())
            nombre = nombre_entry.get()
            calle = calle_entry.get()
            cp = cp_entry.get()
            contacto = contacto_entry.get()

            if not nombre or not calle or not cp or not contacto:
                messagebox.showerror("Error", "No se aceptan campos vacíos.")
                return

            try:
                cp_num = int(cp)
                if cp_num <= 0 or len(cp) != 5:
                    messagebox.showerror("Error", "El código postal debe ser un número positivo de 5 dígitos.")
                    return
            except ValueError:
                messagebox.showerror("Error", "El código postal debe ser un número.")
                return

            try:
                contacto_num = int(contacto)
                if contacto_num <= 0 or len(contacto) != 10:
                    messagebox.showerror("Error", "El número de contacto debe ser un número positivo de 10 dígitos.")
                    return
            except ValueError:
                messagebox.showerror("Error", "El número de contacto debe ser un número.")
                return

            empresa = next(item for item in self.empresas if item["ID Empresa"] == id_empresa)
            empresa["Empresa"] = nombre
            empresa["Calle"] = calle
            empresa["Codigo Postal"] = cp
            empresa["Numero de Contacto"] = contacto

            with open('imagenes/empresas.json', 'w') as f:
                json.dump(self.empresas, f)

            messagebox.showinfo("Éxito", "Se ha actualizado la empresa correctamente.")
            update_empresa_window.destroy()
            self.load_empresas_table()

        CTkButton(master=update_empresa_window, text="Actualizar", command=save_updated_empresa, fg_color="#2A8C55", hover_color="#66d681").pack(pady=20)

    def delete_empresa(self):
        delete_empresa_window = tk.Toplevel(self.parent)
        delete_empresa_window.title("Eliminar Empresa")
        delete_empresa_window.geometry("400x400")

        CTkLabel(master=delete_empresa_window, text="Seleccionar ID Empresa").pack(pady=10)
        id_empresa_var = tk.StringVar()
        id_empresa_dropdown = CTkComboBox(master=delete_empresa_window, values=[str(item["ID Empresa"]) for item in self.empresas], variable=id_empresa_var)
        id_empresa_dropdown.pack()

        empresa_info_label = CTkLabel(master=delete_empresa_window, text="")
        empresa_info_label.pack(pady=10)

        def load_empresa_info(*args):
            id_empresa = int(id_empresa_var.get())
            empresa = next(item for item in self.empresas if item["ID Empresa"] == id_empresa)
            empresa_info_label.configure(text=f"Empresa: {empresa['Empresa']}\nCalle: {empresa['Calle']}\nCodigo Postal: {empresa['Codigo Postal']}\nNumero de Contacto: {empresa['Numero de Contacto']}")

        id_empresa_var.trace("w", load_empresa_info)

        def confirm_delete_empresa():
            id_empresa = int(id_empresa_var.get())
            self.empresas = [item for item in self.empresas if item["ID Empresa"] != id_empresa]

            # Reajustar los IDs
            for idx, item in enumerate(self.empresas):
                item["ID Empresa"] = idx + 1

            with open('imagenes/empresas.json', 'w') as f:
                json.dump(self.empresas, f)

            messagebox.showinfo("Éxito", "Empresa eliminada correctamente.")
            delete_empresa_window.destroy()
            self.load_empresas_table()

        CTkButton(master=delete_empresa_window, text="Eliminar", command=confirm_delete_empresa, fg_color="#2A8C55", hover_color="#66d681").pack(pady=20)
