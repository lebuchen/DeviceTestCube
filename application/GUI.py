import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
from datetime import datetime
import uuid
import xml.etree.ElementTree as ET
from export.Export import Export
from export.PythonSQL import PythonSQL


class DeviceTestCubeApp:
    def __init__(self, master):
        self.export_type = PythonSQL 
        self.selected_files = {}
        self.test_report = None
        self.test_table = []
        self.last_exported_report = None

        # XML-Datei laden
        tree = ET.parse('language.xml')
        root = tree.getroot()
        
        # Alle <language>-Tags finden
        self.languages = [lang.get('name') for lang in root.findall('language')]


        # Configure master window
        master.title("MurrDeviceTester")
        master.geometry("800x600")
        master.config(bg="#e0e0e0")

        self.init_ui(master)

    def init_ui(self, master):
        
        self.color = "lightgray"
        self.accentcolor = "#04B81D"
        
        # Menu bar
        self.init_menu(master)

        # Table frame for files
        self.init_table(master)

        # Button and protocol input frame
        self.init_buttons(master)

        # Console output
        self.console = ScrolledText(master, height=8, state='disabled', bg="#f0f0f0", fg="black", font=("Courier", 10))
        self.console.grid(row=1, column=0, columnspan=2, padx=20, sticky='nsew')

        # Footer
        self.init_footer(master)

        # Master window grid configuration
        master.grid_rowconfigure(0, weight=0)
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=0)

    def init_menu(self, master):
        # Initialize the dropdown menu

        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0, activebackground= self.color)
        self.menu_bar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Ordner öffnen", command=self.select_directory)
        file_menu.add_command(label="Exit", command=lambda: master.quit())


        # Language menu
        language_menu = tk.Menu(self.menu_bar, tearoff=0, activebackground= self.color)
        self.menu_bar.add_cascade(label="Sprache", menu=language_menu)
        main.config(menu=self.menu_bar)

        for lang in self.languages:
            language_name = lang 
            language_menu.add_command(label=language_name, command=lambda lang=language_name: print(f"{lang} ausgewählt"))

        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0, activebackground= self.color)
        self.menu_bar.add_cascade(label="Hilfe", menu=help_menu)
        help_menu.add_command(label="Über", command=lambda: messagebox.showinfo("Über", "MurrDeviceTester v1.0"))

    def init_table(self, master):
        # Initialize table 

        table_frame = tk.LabelFrame(master, text="Test Cases", bg="#e0e0e0", font=("Arial", 12, "bold"))
        table_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

        self.table = ttk.Treeview(table_frame, columns=('File',), show='headings', selectmode='extended', height=15)

        self.table.column('File', anchor='w', width=400)
        self.table.pack(fill='both', expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.map("Treeview", 
            background=[('selected', "lightgray")],
            foreground=[('selected', 'black')])

    def init_buttons(self, master):
        # Initialize buttons

        self.buttons_frame = tk.Frame(master, bg="#f0f0f0")
        self.buttons_frame.grid(row=0, column=1, padx=20, pady=10, sticky='ew')

        entry_frame = tk.LabelFrame(
            self.buttons_frame, text="Testbericht", bg="#f0f0f0", font=("Arial", 12, "bold"), padx=10, pady=10
        )
        entry_frame.grid(row=0, column=0, pady=10, padx=10, sticky='ew')

        tk.Label(entry_frame, text="ArtikelNr:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, sticky='w', pady=5)
        self.protocol_serial = tk.Entry(entry_frame, font=("Arial", 12), bg="#ffffff")
        self.protocol_serial.grid(row=0, column=1, pady=5, padx=5, sticky='ew')

        tk.Label(entry_frame, text="PersNr:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky='w', pady=5)
        self.protocol_personal_ID = tk.Entry(entry_frame, font=("Arial", 12), bg="#ffffff")
        self.protocol_personal_ID.grid(row=1, column=1, pady=5, padx=5, sticky='ew')

        run_file_btn = tk.Button(
            self.buttons_frame,
            text="Ausgewählte Testfälle ausführen",
            command=self.run_selected_files,
            relief="raised",
            bg= self.accentcolor,
            fg="white",
            font=("Arial", 12, "bold"),
        )
        run_file_btn.grid(row=1, column=0, pady=5, padx=10, sticky='ew')

        export_btn = tk.Button(
            self.buttons_frame,
            text="Exportieren",
            command=self.export_report,
            relief="raised",
            bg= self.accentcolor,
            fg="white",
            font=("Arial", 12, "bold"),
        )
        export_btn.grid(row=2, column=0, pady=5, padx=10, sticky='ew')


    def init_footer(self, master):
        # Initialize the footer frame

        footer = tk.Frame(master, bg="#e0e0e0", height=20)
        footer.grid(row=2, column=0, columnspan=2, pady=5, sticky='ew')

        tk.Label(footer, text="© 2024 - Murrelektronik. Alle Rechte vorbehalten.", bg="#e0e0e0").pack(side='left', padx=10)
        tk.Label(footer, text="Version: 1.0.0", bg="#e0e0e0").pack(side='right', padx=10)

    def select_directory(self):
        # Opens a dialog to select a directory and displays its Python files in the table.

        path = filedialog.askdirectory()
        if path:
            for row in self.table.get_children():
                self.table.delete(row)
            self.selected_files.clear()

            for file in os.listdir(path):
                if file.endswith('.py'):
                    full_path = os.path.join(path, file)
                    item_id = self.table.insert('', 'end', values=(file,))
                    self.selected_files[item_id] = full_path

    def run_selected_files(self):
        # Executes the selected Python files one by one and shows output in the console.
        
        if not self.protocol_serial or not self.protocol_personal_ID:
            messagebox.showwarning("Kein Testberichtname", "Bitte geben Sie einen Testberichtnamen ein.")
            return

        selected_items = self.table.selection()
        if not selected_items:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie mindestens eine Python-Datei aus.")
            return
        
        self.serial = self.protocol_serial.get().strip()
        self.personal_ID = self.protocol_personal_ID.get().strip()
        self.unique_id = str(uuid.uuid4())
        self.test_report = f"{self.serial}_{self.personal_ID}_{self.unique_id}"

        selected_files = [self.selected_files[item] for item in selected_items]
        root_dir = os.path.commonpath(selected_files).split("tests")[0]

        self.console.configure(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.insert(tk.END, f"Testbericht: {self.unique_id}\n")

        for file_path in selected_files:
            self._execute_test_file(file_path, root_dir)

        self.console.configure(state='disabled')
        

    def _execute_test_file(self, file_path, root_dir):
        # Executes a single Python test file and logs the result.

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
            test_duration, success, error_description = self._parse_test_output(output)

            error_message = "OK" if success else "FAIL"
            log_message = (
                f"  [{current_time}] Modul {module_name}: {error_message} (Dauer: {test_duration})" +
                (f"\n  Description: {error_description}" if error_description else "") + "\n"
            )

            self.console.insert(tk.END, log_message)
            self.add_test_module(module_name, current_time, test_duration, error_message, error_description)

        except Exception as e:
            self.console.insert(tk.END, f"Fehler beim Ausführen von {file_path}: {e}\n")

    def _parse_test_output(self, output):
        # Parses the test output to extract relevant details.

        test_duration = None
        success = "OK" in output and "FAILED" not in output
        error_description = None

        for line in output.splitlines():
            if line.startswith("Ran") and "test in" in line:
                test_duration = line.split("in")[-1].strip()
            if not success and "AssertionError:" in line:
                error_description = line.strip()

        return test_duration, success, error_description

    def add_test_module(self, module_name, current_time, test_duration, error_message, error_description):
        # Add a new test module to the test log

        self.test_table.append([
            self.unique_id,
            module_name,
            current_time,
            test_duration,
            error_message,
            error_description
        ])
        
    def export_report(self):
        # Add your report export logic here

        if self.test_report == None:
            messagebox.showwarning("Keine Daten" ,"Noch nichts zu exportieren!")
            return
        else:
            if self.test_report == self.last_exported_report:
                messagebox.showwarning("Wiederholung","Daten wurden schon exportiert!")
                return
            else:

                self.last_exported_report = self.test_report

                # Export the report to a file
                self.console.configure(state='normal')
                self.console.insert(tk.END, self.export_type.export_to_database(self.test_report, self.test_table) )
                self.test_table = []
                self.console.configure(state='disable')


if __name__ == '__main__':
    main = tk.Tk()
    main.minsize(800,600)
    main.iconbitmap("murr.ico")
    app = DeviceTestCubeApp(main)
    main.mainloop()