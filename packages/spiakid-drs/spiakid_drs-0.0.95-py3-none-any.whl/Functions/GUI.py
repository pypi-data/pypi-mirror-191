from tkinter import * 
from tkinter.filedialog import *
from tkinter import ttk
import Functions.Modelisation as Model
import matplotlib.pyplot as plt



def interface():


    def path_data():
        filepath = askopenfilename(title="Path",filetypes=[('hdf files','.hdf'),('all files','.*')])
        value_data.set(filepath)


    def path_plot():
        filepath = askdirectory()
        value_plot.set(filepath)


    def Launch():
        Model.Data_read(value_data.get(),value_plot.get(),FormatMenu.get())
        Main_Window.quit()

 

    Main_Window = Tk()
    Main_Window.title('DRS')
    frm = ttk.Frame(Main_Window, padding=10)
    frm.grid()

    value_data = StringVar() 
    FormatList = ['.jpg','.svg','.eps']

    # Taking the data location, HDF5 required
    label = ttk.Label(frm,text="Data location ?").grid(column = 0,row=0)
    entry_data = ttk.Entry(frm, width=30,textvariable=value_data).grid(column=0,row=1)
    button_data = ttk.Button(frm,text='Browse',command=path_data).grid(column=1,row=1)

    label = ttk.Label(frm,text = '                              ').grid(column=2,row=0)

    # Taking Folder and Format for the plot saving
    label = ttk.Label(frm, text = 'Format ?').grid(column=5,row=0)
    label=ttk.Label(frm,text="Results").grid(column=3,row=0)
    button_data = ttk.Button(frm,text='Browse',command=path_plot).grid(column=4,row=1)
    value_plot = StringVar() 
    entry_plot = ttk.Entry(frm, width=30,textvariable=value_plot).grid(column=3,row=1)
    FormatMenu = ttk.Combobox(frm,values=FormatList)
    FormatMenu.current(0)
    FormatMenu.grid(column=5,row=1)

    #Launching the code
    Launch_button=ttk.Button(frm,text="OK", command=Launch).grid(column=0,row=3)
    


    Main_Window.mainloop()
