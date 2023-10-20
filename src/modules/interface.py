import tkinter as tk
import os
from tkinter import ttk
from tkinter import simpledialog
from modules.characters import Character
from datetime import datetime
from tkcalendar import Calendar
from tkintermapview import TkinterMapView


class GandalfApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Gandalf's Tracking App")
        self.create_main_window()
        
    def create_main_window(
        self):

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.tree = ttk.Treeview(
            self.main_frame, 
            columns=("ID", "Name"), 
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.grid(row=0, column=0, columnspan=4)
        
        ttk.Button(
            self.main_frame,
            text="Add Character",
            command=self.add_character_popup
        ).grid(row=1, column=0)
        ttk.Button(
            self.main_frame,
            text="Add Geotag",
            command=self.add_geotag_popup
        ).grid(row=1, column=1)
        ttk.Button(
            self.main_frame,
            text="Show Map",
            command=self.show_map_popup
        ).grid(row=1, column=2)
        ttk.Button(
            self.main_frame,
            text="Refresh",
            command=self.refresh_characters
        ).grid(row=1, column=3)
        
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
        characters = self.db.get_characters()
        
        if not characters:
            tk.messagebox.showerror(
                "Error", 
                "No characters available. Please add a character first."
            )
            return
        
        char_names = [char.name for char in characters]
        char_ids = [char.id for char in characters]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Geotag")
        
        ttk.Label(dialog, text="Select Character:").grid(row=0, column=0)
        selected_char = tk.StringVar(value=char_names[0])
        char_dropdown = ttk.Combobox(
            dialog, 
            textvariable=selected_char, 
            values=char_names
        )
        char_dropdown.grid(row=0, column=1)


        ttk.Label(dialog, text="Select Date:").grid(row=1, column=0)
        cal = Calendar(dialog, selectmode="day", year=2023, month=10, day=20)
        cal.grid(row=1, column=1)
        
        selected_date_label = ttk.Label(dialog, text="Selected date will appear here")
        selected_date_label.grid(row=1, column=2)
        
        def on_date_select(event):
            selected_date_label["text"] = cal.get_date()
            
        cal.bind("<<CalendarSelected>>", on_date_select)

        ttk.Label(dialog, text="Select Time:").grid(row=2, column=0)
        time_frame = ttk.Frame(dialog)
        hour_entry = ttk.Entry(time_frame, width=3)
        minute_entry = ttk.Entry(time_frame, width=3)
        second_entry = ttk.Entry(time_frame, width=3)
        hour_entry.grid(row=1, column=1)
        minute_entry.grid(row=1, column=2)
        second_entry.grid(row=1, column=3)
        time_frame.grid(row=2, column=1)
        
        ttk.Label(dialog, text="Latitude:").grid(row=3, column=0)
        latitude_entry = ttk.Entry(dialog)
        latitude_entry.grid(row=3, column=1)
        
        ttk.Label(dialog, text="Longitude:").grid(row=4, column=0)
        longitude_entry = ttk.Entry(dialog)
        longitude_entry.grid(row=4, column=1)
        
        def add_geotag():
            selected_char_name = selected_char.get()
            if selected_char_name not in char_names:
                tk.messagebox.showerror("Error", "Selected character not found.")
                return

            try:
                latitude = float(latitude_entry.get())
                longitude = float(longitude_entry.get())
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid latitude or longitude.")
                return

            selected_date = cal.get_date()
            try:
                hour = int(hour_entry.get())
                minute = int(minute_entry.get())
                second = int(second_entry.get())
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid time format.")
                return

            timestamp = f"{selected_date} {hour}:{minute}:{second}"
            
            char_id = char_ids[char_names.index(selected_char_name)]
            self.db.add_geotag(char_id, timestamp, latitude, longitude)
            dialog.destroy()
            
        ttk.Button(dialog, text="Add", command=add_geotag).grid(
            row=5, columnspan=4)

    def show_map_popup(self):

        self.map_widget = TkinterMapView(
            width=800, 
            height=600, 
            corner_radius=0, 
            max_zoom=15, 
            database_path="database/offline_tiles.db"
        )
        self.map_widget.grid(row=0, column=0, columnspan=3, sticky="nsew")

        close_button = tk.Button(self.map_widget, text="Close", command=self.map_widget.destroy)
        close_button.grid(row=0, column=1)

        
        characters = self.db.get_characters()
        for char in characters:
            geotags = self.db.get_geotags(char.id)
            
            for geotag in geotags:
                marker = self.map_widget.set_position(geotag['latitude'], geotag['longitude'], marker=True)
                marker.text = char.name + ' ' + geotag['timestamp']
            
            if len(geotags) > 1:
                positions = [(geotag['latitude'], geotag['longitude']) for geotag in geotags]
                self.map_widget.set_path(positions)
