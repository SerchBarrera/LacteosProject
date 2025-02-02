from customtkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog
from fpdf import FPDF
import json
import pandas as pd

class Reportes:
    def __init__(self, parent):
        self.parent = parent
        self.data = []
        self.en_proceso = []
        self.entregado = []

    def show_reportes_view(self):
        title_frame = CTkFrame(master=self.parent, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Reportes", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")

        button_frame = CTkFrame(master=self.parent, fg_color="transparent")
        button_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        CTkButton(master=button_frame, text="Exportar a PDF", font=("Arial", 12), command=self.export_to_pdf,fg_color="#2A8C55",hover_color="#66d681").pack(
            side="left", padx=(0, 10))
        CTkButton(master=button_frame, text="Exportar a CSV", font=("Arial", 12), command=self.export_to_csv,fg_color="#2A8C55",hover_color="#66d681").pack(
            side="left", padx=(0, 10))
        CTkButton(master=button_frame, text="Exportar a JSON", font=("Arial", 12), command=self.export_to_json,fg_color="#2A8C55",hover_color="#66d681").pack(
            side="left", padx=(0, 10))

        self.en_proceso_frame = CTkFrame(master=self.parent, fg_color="transparent")
        self.en_proceso_frame.pack(anchor="n", fill="both", expand=True, padx=27, pady=(10, 0))

        self.entregado_frame = CTkFrame(master=self.parent, fg_color="transparent")
        self.entregado_frame.pack(anchor="n", fill="both", expand=True, padx=27, pady=(10, 0))

        self.load_tables()

    def load_tables(self):
        for widget in self.en_proceso_frame.winfo_children():
            widget.destroy()
        for widget in self.entregado_frame.winfo_children():
            widget.destroy()

        try:
            with open('pedidos.json', 'r') as f:
                self.data = json.load(f)

            self.en_proceso = [order for order in self.data if order["Estatus"] == "en proceso"]
            self.entregado = [order for order in self.data if order["Estatus"] == "completo"]

            self.create_table(self.en_proceso_frame, self.en_proceso, "Pedidos en Proceso")
            self.create_table(self.entregado_frame, self.entregado, "Pedidos Entregados")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla: {e}")

    def create_table(self, parent, data, title):
        CTkLabel(master=parent, text=title, font=("Arial Black", 20), text_color="#2A8C55").pack(anchor="nw", pady=(10, 0))

        columns = ["Folio", "Producto", "Cantidad Vendida", "Precio Unitario", "Precio Total", "Fecha Pedido", "Fecha Entrega", "Estatus"]
        rows = [list(order.values()) for order in data]

        table = CTkScrollableFrame(master=parent, fg_color="transparent")
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

    def export_to_pdf(self):
        pdf = FPDF('L', 'mm', 'A4')  # Landscape orientation
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        def add_table_to_pdf(title, data):
            pdf.set_fill_color(42, 140, 85)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", 'B', 12)  # Text in bold
            pdf.cell(0, 10, txt=title, ln=True, align="C", fill=True)
            pdf.ln(10)

            columns = ["Folio", "Producto", "Cantidad Vendida", "Precio Unitario", "Precio Total", "FechaPedido", "FechaEntrega", "Estatus"]
            cell_widths = [20, 40, 30, 30, 30, 40, 40, 30]  # Ajusta el tamaño de las celdas según sea necesario

            for i, column in enumerate(columns):
                pdf.set_fill_color(42, 140, 85)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(cell_widths[i], 10, column, 1, 0, 'C', fill=True)
            pdf.ln()

            pdf.set_font("Arial", size=12)  # Reset to regular text
            pdf.set_text_color(0, 0, 0)  # Text color to black
            for row in data:
                for i, column in enumerate(columns):
                    pdf.cell(cell_widths[i], 10, str(row[column]), 1)
                pdf.ln()

        add_table_to_pdf("Pedidos en Proceso", self.en_proceso)
        pdf.ln(10)
        add_table_to_pdf("Pedidos Entregados", self.entregado)

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Éxito", "Datos exportados a PDF exitosamente.")

    def export_to_csv(self):
        def save_to_csv(data, filename):
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)

        en_proceso_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Guardar CSV de Pedidos en Proceso")
        if en_proceso_path:
            save_to_csv(self.en_proceso, en_proceso_path)

        entregado_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Guardar CSV de Pedidos Entregados")
        if entregado_path:
            save_to_csv(self.entregado, entregado_path)

        messagebox.showinfo("Éxito", "Datos exportados a CSV exitosamente.")

    def export_to_json(self):
        def save_to_json(data, filename):
            with open(filename, 'w') as f:
                json.dump(data, f)

        en_proceso_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], title="Guardar JSON de Pedidos en Proceso")
        if en_proceso_path:
            save_to_json(self.en_proceso, en_proceso_path)

        entregado_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], title="Guardar JSON de Pedidos Entregados")
        if entregado_path:
            save_to_json(self.entregado, entregado_path)

        messagebox.showinfo("Éxito", "Datos exportados a JSON exitosamente.")
