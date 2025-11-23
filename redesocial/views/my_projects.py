import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk 
import tkinter.font as tkFont 
from .config_layout import *


f = frames["Projetos"]; tk.Label(f, text="Meus Projetos", font=font_roboto_big, bg=colors["bg_frame"], fg=colors["fg_text"]).pack(pady=10)