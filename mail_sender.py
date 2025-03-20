

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Selecione a pasta contendo os PDFs")
    return folder_selected