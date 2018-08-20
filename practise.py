import tkinter as tk
import matplotlib
from tkinter import font  as tkfont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg ,NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
import requests
import datetime
import time
import json
import urllib
import pandas as pd
import numpy as np



text_mainpage="""USD-INR Price Monitor Software
Developer Soumil N Shah"""

x_axis=[]
y_axis=[]

def currency():
    url="https://api.thingspeak.com/apps/thinghttp/send_request?api_key=08UQVZQRNZHZSMNE"
    data=requests.get(url).json()
    y_axis.append(data)
    return data


def get_time():
    time_z=datetime.datetime.now()
    minutes=time_z.minute
    sec=time_z.second
    hr=time_z.hour
    my_timee=str(hr)+":"+ str(minutes) + ":" + str(sec)

    x_axis.append(my_timee)
    return my_timee




style.use("ggplot")
f = Figure(figsize=(4,2), dpi=100)
a = f.add_subplot(111)




def animate(i):
    #call function and append to x_axis and y_axis
    currency()
    get_time()

    a.clear()
    a.plot(x_axis, y_axis)





class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=(text_mainpage), font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Agree",bg="Black",fg="white",
                            command=lambda: controller.show_frame("PageOne"))
     
        button1.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"),relief= tk.RAISED )
        button.pack()



        canvas=FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand= True )

        toolbar= NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack()



app = SampleApp()
ani=animation.FuncAnimation(f,  animate, interval=3000)
app.mainloop()