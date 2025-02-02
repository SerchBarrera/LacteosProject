from customtkinter import *
import tkinter as tk
from tkinter import messagebox
import json

class Inventario:
    def __init__(self, parent):
        self.parent = parent
        self.inventory = []

    def show_inventory_view(self):
        title_frame = CTkFrame(master=self.parent, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Inventario", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")
        button_frame = CTkFrame(master=self.parent, fg_color="transparent")
        button_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        CTkButton(master=button_frame, text="Ver Inventario", font=("Arial", 12), command=self.load_inventory_table, fg_color="#2A8C55", hover_color="#53d573").pack(
            side="left", padx=(0, 10))
        CTkButton(master=button_frame, text="Añadir Producto", font=("Arial", 12), command=self.add_product, fg_color="#2A8C55", hover_color="#53d573").pack(
            side="left", padx=(0, 10))
        CTkButton(master=button_frame, text="Actualizar Producto", font=("Arial", 12), command=self.update_product, fg_color="#2A8C55", hover_color="#53d573").pack(
            side="left", padx=(0, 10))
        CTkButton(master=button_frame, text="Eliminar Producto", font=("Arial", 12), command=self.delete_product, fg_color="#2A8C55", hover_color="#53d573").pack(
            side="left", padx=(0, 10))

        self.table_frame = CTkFrame(master=self.parent, fg_color="transparent")
        self.table_frame.pack(anchor="n", fill="both", expand=True, padx=27, pady=(10, 0))

    def load_inventory_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        try:
            with open('imagenes/inventario.json', 'r') as f:
                self.inventory = json.load(f)

            columns = ["Folio", "Producto", "Cantidad", "Precio", "Unidad de Medida"]
            rows = [list(item.values()) for item in self.inventory]

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
            messagebox.showerror("Error", f"No se pudo cargar la tabla de inventario: {e}")

    def add_product(self):
        add_product_window = tk.Toplevel(self.parent)
        add_product_window.title("Añadir Producto")
        add_product_window.geometry("400x600")

        CTkLabel(master=add_product_window, text="Nombre del Producto").pack(pady=10)
        nombre_entry = CTkEntry(master=add_product_window)
        nombre_entry.pack()

        CTkLabel(master=add_product_window, text="Cantidad").pack(pady=10)
        cantidad_entry = CTkEntry(master=add_product_window)
        cantidad_entry.pack()

        CTkLabel(master=add_product_window, text="Precio").pack(pady=10)
        precio_entry = CTkEntry(master=add_product_window)
        precio_entry.pack()

        CTkLabel(master=add_product_window, text="Unidad de Medida").pack(pady=10)
        unidad_entry = CTkEntry(master=add_product_window)
        unidad_entry.pack()

        def save_product():
            nombre = nombre_entry.get()
            cantidad_str = cantidad_entry.get()
            precio_str = precio_entry.get()
            unidad = unidad_entry.get()

            if not nombre or not cantidad_str or not precio_str or not unidad:
                messagebox.showerror("Error", "Todos los campos son obligatorios. No puedes guardar.")
                return

            try:
                cantidad = int(cantidad_str)
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser un número positivo mayor que cero.")
                    return
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número.")
                return

            try:
                precio = float(precio_str)
                if precio <= 0:
                    messagebox.showerror("Error", "El precio debe ser un número positivo mayor que cero.")
                    return
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número.")
                return

            if not self.inventory:
                folio = 1
            else:
                folio = max(item["Folio"] for item in self.inventory) + 1

            new_product = {
                "Folio": folio,
                "Producto": nombre,
                "Cantidad": cantidad,
                "Precio": precio,
                "Unidad de Medida": unidad
            }

            self.inventory.append(new_product)
            with open('imagenes/inventario.json', 'w') as f:
                json.dump(self.inventory, f)

            messagebox.showinfo("Éxito", f"Se agregó el producto {nombre} con precio de {precio}, cantidad {cantidad} y unidad de medida {unidad}.")
            add_product_window.destroy()
            self.load_inventory_table()

        CTkButton(master=add_product_window, text="Guardar", command=save_product, fg_color="#2A8C55", hover_color="#66d681").pack(pady=20)

    def update_product(self):
        update_product_window = tk.Toplevel(self.parent)
        update_product_window.title("Actualizar Producto")
        update_product_window.geometry("400x600")

        CTkLabel(master=update_product_window, text="Seleccionar Folio").pack(pady=10)
        folio_var = tk.StringVar()
        folio_dropdown = CTkComboBox(master=update_product_window, values=[str(item["Folio"]) for item in self.inventory], variable=folio_var)
        folio_dropdown.pack()

        def load_product_info(*args):
            folio = int(folio_var.get())
            product = next(item for item in self.inventory if item["Folio"] == folio)
            nombre_entry.delete(0, tk.END)
            nombre_entry.insert(0, product["Producto"])
            cantidad_entry.delete(0, tk.END)
            cantidad_entry.insert(0, product["Cantidad"])
            precio_entry.delete(0, tk.END)
            precio_entry.insert(0, product["Precio"])
            unidad_entry.delete(0, tk.END)
            unidad_entry.insert(0, product["Unidad de Medida"])

        folio_var.trace("w", load_product_info)

        CTkLabel(master=update_product_window, text="Nombre del Producto").pack(pady=10)
        nombre_entry = CTkEntry(master=update_product_window)
        nombre_entry.pack()

        CTkLabel(master=update_product_window, text="Cantidad").pack(pady=10)
        cantidad_entry = CTkEntry(master=update_product_window)
        cantidad_entry.pack()

        CTkLabel(master=update_product_window, text="Precio").pack(pady=10)
        precio_entry = CTkEntry(master=update_product_window)
        precio_entry.pack()

        CTkLabel(master=update_product_window, text="Unidad de Medida").pack(pady=10)
        unidad_entry = CTkEntry(master=update_product_window)
        unidad_entry.pack()

        def save_updated_product():
            folio = int(folio_var.get())
            nombre = nombre_entry.get()
            cantidad_str = cantidad_entry.get()
            precio_str = precio_entry.get()
            unidad = unidad_entry.get()

            if not nombre or not cantidad_str or not precio_str or not unidad:
                messagebox.showerror("Error", "Todos los campos son obligatorios. No puedes actualizar.")
                return

            try:
                cantidad = int(cantidad_str)
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser un número positivo mayor que cero.")
                    return
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número.")
                return

            try:
                precio = float(precio_str)
                if precio <= 0:
                    messagebox.showerror("Error", "El precio debe ser un número positivo mayor que cero.")
                    return
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número.")
                return

            product = next(item for item in self.inventory if item["Folio"] == folio)
            product["Producto"] = nombre
            product["Cantidad"] = cantidad
            product["Precio"] = precio
            product["Unidad de Medida"] = unidad

            with open('imagenes/inventario.json', 'w') as f:
                json.dump(self.inventory, f)

            messagebox.showinfo("Éxito", "Se ha actualizado el producto correctamente.")
            update_product_window.destroy()
            self.load_inventory_table()

        CTkButton(master=update_product_window, text="Actualizar", command=save_updated_product, fg_color="#2A8C55", hover_color="#66d681").pack(pady=20)

    def delete_product(self):
        delete_product_window = tk.Toplevel(self.parent)
        delete_product_window.title("Eliminar Producto")
        delete_product_window.geometry("400x400")

        CTkLabel(master=delete_product_window, text="Seleccionar Folio").pack(pady=10)
        folio_var = tk.StringVar()
        folio_dropdown = CTkComboBox(master=delete_product_window, values=[str(item["Folio"]) for item in self.inventory], variable=folio_var)
        folio_dropdown.pack()

        product_info_label = CTkLabel(master=delete_product_window, text="")
        product_info_label.pack(pady=10)

        def load_product_info(*args):
            folio = int(folio_var.get())
            product = next(item for item in self.inventory if item["Folio"] == folio)
            product_info_label.configure(text=f"Producto: {product['Producto']}\nCantidad: {product['Cantidad']}\nPrecio: {product['Precio']}\nUnidad de Medida: {product['Unidad de Medida']}")

        folio_var.trace("w", load_product_info)

        def confirm_delete_product():
            folio = int(folio_var.get())
            self.inventory = [item for item in self.inventory if item["Folio"] != folio]

            # Reajustar los folios
            for idx, item in enumerate(self.inventory):
                item["Folio"] = idx + 1

            with open('imagenes/inventario.json', 'w') as f:
                json.dump(self.inventory, f)

            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            delete_product_window.destroy()
            self.load_inventory_table()

        CTkButton(master=delete_product_window, text="Eliminar", command=confirm_delete_product, fg_color="#2A8C55", hover_color="#66d681").pack(pady=20)

