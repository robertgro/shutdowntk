import tkinter as tk
from tkinter import ttk
#https://stackoverflow.com/questions/22245711/from-import-or-import-as-for-modules tkinter ttk widget difference
from subprocess import Popen

class ShutdownTK:
    def __init__(self, root):
        self.configRoot(root)
        self.setupWidgets(root)
        self.setupGrid()

    def configRoot(self, root):
        root.title("Automatische Abschaltung")
        #https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter
        root.geometry("355x130")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        #https://stackoverflow.com/questions/31545559/how-to-change-background-color-in-ttk-comboboxs-listview
        root.option_add("*TCombobox*Listbox*Background", '#031f30')
        root.option_add('*TCombobox*Listbox*Foreground', '#9cd4f7')
        root.option_add('*TCombobox*Listbox*selectBackground', '#e79a5c')
        root.option_add('*TCombobox*Listbox*selectForeground', '#23527c')

    def setupWidgets(self, root):
        self.labelstr = tk.StringVar(value="Zeit auswählen")
        self.radiostr = tk.StringVar()
        self.comboboxstr = tk.StringVar()
        self.style = ttk.Style(root)
        self.style.configure('.', font=('Segoe UI Variable', 10), background="#031f30", foreground="#f9e3ae")
        self.contentframe = ttk.Frame(root, padding="3 3 12 12") # main frame
        self.comboboxframe = ttk.Frame(self.contentframe, borderwidth=0, width=200, height=100, padding="5")
        self.radioframe = ttk.Frame(self.contentframe, borderwidth=0, width=200, height=100, padding="10")
        self.combobox = ttk.Combobox(self.comboboxframe, values=("2 Stunden", "3 Stunden", "4 Stunden"), textvariable=self.comboboxstr)
        self.combobox.bind("<<ComboboxSelected>>", lambda event: self.comboboxCallback(event, root))
        self.label = ttk.Label(self.comboboxframe, text="test", font=("Helvetica", 10), textvariable=self.labelstr, padding="0 5")
        self.radiohalfhour = ttk.Radiobutton(self.radioframe, text="30 Minuten", variable=self.radiostr, value="1800", command=lambda: self.initFunc(root))
        self.radioquaterhour = ttk.Radiobutton(self.radioframe, text="45 Minuten", variable=self.radiostr, value="2700", command=lambda: self.initFunc(root))
        self.radiohour = ttk.Radiobutton(self.radioframe, text="1 Stunde", variable=self.radiostr, value="3600", command=lambda: self.initFunc(root))
        self.radiohourandhalf = ttk.Radiobutton(self.radioframe, text="1 Stunde 30 Minuten", variable=self.radiostr, value="5400", command=lambda: self.initFunc(root))

    def setupGrid(self):
        self.contentframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.comboboxframe.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.radioframe.grid(column=1, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.label.grid(column=0, row=0, sticky=tk.W)
        self.combobox.grid(column=0, row=1, sticky=tk.W)
        self.radiohalfhour.grid(column=0, row=1, sticky=tk.W)
        self.radioquaterhour.grid(column=0, row=2, sticky=tk.W)
        self.radiohour.grid(column=0, row=3, sticky=tk.W)
        self.radiohourandhalf.grid(column=0, row=4, sticky=tk.W)
        for child in self.contentframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
    
    def initFunc(self, root, event=None):
        self.clocktimer = 0
        if event:
            match self.comboboxstr.get()[0]:
                case "2":
                    self.clocktimer = 7200
                case "3":
                    self.clocktimer = 10800
                case "4":
                    self.clocktimer = 14400
        else:
            self.clocktimer = int(self.radiostr.get())

        self.clockstr = tk.StringVar()
        self.clockstr.set("00:00:00")
        self.clockwindow = tk.Toplevel()
        self.clockwindow.title("Abschaltung in")
        self.clockwindow.geometry("250x45")
        self.clockwindow.columnconfigure(0, weight=1)
        self.clockwindow.rowconfigure(0, weight=1)
        self.clockstyle = ttk.Style(self.clockwindow)
        self.clockstyle.configure('.', font=('Segoe UI Variable', 12), background="#031f30", foreground="#f9e3ae", padding="0 5")
        #https://stackoverflow.com/questions/29472454/passing-arguments-to-a-tkinter-event-callback-bound-to-a-key
        self.clockframe = ttk.Frame(self.clockwindow, padding="3 3 12 12") # main frame
        self.clocklabel = ttk.Label(self.clockframe, text="00:00:00", textvariable=self.clockstr)
        self.clockframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.clocklabel.grid(column=0, row=0, sticky=tk.W)
        self.clocklabel.bind("<Destroy>", lambda event: self.abortFunc(event, root))
        root.withdraw()
        self.countdownProc()

    def comboboxCallback(self, event, root):
        #print(repr(event))
        self.initFunc(root, event)

    def abortFunc(self, event, root):
        self.clocktimer = 0
        root.deiconify()
        self.clockwindow.destroy()
        self.clockwindow.update()

    def countdownProc(self):
        #https://stackoverflow.com/questions/66929934/python-tkinter-after-method-not-working-as-expected
        if self.clocktimer:
            hours, rem = divmod(self.clocktimer, 3600)
            mins, secs = divmod(rem, 60)
            timer = '{:0>2}:{:0>2}:{:02}'.format(int(hours),int(mins),int(secs))
            #print(timer, end="\r")
            self.clockstr.set(timer)
            self.clocktimer -= 1
            self.clockwindow.after(1000, self.countdownProc)
        else:
            Popen('shutdown -s -f -t 0')
            