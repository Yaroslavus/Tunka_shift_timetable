#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 01:15:40 2021

@author: yaroslav
"""
import tkinter as tk
import tkinter.ttk as ttk


class IACT_run:
    
    list_of_runs = []
    
    def __init__(self, iact_number="01", run_number="", target="", start_time="", stop_time="", av_count_rate="", comments="", problems=""):
        
        self.iact_number = iact_number
        self.run_number = run_number
        self.target = target
        self.start_time = start_time
        self.stop_time = stop_time
        self.av_count_rate = av_count_rate
        self.comments = comments
        self.problems = problems
        self.list_of_Sources.append (self)
        
    def show_item (self):
        print("{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}".format(
                "iact_number:", self.iact_number, # 1
                "run_number:", self.run_number, # 2
                "target:", self.target, # 3
                "start_time:", self.start_time, # 4
                "stop_time:", self.stop_time, # 5
                "av_count_rate:", self.av_count_rate, # 6
                "comments:", self.comments, # 7
                "problems:", self.problems, # 8
                ))
        
main_form = tk.Tk()
detectors_frame = tk.Frame(master=main_form, relief=tk.GROOVE, borderwidth=1, width=1100, height=1000)
detectors_frame.pack(side=tk.LEFT, padx=5, pady=5)
prewiev_frame = tk.Frame(master=main_form, relief=tk.GROOVE, borderwidth=1, width=700, height=1000)
prewiev_frame.pack(side=tk.LEFT, padx=5, pady=5)

nb = ttk.Notebook(detectors_frame)
nb.pack(side=tk.TOP, fill="both", expand=True)

weather_frame = ttk.Frame(detectors_frame)
iact_frame = ttk.Frame(detectors_frame)
hiscore_frame = ttk.Frame(detectors_frame)
tunka133_grande_frame = ttk.Frame(detectors_frame)
grande_frame = ttk.Frame(detectors_frame)
taiga_muon_frame = ttk.Frame(detectors_frame)

nb.add(weather_frame, text='Weather')
nb.add(iact_frame, text='IACTs')
nb.add(hiscore_frame, text='HiScore')
nb.add(tunka133_grande_frame, text='Tunka133 + Grande')
nb.add(grande_frame, text='Grande')
nb.add(taiga_muon_frame, text='TAIGA-Muon')



main_form.title("TAIGA shift reporter")
main_form.mainloop()