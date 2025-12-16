import tkinter as tk
from tkinter import ttk
import os
import pathlib

def file_picker_dialog(parent: tk.Tk, default_filename: str, default_directory: str,
                       window_title: str = 'File picker') -> str | None:
    file_path = tk.StringVar()
    popup = FilePickerWindow(parent, file_path, default_filename, default_directory, window_title)
    parent.wait_window(popup.window)
    selected_path = file_path.get()
    if selected_path != '':
        return selected_path
    return None

def file_picker_from_file_path_dialog(parent: tk.Tk, default_filepath: str,
                                      window_title: str = 'File picker') -> str | None:
    full_path = os.path.realpath(default_filepath)
    dir_path = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    return file_picker_dialog(parent, filename, dir_path, window_title)

class FilePickerWindow:
    def __init__(self, parent: tk.Tk, selected_path_output: tk.StringVar, default_filename: str,
                 default_directory: str | None, window_title: str):
        self.window = tk.Toplevel(parent)
        self.window.wm_title(window_title)
        self.file_path = selected_path_output

        # make modal
        self.parent = parent
        self.window.wait_visibility()
        self.window.grab_set()
        self.window.transient(parent)

        if default_directory is None or not os.path.isdir(default_directory):
            self.directory_path = pathlib.Path(os.getcwd())
        else:
            self.directory_path = pathlib.Path(default_directory)

        self.directory_contents = ['']

        # label at top showing current directory
        self.path_frame = ttk.Frame(self.window)
        self.path_frame.pack()
        self.refresh_path_buttons()

        # tree view underneath showing files in directory
        self.file_tree = ttk.Treeview(self.window, columns='Filename', show='headings', selectmode='browse')
        self.file_tree.column('Filename', width=200)
        self.file_tree.bind('<Double-1>', self.file_tree_double_clicked)

        self.file_tree.pack()

        self.initialise_directory_location()

        # file name box at bottom
        file_frame = ttk.Frame(self.window)
        self.file_name = tk.StringVar()
        self.file_name.set(default_filename)
        output_box = ttk.Entry(file_frame, textvariable=self.file_name, width=20)
        output_button = ttk.Button(file_frame, text="Select", command=lambda: self.select_button_clicked())

        file_frame.pack()
        output_box.grid(column=0, row=0)
        output_button.grid(column=1, row=0)

    def file_tree_double_clicked(self, event):
        region = self.file_tree.identify('region', event.x, event.y)
        if not region == 'cell':
            return
        selection_index = self.file_tree.selection()[0]
        display_index = self.file_tree.index(selection_index)
        selected_dir = self.directory_contents[display_index]
        if os.path.isdir(selected_dir):
            self.directory_path = pathlib.Path(selected_dir)
        else:
            self.file_name.set(selected_dir)

    def refresh_path_buttons(self):
        for child in self.path_frame.winfo_children():
            child.destroy()
        i = 0
        locations = []
        current_location = self.directory_path
        while i < 5 and current_location.stem != '':
            i = i + 1
            locations.append(current_location)
            current_location = current_location.parent

        column_no = 0
        for i in range(len(locations)-1, 0, -1):
            location = locations[i]
            button = ttk.Button(self.path_frame, text=location.stem)
            button.bind('<Button-1>', lambda event: self.folder_button_clicked(locations[i]))
            button.grid(row=0, column=column_no)
            column_no += 1

    def folder_button_clicked(self, location: pathlib.Path):
        self.directory_path = location
        self.refresh_path_buttons()

    def initialise_directory_location(self):
        self.refresh_path_buttons()
        self.file_tree.heading('Filename', text=self.directory_path.stem)
        directory_contents = os.listdir(self.directory_path)

        files = []
        folders = []
        for f in directory_contents:
            full_path = self.directory_path.joinpath(f)
            if os.path.isdir(full_path):
                folders.append(f)
            elif os.path.isfile(full_path):
                files.append(f)

        self.directory_contents = folders + files
        self.file_tree.delete(*self.file_tree.get_children())
        for f in self.directory_contents:
            self.file_tree.insert('', 'end', values=([f]))


    def select_button_clicked(self):
        self.file_path.set(self.directory_path.joinpath(self.file_name.get()).as_posix())
        self.window.grab_release()
        self.window.destroy()