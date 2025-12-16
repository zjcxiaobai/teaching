import tkinter as tk
from tkinter import ttk
import datetime

import animal
import data
import add_animal_window
import adoption_form_window
import generate_imgs
import file_picker_window

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Animal Rescue')
        self.root.minsize(650, 200)
        self.root.geometry('300x300+50+50')

        # load animal data early because various components reference it
        self.animal_file = 'animals.csv'
        self.animal_data = data.load_animals(self.animal_file)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # create treeview so menus can reference it
        self.animals_tree = ttk.Treeview(self.root, columns=('Name', 'Species', 'Age', 'Adopted'), show='headings')

        file_menu = tk.Menu(self.menubar, tearoff=False)
        file_menu.add_command(label='Save', command=self.save_menu_clicked)
        file_menu.add_command(label='Save as', command=self.save_as_menu_clicked)
        file_menu.add_command(label='Load', command=self.load_menu_clicked)
        file_menu.add_command(label='Exit', command=self.root.destroy)

        edit_menu = tk.Menu(self.menubar, tearoff=False)
        edit_menu.add_command(label='Add animal', command=self.add_animal_clicked)
        edit_menu.add_command(label='Delete selected', command=self.delete_animal_clicked)

        adoption_menu = tk.Menu(self.menubar, tearoff=False)
        adoption_menu.add_command(label='Adopt selected', command=self.adopt_animal_clicked)
        adoption_menu.add_command(label='Adoption poster', command=self.adoption_poster_clicked)

        self.menubar.add_cascade(label='File', menu=file_menu, underline=0)
        self.menubar.add_cascade(label='Edit', menu=edit_menu, underline=0)
        self.menubar.add_cascade(label='Adoption', menu=adoption_menu, underline=0)

        # display animals in treeview
        self.animals_tree.heading('Name', text='Name')
        self.animals_tree.heading('Species', text='Species')
        self.animals_tree.heading('Age', text='Age')
        self.animals_tree.heading('Adopted', text='Adopted')

        self.animals_tree.column('Name', width=150)
        self.animals_tree.column('Species', width=60)
        self.animals_tree.column('Age', width=150)
        self.animals_tree.column('Adopted', width=60)

        filter_frame = ttk.Frame(self.root)

        dog_var = tk.IntVar()
        cat_var = tk.IntVar()
        child_var = tk.IntVar()

        search_label = ttk.Label(filter_frame, text="Search:")
        self.search_item = tk.StringVar()
        search_box = ttk.Entry(filter_frame, textvariable=self.search_item, width=20)
        search_box.bind('<Return>', self.search_animal)

        filter_label = ttk.Label(filter_frame, text='Species filter')
        filter_list_var = tk.StringVar()
        filter_list_var.set(animal.SPECIES)
        filter_listbox = tk.Listbox(filter_frame, listvariable=filter_list_var, selectmode='extended',
                                    height=len(animal.SPECIES))

        dog_checkbox = tk.Checkbutton(filter_frame, text='Dog friendly', variable=dog_var, onvalue=1, offvalue=0)
        cat_checkbox = tk.Checkbutton(filter_frame, text='Cat friendly', variable=cat_var, onvalue=1, offvalue=0)
        child_checkbox = tk.Checkbutton(filter_frame, text='Child friendly', variable=child_var, onvalue=1, offvalue=0)

        filter_button = ttk.Button(filter_frame, text='Filter', command=lambda:
        self.filter_button_clicked(filter_listbox, dog_var, cat_var, child_var))
        reset_button = ttk.Button(filter_frame, text='Reset filter', command=self.reset_displayed_animals)

        search_label.pack()
        search_box.pack()
        filter_label.pack()
        filter_listbox.pack()
        dog_checkbox.pack()
        cat_checkbox.pack()
        child_checkbox.pack()
        filter_button.pack()
        reset_button.pack()

        self.animals_tree.grid(column=0, row=0)
        filter_frame.grid(column=1, row=1)

        self.load_data()
        self.reset_displayed_animals()

    def run(self):
        self.root.mainloop()

    def search_animal(self, event):
        self.animal_data.search_animal_name(self.search_item.get())
        self.refresh_animals_tree()

    def reset_displayed_animals(self):
        self.animal_data.reset_displayed_animals()
        self.refresh_animals_tree()

    def refresh_animals_tree(self):
        display_list = self.animal_data.get_displayed_animal_list()
        self.animals_tree.delete(*self.animals_tree.get_children())
        for a in display_list:
            self.animals_tree.insert('', 'end', values=(a.name, a.species, a.get_age(), a.get_adopted()))

    def save_menu_clicked(self):
        self.animal_data.save_animals(self.animal_file)

    def save_as_menu_clicked(self):
        result = file_picker_window.file_picker_from_file_path_dialog(self.root, self.animal_file)
        if result is not None:
            self.animal_file = result
            self.animal_data.save_animals(self.animal_file)

    def load_menu_clicked(self):
        result = file_picker_window.file_picker_from_file_path_dialog(self.root, self.animal_file)
        if result is not None:
            self.animal_file = result
            self.load_data()
            self.reset_displayed_animals()

    def load_data(self):
        self.animal_data = data.load_animals(self.animal_file)

    def add_animal_clicked(self):
        """
        Show popup window to collect info and add a new animal to the list of all animals.
        """
        add_animal_window.AddAnimalWindow(self.save_animal_clicked)

    def adoption_poster_clicked(self):
        generate_imgs.generate_adoption_poster('new_adoption_poster.png', self.animal_data.get_longest_resident(), 'resources/adoption_poster.png')

    def add_animal(self, new_animal: animal.Animal):
        self.animal_data.add_animal(new_animal)
        self.refresh_animals_tree()

    def save_animal_clicked(self, animal_window: add_animal_window.AddAnimalWindow):
        name = animal_window.name_var.get()
        species = animal_window.species_var.get()
        dob = animal_window.dob_var.get()
        cat_friendly = bool(animal_window.cat_var.get())
        dog_friendly = bool(animal_window.dog_var.get())
        child_friendly = bool(animal_window.child_var.get())

        parsed_dob = datetime.datetime.strptime(dob, '%d/%m/%Y')
        today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())

        new_animal = animal.Animal(name, species, parsed_dob, today, cat_friendly, dog_friendly,
                                   child_friendly, False)
        self.add_animal(new_animal)
        animal_window.window.destroy()

    def get_selected(self) -> list[animal.Animal]:
        """
        Get the animal objects that correspond to the animals selected in the animals_tree view.
        :return: References to selected animals
        """
        selected = [self.animals_tree.focus()]
        displayed = self.animal_data.get_animals_list()
        selected_animals = []
        for s in selected:
            display_index = self.animals_tree.index(s)
            selected_animals.append(displayed[display_index])

        return selected_animals

    def adopt_animal_clicked(self):
        selected = self.get_selected()
        # show adoption form popup
        adoption_form_window.AdoptionFormWindow(self.root, selected, self.generate_adoption_form_clicked)

    def generate_adoption_form_clicked(self, adoption_form: adoption_form_window.AdoptionFormWindow):
        adopted_animals = adoption_form.to_adopt
        adopter_name = adoption_form.name_var.get()
        adopter_address = adoption_form.address_box.get('1.0', 'end-1c')
        filepath = adoption_form.display_path.get()
        for a in adopted_animals:
            generate_imgs.generate_adoption_form(filepath, a, adopter_name, adopter_address,
                                                 'resources/adoption_form.png')
        adoption_form.window.destroy()

        window = tk.Toplevel()
        window.wm_title('Adoption form saved')
        confirmation_label = ttk.Label(window, text=f'Adoption form saved in {filepath}')
        confirmation_label.pack()

        for a in adopted_animals:
            self.animal_data.mark_adopted(a)
        self.refresh_animals_tree()

    def delete_animal_clicked(self):
        to_delete = self.get_selected()
        for a in to_delete:
            self.animal_data.delete_animal(a)
        self.refresh_animals_tree()

    def filter_button_clicked(self, filter_listbox, dog_var, cat_var, child_var):
        selected_indexes = filter_listbox.curselection()
        selected = []
        for i in selected_indexes:
            selected.append(filter_listbox.get(i))
        self.animal_data.apply_filter(selected, dog_var.get(), cat_var.get(), child_var.get())
        self.refresh_animals_tree()
        