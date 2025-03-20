import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter.ttk import Progressbar
import logging
from employee import employee_names, identify_employee_name
from pdf_processor import process_pdf


# Setup logger
def setup_logger():
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )


# Utility functions
def sanitize_input(value, field_name):
    """Validates and sanitizes input."""
    if not value.strip():
        raise ValueError(f"{field_name} não pode estar vazio.")
    return value.strip()

'''def select_folder():
    select_directory = filedialog.askdirectory(initialdir=initial_directory)
    print("Select Directory:", select_directory)'''


def validate_year_month(year, month):
    """Validates the year and month inputs."""
    if not (year.isdigit() and len(year) == 4):
        raise ValueError("Ano inválido! Insira no formato yyyy.")
    if not (month.isdigit() and 1 <= int(month) <= 12):
        raise ValueError("Mês inválido! Insira no formato mm.")
    return year, month.zfill(2)  # Add leading zero to month if missing


# Event handlers
def load_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_label.config(text=os.path.basename(file_path))
        global pdf_file_path
        pdf_file_path = file_path


def start_processing():
    global year, month
    try:
        year = sanitize_input(year_entry.get(), "Ano")
        month = sanitize_input(month_entry.get(), "Mês")
        output_dir = sanitize_input(folder_entry.get(), "Pasta de destino")

        validate_year_month(year, month)

        if not pdf_file_path:
            raise ValueError("Nenhum arquivo PDF foi carregado.")

        def progress_callback(current, total):
            progress["maximum"] = total
            progress["value"] = current
            root.update_idletasks()

        def cancel_callback():
            return cancel_process

        process_pdf(
            pdf_file_path, 
            output_dir, 
            year, 
            month, 
            progress_callback, 
            cancel_callback,
            #select_folder
        )

        messagebox.showinfo("Sucesso", "Processo concluído com sucesso!")

    except ValueError as e:
        logging.error(str(e))
        messagebox.showerror("Erro", str(e))


def cancel_processing():
    global cancel_process
    cancel_process = True


# GUI Setup
root = tk.Tk()
root.title("Processador de Contracheques")
'''initial_directory = "Documentos"'''
root.geometry("500x600")
root.configure(bg='white')

# Logger
setup_logger()

# GUI Widgets

label = ttk.Label(text="CONTRACHEQUES")
label.pack()

load_button = ttk.Button(root, text="Carregar PDF", command=load_pdf)
load_button.pack(pady=10)

pdf_label = tk.Label(root, text="Nenhum PDF carregado")
pdf_label.pack(pady=5)

tk.Label(root, text="Pasta de destino:").pack()
folder_entry = tk.Entry(root, width=50)
folder_entry.pack(pady=5)

'''load_button_folder= ttk.Button(text= "Escolher pasta de Destino", command=select_folder)
load_button_folder.pack(pady=10)'''

tk.Label(root, text="Ano (yyyy):").pack()
year_entry = tk.Entry(root, width=10)
year_entry.pack(pady=5)

tk.Label(root, text="Mês (mm):").pack()
month_entry = tk.Entry(root, width=10)
month_entry.pack(pady=5)

process_button = ttk.Button(root, text="Iniciar", command=start_processing)
process_button.pack(pady=10)

cancel_button = ttk.Button(root, text="Cancelar", command=cancel_processing, state=tk.DISABLED)
cancel_button.pack(pady=5)

progress = Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
progress.pack(pady=10)

# Control variables
pdf_file_path = None
cancel_process = False

# Main loop
root.mainloop()
