#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 00:36:14 2021

@author: yaroslav
"""

import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import subprocess

SET_OF_TIMETABLE_FILETYPES={"txt"}
TIMETABLE_FILETYPE="*.txt"

def choose_the_file_through_pressing_Enter(e):

    to_choose_the_file()
    
def to_choose_the_file():

    file_path = fd.askopenfilename(filetypes=[("Text TAIGA timetable file", TIMETABLE_FILETYPE)])
    if file_path:
        file_name, file_extention = file_path.split(".")
    if file_name and (file_extention not in SET_OF_TIMETABLE_FILETYPES):
        mb.showerror("Error", "Wrong file type")
        return 0
    subprocess.run(["chmod", "+x", "TAIGA_shift_timetable.py"])
    main_form.destroy()
    subprocess.run(["./TAIGA_shift_timetable.py", file_path])


main_form = tk.Tk()
main_form.title("IACT Timetable")
main_form.geometry("200x50")
main_form.resizable(width=True, height=True)

open_spot_image_button = tk.Button(main_form, text="Choose the timetable file",
                              command=to_choose_the_file, state=tk.NORMAL)
open_spot_image_button.pack(fill=None, expand=True)

main_form.bind ('<Return>', choose_the_file_through_pressing_Enter)
main_form.bind('<Escape>', lambda e: main_form.destroy())
main_form.mainloop()