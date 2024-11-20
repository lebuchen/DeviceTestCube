import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
from datetime import datetime


class DeviceTestCubeApp:
    def __init__(self, master):
        self.selected_files = {}  # Maps table item IDs to their full paths
        self.test_report = ""  # Variable to store protocol name

        # Configure master window
        master.title("DeviceTestCube")
        master.geometry("800x600")
        master.config(bg="#f0f0f0")  # Background color




        # Create menu bar
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        # Create "Datei" menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Datei", menu=self.file_menu)
        self.file_menu.add_command(label="Ordner öffnen", command=self.select_directory)

        # Placeholder for "Run" menu
        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Appearence", menu=self.run_menu)
        self.run_menu.add_command(label="Toggle DarkMode", command=lambda: print("Run Option 1 clicked"))  # Placeholder command

        # Placeholder for "Sprache" menu
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Sprache", menu=self.language_menu)
        self.language_menu.add_command(label="Deutsch", command=lambda: print("Sprache auf Deutsch gesetzt"))  # Placeholder
        self.language_menu.add_command(label="Englisch", command=lambda: print("Sprache auf Englisch gesetzt"))  # Placeholder

        # Placeholder for "Help" menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Über", command=lambda: print("Über Hilfe angeklickt"))  # Placeholder






        # Frame for the Table
        self.table_frame = tk.LabelFrame(
            master, text="Test Cases", bg="#f0f0f0", font=("Arial", 12, "bold"), padx=10, pady=10
        )
        self.table_frame.grid(row=0, column=0, padx=20, pady=10, sticky='nsew')

        # Table for displaying .py files
        self.table = ttk.Treeview(
            self.table_frame, columns=('File',), show='headings', selectmode='extended', height=15
        )
        self.table.column('File', anchor='w', width=400)
        self.table.pack(fill='both', expand=True, padx=5, pady=5)




        # Scrollbars for the table
        ysb = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.table.yview)
        xsb = ttk.Scrollbar(self.table_frame, orient='horizontal', command=self.table.xview)
        self.table.configure(yscroll=ysb.set, xscroll=xsb.set)

        # Place the Table and Scrollbars
        self.table.grid(row=1, column=0, sticky='nsew')
        ysb.grid(row=1, column=1, sticky='ns')
        xsb.grid(row=2, column=0, sticky='ew')

        # Frame expansion in window
        self.table_frame.grid_rowconfigure(1, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        # Buttons Frame
        self.buttons_frame = tk.Frame(master, bg="#f0f0f0")
        self.buttons_frame.grid(row=0, column=1, padx=20, pady=10, sticky='ew')



        # Protocol Name LabelFrame and Entry
        protocol_frame = tk.LabelFrame(
            self.buttons_frame, text="Protokollname", bg="#f0f0f0", font=("Arial", 12, "bold"), padx=10, pady=10
        )
        protocol_frame.grid(row=0, column=0, pady=10, padx=10, sticky='ew')

        self.protocol_entry = tk.Entry(protocol_frame, font=("Arial", 12,), bg="#ffffff")
        self.protocol_entry.pack(fill='x', padx=5, pady=5)
        
        # Deactivate caret blinking by removing focus until clicked
        self.protocol_entry.bind("<FocusIn>", lambda e: self.protocol_entry.config(insertbackground="white"))



        # Button to run selected Python files
        run_file_btn = tk.Button(
            self.buttons_frame,
            text="Ausgewählte Dateien ausführen",
            command=self.run_selected_files,
            relief="raised",
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        run_file_btn.grid(row=2, column=0, pady=5, padx=10, sticky='ew')

        # Console output (ScrolledText widget)
        self.console = ScrolledText(master, height=8, state='disabled', bg="#333", fg="white", font=("Courier", 10))
        self.console.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky='nsew')

        # Configure master grid
        master.grid_rowconfigure(0, weight=0)
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=0)

    def select_directory(self):
        """Opens a dialog to select a directory and displays its Python files in the table."""
        path = filedialog.askdirectory()
        if path:
            # Clear existing table data and selected files
            for row in self.table.get_children():
                self.table.delete(row)
            self.selected_files.clear()

            # List .py files in the selected directory
            abspath = os.path.abspath(path)
            for file in os.listdir(abspath):
                if file.endswith('.py'):
                    full_path = os.path.join(abspath, file)
                    item_id = self.table.insert('', 'end', values=(file,))
                    self.selected_files[item_id] = full_path

    def run_selected_files(self):
        """Executes the selected Python files one by one and shows output in the console."""
        self.test_report = self.protocol_entry.get().strip()
        if not self.test_report:
            messagebox.showwarning("Kein Protokollname", "Bitte geben Sie einen Protokollnamen ein.")
            return

        selected_items = self.table.selection()
        if not selected_items:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie mindestens eine Python-Datei aus.")
            return

        selected_files = [self.selected_files[item] for item in selected_items]
        root_dir = os.path.commonpath(selected_files)
        root_dir = root_dir.split("tests")[0]
        
        self.console.configure(state='normal')
        self.console.delete(1.0, tk.END)

        self.console.insert(tk.END, f"Testbericht: {self.test_report}\n")

        for file_path in selected_files:
            try:
                module_name = os.path.splitext(os.path.basename(file_path))[0]
                result = subprocess.run(
                    ['python', '-m', f'tests.{module_name}'],
                    cwd=root_dir,
                    capture_output=True,
                    text=True
                )
                output = result.stderr
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                test_duration = None
                success = "OK" in output and "FAILED" not in output
                error_description = None

                for line in output.splitlines():
                    if line.startswith("Ran") and "test in" in line:
                        test_duration = line.split("in")[-1].strip()

                if not success:
                    error_message = "FAIL"
                    error_description = "Error: Unknown"
                    for line in output.splitlines():
                        if "AssertionError:" in line:
                            error_description = line.strip()

                if success:
                    error_message = "OK"

                self.console.insert(
                    tk.END,
                    f"  [{current_time}] Modul {module_name}: {error_message} (Dauer: {test_duration})" +
                    (f"\n  Description: {error_description}" if error_description else "") + "\n"
                )


            except Exception as e:
                self.console.insert(tk.END, f"Fehler beim Ausführen von {file_path}: {e}\n")
                #maybe muss hier noch ein script reihn mit dem das Programm abgebrochen wird


        self.console.insert(tk.END, f"\n  Möchten Sie den Bericht exportieren? [y/N]\n")
        #abfrage welche ob y oder N geschrieben wurde und mit Enter bestätigt wurde
        
        #hier bitte eine Platzhalter funktion auf rufen falls mit y geantwortet wird 


        self.console.configure(state='disable')
        self.console.yview(tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    app = DeviceTestCubeApp(root)
    root.mainloop()
