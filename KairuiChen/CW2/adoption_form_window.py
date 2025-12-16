import tkinter as tk
from tkinter import ttk
import animal
import file_picker_window

class AdoptionFormWindow:
    def __init__(self, parent, to_adopt: list[animal.Animal], generate_adoption_form_event_handler):
        self.to_adopt = to_adopt
        self.window = tk.Toplevel(parent)
        self.window.wm_title('Adoption')
        self.parent = parent

        self.window.wait_visibility()
        self.window.grab_set()
        self.window.transient(parent)

        details_frame = ttk.Frame(self.window)
        details_frame.pack()
        # keep track of current row with variable to make reordering components in the code easier
        current_row = 0
        # display animal details
        self.animals_tree = ttk.Treeview(details_frame, columns=('Name', 'Species', 'Age'), show='headings',
                                         height=len(self.to_adopt))

        self.animals_tree.heading('Name', text='Name')
        self.animals_tree.heading('Species', text='Species')
        self.animals_tree.heading('Age', text='Age')

        self.animals_tree.column('Name', width=150)
        self.animals_tree.column('Species', width=100)
        self.animals_tree.column('Age', width=150)

        for a in self.to_adopt:
            self.animals_tree.insert('', 'end', values=(a.name, a.species, a.get_age()))

        self.animals_tree.grid(column=0, row=current_row, columnspan=2, sticky=tk.W+tk.E)
        current_row += 1

        # add ui elements to collect adopter details
        name_label = ttk.Label(details_frame, text='Adopter name:')
        self.name_var = tk.StringVar()
        name_box = ttk.Entry(details_frame, textvariable=self.name_var, width=50)
        name_label.grid(column=0, row=current_row)
        name_box.grid(column=1, row=current_row)
        current_row += 1

        address_label = ttk.Label(details_frame, text='Address:')
        self.address_box = tk.Text(details_frame, width=50, height=10)
        address_label.grid(column=0, row=current_row)
        self.address_box.grid(column=1, row=current_row)
        current_row += 1

        file_picker_frame = ttk.Frame(self.window)
        file_picker_frame.pack()
        current_row = 0
        output_label = ttk.Label(file_picker_frame, text="Save as:")
        self.display_path = tk.StringVar()
        self.real_path = 'adoption.png'
        self.display_path.set(self.real_path)

        selected_path = ttk.Label(file_picker_frame, textvariable=self.display_path, width=50, anchor='e')
        output_button = ttk.Button(file_picker_frame, text="Select", command=lambda: self.directory_button_clicked())
        output_label.grid(column=0, row=current_row)
        current_row += 1
        selected_path.grid(column=0, row=current_row)
        output_button.grid(column=1, row=current_row)
        current_row += 1

        generate_button = ttk.Button(self.window, text='Generate adoption form', command=lambda:
        generate_adoption_form_event_handler(self))
        generate_button.pack()

    def directory_button_clicked(self):
        result = file_picker_window.file_picker_from_file_path_dialog(self.parent, self.real_path)
        if result is not None:
            self.real_path = result
            self.display_path.set(f'...{result[-50:]}')
