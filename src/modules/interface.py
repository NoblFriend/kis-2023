import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from characters import Character

class GandalfApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Gandalf's Tracking App")
        self.create_main_window()
        
    def create_main_window(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Name"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.grid(row=0, column=0, columnspan=4)
        
        ttk.Button(self.main_frame, text="Add Character", command=self.add_character_popup).grid(row=1, column=0)
        ttk.Button(self.main_frame, text="Add Geotag", command=self.add_geotag_popup).grid(row=1, column=1)
        ttk.Button(self.main_frame, text="Show Map", command=self.show_map_popup).grid(row=1, column=2)
        ttk.Button(self.main_frame, text="Refresh", command=self.refresh_characters).grid(row=1, column=3)
        
        self.refresh_characters()
        
    def refresh_characters(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        characters = self.db.get_characters()
        for char in characters:
            self.tree.insert("", tk.END, values=(char.id, char.name))
            
    def add_character_popup(self):
        name = simpledialog.askstring("Input", "Enter the character name:")
        if name:
            new_char = Character(name=name)
            self.db.add_character(new_char)
            self.refresh_characters()
            
    def add_geotag_popup(self):
        # Placeholder
        print("Add Geotag clicked")
        
    def show_map_popup(self):
        # Placeholder
        print("Show Map clicked")