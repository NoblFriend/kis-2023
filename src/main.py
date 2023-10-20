# from modules.characters import GandalfAppDatabase
from modules.interface import GandalfApp
from modules.sqlite_manager import CharacterAppDatabase
from modules.models import Character, Geotag
from datetime import datetime

import tkinter as tk

root = tk.Tk()

db = CharacterAppDatabase()


app = GandalfApp(root, db)

root.mainloop()