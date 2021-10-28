#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 20:55:06 2021

@author: yaroslav
"""

import datetime
import tkinter as tk
import threading
from time import sleep
import sys
import re
import pytz

Source_NAME_PATTERN = re.compile(r"[A-Z][a-z]+")
RA_PATTERN = re.compile(r"ra=(\d*.\d*)")
DEC_PATTERN = re.compile(r"dec=(\d*.\d*)")
file_name = sys.argv[1] 
timezone_irkutsk = pytz.timezone('Asia/Irkutsk')
timezone_utc = pytz.timezone('UTC')
# =============================================================================
#
# =============================================================================

def duration(date, start_time, stop_time):
    
    d, m, y = [int(x) for x in date.split(".")]
    h_start, min_start = [int(x) for x in start_time.split(":")]
    h_stop, min_stop = [int(x) for x in stop_time.split(":")]

    start_datetime = datetime.datetime(y, m, d, h_start, min_start)
    stop_datetime = datetime.datetime(y, m, d, h_stop, min_stop)
    
    return stop_datetime - start_datetime

def time_checker(current_utc_datetime, utc_source_date,
                 utc_source_start_time, utc_source_stop_time):

    cur_y, cur_m, cur_d, cur_h, cur_min, cur_s = current_utc_datetime.timetuple()[:6]
    
    d, m, y = [int(x) for x in utc_source_date.split(".")]
    h_start, min_start = [int(x) for x in utc_source_start_time.split(":")]
    h_stop, min_stop = [int(x) for x in utc_source_stop_time.split(":")]

    start_datetime = datetime.datetime(y, m, d, h_start, min_start)
    stop_datetime = datetime.datetime(y, m, d, h_stop, min_stop)
    current_datetime = datetime.datetime(cur_y, cur_m, cur_d, cur_h, cur_min, cur_s)

    if current_datetime <= start_datetime:
        status_label = "Time to run:"
        time_label = start_datetime - current_datetime
        color = "blue"
    elif start_datetime <= current_datetime <= stop_datetime:
        status_label = "RUN IS GOING! Time to stop:"
        time_label = stop_datetime - current_datetime
        color = "green"
    else:
        status_label = "Run has been finished:"
        time_label = current_datetime - stop_datetime
        color = "red"

    return status_label, time_label, color        
        
def page_content_update():
    
    while True:
        tunka_datetime_now = datetime.datetime.now(timezone_irkutsk)
        tunka_time_now = tunka_datetime_now.strftime("%H:%M:%S")
        tunka_date_now = tunka_datetime_now.strftime("%d:%m:%Y")
        
        local_datetime_now = datetime.datetime.now()
        local_time_now = local_datetime_now.strftime("%H:%M:%S")
        local_date_now = local_datetime_now.strftime("%d:%m:%Y")

        utc_datetime_now = datetime.datetime.now(timezone_utc)
        utc_time_now = utc_datetime_now.strftime("%H:%M:%S")
        utc_date_now = utc_datetime_now.strftime("%d:%m:%Y")   

        tunka_time_now_label['text'] = tunka_time_now
        local_time_now_label['text'] = local_time_now
        utc_time_now_label['text'] = utc_time_now
        tunka_date_now_label['text'] = tunka_date_now
        local_date_now_label['text'] = local_date_now
        utc_date_now_label['text'] = utc_date_now
        
        
        run_status, run_time, run_color = time_checker(utc_datetime_now, not_zero_duration_sources[0].utc_date,
                                               not_zero_duration_sources[0].utc_time_beg,
                                               not_zero_duration_sources[-1].utc_time_end)
        
        hiscore_run_status_text_label = tk.Label(master=timetable_frame, text=run_status, fg = run_color)
        hiscore_run_status_label = tk.Label(master=timetable_frame, text=run_time, fg=run_color)
        hiscore_run_status_text_label.grid(row=5, column=7)
        hiscore_run_status_label.grid(row=6, column=7)
        
        for i in range(len(not_zero_duration_sources)):

            run_status, run_time, run_color = time_checker(utc_datetime_now, not_zero_duration_sources[i].utc_date,
                                                           not_zero_duration_sources[i].utc_time_beg,
                                                           not_zero_duration_sources[i].utc_time_end)

            name_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].name, fg=run_color)
            run_status_label = tk.Label(master=timetable_frame, text=run_status, fg = run_color)
            run_time_label = tk.Label(master=timetable_frame, text=run_time, fg=run_color)
            run_status_label.grid(row=4*i+18, column=7, ipadx=4, padx=4)
            run_time_label.grid(row=4*i+19, column=7, ipadx=4, padx=4)
            name_label.grid(row=4*i+17, column=1, ipadx=4, padx=4)


        sleep(1)
# =============================================================================
#
# =============================================================================        
        
class Source:
    
    list_of_Sources = []
    
    def __init__(self, name="Source", code="code", ra=0.0, dec=0.0, dt=0, utc_date=0, utc_time_beg=0,
                 utc_time_end=0, tunka_date_beg=0, tunka_time_beg=0, tunka_date_end=0, tunka_time_end=0):
        
        self.name = name
        self.code = code
        self.ra = ra
        self.dec = dec
        self.dt = dt
        self.utc_date = utc_date
        self.utc_time_beg = utc_time_beg
        self.utc_time_end = utc_time_end
        self.tunka_date_beg = tunka_date_beg
        self.tunka_time_beg = tunka_time_beg
        self.tunka_date_end = tunka_date_end
        self.tunka_time_end = tunka_time_end
        self.list_of_Sources.append (self)
        
    def show_item (self):
        print("{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}".format(
                "name:", self.name, # 1
                "code:", self.code, # 2
                "ra:", self.ra, # 3
                "dec:", self.dec, # 4
                "dt:", self.dt, # 5
                "utc_date:", self.utc_date, # 6
                "utc_time_beg:", self.utc_time_beg, # 7
                "utc_time_end:", self.utc_time_end, # 8
                "tunka_date_beg:", self.tunka_date_beg, # 9
                "tunka_time_beg:", self.tunka_time_beg, # 10
                "tunka_date_end:", self.tunka_date_end, # 11
                "tunka_time_end:", self.tunka_time_end # 12
                ))
# =============================================================================
#
# =============================================================================

timetable_data = []
with open(file_name, "r", encoding="cp1251") as fin:

    Source_string = fin.readline()
    Source_list = re.findall(Source_NAME_PATTERN, Source_string)
    ra_list = re.findall(RA_PATTERN, Source_string)
    dec_list = re.findall(DEC_PATTERN, Source_string)    
    for _ in range(2):
        trash_string = fin.readline()

    string = fin.read().split('\n')
    for i in range(len(string)):
        new_string = string[i].split()
        if (new_string) and (new_string[0] == datetime.datetime.now().strftime("%d.%m.%Y")):
            today_data = new_string
            break

today_date = today_data[0]
for i in range(1, len(today_data), 7):
    Source(name = Source_list[(i-1)//7],
           ra = ra_list[(i-1)//7],
           dec = dec_list[(i-1)//7],
           dt = today_data[i],
           utc_date = today_date,
           utc_time_beg = today_data[i+1],
           utc_time_end = today_data[i+2],
           tunka_date_beg = today_data[i+3],
           tunka_time_beg = today_data[i+4],
           tunka_date_end = today_data[i+5],
           tunka_time_end = today_data[i+6])
    
not_zero_duration_sources = []
for item in Source.list_of_Sources:
    if item.dt != "00:00":
        not_zero_duration_sources.append(item)
###################  Затычка ######################
#    else:
#        not_zero_duration_sources.append(item)
###############  Конец затычки ####################
# =============================================================================
#
# =============================================================================

utc_datetime_now = datetime.datetime.now(timezone_utc)
utc_time_now = utc_datetime_now.strftime("%H:%M:%S")
utc_date_now = utc_datetime_now.strftime("%d:%m:%Y")    
tunka_datetime_now = datetime.datetime.now(timezone_irkutsk)
tunka_time_now = tunka_datetime_now.strftime("%H:%M:%S")
tunka_date_now = tunka_datetime_now.strftime("%d:%m:%Y")
local_datetime_now = datetime.datetime.now()
local_time_now = local_datetime_now.strftime("%H:%M:%S")
local_date_now = local_datetime_now.strftime("%d:%m:%Y")
# =============================================================================
#
# =============================================================================
main_form = tk.Tk()
timetable_frame = tk.Frame(relief=tk.GROOVE, borderwidth=1)
timetable_frame.pack()

###################  Разметка общего вывода  ######################

utc_date_title_label = tk.Label(master=timetable_frame, text="UTC Date:")
utc_date_now_label = tk.Label(master=timetable_frame, text=utc_date_now)
utc_time_title_label = tk.Label(master=timetable_frame, text="UTC Time:")
utc_time_now_label = tk.Label(master=timetable_frame, text=utc_time_now)
tunka_date_title_label = tk.Label(master=timetable_frame, text="Tunka Date:")
tunka_date_now_label = tk.Label(master=timetable_frame, text=tunka_date_now)
tunka_time_title_label = tk.Label(master=timetable_frame, text="Tunka Time:")
tunka_time_now_label = tk.Label(master=timetable_frame, text=tunka_time_now)
local_date_title_label = tk.Label(master=timetable_frame, text="Local Date:")
local_date_now_label = tk.Label(master=timetable_frame, text=local_date_now)
local_time_title_label = tk.Label(master=timetable_frame, text="Local Time:")
local_time_now_label = tk.Label(master=timetable_frame, text=local_time_now)

utc_date_title_label.grid(row=0, column=0, ipadx=4, padx=4)
utc_date_now_label.grid(row=0, column=1, ipadx=4, padx=4)
utc_time_title_label.grid(row=0, column=2, ipadx=4, padx=4)
utc_time_now_label.grid(row=0, column=3, ipadx=4, padx=4)
tunka_date_title_label.grid(row=1, column=0, ipadx=4, padx=4)
tunka_date_now_label.grid(row=1, column=1, ipadx=4, padx=4)
tunka_time_title_label.grid(row=1, column=2, ipadx=4, padx=4)
tunka_time_now_label.grid(row=1, column=3, ipadx=4, padx=4)
local_date_title_label.grid(row=2, column=0, ipadx=4, padx=4)
local_date_now_label.grid(row=2, column=1, ipadx=4, padx=4)
local_time_title_label.grid(row=2, column=2, ipadx=4, padx=4)
local_time_now_label.grid(row=2, column=3, ipadx=4, padx=4)
# =============================================================================
#
# =============================================================================

run_status, run_time, run_color = time_checker(utc_datetime_now, not_zero_duration_sources[0].utc_date,
                                               not_zero_duration_sources[0].utc_time_beg,
                                               not_zero_duration_sources[-1].utc_time_end)

###################  Разметка вывода  HiScore  ######################

hiscore_label = tk.Label(master=timetable_frame, text="HiScore timetable")

hiscore_time_utc_start_text_label = tk.Label(master=timetable_frame, text="UTC start time")
hiscore_time_utc_stop_text_label = tk.Label(master=timetable_frame, text="UTC stop time")
hiscore_time_tunka_start_text_label = tk.Label(master=timetable_frame, text="Tunka start time")
hiscore_date_tunka_start_text_label = tk.Label(master=timetable_frame, text="Tunka start date")
hiscore_time_tunka_stop_text_label = tk.Label(master=timetable_frame, text="Tunka stop time")
hiscore_date_tunka_stop_text_label = tk.Label(master=timetable_frame, text="Tunka stop date")
hiscore_run_status_text_label = tk.Label(master=timetable_frame, text="RUN status")
hiscore_run_duration_text_label = tk.Label(master=timetable_frame, text="Duration")

hiscore_time_utc_start_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[0].utc_time_beg)
hiscore_time_utc_stop_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[-1].utc_time_end)
hiscore_time_tunka_start_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[0].tunka_time_beg)
hiscore_date_tunka_start_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[0].tunka_date_beg)
hiscore_time_tunka_stop_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[-1].tunka_time_end)
hiscore_date_tunka_stop_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[-1].tunka_date_end)
hiscore_run_duration_label = tk.Label(master=timetable_frame, text=duration(not_zero_duration_sources[0].utc_date,
        not_zero_duration_sources[0].utc_time_beg, not_zero_duration_sources[0].utc_time_end
        ))
hiscore_run_status_label = tk.Label(master=timetable_frame, text=run_time, fg=run_color)

hiscore_label.grid(row=4, column=0, ipadx=4, padx=4)
hiscore_time_utc_start_text_label.grid(row=5, column=1, ipadx=4, padx=4)
hiscore_time_utc_stop_text_label.grid(row=5, column=2, ipadx=4, padx=4)
hiscore_time_tunka_start_text_label.grid(row=5, column=4, ipadx=4, padx=4)
hiscore_date_tunka_start_text_label.grid(row=5, column=3, ipadx=4, padx=4)
hiscore_time_tunka_stop_text_label.grid(row=5, column=6, ipadx=4, padx=4)
hiscore_date_tunka_stop_text_label.grid(row=5, column=5, ipadx=4, padx=4)
hiscore_run_status_text_label.grid(row=5, column=7, ipadx=4, padx=4)
hiscore_run_duration_text_label.grid(row=5, column=0, ipadx=4, padx=4)

hiscore_time_utc_start_label.grid(row=6, column=1, ipadx=4, padx=4)
hiscore_time_utc_stop_label.grid(row=6, column=2, ipadx=4, padx=4)
hiscore_time_tunka_start_label.grid(row=6, column=4, ipadx=4, padx=4)
hiscore_date_tunka_start_label.grid(row=6, column=3, ipadx=4, padx=4)
hiscore_time_tunka_stop_label.grid(row=6, column=6, ipadx=4, padx=4)
hiscore_date_tunka_stop_label.grid(row=6, column=5, ipadx=4, padx=4)
hiscore_run_duration_label.grid(row=6, column=0, ipadx=4, padx=4)
hiscore_run_status_label.grid(row=6, column=7, ipadx=4, padx=4)
# =============================================================================
#
# =============================================================================
###################  Разметка вывода  IACT  ######################

iact_label = tk.Label(master=timetable_frame, text="IACTs timetable")
iact_label.grid(row=7, column=0, ipadx=4, padx=4)

for i in range(len(not_zero_duration_sources)):

################### Рассчеты ######################
    
    run_status, run_time, run_color = time_checker(utc_datetime_now, not_zero_duration_sources[i].utc_date,
                                                   not_zero_duration_sources[i].utc_time_beg,
                                                   not_zero_duration_sources[i].utc_time_end)

###################  Разметка вывода  IACT  ######################
    dt_text_label = tk.Label(master=timetable_frame, text="Duration")
    name_text_label = tk.Label(master=timetable_frame, text="Source")
    ra_text_label = tk.Label(master=timetable_frame, text="ra")
    dec_text_label = tk.Label(master=timetable_frame, text="dec")
    ut_time_beg_text_label = tk.Label(master=timetable_frame, text="UTC start time")
    ut_time_end_text_label = tk.Label(master=timetable_frame, text="UTC stop time")
    loc_date_beg_text_label = tk.Label(master=timetable_frame, text="Tunka start date")
    loc_time_beg_text_label = tk.Label(master=timetable_frame, text="Tunka start time")
    loc_date_end_text_label = tk.Label(master=timetable_frame, text="Tunka stop date")
    loc_time_end_text_label = tk.Label(master=timetable_frame, text="Tunka stop time")

    run_status_label = tk.Label(master=timetable_frame, text=run_status, fg = run_color)
    run_time_label = tk.Label(master=timetable_frame, text=run_time, fg=run_color)

    dt_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].dt)
    name_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].name)
    ra_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].ra)
    dec_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].dec)
    ut_time_beg_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].utc_time_beg)
    ut_time_end_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].utc_time_end)
    tunka_date_beg_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].tunka_date_beg)
    tunka_time_beg_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].tunka_time_beg)
    tunka_date_end_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].tunka_date_end)
    tunka_time_end_label = tk.Label(master=timetable_frame, text=not_zero_duration_sources[i].tunka_time_end)
    
    name_text_label.grid(row=4*i+16, column=1, ipadx=4, padx=4)
    ra_text_label.grid(row=4*i+16, column=2, ipadx=4, padx=4)
    dec_text_label.grid(row=4*i+16, column=3, ipadx=4, padx=4)
    run_status_label.grid(row=4*i+18, column=7, ipadx=4, padx=4)
    
    name_label.grid(row=4*i+17, column=1, ipadx=4, padx=4)
    ra_label.grid(row=4*i+17, column=2, ipadx=4, padx=4)
    dec_label.grid(row=4*i+17, column=3, ipadx=4, padx=4)
    run_time_label.grid(row=4*i+19, column=7, ipadx=4, padx=4)    
    
    dt_text_label.grid(row=4*i+18, column=0, ipadx=4, padx=4)
    ut_time_beg_text_label.grid(row=4*i+18, column=1, ipadx=4, padx=4)
    ut_time_end_text_label.grid(row=4*i+18, column=2, ipadx=4, padx=4)
    loc_date_beg_text_label.grid(row=4*i+18, column=3, ipadx=4, padx=4)
    loc_time_beg_text_label.grid(row=4*i+18, column=4, ipadx=4, padx=4)
    loc_date_end_text_label.grid(row=4*i+18, column=5, ipadx=4, padx=4)
    loc_time_end_text_label.grid(row=4*i+18, column=6, ipadx=4, padx=4)

        
    dt_label.grid(row=4*i+19, column=0, ipadx=4, padx=4)
    ut_time_beg_label.grid(row=4*i+19, column=1, ipadx=4, padx=4)
    ut_time_end_label.grid(row=4*i+19, column=2, ipadx=4, padx=4)
    tunka_date_beg_label.grid(row=4*i+19, column=3, ipadx=4, padx=4)
    tunka_time_beg_label.grid(row=4*i+19, column=4, ipadx=4, padx=4)
    tunka_date_end_label.grid(row=4*i+19, column=5, ipadx=4, padx=4)
    tunka_time_end_label.grid(row=4*i+19, column=6, ipadx=4, padx=4)
# =============================================================================
#
# =============================================================================

process = threading.Thread(target=page_content_update)
process.start()
main_form.title("Today ({}) TAIGA-IACTs timetable".format(today_date))
main_form.mainloop()