import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from datetime import datetime
from tkcalendar import Calendar, DateEntry
from tkintermapview import TkinterMapView

from modules.models import Character, Geotag  
from modules.sqlite_manager import CharacterAppDatabase 

class GandalfApp:
    def __init__(self, root, db):
        self.root = root
        self.db : CharacterAppDatabase = db
        self.root.title("Gandalf's Tracking App")
        self.create_main_window()
        self.marker_path = None
        
    def create_main_window(self):
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
            self.tree.insert("", tk.END, values=(char.id[:6], char.name))
            
    def add_character_popup(self):
        name = simpledialog.askstring("Input", "Enter the character name:")
        if name:
            new_char = Character(name=name)
            print(new_char)
            self.db.add_character(new_char)
            self.refresh_characters()
            
    def add_geotag_popup(self):
        characters = self.db.get_characters()
        
        if not characters:
            tk.messagebox.showerror("Error", "No characters available. Please add a character first.")
            return

        char_names = [char.name for char in characters]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Geotag")
        
        ttk.Label(dialog, text="Select Character:").grid(row=0, column=0)
        selected_char = tk.StringVar(value=char_names[0])
        char_dropdown = ttk.Combobox(dialog, textvariable=selected_char, values=char_names)
        char_dropdown.grid(row=0, column=1)
        
        ttk.Label(dialog, text="Select Date:").grid(row=1, column=0)
        cal = Calendar(dialog, selectmode="day", year=2023, month=10, day=20)
        cal.grid(row=1, column=1)
        

        def validate_time(P):
            if P == "":
                return True
            try:
                value = int(P)
            except ValueError:
                return False
            if 0 <= value <= 59:  
                return True
            return False

        def validate_hour(P):
            if P == "":
                return True
            try:
                value = int(P)
            except ValueError:
                return False
            if 0 <= value <= 23: 
                return True
            return False

        vcmd_time = dialog.register(validate_time)
        vcmd_hour = dialog.register(validate_hour)
        
        ttk.Label(dialog, text="Select Time:").grid(row=2, column=0)
        time_frame = ttk.Frame(dialog)
        hour_entry = ttk.Entry(time_frame, validate='key', validatecommand=(vcmd_hour, '%P'), width=3)
        minute_entry = ttk.Entry(time_frame, validate='key', validatecommand=(vcmd_time, '%P'), width=3)
        second_entry = ttk.Entry(time_frame, validate='key', validatecommand=(vcmd_time, '%P'), width=3)
        hour_entry.grid(row=0, column=0)
        minute_entry.grid(row=0, column=1)
        second_entry.grid(row=0, column=2)
        time_frame.grid(row=2, column=1)
        
        ttk.Label(dialog, text="Latitude:").grid(row=3, column=0)
        latitude_entry = ttk.Entry(dialog)
        latitude_entry.grid(row=3, column=1)
        
        ttk.Label(dialog, text="Longitude:").grid(row=4, column=0)
        longitude_entry = ttk.Entry(dialog)
        longitude_entry.grid(row=4, column=1)
        
        def add_geotag():
            selected_char_name = selected_char.get()
            selected_char_obj = next((char for char in characters if char.name == selected_char_name), None)
            
            if selected_char_obj is None:
                tk.messagebox.showerror("Error", "Selected character not found.")
                return

            try:
                latitude = float(latitude_entry.get())
                longitude = float(longitude_entry.get())
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid latitude or longitude.")
                return

            selected_date = cal.get_date().split("/")
            try:
                month, day, year = map(int, selected_date)
                hour = int(hour_entry.get())
                minute = int(minute_entry.get())
                second = int(second_entry.get())
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid time format.")
                return

            timestamp = datetime(year+2000, month, day, hour, minute, second).isoformat()
            
            new_geotag = Geotag(character_id=selected_char_obj.id, timestamp=timestamp, latitude=latitude, longitude=longitude)
            self.db.add_geotag(new_geotag)
            dialog.destroy()

        
            
        ttk.Button(dialog, text="Add", command=add_geotag).grid(row=5, columnspan=4)


    def show_map_popup(self):
        self.map_widget = TkinterMapView(
            width=800, 
            height=600, 
            corner_radius=0, 
            max_zoom=15, 
            database_path="database/offline_tiles.db"
        )
        self.map_widget.grid(row=0, column=0, sticky="nsew")

        close_button = tk.Button(self.map_widget, text="Close", command=self.map_widget.destroy)
        close_button.grid(row=0, column=1)

        characters = self.db.get_characters()
        char_names = [char.name for char in characters]
        marker_list = []

        ttk.Label(self.map_widget, text="From:").grid(row=1, column=0)
        start_date_entry = DateEntry(self.map_widget)
        start_date_entry.grid(row=1, column=1)

        start_hour_entry = ttk.Entry(self.map_widget, width=3)
        start_hour_entry.grid(row=1, column=2)
        start_hour_entry.insert('0', '00')
        start_minute_entry = ttk.Entry(self.map_widget, width=3)
        start_minute_entry.grid(row=1, column=3)
        start_minute_entry.insert('0', '00')
        start_second_entry = ttk.Entry(self.map_widget, width=3)
        start_second_entry.grid(row=1, column=4)
        start_second_entry.insert('0', '00')

        ttk.Label(self.map_widget, text="To:").grid(row=2, column=0)
        end_date_entry = DateEntry(self.map_widget)
        end_date_entry.grid(row=2, column=1)
        
        end_hour_entry = ttk.Entry(self.map_widget, width=3)
        end_hour_entry.grid(row=2, column=2)
        end_hour_entry.insert('0', '00')
        end_minute_entry = ttk.Entry(self.map_widget, width=3)
        end_minute_entry.grid(row=2, column=3)
        end_minute_entry.insert('0', '00')
        end_second_entry = ttk.Entry(self.map_widget, width=3)
        end_second_entry.grid(row=2, column=4)
        end_second_entry.insert('0', '00')

        def clear():
            for marker in marker_list:
                self.map_widget.delete(marker)
            marker_list.clear()

            if self.marker_path is not None:
                self.map_widget.delete(self.marker_path)

        def update_map():
            clear()
            selected_char_name = selected_char.get()
            if selected_char_name not in char_names:
                return
            char_id = characters[char_names.index(selected_char_name)].id
            geotags = self.db.get_geotags(char_id)

            start_date = start_date_entry.get_date()
            start_time = f"{start_hour_entry.get()}:{start_minute_entry.get()}:{start_second_entry.get()}"
            start_datetime = datetime.combine(start_date, datetime.strptime(start_time, '%H:%M:%S').time())
            
            end_date = end_date_entry.get_date()
            end_time = f"{end_hour_entry.get()}:{end_minute_entry.get()}:{end_second_entry.get()}"
            end_datetime = datetime.combine(end_date, datetime.strptime(end_time, '%H:%M:%S').time())
            

            filtered_geotags = [geotag for geotag in geotags if ( geotag['timestamp'] <= end_datetime) and (geotag['timestamp'] >= start_datetime)]
            sorted_geotags = sorted(filtered_geotags, key=lambda x: x['timestamp'])
            
            for geotag in sorted_geotags:
                marker = self.map_widget.set_position(geotag['latitude'], geotag['longitude'], marker=True)
                marker.text = selected_char_name + ' ' + str(geotag['timestamp'])
                marker_list.append(marker)
            
            if len(sorted_geotags) > 1:
                positions = [(geotag['latitude'], geotag['longitude']) for geotag in sorted_geotags]
                self.marker_path = self.map_widget.set_path(positions)


        selected_char = tk.StringVar(value=char_names[0] if char_names else "")
        char_dropdown = ttk.Combobox(
            self.map_widget, 
            textvariable=selected_char, 
            values=char_names
        )
        char_dropdown.grid(row=0, column=2)

        update_button = tk.Button(self.map_widget, text="Update Map", command=update_map)
        update_button.grid(row=0, column=3)

        if char_names:
            update_map()
