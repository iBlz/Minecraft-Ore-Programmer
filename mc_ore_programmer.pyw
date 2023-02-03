from tkinter.colorchooser import askcolor
from tkinter import *
import threading
import pymsgbox
import serial
import time
import sys
import os
import re

window = Tk()
rgb = 0

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def check_for_connection():
    global ser
    while True:
        time.sleep(1)
        try:
            ser.readlines()
            connected.place(x=10,y=150)
            disconnected.place_forget()
        except:
            disconnected.place(x=10,y=150)
            connected.place_forget()
            try:
                ser = serial.Serial(
                    port='COM9',
                    baudrate=9600,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                )
            except:
                pass

def apply():
    try:
        if rgb == 1:
            ser.write('{{"brightness": "{}","hex": "{}","rgb_toggle": "{}"}}'.format(brightness.get(),color[1].replace("#",""),rgb).encode())
        else:
            ser.write('{{"brightness": "{}","hex": "{}","rgb_toggle": "{}"}}'.format(brightness.get(),"FFFFFF".replace("#",""),rgb).encode())
    except:
        pymsgbox.alert('You must choose the color!', 'Warning!')

def choose_color():
    global color
    color = askcolor(title="Choose Minecraft Ore Color")

def rgb_on():
    global rgb
    rgb_off_button.pack(ipadx=5, ipady=5, expand=True)
    rgb_off_button.place(x=10, y=240)
    rgb_on_button.place_forget()
    rgb = 1

def rgb_off():
    global rgb
    rgb_on_button.pack(ipadx=5, ipady=5, expand=True)
    rgb_on_button.place(x=10, y=240)
    rgb_off_button.place_forget()
    rgb = 0

def background_threads():
    check_for_connection_thread = threading.Thread(target=check_for_connection)
    check_for_connection_thread.daemon = True 
    check_for_connection_thread.start()

window.geometry('620x500')
window.resizable('0', '0')
window.title("Minecraft Ore Programmer - by iBlz")
icon = PhotoImage(file=resource_path("images\\icon.png"))
window.iconphoto(False, icon)
window.configure(background='#2c394b')

box1_img = PhotoImage(file=resource_path("images\\logo.png"))
box1 = Canvas(window, width = 595, height = 94, highlightthickness=0, bd=0)
box1.create_image(0, 0, anchor=NW, image=box1_img) 
box1.place(x=10,y=10)

apply_img=PhotoImage(file=resource_path("images\\apply.png"))
apply_button = Button(window, highlightthickness=0, bd=0, text='', image=apply_img, command=lambda: apply())
apply_button.pack(ipadx=5, ipady=5, expand=True)
apply_button.place(x=10, y=420)

choose_color_img=PhotoImage(file=resource_path("images\\custom_color.png"))
choose_color_button = Button(window, highlightthickness=0, bd=0, text='', image=choose_color_img, command=lambda: choose_color())
choose_color_button.pack(ipadx=5, ipady=5, expand=True)
choose_color_button.place(x=10, y=330)

rgb_on_img=PhotoImage(file=resource_path("images\\rgb_on.png"))
rgb_on_button = Button(window, highlightthickness=0, bd=0, text='', image=rgb_on_img, command=lambda: rgb_on())
rgb_on_button.pack(ipadx=5, ipady=5, expand=True)
rgb_on_button.place(x=10, y=240)

rgb_off_img=PhotoImage(file=resource_path("images\\rgb_off.png"))
rgb_off_button = Button(window, highlightthickness=0, bd=0, text='', image=rgb_off_img, command=lambda: rgb_off())

brightness = Scale(window, from_=0, to=255, length=350, troughcolor='#2c394b',width='40', label="Brightness",highlightcolor='#2c394b',highlightbackground='#2c394b',fg='#2c394b')
brightness.pack(expand=True)
brightness.place(x=470,y=130)
brightness.set(25)

disconnected_img = PhotoImage(file=resource_path("images\\disconnected.png"))
disconnected = Canvas(window, width = 416, height = 66, highlightthickness=0, bd=0)
disconnected.create_image(0, 0, anchor=NW, image=disconnected_img) 
disconnected.place(x=10,y=150)

connected_img = PhotoImage(file=resource_path("images\\connected.png"))
connected = Canvas(window, width = 387, height = 66, highlightthickness=0, bd=0)
connected.create_image(0, 0, anchor=NW, image=connected_img) 

background_threads()
window.mainloop()