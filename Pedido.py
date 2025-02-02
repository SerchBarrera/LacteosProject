import json
from customtkinter import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Pedidos:
    def __init__(self, parent):
        self.parent = parent
        self.orders = []
        self.inventario = []

    def show_orders_view(self):
        title_frame = CTkFrame(master=self.parent, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Pedidos", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")
        button_frame = CTkFrame(master=self.parent, fg_color="transparent")
        button_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        CTkButton(master=button_frame, text="+ Nuevo Pedido", font=("Arial Black", 15), text_color="#fff",
                  fg_color="#2A8C55", hover_color="#207244", command=self.add_order).pack(anchor="ne", side="right")
        CTkButton(master=button_frame, text="Actualizar Pedido", font=("Arial Black", 15), text_color="#fff",
                  fg_color="#2A8C55", hover_color="#207244", command=self.update_order).pack(anchor="ne", side="right", padx=(0, 10))

        self.inventory_frame = CTkFrame(master=self.parent, fg_color="transparent")
        self.inventory_frame.pack(anchor="n", fill="both", expand=True, padx=27, pady=(10, 0))

        self.orders_frame = CTkFrame(master=self.parent, fg_color="transparent")
        self.orders_frame.pack(anchor="n", fill="both", expand=True, padx=27, pady=(10, 0))

        self.load_inventory_table()
        self.load_orders_table()

    def load_inventory_table(self):
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

        try:
            with open('imagenes/inventario.json', 'r') as f:
                self.inventario = json.load(f)

            columns = ["Folio", "Producto", "Cantidad", "Precio", "Unidad de Medida"]
            rows = [list(item.values()) for item in self.inventario]

            table = CTkScrollableFrame(master=self.inventory_frame, fg_color="transparent")
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

    def load_orders_table(self):
        for widget in self.orders_frame.winfo_children():
            widget.destroy()

        try:
            with open('pedidos.json', 'r') as f:
                self.orders = json.load(f)

            columns = ["Folio", "Producto", "Cantidad Vendida", "Precio Unitario", "Precio Total", "FechaPedido", "FechaEntrega", "Estatus"]
            rows = [list(order.values()) for order in self.orders]

            table = CTkScrollableFrame(master=self.orders_frame, fg_color="transparent")
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
            messagebox.showerror("Error", f"No se pudo cargar la tabla de pedidos: {e}")

    def add_order(self):
        new_order_window = tk.Toplevel(self.parent)
        new_order_window.title("Añadir Nuevo Pedido")
        new_order_window.geometry("400x600")
        new_order_window.configure(bg='white')

        CTkLabel(master=new_order_window, text="Producto", bg_color="white").pack(pady=10)
        producto_var = tk.StringVar()
        producto_dropdown = CTkComboBox(master=new_order_window, values=[item["Producto"] for item in self.inventario], variable=producto_var)
        producto_dropdown.pack()

        CTkLabel(master=new_order_window, text="Cantidad Vendida", bg_color="white").pack(pady=10)
        cantidad_entry = CTkEntry(master=new_order_window)
        cantidad_entry.pack()

        fecha_hoy = datetime.today().strftime('%Y-%m-%d')

        CTkLabel(master=new_order_window, text="Fecha de Pedido (YYYY-MM-DD)", bg_color="white").pack(pady=10)
        fecha_pedido_var = tk.StringVar(value=fecha_hoy)
        fecha_pedido_entry = CTkEntry(master=new_order_window, textvariable=fecha_pedido_var, state="readonly")
        fecha_pedido_entry.pack()

        CTkLabel(master=new_order_window, text="Fecha de Entrega (YYYY-MM-DD)", bg_color="white").pack(pady=10)
        fecha_entrega_entry = CTkEntry(master=new_order_window)
        fecha_entrega_entry.pack()

        estatus_var = tk.StringVar(value="en proceso")
        CTkLabel(master=new_order_window, text="Estatus", bg_color="white").pack(pady=10)
        estatus_entry = CTkEntry(master=new_order_window, textvariable=estatus_var, state="readonly")
        estatus_entry.pack()

        def save_order():
            producto = producto_var.get()
            if not producto:
                messagebox.showerror("Error", "El campo Producto no puede estar vacío. No puedes guardar.")
                return
            if not cantidad_entry.get():
                messagebox.showerror("Error", "El campo Cantidad Vendida no puede estar vacío. No puedes guardar.")
                return
            if not fecha_entrega_entry.get():
                messagebox.showerror("Error", "El campo Fecha de Entrega no puede estar vacío. No puedes guardar.")
                return

            try:
                cantidad = int(cantidad_entry.get())
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad vendida debe ser un número positivo.")
                    return
            except ValueError:
                messagebox.showerror("Error", "La cantidad vendida debe ser un número.")
                return

            fecha_pedido = fecha_pedido_var.get()
            fecha_entrega = fecha_entrega_entry.get()
            estatus = estatus_var.get()

            try:
                fecha_pedido_dt = datetime.strptime(fecha_pedido, '%Y-%m-%d')
                fecha_entrega_dt = datetime.strptime(fecha_entrega, '%Y-%m-%d')
                if fecha_entrega_dt < fecha_pedido_dt:
                    messagebox.showerror("Error", "La fecha de entrega no puede ser menor que la fecha de pedido.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD.")
                return

            item = next((item for item in self.inventario if item["Producto"] == producto), None)
            if item is None:
                messagebox.showerror("Error", "El producto no existe en el inventario.")
                return

            if cantidad > item["Cantidad"]:
                messagebox.showerror("Error", "La cantidad vendida excede la cantidad disponible en inventario.")
                return

            precio_unitario = item["Precio"]
            precio_total = cantidad * precio_unitario

            if not self.orders:
                folio = 1
            else:
                folio = max(order["Folio"] for order in self.orders) + 1

            new_order = {
                "Folio": folio,
                "Producto": producto,
                "Cantidad Vendida": cantidad,
                "Precio Unitario": precio_unitario,
                "Precio Total": precio_total,
                "FechaPedido": fecha_pedido,
                "FechaEntrega": fecha_entrega,
                "Estatus": estatus
            }

            self.orders.append(new_order)
            item["Cantidad"] -= cantidad

            with open('pedidos.json', 'w') as f:
                json.dump(self.orders, f)

            with open('imagenes/inventario.json', 'w') as f:
                json.dump(self.inventario, f)

            messagebox.showinfo("Éxito", "Pedido añadido exitosamente.")
            new_order_window.destroy()
            self.load_orders_table()

        CTkButton(master=new_order_window, text="Guardar", command=save_order, fg_color="#2A8C55", hover_color="#66d681").pack(pady=20)

    def update_order(self):
        update_order_window = tk.Toplevel(self.parent)
        update_order_window.title("Actualizar Pedido")
        update_order_window.geometry("400x500")
        update_order_window.configure(bg='white')

        CTkLabel(master=update_order_window, text="Seleccionar Folio del Pedido", bg_color="white").pack(pady=10)
        folio_var = tk.StringVar()
        folio_dropdown = CTkComboBox(master=update_order_window, values=[str(order["Folio"]) for order in self.orders], variable=folio_var)
        folio_dropdown.pack()

        CTkLabel(master=update_order_window, text="Cantidad Vendida", bg_color="white").pack(pady=10)
        cantidad_entry = CTkEntry(master=update_order_window)
        cantidad_entry.pack()

        CTkLabel(master=update_order_window, text="Fecha de Entrega (YYYY-MM-DD)", bg_color="white").pack(pady=10)
        fecha_entrega_entry = CTkEntry(master=update_order_window)
        fecha_entrega_entry.pack()

        estatus_var = tk.StringVar(value="en proceso")
        CTkLabel(master=update_order_window, text="Estatus", bg_color="white").pack(pady=10)
        estatus_entry = CTkEntry(master=update_order_window, textvariable=estatus_var)
        estatus_entry.pack()

        def load_order_info(*args):
            folio = int(folio_var.get())
            order = next((order for order in self.orders if order["Folio"] == folio), None)
            if order:
                cantidad_entry.delete(0, tk.END)
                cantidad_entry.insert(0, order["Cantidad Vendida"])
                fecha_entrega_entry.delete(0, tk.END)
                fecha_entrega_entry.insert(0, order["FechaEntrega"])
                estatus_var.set(order["Estatus"])

        folio_var.trace("w", load_order_info)

        def save_updated_order():
            folio = int(folio_var.get())
            if not cantidad_entry.get():
                messagebox.showerror("Error", "El campo Cantidad Vendida no puede estar vacío. No puedes actualizar.")
                return
            if not fecha_entrega_entry.get():
                messagebox.showerror("Error", "El campo Fecha de Entrega no puede estar vacío. No puedes actualizar.")
                return

            try:
                cantidad = int(cantidad_entry.get())
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad vendida debe ser un número positivo.")
                    return
            except ValueError:
                messagebox.showerror("Error", "La cantidad vendida debe ser un número.")
                return

            fecha_entrega = fecha_entrega_entry.get()
            estatus = estatus_var.get()

            order = next((order for order in self.orders if order["Folio"] == folio), None)
            if order:
                item = next((item for item in self.inventario if item["Producto"] == order["Producto"]), None)
                if item is None:
                    messagebox.showerror("Error", "El producto no existe en el inventario.")
                    return

                if cantidad < 0 or cantidad > (item["Cantidad"] + order["Cantidad Vendida"]):
                    messagebox.showerror("Error", "La cantidad vendida no puede ser menor que 0 o exceder la cantidad disponible en inventario.")
                    return

                order["Cantidad Vendida"] = cantidad
                order["FechaEntrega"] = fecha_entrega
                order["Estatus"] = estatus

                precio_unitario = order["Precio Unitario"]
                order["Precio Total"] = cantidad * precio_unitario

                try:
                    fecha_pedido_dt = datetime.strptime(order["FechaPedido"], '%Y-%m-%d')
                    fecha_entrega_dt = datetime.strptime(fecha_entrega, '%Y-%m-%d')
                    if fecha_entrega_dt < fecha_pedido_dt:
                        messagebox.showerror("Error", "La fecha de entrega no puede ser menor que la fecha de pedido.")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD.")
                    return

                item["Cantidad"] += order["Cantidad Vendida"]
                item["Cantidad"] -= cantidad

                with open('pedidos.json', 'w') as f:
                    json.dump(self.orders, f)

                with open('imagenes/inventario.json', 'w') as f:
                    json.dump(self.inventario, f)

                messagebox.showinfo("Éxito", "Pedido actualizado exitosamente.")
                update_order_window.destroy()
                self.load_orders_table()

        CTkButton(master=update_order_window, text="Guardar", command=save_updated_order, fg_color="#2A8C55", hover_color="#66d681").pack(pady=20)

