# Mandy Abernathy
# GUI

import tkinter
from tkinter import ttk # themed widgets
from tkinter import scrolledtext

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

import model
import plotter

class App(ttk.Frame):
    """
    Class for Biofilm Gui
    """
    def __init__ (self, master):
        super().__init__(master)
        self.master = master

        self.growth_rates = {
            'P. aeruginosa' : 0.957,
            'L. plantarum' : 0.612,
            'S. aereus' : 0.386
        }

        self.data = {
            'P. aeruginosa' : [
                [0, 1, 2, 3, 4, 5, 6, 7],
                [0.002, 0.019, 0.024, 0.068, 0.085, 0.355, 0.979, 1.496]
            ],
            'L. plantarum' : [
                [0, 1, 2, 3, 4, 5, 6, 7],
                [0.001, 0.015, 0.02, 0.05, 0.07, 0.15, 0.6, 0.95]
            ],
            'S. aereus' : [
                [0, 1, 2, 3, 4, 5, 6, 7],
                [0.002, 0.007, 0.015, 0.025, 0.056, 0.09, 0.14, 0.345]
            ]
            
        }
        
        button_style = ttk.Style()
        button_style.configure('my.TButton', font=('Helvetica', 12))
        label_style = ttk.Style()
        label_style.configure('my.TLabel', font=('Helvetica', 12))
            
        self.create_tabs()
        self.create_tab1()
        self.create_tab2()
        self.create_tab3()


    def create_tabs(self):
        """Creates tabs for biofilm model, bacteria growth plot, and data entry"""
        tabControl = ttk.Notebook(root)

        self.tab1 = ttk.Frame(tabControl) # biofilm graph
        self.tab2 = ttk.Frame(tabControl) # bacteria plot
        self.tab3 = ttk.Frame(tabControl) # input data


        tabControl.add(self.tab1, text='Biofilm Model')
        tabControl.add(self.tab2, text='Bacteria Growth')
        tabControl.add(self.tab3, text='Data Input')
        tabControl.pack(expand = 1, fill ="both")

    def create_tab1(self):
        """Creates tab for the biofilm model."""
        # current parameters for biofilm model
        self.selected_bacteria = tkinter.StringVar(self)
        self.selected_initialstate = tkinter.StringVar(self, '0.002')
        self.selected_maxvalue = tkinter.StringVar(self, '1.75')
        self.antibiotic_MIC = tkinter.StringVar(self, '0')
        self.antibiotic_conc = tkinter.StringVar(self, '0')

        # create frames
        self.top_frame = ttk.Frame(self.tab1)
        self.top_frame.grid(row=0, column=0)
        self.middle_frame = ttk.Frame(self.tab1)
        self.middle_frame.grid(row=1, column=0)
        self.bottom_frame = ttk.Frame(self.tab1)
        self.bottom_frame.grid(row=2, column=0)
            
        # create widgets

            # frame title
        lbl_title1 = ttk.Label(self.top_frame, text="Bacterial Biofilm Growth", style='my.TLabel')
        lbl_title1.grid(row=0, column=0, padx=0, pady=20)

        #lbl_bacteria = ttk.Label(self.bottom_frame, width=10, text='Bacteria:')
        #lbl_bacteria.grid(row=5, column=0, padx=40, pady=10, sticky=tkinter.W)

            # bacteria selection menu
        bacteria_options = list(self.growth_rates.keys())
        self.selected_bacteria.set('P. aeruginosa') # set default to Pseudomonas
        self.menu_bacteria = ttk.OptionMenu(self.middle_frame, self.selected_bacteria, bacteria_options[0], *bacteria_options, command=self.plot_biofilm)
        self.menu_bacteria.grid(row=5, column=0, padx=40, pady=10, sticky=tkinter.W)

            # initial state text box
        lbl_initialstate = ttk.Label(self.bottom_frame, width=20, text="Initial Value: (OD)")
        lbl_initialstate.grid(row=6, column=0, padx=40, pady=0, sticky=tkinter.W)
        ent_initialstate = ttk.Entry(self.bottom_frame, width=20, textvariable=self.selected_initialstate)
        ent_initialstate.grid(row=7, column=0, columnspan=1, padx=40, pady=5, sticky=tkinter.W)
        ent_initialstate.bind('<Return>', self.plot_biofilm)

            # maximum biofilm text box
        lbl_maxvalue = ttk.Label(self.bottom_frame,  width=20, text="Maximum value: (OD)")
        lbl_maxvalue.grid(row=10, column=0, padx=40, pady=0, sticky=tkinter.W)
        ent_maxvalue = ttk.Entry(self.bottom_frame,  width=20, textvariable=self.selected_maxvalue)
        ent_maxvalue.grid(row=11, column=0, padx=40, pady=5, sticky=tkinter.W)
        ent_maxvalue.bind('<Return>', self.plot_biofilm)

            # antibiotic MIC text box
        lbl_antibiotic_MIC = ttk.Label(self.bottom_frame, width=28, text="Antibiotic MIC: (µg/ml)")
        lbl_antibiotic_MIC.grid(row=6, column=3, columnspan=1, padx=0, pady=0, sticky=tkinter.W)
        ent_MIC = ttk.Entry(self.bottom_frame, width=20, textvariable=self.antibiotic_MIC)
        ent_MIC.grid(row=7, column=3, columnspan=1, padx=0, pady=5, sticky=tkinter.W)
        ent_MIC.bind('<Return>', self.plot_biofilm)

            # antibiotic concentration text box
        lbl_concentration = ttk.Label(self.bottom_frame, width=28, text="Antibiotic conc: (µg/ml)")
        lbl_concentration.grid(row=10, column=3, columnspan=1, padx=0, pady=0, sticky=tkinter.W)
        ent_concentration = ttk.Entry(self.bottom_frame, width=20, textvariable=self.antibiotic_conc)
        ent_concentration.grid(row=11, column=3, columnspan=1, padx=0, pady=5, sticky=tkinter.W)
        ent_concentration.bind('<Return>', self.plot_biofilm)

            # quit button
        btn_quit = ttk.Button(self.bottom_frame, text="Quit", style='my.TButton', command=root.destroy)
        btn_quit.grid(row=11, column=4, padx=40, pady=5, sticky=tkinter.E)
       
        # create plot
        self.plot_biofilm()

    def create_tab2(self):
        """Creates tab for planktonic bacteria growth plot."""

        # current parameters
        self.plotted_bacteria = tkinter.StringVar(self, 'P. aeruginosa')

        # create frames
        self.tab2_top_frame = ttk.Frame(self.tab2)
        self.tab2_top_frame.grid(row=0, column=0)
        self.tab2_bottom_frame = ttk.Frame(self.tab2)
        self.tab2_bottom_frame.grid(row=1, column=0)

        # create widgets

            # frame title
        lbl_title2 = ttk.Label(self.tab2_top_frame, text="Planktonic Bacteria Growth", style='my.TLabel')
        lbl_title2.grid(row=0, column=50, padx=0, pady=20)
    
            # panktonic bacteria menu
        bacteria_options = list(self.growth_rates.keys())
        self.menu_pltbacteria = ttk.OptionMenu(self.tab2_bottom_frame, self.plotted_bacteria, bacteria_options[0], *bacteria_options, command=self.plot_bacteria)
        self.menu_pltbacteria.grid(row=3, column=0, padx=40, pady=10, sticky=tkinter.W)

        # create plot
        self.plot_bacteria()

    def create_tab3(self):
        """Creates tab for entering data for a new bacteria."""
        
        # current values
        self.new_bacteria = tkinter.StringVar(self)
        self.start_time = tkinter.StringVar(self, '0')
        self.end_time = tkinter.StringVar(self, '8')
        self.input_data = tkinter.StringVar(self)
            
        # create frames
        self.tab3_frame = ttk.Frame(self.tab3)
        self.tab3_frame.grid(row=5, column=0)

        # create widgets

            # frame title
        lbl_title3 = ttk.Label(self.tab3_frame, text="Data Input for Bacteria Growth", style='my.TLabel')
        lbl_title3.grid(row=0, column=0, columnspan=2, padx=40, pady=20)

            # new bacteria information
        lbl_newbacteria = ttk.Label(self.tab3_frame, text="New bacteria:") #, style='my.TLabel')
        lbl_newbacteria.grid(row=1, column=0, padx=40, pady=0, sticky=tkinter.W)
            # bacteria name
        ent_newbacteria = ttk.Entry(self.tab3_frame, textvariable=self.new_bacteria)
        ent_newbacteria.grid(row=2, column=0, padx=40, pady=5, sticky=tkinter.W)
            # start time (hours)
        lbl_starttime = ttk.Label(self.tab3_frame, text="Start time: (hour)")
        lbl_starttime.grid(row=3, column=0, padx=40, pady=0, sticky=tkinter.W)
        self.ent_starttime = ttk.Entry(self.tab3_frame, textvariable=self.start_time)
        self.ent_starttime.grid(row=4, column=0, padx=40, pady=5, sticky=tkinter.W)
            # end time
        lbl_endtime = ttk.Label(self.tab3_frame, text="End time: (hour)")
        lbl_endtime.grid(row=5, column=0, padx=40, pady=0, sticky=tkinter.W)
        self.ent_endtime = ttk.Entry(self.tab3_frame, textvariable=self.end_time)
        self.ent_endtime.grid(row=6, column=0, padx=40, pady=5, sticky=tkinter.W)
            #data points
        lbl_data = ttk.Label(self.tab3_frame, text="Data:")
        lbl_data.grid(row=1, column=2, padx=40, pady=0, sticky=tkinter.W)
        self.ent_data = scrolledtext.ScrolledText(self.tab3_frame, height=6, width=24, wrap=tkinter.WORD)
        self.ent_data.grid(row=2, rowspan=4, column=2, padx=40, pady=10, sticky=tkinter.E)

            # add bacteria button
        btn_addbacteria = ttk.Button(self.tab3_frame, text="Add Bacteria", style='my.TButton', command=self.add_bacteria)
        btn_addbacteria.grid(row=8, column=2, padx=40, pady=5, sticky=tkinter.E)

            # help button for data entry syntax
        self.button_showinfo = ttk.Button(self.tab3_frame, text="Help", command=self.popup_showinfo)
        self.button_showinfo.grid(row=6, column=2, padx=40, pady=5, sticky=tkinter.E)        

            # secret
        self.button_bonus = ttk.Button(self.tab3_frame, text="Bonus", command=self.popup_bonus)
        self.button_bonus.grid(row=50, column=2, padx=40, pady=(310, 0), sticky=tkinter.E)

    def plot_biofilm(self, *args):
        """
        Plots biofilm growth using a Model object.
        Called when any entry box on tab 1 is updated.
        """
        # get parameters, convert to floats
        try:
            bacteria = self.selected_bacteria.get()
            growth_rate = self.growth_rates[bacteria]
            init_conditions = float(self.selected_initialstate.get())
            max_value = float(self.selected_maxvalue.get())
            MIC = float(self.antibiotic_MIC.get())
            conc = float(self.antibiotic_conc.get())
        except ValueError:
            tkinter.messagebox.showerror("Input Error", "Please enter digits.")
            return

        # create figure
        m = model.Model(growth_rate, init_conditions, max_value, MIC, conc)
        fig = m.figure()

        # embed in frame
        canvas = FigureCanvasTkAgg(fig, master=self.middle_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=40)

    def plot_bacteria(self, *args):
        """
        Plots bacteria growth using a Plotter object.
        Called when the selected bacteria on tab 2 is changed.
        """
        # get values to plot
        bacteria = self.plotted_bacteria.get()
        t_span = self.data[bacteria][0]
        y_data = self.data[bacteria][1]

        # create figure
        p = plotter.Plotter(t_span, y_data)
        fig = p.figure()

        # embed in frame
        canvas = FigureCanvasTkAgg(fig, master=self.tab2_bottom_frame) 
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=40, pady=0)


    def add_bacteria(self):
        """
        Takes bacteria, time points, and data entry from tab3, adds it to bacteria
        data to the App class, and updates the options in the menus on tabs 1 and 2.
        """
        # get entered data
        bacteria = self.new_bacteria.get()
        if bacteria == '':
            tkinter.messagebox.showwarning("Warning", "Please enter bacteria name." )
            return

        input_data = self.ent_data.get('1.0', tkinter.END)
        
        # add data and constants to data dictionaries
        self.add_data(bacteria, input_data)

        # update menus on tabs 1 and 2
        new_options = list(self.data.keys())
        self.menu_pltbacteria.set_menu(new_options[0], *new_options)
        self.menu_bacteria.set_menu(new_options[0], *new_options)

    def add_data(self, bacteria, input):
        """
        Creates lists of data entered in tab 3 and adds data to the dictionaries
        saved in the App class.
        """
        # create list of time points from start and end time entries
        try:
            t_0 = int(self.ent_starttime.get())
            t_n = int(self.ent_endtime.get())
            t_points = list(np.linspace(t_0, t_n, t_n+1))
        except ValueError:
            tkinter.messagebox.showerror("Input Error", "Please enter digits for start and end times.")

        # parse text from data text box
        try:
            y_data = []
            for val in input.split():
                y_data.append(float(val.strip(',')))
        except ValueError:
            tkinter.messagebox.showerror("Data Error", "Syntax error in data input.")
            return

        # save data to dictionary
        data = [t_points, y_data]
        self.data[bacteria] = data

        # add growth rate to dictionary
        try:
            p = plotter.Plotter(t_points, y_data)
            new_rate = p.fit()
        except ValueError:
            tkinter.messagebox.showerror("Data Error", "Not enough entries in data input.")
            return

        self.growth_rates[bacteria] = new_rate

    def popup_showinfo(self):
        """Displays help informations for data entry text box."""
        help_text = (
            "Please enter OD measurements of bacteria growth taken at "
            "equally spaced intervals. Enter data points in the text box, "
            "either one value per line, as a space-separated list, or as "
            "a comma-separated list."
        )
        tkinter.messagebox.showinfo("Data information", help_text)

    def popup_bonus(self):
        """Christian made me do it."""
        win = tkinter.Toplevel()
        win.wm_title("Bonus")

        l = tkinter.Label(win, text="(つ -‘ _ ‘- )つ")
        l.grid(row=0, column=0)
        b = ttk.Button(win, text="Okay", command=win.destroy)
        b.grid(row=1, column=0)

    #####################################

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Bacterial Biofilms")
    app = App(root)
    app.mainloop()
    

    