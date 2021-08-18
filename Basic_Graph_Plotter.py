from ast import literal_eval
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np


class InputFrame(Frame):
    def __init__(self, master=None, outframe=None):
        Frame.__init__(self, master, bg="black")
        self.master = master
        self.outframe = outframe
        self.grid(row=0, column=0)
        self.label1 = Label(self,
                            text="Enter the Function Below\n",
                            width=40, height=5, fg="black", bg="yellow"
                            )
        self.label1.grid(row=0, column=0, sticky=S + N + E + W, columnspan=2,
                         padx=5, pady=5)

        self.exprs = Text(self, fg="black", bg="white",
                          width=40, height=2)
        self.exprs.grid(row=1, column=0, sticky=S + N + E + W, columnspan=2)

        self.label2 = Label(self, text="Enter the Range Below:",
                            width=40, height=2, fg="black", bg="yellow")
        self.label2.grid(row=2, column=0, sticky=S + N + E + W, columnspan=2,
                         padx=5, pady=5)

        self.labela = Label(self, text="Format : (a,b)",
                            width=20, height=5, fg="black", bg="green")
        self.labela.grid(row=3, column=0, sticky=S + N + E + W,
                         padx=5, pady=5)
        self.Range_a = Text(self, fg="black", bg="white",
                            width=40, height=2)
        self.Range_a.grid(row=3, column=1, sticky=S + N + E + W)

        self.evalbutton = Button(self, text="Plot", width=15, height=3,
                                 command=self.plotter)
        self.evalbutton.grid(row=5, column=0, sticky="news")

        self.exitbutton = Button(self, text="Exit", command=exit, width=15, height=3)
        self.exitbutton.grid(row=5, column=1, sticky="news", columnspan=2)

       # self.clearbutton = Button(self, text="clear", width=15, height=3,
        #                           command = self.clear)
       # self.clearbutton.grid(row=5, column=1, sticky="news")

        master.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
        master.columnconfigure([0, 1], weight=1)

    def plotter(self):
        k = []
        c = []
        varval = self.Range_a.get(1.0, END)
        a = literal_eval(varval)
        func = self.exprs.get(1.0, END)
        for x in np.linspace(a[0], a[1], 1000):
            y = eval(func)
            k.append(x)
            c.append(y)

        f = Figure(figsize=(5, 5), dpi=100)
        fig = f.add_subplot(111)
        fig.plot(k, c)

        canvas = FigureCanvasTkAgg(f, self.outframe)
        canvas.draw()
        canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(canvas, self.outframe)
        toolbar.update()
        canvas.get_tk_widget().pack()


class OutputFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(row=0, column=1)
        self.label = Label(self, text="Plot of Given Function",
                           width=40, height=4)
        self.label.pack()


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=None)
        self.master = master
        self.oframe = OutputFrame(master)
        self.iframe = InputFrame(master, self.oframe)
        master.geometry("1000x600")
        self.grid(row=0, column=0, sticky="nsew")


root = Tk()

adv = Window(root)
adv.mainloop()
