import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
from PIL import Image, ImageTk

class App:
    def __init__(self, master):
        self.nodes = {}
        self.selected_files = set()  # Stores paths of selected Python files

        # Load checkbox icons for files only
        self.checked_icon = ImageTk.PhotoImage(Image.new("RGB", (16, 16), "black"))  # Placeholder for checked icon
        self.unchecked_icon = ImageTk.PhotoImage(Image.new("RGB", (16, 16), "white"))  # Placeholder for unchecked icon

        # Frame for the Treeview and Scrollbars on the left
        self.tree_frame = tk.Frame(master)
        self.tree_frame.grid(row=0, column=0, padx=20, pady=10, sticky='nsew')
        
        # Treeview for folder structure
        self.tree = ttk.Treeview(self.tree_frame, selectmode='none')
        ysb = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Project tree', anchor='w')
        
        # Place the Treeview and Scrollbars
        self.tree.grid(row=1, column=0, sticky='nsew')  # Row 1 to leave space for button at row 0
        ysb.grid(row=1, column=1, sticky='ns')
        xsb.grid(row=2, column=0, sticky='ew')
        
        # Frame expansion in window
        self.tree_frame.grid_rowconfigure(1, weight=1)  # Allow tree to expand vertically
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # Button to select a directory, placed at the top of the Treeview
        self.select_dir_btn = tk.Button(self.tree_frame, text="Ordner auswählen", command=self.select_directory)
        self.select_dir_btn.grid(row=0, column=0, pady=5, sticky='ew')  # Positioned above the treeview

        # Button to run selected Python files, now placed in the main window to the right of the tree_frame
        run_file_btn = tk.Button(master, text="Ausgewählte Dateien ausführen", command=self.run_selected_files)
        run_file_btn.grid(row=0, column=1, padx=10, pady=5, sticky='n')

        # Console output (ScrolledText widget) with fixed height, positioned below both the tree and run button, spanning full width
        self.console = ScrolledText(master, height=8, state='disabled')
        self.console.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='ew')  # Fixed height, spans both columns

        # Configure master grid to allow tree_frame to expand vertically
        master.grid_rowconfigure(0, weight=1)  # Allow only row 0 (with tree_frame) to expand vertically
        master.grid_columnconfigure(0, weight=1)  # Allow left column (tree_frame) to expand horizontally
        master.grid_columnconfigure(1, weight=0)  # Right column has fixed width for the button

        # Bind tree events
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind("<Button-1>", self.on_click)



    def select_directory(self):
        """Opens a dialog to select a directory and displays its structure."""
        path = filedialog.askdirectory()
        if path:
            # Clear existing tree nodes and selected files
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.selected_files.clear()

            # Insert the selected directory
            abspath = os.path.abspath(path)
            self.insert_node('', abspath, abspath)

    def insert_node(self, parent, text, abspath):
        """Inserts a node into the Treeview with a checkbox icon for files only."""
        # Only assign an icon if the item is a file
        if os.path.isfile(abspath):
            icon = self.checked_icon if abspath in self.selected_files else self.unchecked_icon
            node = self.tree.insert(parent, 'end', text=text, image=icon, open=False)
            self.nodes[node] = abspath  # Track file paths for toggling
        else:
            # For folders, no icon is used
            node = self.tree.insert(parent, 'end', text=text, open=False)
            self.nodes[node] = abspath  # Track directory paths

        # If the node is a directory, add a dummy child for expand icon
        if os.path.isdir(abspath):
            self.tree.insert(node, 'end')

    def open_node(self, event):
        """Expands a directory in the Treeview."""
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            # Remove the dummy child and list directory contents
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

    def on_click(self, event):
        """Handle clicks on the Treeview to toggle selection state (checkbox) only for files."""
        # Identify the item at the click position
        item = self.tree.identify_row(event.y)
        
        # Check if the clicked item is valid and a file
        if item and item in self.nodes:
            abspath = self.nodes[item]
            if os.path.isfile(abspath):  # Only toggle checkbox if it's a file
                # Toggle selection state
                if abspath in self.selected_files:
                    self.selected_files.remove(abspath)
                    self.tree.item(item, image=self.unchecked_icon)
                else:
                    # Only add Python files to the selection
                    if abspath.endswith('.py'):
                        self.selected_files.add(abspath)
                        self.tree.item(item, image=self.checked_icon)
                    else:
                        messagebox.showwarning("Ungültige Auswahl", "Bitte wählen Sie nur Python-Dateien (.py) aus.")




    def run_selected_files(self):
        """Executes the selected Python files one by one and shows output in console."""
        if not self.selected_files:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie mindestens eine Python-Datei aus.")
            return

        # Run each selected Python file and display output in the console
        self.console.configure(state='normal')
        self.console.delete(1.0, tk.END)  # Clear previous console output

        for file_path in self.selected_files:
            self.console.insert(tk.END, f"Ausführen von {file_path}...\n")
            try:
                # Run the Python file and capture output
                result = subprocess.run(['python', file_path], capture_output=True, text=True)
                self.console.insert(tk.END, result.stdout)
                if result.stderr:
                    self.console.insert(tk.END, f"Fehler:\n{result.stderr}\n")
            except Exception as e:
                self.console.insert(tk.END, f"Fehler beim Ausführen der Datei {file_path}:\n{e}\n")
            self.console.insert(tk.END, "-" * 40 + "\n")

        self.console.configure(state='disabled')  # Disable editing console output
        self.console.yview(tk.END)  # Scroll to the end of the console

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Python-Datei-Browser und -Ausführer")
    root.geometry("800x600")
    app = App(root)
    root.mainloop()



# import os
# import tkinter as tk
# import tkinter.ttk as ttk
# from tkinter import filedialog, messagebox
# from tkinter.scrolledtext import ScrolledText
# import subprocess
# from PIL import Image, ImageTk

# class App:
#     def __init__(self, master):
#         self.nodes = {}
#         self.selected_files = set()  # Stores paths of selected Python files

#         # Load checkbox icons
#         self.checked_icon = ImageTk.PhotoImage(Image.new("RGB", (16, 16), "black"))  # Placeholder for checked icon
#         self.unchecked_icon = ImageTk.PhotoImage(Image.new("RGB", (16, 16), "gray"))  # Placeholder for unchecked icon

#         # Frame for the Treeview and Scrollbars
#         frame = tk.Frame(master)
        
#         # Treeview for folder structure
#         self.tree = ttk.Treeview(frame, selectmode='none')
#         ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
#         xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
#         self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
#         self.tree.heading('#0', text='Project tree', anchor='w')
        
#         # Place the Treeview and Scrollbars
#         self.tree.grid(row=0, column=0, sticky='nsew')
#         ysb.grid(row=0, column=1, sticky='ns')
#         xsb.grid(row=1, column=0, sticky='ew')
#         frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
#         # Frame expansion in window
#         frame.grid_rowconfigure(0, weight=1)
#         frame.grid_columnconfigure(0, weight=1)
        
#         # Button to select a directory
#         select_dir_btn = tk.Button(master, text="Ordner auswählen", command=self.select_directory)
#         select_dir_btn.grid(row=1, column=0, pady=5)

#         # Button to run selected Python files
#         run_file_btn = tk.Button(master, text="Ausgewählte Dateien ausführen", command=self.run_selected_files)
#         run_file_btn.grid(row=2, column=0, pady=5)

#         # Console output (ScrolledText widget)
#         self.console = ScrolledText(master, height=10, state='disabled')
#         self.console.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

#         # Expand console output
#         master.grid_rowconfigure(3, weight=1)
#         master.grid_columnconfigure(0, weight=1)

#         # Bind tree events
#         self.tree.bind('<<TreeviewOpen>>', self.open_node)
#         self.tree.bind("<Button-1>", self.on_click)

#     def select_directory(self):
#         """Opens a dialog to select a directory and displays its structure."""
#         path = filedialog.askdirectory()
#         if path:
#             # Clear existing tree nodes and selected files
#             for item in self.tree.get_children():
#                 self.tree.delete(item)
#             self.selected_files.clear()

#             # Insert the selected directory
#             abspath = os.path.abspath(path)
#             self.insert_node('', abspath, abspath)

#     def insert_node(self, parent, text, abspath):
#         """Inserts a node into the Treeview with a checkbox icon."""
#         icon = self.checked_icon if abspath in self.selected_files else self.unchecked_icon
#         node = self.tree.insert(parent, 'end', text=text, image=icon, open=False)
#         if os.path.isdir(abspath):
#             self.nodes[node] = abspath
#             # Insert a dummy child to show expand icon if directory
#             self.tree.insert(node, 'end')
#         else:
#             # Add to the nodes dictionary for files as well
#             self.nodes[node] = abspath
    
#     def open_node(self, event):
#         """Expands a directory in the Treeview."""
#         node = self.tree.focus()
#         abspath = self.nodes.pop(node, None)
#         if abspath:
#             # Remove the dummy child and list directory contents
#             self.tree.delete(self.tree.get_children(node))
#             for p in os.listdir(abspath):
#                 self.insert_node(node, p, os.path.join(abspath, p))

#     def on_click(self, event):
#         """Handle clicks on the Treeview to toggle selection state (checkbox)."""
#         item = self.tree.identify_row(event.y)
#         if item and item in self.nodes:
#             abspath = self.nodes[item]
#             # Toggle selection state
#             if abspath in self.selected_files:
#                 self.selected_files.remove(abspath)
#                 self.tree.item(item, image=self.unchecked_icon)
#             else:
#                 # Only add Python files to the selection
#                 if os.path.isfile(abspath) and abspath.endswith('.py'):
#                     self.selected_files.add(abspath)
#                     self.tree.item(item, image=self.checked_icon)
#                 else:
#                     messagebox.showwarning("Ungültige Auswahl", "Bitte wählen Sie nur Python-Dateien (.py) aus.")

#     def run_selected_files(self):
#         """Executes the selected Python files one by one and shows output in console."""
#         if not self.selected_files:
#             messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie mindestens eine Python-Datei aus.")
#             return

#         # Run each selected Python file and display output in the console
#         self.console.configure(state='normal')
#         self.console.delete(1.0, tk.END)  # Clear previous console output

#         for file_path in self.selected_files:
#             self.console.insert(tk.END, f"Ausführen von {file_path}...\n")
#             try:
#                 # Run the Python file and capture output
#                 result = subprocess.run(['python', file_path], capture_output=True, text=True)
#                 self.console.insert(tk.END, result.stdout)
#                 if result.stderr:
#                     self.console.insert(tk.END, f"Fehler:\n{result.stderr}\n")
#             except Exception as e:
#                 self.console.insert(tk.END, f"Fehler beim Ausführen der Datei {file_path}:\n{e}\n")
#             self.console.insert(tk.END, "-" * 40 + "\n")

#         self.console.configure(state='disabled')  # Disable editing console output
#         self.console.yview(tk.END)  # Scroll to the end of the console

# if __name__ == '__main__':
#     root = tk.Tk()
#     root.title("Python-Datei-Browser und -Ausführer")
#     root.geometry("800x600")
#     app = App(root)
#     root.mainloop()


# # import os
# # import tkinter as tk
# # import tkinter.ttk as ttk
# # from tkinter import filedialog, messagebox
# # import subprocess
# # from tkinter.scrolledtext import ScrolledText

# # class App:
# #     def __init__(self, master):
# #         self.nodes = dict()
        
# #         # Frame for the Treeview and Scrollbars
# #         frame = tk.Frame(master)
        
# #         # Treeview for folder structure with support for multiple selection
# #         self.tree = ttk.Treeview(frame, selectmode='extended')
# #         ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
# #         xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
# #         self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
# #         self.tree.heading('#0', text='Project tree', anchor='w')
        
# #         # Place the Treeview and Scrollbars
# #         self.tree.grid(row=0, column=0, sticky='nsew')
# #         ysb.grid(row=0, column=1, sticky='ns')
# #         xsb.grid(row=1, column=0, sticky='ew')
# #         frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
# #         # Frame expansion in window
# #         frame.grid_rowconfigure(0, weight=1)
# #         frame.grid_columnconfigure(0, weight=1)
        
# #         # Button to select a directory
# #         select_dir_btn = tk.Button(master, text="Ordner auswählen", command=self.select_directory)
# #         select_dir_btn.grid(row=1, column=0, pady=5)

# #         # Button to run selected Python files
# #         run_file_btn = tk.Button(master, text="Ausgewählte Dateien ausführen", command=self.run_selected_files)
# #         run_file_btn.grid(row=2, column=0, pady=5)

# #         # Console output (ScrolledText widget)
# #         self.console = ScrolledText(master, height=10, state='disabled')
# #         self.console.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

# #         # Expand console output
# #         master.grid_rowconfigure(3, weight=1)
# #         master.grid_columnconfigure(0, weight=1)

# #         # Bind tree events
# #         self.tree.bind('<<TreeviewOpen>>', self.open_node)

# #     def select_directory(self):
# #         """Opens a dialog to select a directory and displays its structure."""
# #         path = filedialog.askdirectory()
# #         if path:
# #             # Clear existing tree nodes
# #             for item in self.tree.get_children():
# #                 self.tree.delete(item)
            
# #             # Insert the selected directory
# #             abspath = os.path.abspath(path)
# #             self.insert_node('', abspath, abspath)

# #     def insert_node(self, parent, text, abspath):
# #         """Inserts a node into the Treeview."""
# #         node = self.tree.insert(parent, 'end', text=text, open=False)
# #         if os.path.isdir(abspath):
# #             self.nodes[node] = abspath
# #             # Insert a dummy child to show expand icon if directory
# #             self.tree.insert(node, 'end')
    
# #     def open_node(self, event):
# #         """Expands a directory in the Treeview."""
# #         node = self.tree.focus()
# #         abspath = self.nodes.pop(node, None)
# #         if abspath:
# #             # Remove the dummy child and list directory contents
# #             self.tree.delete(self.tree.get_children(node))
# #             for p in os.listdir(abspath):
# #                 self.insert_node(node, p, os.path.join(abspath, p))

# #     def run_selected_files(self):
# #         """Executes the selected Python files one by one and shows output in console."""
# #         selected_items = self.tree.selection()
# #         if not selected_items:
# #             messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie mindestens eine Python-Datei aus.")
# #             return

# #         # Collect file paths of selected Python files
# #         python_files = []
# #         for item in selected_items:
# #             file_path = self.tree.item(item, 'text')
# #             parent = item
# #             while self.tree.parent(parent):
# #                 parent = self.tree.parent(parent)
# #                 file_path = os.path.join(self.tree.item(parent, 'text'), file_path)
            
# #             # Check if the selected item is a Python file
# #             if os.path.isfile(file_path) and file_path.endswith('.py'):
# #                 python_files.append(file_path)

# #         if not python_files:
# #             messagebox.showwarning("Ungültige Auswahl", "Bitte wählen Sie gültige Python-Dateien (.py) aus.")
# #             return

# #         # Run each selected Python file and display output in the console
# #         self.console.configure(state='normal')
# #         self.console.delete(1.0, tk.END)  # Clear previous console output

# #         for file_path in python_files:
# #             self.console.insert(tk.END, f"Ausführen von {file_path}...\n")
# #             try:
# #                 # Run the Python file and capture output
# #                 result = subprocess.run(['python', file_path], capture_output=True, text=True)
# #                 self.console.insert(tk.END, result.stdout)
# #                 if result.stderr:
# #                     self.console.insert(tk.END, f"Fehler:\n{result.stderr}\n")
# #             except Exception as e:
# #                 self.console.insert(tk.END, f"Fehler beim Ausführen der Datei {file_path}:\n{e}\n")
# #             self.console.insert(tk.END, "-" * 40 + "\n")

# #         self.console.configure(state='disabled')  # Disable editing console output
# #         self.console.yview(tk.END)  # Scroll to the end of the console

# # if __name__ == '__main__':
# #     root = tk.Tk()
# #     root.title("Python-Datei-Browser und -Ausführer")
# #     root.geometry("800x600")
# #     app = App(root)
# #     root.mainloop()


# # # import os
# # # import tkinter as tk
# # # import tkinter.ttk as ttk
# # # from tkinter import filedialog, messagebox
# # # import subprocess

# # # class App:
# # #     def __init__(self, master):
# # #         self.nodes = dict()
        
# # #         # Frame for the Treeview and Scrollbars
# # #         frame = tk.Frame(master)
        
# # #         # Treeview for folder structure
# # #         self.tree = ttk.Treeview(frame)
# # #         ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
# # #         xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
# # #         self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
# # #         self.tree.heading('#0', text='Project tree', anchor='w')
        
# # #         # Place the Treeview and Scrollbars
# # #         self.tree.grid(row=0, column=0, sticky='nsew')
# # #         ysb.grid(row=0, column=1, sticky='ns')
# # #         xsb.grid(row=1, column=0, sticky='ew')
# # #         frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
# # #         # Frame expansion in window
# # #         frame.grid_rowconfigure(0, weight=1)
# # #         frame.grid_columnconfigure(0, weight=1)
        
# # #         # Button to select a directory
# # #         select_dir_btn = tk.Button(master, text="Ordner auswählen", command=self.select_directory)
# # #         select_dir_btn.grid(row=1, column=0, pady=10)

# # #         # Button to run selected Python file
# # #         run_file_btn = tk.Button(master, text="Ausgewählte Datei ausführen", command=self.run_selected_file)
# # #         run_file_btn.grid(row=2, column=0, pady=10)

# # #         # Bind tree events
# # #         self.tree.bind('<<TreeviewOpen>>', self.open_node)

# # #     def select_directory(self):
# # #         """Opens a dialog to select a directory and displays its structure."""
# # #         path = filedialog.askdirectory()
# # #         if path:
# # #             # Clear existing tree nodes
# # #             for item in self.tree.get_children():
# # #                 self.tree.delete(item)
            
# # #             # Insert the selected directory
# # #             abspath = os.path.abspath(path)
# # #             self.insert_node('', abspath, abspath)

# # #     def insert_node(self, parent, text, abspath):
# # #         """Inserts a node into the Treeview."""
# # #         node = self.tree.insert(parent, 'end', text=text, open=False)
# # #         if os.path.isdir(abspath):
# # #             self.nodes[node] = abspath
# # #             # Insert a dummy child to show expand icon if directory
# # #             self.tree.insert(node, 'end')
    
# # #     def open_node(self, event):
# # #         """Expands a directory in the Treeview."""
# # #         node = self.tree.focus()
# # #         abspath = self.nodes.pop(node, None)
# # #         if abspath:
# # #             # Remove the dummy child and list directory contents
# # #             self.tree.delete(self.tree.get_children(node))
# # #             for p in os.listdir(abspath):
# # #                 self.insert_node(node, p, os.path.join(abspath, p))

# # #     def run_selected_file(self):
# # #         """Executes the selected Python file."""
# # #         selected_item = self.tree.focus()
# # #         if not selected_item:
# # #             messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie eine Python-Datei aus.")
# # #             return

# # #         # Get the absolute path of the selected item
# # #         file_path = self.tree.item(selected_item, 'text')
# # #         parent = selected_item
# # #         while self.tree.parent(parent):
# # #             parent = self.tree.parent(parent)
# # #             file_path = os.path.join(self.tree.item(parent, 'text'), file_path)
        
# # #         # Check if the selected item is a Python file
# # #         if os.path.isfile(file_path) and file_path.endswith('.py'):
# # #             try:
# # #                 # Run the Python file in a subprocess
# # #                 subprocess.run(['python', file_path], check=True)
# # #             except subprocess.CalledProcessError as e:
# # #                 messagebox.showerror("Fehler", f"Fehler beim Ausführen der Datei:\n{e}")
# # #         else:
# # #             messagebox.showwarning("Ungültige Auswahl", "Bitte wählen Sie eine gültige Python-Datei (.py) aus.")

# # # if __name__ == '__main__':
# # #     root = tk.Tk()
# # #     root.title("Python-Datei-Browser und -Ausführer")
# # #     root.geometry("600x400")
# # #     app = App(root)
# # #     root.mainloop()






# # # # import os
# # # # import tkinter as tk
# # # # import tkinter.ttk as ttk


# # # # class App(object):
# # # #     def __init__(self, master, path):
# # # #         self.nodes = dict()
# # # #         frame = tk.Frame(master)
# # # #         self.tree = ttk.Treeview(frame)
# # # #         ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
# # # #         xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
# # # #         self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
# # # #         self.tree.heading('#0', text='Project tree', anchor='w')

# # # #         self.tree.grid()
# # # #         ysb.grid(row=0, column=1, sticky='ns')
# # # #         xsb.grid(row=1, column=0, sticky='ew')
# # # #         frame.grid()

# # # #         abspath = os.path.abspath(path)
# # # #         self.insert_node('', abspath, abspath)
# # # #         self.tree.bind('<<TreeviewOpen>>', self.open_node)

# # # #     def insert_node(self, parent, text, abspath):
# # # #         node = self.tree.insert(parent, 'end', text=text, open=False)
# # # #         if os.path.isdir(abspath):
# # # #             self.nodes[node] = abspath
# # # #             self.tree.insert(node, 'end')

# # # #     def open_node(self, event):
# # # #         node = self.tree.focus()
# # # #         abspath = self.nodes.pop(node, None)
# # # #         if abspath:
# # # #             self.tree.delete(self.tree.get_children(node))
# # # #             for p in os.listdir(abspath):
# # # #                 self.insert_node(node, p, os.path.join(abspath, p))


# # # # if __name__ == '__main__':
# # # #     root = tk.Tk()
# # # #     app = App(root, path='.')
# # # #     root.mainloop()




# # # # # import tkinter as tk
# # # # # from tkinter import filedialog, scrolledtext, messagebox
# # # # # import subprocess

# # # # # class PythonFileExecutor:
# # # # #     def __init__(self, root):
# # # # #         self.root = root
# # # # #         self.root.title("Python File Executor")
        
# # # # #         # Create the GUI elements
# # # # #         self.label = tk.Label(root, text="Choose a Python file to execute:")
# # # # #         self.label.pack(pady=10)

# # # # #         self.file_button = tk.Button(root, text="Browse", command=self.browse_file)
# # # # #         self.file_button.pack(pady=5)

# # # # #         self.run_button = tk.Button(root, text="Run", command=self.run_file, state="disabled")
# # # # #         self.run_button.pack(pady=5)

# # # # #         self.output_text = scrolledtext.ScrolledText(root, height=20, width=60)
# # # # #         self.output_text.pack(pady=10)

# # # # #         self.filepath = None

# # # # #     def browse_file(self):
# # # # #         # Open file dialog to choose Python files
# # # # #         self.filepath = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
# # # # #         if self.filepath:
# # # # #             self.run_button.config(state="normal")
# # # # #             self.output_text.insert(tk.END, f"Selected file: {self.filepath}\n")

# # # # #     def run_file(self):
# # # # #         if self.filepath:
# # # # #             try:
# # # # #                 # Run the selected Python file and capture the output
# # # # #                 result = subprocess.run(['python', self.filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
# # # # #                 # Clear the output text area and insert new output
# # # # #                 self.output_text.delete(1.0, tk.END)
# # # # #                 self.output_text.insert(tk.END, f"Output from {self.filepath}:\n\n")
# # # # #                 self.output_text.insert(tk.END, result.stdout)
# # # # #                 self.output_text.insert(tk.END, result.stderr)

# # # # #             except Exception as e:
# # # # #                 messagebox.showerror("Error", f"An error occurred while executing the file:\n{e}")

# # # # # # Create the main window
# # # # # root = tk.Tk()
# # # # # app = PythonFileExecutor(root)

# # # # # # Start the GUI event loop
# # # # # root.mainloop()