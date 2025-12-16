import tkinter as tk
from tkinter import ttk

class AddAnimalWindow:
    def __init__(self, save_animal_event_handler):
        self.window = tk.Toplevel()
        self.window.wm_title('Add new animal')

        # keep track of current row with variable to make reordering components in the code easier
        current_row = 0

        name_label = ttk.Label(self.window, text='Name:')
        self.name_var = tk.StringVar()
        name_box = ttk.Entry(self.window, textvariable=self.name_var, width=20)
        name_label.grid(column=0, row=current_row)
        name_box.grid(column=1, row=current_row)
        current_row += 1

        species_label = ttk.Label(self.window, text='Species:')
        self.species_var = tk.StringVar()
        species_box = ttk.Entry(self.window, textvariable=self.species_var, width=20)
        species_label.grid(column=0, row=current_row)
        species_box.grid(column=1, row=current_row)
        current_row += 1

        dob_label = ttk.Label(self.window, text='Date of birth (dd/mm/yyyy):')
        self.dob_var = tk.StringVar()
        dob_box = ttk.Entry(self.window, textvariable=self.dob_var, width=10)
        dob_label.grid(column=0, row=current_row)
        dob_box.grid(column=1, row=current_row)
        current_row += 1

        self.dog_var = tk.IntVar()
        self.cat_var = tk.IntVar()
        self.child_var = tk.IntVar()

        dog_label = ttk.Label(self.window, text='Dog friendly:')
        dog_checkbox = tk.Checkbutton(self.window, text='Dog friendly', variable=self.dog_var, onvalue=1, offvalue=0)
        dog_label.grid(column=0, row=current_row)
        dog_checkbox.grid(column=1, row=current_row)
        current_row += 1

        cat_label = ttk.Label(self.window, text='Cat friendly:')
        cat_checkbox = tk.Checkbutton(self.window, text='Cat friendly', variable=self.cat_var, onvalue=1, offvalue=0)
        cat_label.grid(column=0, row=current_row)
        cat_checkbox.grid(column=1, row=current_row)
        current_row += 1

        child_label = ttk.Label(self.window, text='Child friendly:')
        child_checkbox = tk.Checkbutton(self.window, text='Child friendly', variable=self.child_var, onvalue=1, offvalue=0)
        child_label.grid(column=0, row=current_row)
        child_checkbox.grid(column=1, row=current_row)
        current_row += 1

        save_button = ttk.Button(self.window, text='Save', command=lambda:
        save_animal_event_handler(self))
        save_button.grid(column=0, row=current_row)

