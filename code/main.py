import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import uuid

ID_COLUMN = 'ID'
NAME_COLUMN = 'Name'
SURNAME_COLUMN = 'Surname'
AGE_COLUMN = 'Age'
GENDER_COLUMN = 'Gender'
BIRTHDATE_COLUMN = 'Birthdate'
PHONE_COLUMN = 'Phone Number'

class Person:
    people_dict = {}

    def __init__(self, id, name, surname, birthdate, gender, phone_number):
        self.id = id
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.gender = gender
        self.phone_number = phone_number
        self.calculate_age()

    def calculate_age(self):
        if self.birthdate and self.birthdate != '?':
            try:
                birthdate_date = datetime.strptime(self.birthdate, '%d/%m/%Y')
                today = datetime.today()
                age = today.year - birthdate_date.year - ((today.month, today.day) < (birthdate_date.month, birthdate_date.day))
                self.age = age
            except ValueError:
                self.age = '?'
        else:
            self.age = '?'

    @classmethod
    def add_person(cls, id, name, surname, birthdate, gender, phone_number):
        new_person = cls(id, name, surname, birthdate, gender, phone_number)
        cls.people_dict[id] = new_person
        return new_person

    @classmethod
    def remove_person(cls, person_id):
        if person_id in cls.people_dict:
            removed_person = cls.people_dict.pop(person_id)
            return f"Person with ID {person_id} removed."
        else:
            return f"Person with ID {person_id} not found in the list."

    @classmethod
    def update_person(cls, id, name, surname, birthdate, gender, phone_number):
        if id in cls.people_dict:
            person = cls.people_dict[id]
            person.name = name
            person.surname = surname
            person.birthdate = birthdate
            person.gender = gender
            person.phone_number = phone_number
            person.calculate_age()
            return "Person updated successfully."
        else:
            return f"Person with ID {id} not found in the list."

    @classmethod
    def get_people(cls):
        return list(cls.people_dict.values())

    @classmethod
    def save_data_to_file(cls, filename='app/data.json'):
        data = {
            "people": [
                {
                    "ID": person.id,
                    "Name": person.name,
                    "Surname": person.surname,
                    "Birthdate": person.birthdate,
                    "Gender": person.gender,
                    "Phone Number": person.phone_number
                } for person in cls.get_people()
            ]
        }

        try:
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=2)

            return f"Data were saved"
        except Exception as e:
            return f"Error saving data to '{filename}' file: {e}"

    @classmethod
    def load_from_file(cls, filename='app/data.json'):
        try:
            with open(filename, 'r') as json_file:
                data = json.load(json_file)

            if 'people' in data:
                cls.people_dict = {}

                for person_data in data['people']:
                    id = str(person_data['ID'])
                    name = str(person_data['Name'])
                    surname = str(person_data['Surname'])
                    birthdate = str(person_data['Birthdate'])
                    gender = str(person_data['Gender'])
                    phone_number = str(person_data['Phone Number'])

                    cls.people_dict[id] = cls(id, name, surname, birthdate, gender, phone_number)

                return f"Loaded {len(cls.people_dict)} people from '{filename}' file."
            else:
                return f"No 'people' key found in '{filename}' file. No person loaded."

        except FileNotFoundError:
            return f"File '{filename}' not found."
        except json.JSONDecodeError:
            return f"Error decoding JSON data in '{filename}'."
        except Exception as e:
            return f"Error loading data from '{filename}' file: {e}"

class GUI:
    def __init__(self, root, filename='app/data.json'):
        self.root = root
        self.root.title("People Management")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.filename = filename

        self.create_widgets()

        Person.load_from_file(self.filename)
        self.populate_treeview()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.tree = ttk.Treeview(self.frame, columns=(ID_COLUMN, NAME_COLUMN, SURNAME_COLUMN, AGE_COLUMN, GENDER_COLUMN, BIRTHDATE_COLUMN, PHONE_COLUMN), show='headings', style='Treeview')
        self.tree.heading(ID_COLUMN, text=ID_COLUMN)
        self.tree.heading(NAME_COLUMN, text=NAME_COLUMN)
        self.tree.heading(SURNAME_COLUMN, text=SURNAME_COLUMN)
        self.tree.heading(AGE_COLUMN, text=AGE_COLUMN)
        self.tree.heading(GENDER_COLUMN, text=GENDER_COLUMN)
        self.tree.heading(BIRTHDATE_COLUMN, text=BIRTHDATE_COLUMN)
        self.tree.heading(PHONE_COLUMN, text=PHONE_COLUMN)

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        btn_add = tk.Button(self.root, text="Add Person", command=self.add_person)
        btn_remove = tk.Button(self.root, text="Remove Person", command=self.remove_person)
        btn_edit = tk.Button(self.root, text="Edit Person", command=self.edit_person)
        btn_save = tk.Button(self.root, text="Save to File", command=self.save_data_to_file)

        btn_add.pack(pady=5)
        btn_remove.pack(pady=5)
        btn_edit.pack(pady=5)
        btn_save.pack(pady=5)

    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())  # Clear current data in treeview
        for person in Person.get_people():
            self.tree.insert('', 'end', values=(person.id, person.name, person.surname, person.age, person.gender, person.birthdate, person.phone_number))

    def add_person(self):
        popup = tk.Toplevel(self.root)
        popup.grab_set()
        popup.title("Add Person")

        name_label = tk.Label(popup, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        surname_label = tk.Label(popup, text="Surname:")
        surname_label.grid(row=1, column=0, padx=5, pady=5)
        surname_entry = tk.Entry(popup)
        surname_entry.grid(row=1, column=1, padx=5, pady=5)

        birthdate_label = tk.Label(popup, text="Birthdate (dd/mm/yyyy):")
        birthdate_label.grid(row=2, column=0, padx=5, pady=5)
        birthdate_entry = tk.Entry(popup)
        birthdate_entry.grid(row=2, column=1, padx=5, pady=5)

        gender_label = tk.Label(popup, text="Gender (M/F):")
        gender_label.grid(row=3, column=0, padx=5, pady=5)
        gender_entry = tk.Entry(popup)
        gender_entry.grid(row=3, column=1, padx=5, pady=5)

        phone_label = tk.Label(popup, text="Phone Number:")
        phone_label.grid(row=4, column=0, padx=5, pady=5)
        phone_entry = tk.Entry(popup)
        phone_entry.grid(row=4, column=1, padx=5, pady=5)

        submit_button = tk.Button(popup, text="Submit", command=lambda: self.submit_person(popup, name_entry.get(), surname_entry.get(), birthdate_entry.get(), gender_entry.get(), phone_entry.get()))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_person(self, popup, name, surname, birthdate, gender, phone_number):
        if not name.isalpha():
            messagebox.showerror("Error", "Name should only contain alphabetic characters.")
            return
        if not surname.isalpha():
            messagebox.showerror("Error", "Surname should only contain alphabetic characters.")
            return
        try:
            datetime.strptime(birthdate, '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Error", "Birthdate must be in the format dd/mm/yyyy.")
            return

        new_id = str(uuid.uuid4())
        Person.add_person(new_id, name, surname, birthdate, gender, phone_number)

        self.populate_treeview()  # Update the Treeview with new data
        popup.destroy()

    def remove_person(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No person selected.")
            return

        selected_id = self.tree.item(selected_item[0])['values'][0]
        Person.remove_person(selected_id)
        self.populate_treeview()

    def edit_person(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No person selected.")
            return

        selected_values = self.tree.item(selected_item[0])['values']
        selected_id = selected_values[0]
        selected_person = Person.people_dict[selected_id]

        popup = tk.Toplevel(self.root)
        popup.grab_set()
        popup.title("Edit Person")

        name_label = tk.Label(popup, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, selected_person.name)

        surname_label = tk.Label(popup, text="Surname:")
        surname_label.grid(row=1, column=0, padx=5, pady=5)
        surname_entry = tk.Entry(popup)
        surname_entry.grid(row=1, column=1, padx=5, pady=5)
        surname_entry.insert(0, selected_person.surname)

        birthdate_label = tk.Label(popup, text="Birthdate (dd/mm/yyyy):")
        birthdate_label.grid(row=2, column=0, padx=5, pady=5)
        birthdate_entry = tk.Entry(popup)
        birthdate_entry.grid(row=2, column=1, padx=5, pady=5)
        birthdate_entry.insert(0, selected_person.birthdate)

        gender_label = tk.Label(popup, text="Gender (M/F):")
        gender_label.grid(row=3, column=0, padx=5, pady=5)
        gender_entry = tk.Entry(popup)
        gender_entry.grid(row=3, column=1, padx=5, pady=5)
        gender_entry.insert(0, selected_person.gender)

        phone_label = tk.Label(popup, text="Phone Number:")
        phone_label.grid(row=4, column=0, padx=5, pady=5)
        phone_entry = tk.Entry(popup)
        phone_entry.grid(row=4, column=1, padx=5, pady=5)
        phone_entry.insert(0, selected_person.phone_number)

        submit_button = tk.Button(popup, text="Submit", command=lambda: self.submit_person_edit(popup, selected_id, name_entry.get(), surname_entry.get(), birthdate_entry.get(), gender_entry.get(), phone_entry.get()))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_person_edit(self, popup, id, name, surname, birthdate, gender, phone_number):
        if not name.isalpha():
            messagebox.showerror("Error", "Name should only contain alphabetic characters.")
            return
        if not surname.isalpha():
            messagebox.showerror("Error", "Surname should only contain alphabetic characters.")
            return
        try:
            datetime.strptime(birthdate, '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Error", "Birthdate must be in the format dd/mm/yyyy.")
            return

        Person.update_person(id, name, surname, birthdate, gender, phone_number)
        self.populate_treeview()  # Update the Treeview with new data
        popup.destroy()

    def save_data_to_file(self):
        result = Person.save_data_to_file(self.filename)
        messagebox.showinfo("Save Data", result)

if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
