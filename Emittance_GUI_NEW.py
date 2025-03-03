# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 09:52:39 2024

@author: SBModre
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import Emittance_scanner
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import json
import ctypes

class EmittanceScanGUI:
    def __init__(self, root):
        """
        Initiates instances of the Emittance_scanner Motor and Variables Classes.
        Creates root, as well as all the frames and a few buttons. Calls the create_widgets method at the end.
        Additionally, a few variables are defined, like x/y_scans (Number of scans on x?y axis), running (Array that shows if a scan is currently happening and if so, on which axis) 
        and the variables_dict (A dictionary containing the variables from the Variables class as well as their names and labels)
        """
        self.root = root
        try:
            ctypes.windl.shcore.SetProcessDpiAwareness(1) #makes sure that rgardless of screensize, window takes same percentage of space
        except:
            pass
        self.root.title("Emittance Scan")
        #self.root.columnconfigure(0, weight=1)
        self.running = [False, None]
        self.x_scans = None
        self.y_scans = None
        self.Var = Emittance_scanner.Variables()
        self.Mot = Emittance_scanner.Motor()
        self.variables_dict = np.array([
            ["Extraction Voltage U [V]", "V_extr", self.Var.V_extr],
            ["Maximal x' [mrad]", "xp_max", self.Var.xp_max], 
            ["x' Step Size [mrad]", "xp_step", self.Var.xp_step],
            ["Minimal x' [mm]", "xp_min", self.Var.xp_min],
            ["Maximal y' [mrad]", "yp_max", self.Var.yp_max], 
            ["y' Step Size [mrad]", "yp_step", self.Var.yp_step],
            ["Minimal y' [mm]", "yp_min", self.Var.yp_min],
            ["Maximal x [mm]", "x_max", self.Var.x_max],
            ["x Step Size [mm]", "x_step", self.Var.x_step],
            ["Minimal x [mm]", "x_min", self.Var.x_min],
            ["Maximal y [mm]", "y_max", self.Var.y_max],
            ["y Step Size [mm]", "y_step", self.Var.y_step],
            ["Minimal y [mm]", "y_min", self.Var.y_min],
            ["Charge Number Q", "Q", self.Var.Q], 
            ["Mass Number M", "M", self.Var.M]
        ])
        
        self.style = ttk.Style() #style configurations for ttk widgets
        self.style.configure("TButton", font=("Helvetica", 10))
        self.style.configure("Green.TButton", background="lightgreen", foreground="black")
        self.style.configure("Grey.TButton", background = "lightgrey", foreground="black")
        self.style.configure("Custom.TMenubutton", background="lightgrey")
        
        icon = tk.PhotoImage(file="emittance_icon.png")
        self.root.iconphoto(False, icon, icon)
        
        # Create the main frames
        self.frame1 = ttk.Frame(self.root, borderwidth=1)
        self.frame1.grid(row=0, column=0,columnspan=2, sticky="ew", padx=5, pady=5)
        self.frame1.columnconfigure(3, weight=1)
        
        self.frame2 = ttk.Frame(self.root, relief="solid", borderwidth=1)
        self.frame2.grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        
        self.frame3 = ttk.Frame(self.root, relief="solid", borderwidth=1)
        self.frame3.grid(row=1, column=1, padx=5, pady=5)
        
        self.frame4 = ttk.Frame(self.root, relief="solid", borderwidth=1)
        self.frame4.grid(row=2, column=0,stick="w", padx=5, pady=5)
        
        self.frame41 = ttk.Frame(self.frame4, borderwidth=1) #frame41, i.e. frame in frame4
        self.frame41.grid(row=0, column=4, rowspan=2, padx=5, pady=5)
        
        self.frame5 = ttk.Frame(self.root, relief = "solid", borderwidth=1)
        self.frame5.grid(row=4, column=0, columnspan = 2, sticky="w", padx=5, pady=5)
        
        self.frame6 = ttk.Frame(self.root, relief = "solid", borderwidth =1)
        self.frame6.grid(row=2, column=1,sticky="w", padx=5, pady=5)
        
        self.frame7 = ttk.Frame(self.root, relief="solid", borderwidth=1)
        self.frame7.grid(row=3, column=1, padx=5, pady=5)
        
        self.frame8 = ttk.Frame(self.root, relief="solid", borderwidth=1)
        self.frame8.grid(row=3, column=0, padx=5, pady=5)
        
        self.frame9 = ttk.Frame(self.root, relief="flat", borderwidth=1)
        self.frame9.grid(row=4, column=1, padx=5, pady=5, sticky ='ens')
        self.frame9.rowconfigure(3, weight=1)
        
        endP_btn = tk.Button(self.frame9, text="End Program", command = self.end_program, bg="red", fg="white")
        endP_btn.grid(row=4, column=0, sticky="es", padx=5, pady=5)
        
        reset_btn = tk.Button(self.frame9, text="Reset Program", command = self.reset_program, bg="orange")
        reset_btn.grid(row=3, column=0, sticky ="es", padx=5, pady=5)
        
        load_data_btn = ttk.Button(self.frame9, text="Load Data", command = self.load_emittance)
        load_data_btn.grid(row=0, column = 0, sticky="en", padx=5, pady=5)
        # Initialize the GUI components
        self.create_widgets()
    
    def create_widgets(self):
        # Buttons for file operations
        existingfile_btn = ttk.Button(self.frame1, text="Open file", command=self.select_file) #loads a variables file
        existingfile_btn.grid(row=0, column=0)
        
        savefile_btn = ttk.Button(self.frame1, text="Save File", command=self.save)#saves the variables in a file
        savefile_btn.grid(row=0, column=1)
        
        showvar_btn = ttk.Button(self.frame1, text="Show Emittance Scan Variables", command=self.show_variables) #opens seperate window that shows variables and lets user change variables
        showvar_btn.grid(row=0, column=2)
        
        self.selected_label = ttk.Label(self.frame2, text="No beam line selected", font=("Helvetica", 10)) #shows which beam line was selected
        self.selected_label.grid(row=0, column=0, columnspan = 2, pady=10)
        
        for i, j in enumerate(["x", "y"]): #creates an option to set the number of scans per axis
            label = ttk.Label(self.frame2, text=f"Number of Scans on {j}-Axis:")
            label.grid(row=i+2, column=0, padx=5, pady=5)
            entry = tk.Entry(self.frame2)
            scans_name = f"{j}_scans"
            scans = getattr(self, scans_name)
            entry.insert(0, str(scans))
            entry.grid(row=i+2, column=1, padx=5, pady=5)    
            entry.bind("<Return>", lambda event, e=entry, vn=scans_name: self.set_scan_num(vn, e))
            set_btn = ttk.Button(self.frame2, text="Set", command=lambda e=entry, vn=scans_name: self.set_scan_num(vn, e))
            set_btn.grid(row=i+2, column=2, padx=5, pady=5)
        
        
        self.venus = ttk.Button(self.frame2, state="normal", text="VENUS", command = lambda: self.select_BeamLine(0)) #selects VENUS as active beam line. beam_line = 0
        self.venus.grid(row=1, column=0)
        
        self.aecr = ttk.Button(self.frame2, state="normal", text="AECR", command = lambda: self.select_BeamLine(1)) #selects aecr as active beam_line, beam_line = 1
        self.aecr.grid(row=1, column=1)
        
        emergency_stop = tk.Button(self.frame1, text="Kill All Motion", command = lambda: self.Mot.send_command("SET BIT8467 : SET BIT8499 : SET BIT8531 : SET BIT8563"), bg="red", fg="white") 
        emergency_stop.grid(row=0, column=3, sticky="e") #emergency stop ends all movement and sets a kill all motion request, that won't allow further motion
        
        clear_kill_all = tk.Button(self.frame1, text="Clear Kill All Motion", command = lambda: self.Mot.send_command("CLR BIT8467 : CLR BIT8499 : CLR BIT8531 : CLR BIT8563"), bg="green", fg="white")
        clear_kill_all.grid(row=1, column=3, sticky="e") #clears kill all motion request, i.e. after pressing, motion is possible again
        
        voltage_gain_label = ttk.Label(self.frame7, text = "Current to Voltage Gain [V/A]") #sets voltage gain (only in programm, not on the device (keithley 428))
        voltage_gain_label.grid(row=0, column=0, padx=5)
        allowed_values = [1e3, 1e4, 1e5, 1e6, 1e7,1e8, 1e9, 1e10, 1e11]
        self.gain_var = tk.StringVar(value=format(self.Mot.Voltagecurrentfactor, '.0e'))
        self.gain_dropdown = ttk.OptionMenu(self.frame7, self.gain_var, format(self.Mot.Voltagecurrentfactor, '.0e'), *[format(val, '.0e') for val in allowed_values], command=lambda value: self.set_gain_from_dropdown(value))
        self.gain_dropdown.grid(row=1, column=0, padx=5, pady=5)
        self.gain_dropdown.configure(style = "Custom.TMenubutton")
        
        #front shield gain curently has no use. May be of use later on. 
        front_shield_gain_label = ttk.Label(self.frame7, text = "Front Shield Gain [V/A]", font=('Helvetica', 9))
        front_shield_gain_label.grid(row=2, column=0, padx=5, pady=5)
        allowed_values = [1e3, 1e4, 1e5, 1e6, 1e7,1e8, 1e9, 1e10, 1e11]
        self.fs_gain_var = tk.StringVar(value=format(self.Mot.frontshield_gain, '.0e'))
        self.fs_gain_dropdown = ttk.OptionMenu(self.frame7, self.fs_gain_var, format(self.Mot.frontshield_gain, '.0e'), *[format(val, '.0e') for val in allowed_values], command=lambda value: self.set_frontshield_gain_from_dropdown(value))
        self.fs_gain_dropdown.grid(row=3, column=0, padx=5, pady=5)
        self.fs_gain_dropdown.configure(style = "Custom.TMenubutton")
        
        self.canvas = tk.Canvas(self.frame5, width=420, height=360, bg = "white") #empty canvas to create space for plots 
        self.canvas.grid(row=0, column=0, columnspan=5)
        
        tk.Label(self.frame5, text="Epsilon: None", font=("Helvetica", 10), bg="lightgrey").grid(row=1, column=0)
        tk.Label(self.frame5, text="Alpha: None", font=("Helvetica", 10), bg="lightgrey").grid(row=1, column=2, sticky="e")
        tk.Label(self.frame5, text="Beta: None", font=("Helvetica", 10), bg="lightgrey").grid(row=2, column=0)
        tk.Label(self.frame5, text="Gamma: None", font=("Helvetica", 10), bg="lightgrey").grid(row=2, column=2, sticky="e")
        
        self.create_LEDs()      
        self.create_axis_status()       
        self.create_run_buttons()
        self.create_center_retract_buttons()
        self.create_retraction_status()
        self.create_position_scale()
        
        
    def reset_program(self):
        """
        Resets most variables but keeps the Motor instance as is. That way, new scans can be made with new variables without restarting the program and without reinitiating the Motor class. 
        Saves time, to not have to define center position again.

        """
        if self.running[0]:
            self.Mot.send_command("SET BIT8467 : SET BIT8499 : SET BIT8531 : SET BIT8563")
            self.Mot.send_command("CLR BIT8467 : CLR BIT8499 : CLR BIT8531 : CLR BIT8563")
            self.Mot.move_out(self.running[1])
        self.Var = Emittance_scanner.Variables()
        self.Mot.beam_line = None
        self.x_scans = None
        self.y_scans = None
        self.venus.config(state="normal", style="TButton")
        self.aecr.config(state="normal", style="TButton")
        self.selected_label.config(text="No beam line selected", foreground="black")
        
    def create_position_scale(self):
        """
        Scales for x and y axis, that show location of Emittance Scanner. Initially, the scale goes from 0 to 200, but once the scanner is centered,
        the scale changes to go from -160 to 40, with 0 being the center of the beam. If a scan is currentyly happening, the scale is further reduced
        to only show positions between the minimum and maximum of the scan process.
        """
        self.scales = {}
        self.tick_canvases ={}
        self.scale_labels = {}
        self.scale_positions = {}
        for i in range(2):
            self.scales[i] = tk.Scale(self.frame8, from_= -200, to=0,sliderlength=30, orient="horizontal", length=294, resolution=0.001)
            self.scales[i].grid(row=0 +2*i, column=1, padx=5)
            self.scales[i].bind("<ButtonPress-1>", lambda event: "break")
            self.scales[i].bind("<B1-Motion>", lambda event: "break")  #scale should not be moveable by user
            self.scales[i].bind("<ButtonRelease-1>", lambda event: "break")
            self.tick_canvases[i] = tk.Canvas(self.frame8, width=294, height=20, bg='white')
            self.tick_canvases[i].grid(row=1+2*i, column=1, padx=5)
            self.draw_ticks(self.tick_canvases[i], self.scales[i], 20)
            self.scale_labels[i] = ttk.Label(self.frame8, text = f"{['X', 'Y'][i]}-Axis Position")
            self.scale_labels[i].grid(row=0 + 2*i, column=0, columnspan=1)
            self.scale_positions[i] = 0
            self.update_scale(i)
    
    def draw_ticks(self, canvas, scale, tick_interval):
        """
        This is the canvas that shows the positions under the scale widget.
        """
        canvas.delete("all")
        min_value = scale.cget("from")
        max_value = scale.cget("to")
        length = int(scale.cget("length"))
        slider_offset = int(scale.cget("sliderlength"))//2
        slider_min_x = slider_offset
        for value in range(int(min_value), int(max_value)+1, tick_interval):
            x = slider_min_x + (value-min_value)/(max_value-min_value)*(length-2*slider_offset) #+ (160-value)*0.01
            canvas.create_line(x, 0, x, 10, fill="black")
            canvas.create_text(x, 10, text=str(value), anchor="n", font=("Helvetica", 8))
        
    def update_scale(self, i):
        """
        This updates the scales, canvases and positions every 42ms ~ 24fps for a smooth motion.
        """
        if self.Mot.beam_line != None: #No need to update if no beam line has been selected
            axis = i + 2*self.Mot.beam_line
            self.scale_positions[i] = self.Mot.send_command(f"?P(12288 + {axis}*256")/self.Mot.factor #asking the controller for the current position and converting to mm
            self.scales[i].set(self.scale_positions[i])
            if self.Mot.centered[i+2*self.Mot.beam_line]:
                min_position = -40
                max_position = 160
                self.scales[i].config(from_= min_position, to = max_position)
                self.draw_ticks(self.tick_canvases[i], self.scales[i], 20)
            if self.running[0] and self.running[1]%2 == i:     
                max_position = [self.Var.x_max, self.Var.y_max][i]
                min_position = [self.Var.x_min, self.Var.y_min][i]
                self.scales[i].config(from_= min_position, to = max_position)
                self.draw_ticks(self.tick_canvases[i], self.scales[i], 4)
        self.root.after(42, lambda : self.update_scale(i))
        
    def set_gain_from_dropdown(self, value):
        try:
            gain_value = float(value)
            self.Mot.Voltagecurrentfactor = gain_value
        except ValueError:
            pass
        
    def set_frontshield_gain_from_dropdown(self, value):
        try:
            gain_value = float(value)
            self.Mot.frontshield_gain = gain_value
        except ValueError:
            pass 
    
    def load_emittance(self):
        """
        Opens an emittance scan data file and displays the results, i.e. the plot and the twiss parameters.

        """
        while True:
            file_path = filedialog.askopenfilename()
            try:
                if file_path:
                    self.display_results(axis=None, filepath =file_path)
                    break
                else:
                    break
            except Exception as e:
                print(f"Error opening file: {e}")
                continue
        
    def end_program(self): #stops all motion and moves all scanners out
        """
        Stops all motion, moves out the axes and ends the program.

        """
        self.Mot.send_command("SET BIT8467 : SET BIT8499 : SET BIT8531 : SET BIT8563")
        self.Mot.send_command("CLR BIT8467 : CLR BIT8499 : CLR BIT8531 : CLR BIT8563")
        if self.Mot.beam_line != None:
            self.Mot.move_out([0,2][self.Mot.beam_line])
            self.Mot.move_out([1,3][self.Mot.beam_line])
        else:
            for i in range(4):
                self.Mot.move_out(i)
        self.root.destroy()
        
    def create_retraction_status(self): #status lights to show if x and y are retracted or not
        """
        Status 'LEDs' that indicate wether an axis is cleared, i.e. at out Limit (green) or not (grey)
        """
        self.retraction_canvas = tk.Canvas(self.frame41, width = 118, height = 57, bg = "lightgrey") #canvas for 'LEDs'
        self.retraction_canvas.grid(row=1, column=0, padx=5, pady=0)
        axes = ["X retracted", "Y retracted"]
        self.retraction=[]
        for i in range(2): #axes x and y
            x = 12
            y = 12 + i*24
            signal = self.retraction_canvas.create_oval(x,y,x+12, y+12, fill="grey", outline="black")
            self.retraction.append(signal)
            self.retraction_canvas.create_text(x + 22, y + 6, text=f"{axes[i]}", anchor="w", font=("Helvetica", 10))
        self.update_retraction_status()
        
    def update_retraction_status(self): 
        """
        Updates retraction status 'LEDs' every second

        """
        if self.Mot.beam_line != None:
            axes= np.array([[0,1], [2,3]])
            for i in axes[self.Mot.beam_line]:
                retracted = self.Mot.send_command(f"?BIT(16129 + {i}*32)")  #negative EOT Limit current status (0=not encountered, -1 = encountered)
                if retracted:
                    color = "green3" #axis retracted
                else:
                    color = "grey"
        else:
            color = "grey"
        self.retraction_canvas.itemconfig(self.retraction[i], fill=color)
        self.root.after(1000, self.update_retraction_status)
        
    def create_center_retract_buttons(self):
        """
        Creates buttons for centering the x and y axis and retracting them. 
        Seperate retraction buttons would be unnecessary, since if for example x is centered and y is not retracted, than the program catches that and retracts y automatically.
        """
        self.center_x_btn = ttk.Button(self.frame6, text="Center X-Axis", state = "disabled", command = lambda: self.Mot.centering([0,2][self.Mot.beam_line]))
        self.center_x_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.center_y_btn = ttk.Button(self.frame6, text="Center Y-Axis", state = "disabled", command = lambda: self.Mot.centering([1,3][self.Mot.beam_line]))
        self.center_y_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.retract_both_btn = ttk.Button(self.frame6, text="Retract Both Axes", state = "normal", command = lambda: (self.Mot.move_out([0,2][self.Mot.beam_line]), self.Mot.move_out([1,3][self.Mot.beam_line])))
        self.retract_both_btn.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        self.update_center_retract_buttons()
        
    def update_center_retract_buttons(self):
        """
        Updates centering and retraction buttons, i.e. disables them if no beam line is selected.

        """
        if self.Mot.beam_line != None:
            #x = [0,2][self.Mot.beam_line]
            #x_clear = self.Mot.axis_clear(x) #boolean
            #x_state = ["disabled", "normal"][int(x_clear)] #don"t have to check if the axis is clear becasue this is done in the centering method anyways
            FC_state = ["disabled", "normal"][int(self.Mot.check_FC())]
            self.center_x_btn.config(state = FC_state)
            #y = [1,3][self.Mot.beam_line]
            #y_clear = self.Mot.axis_clear(y) #boolean
            #y_state = ["disabled", "normal"][int(y_clear)]          
            self.center_y_btn.config(state = FC_state)
            self.retract_both_btn.config(state="normal")
        else:
            self.center_x_btn.config(state = "disabled")
            self.center_y_btn.config(state = "disabled")
            self.retract_both_btn.config(state="disabled")
        self.root.after(1000, self.update_center_retract_buttons)
        
        
    def create_run_buttons(self):
        """
        Buttons that start the emittance scans
        """
        self.run_x_btn = ttk.Button(self.frame4, state="disabled", text="Run X Scans", command = lambda : self.run_scan([0,2][self.Mot.beam_line]))
        self.run_x_btn.grid(row=1, column=0,columnspan=2, padx=5, pady=5)
        
        self.run_y_btn = ttk.Button(self.frame4, state="disabled", text="Run Y Scans", command = lambda  : self.run_scan([1,3][self.Mot.beam_line]))
        self.run_y_btn.grid(row=1, column=2,columnspan=2, padx=5, pady=5)
        
        self.update_run_buttons()
        
    def update_run_buttons(self):
        """
        Updates run buttons depending if the beam line has been selected and variables are not None.

        """
        if self.Mot.beam_line != None and all(val is not None for val in [self.Var.Q, self.Var.M, self.Var.V_extr]):
            FC_state = ["disabled", "normal"][int(self.Mot.check_FC())]
            if self.x_scans != None:
                if all(val is not None for val in [self.Var.x_max, self.Var.x_min, self.Var.xp_max, self.Var.x_step, self.Var.xp_step]):
                    #x = [0,2][self.Mot.beam_line]
                    #x_clear = self.Mot.axis_clear(x) #boolean
                    #x_state = ["disabled", "normal"][int(x_clear)] #again, no need to check if axis is clear because if not, it will be cleared
                    self.run_x_btn.config(state = FC_state)
            else:
                self.run_x_btn.config(state="disabled")
            if self.y_scans != None:
                if all(val is not None for val in [self.Var.y_max, self.Var.y_min, self.Var.yp_max, self.Var.y_step, self.Var.yp_step]):
                    #y = [1,3][self.Mot.beam_line]
                    #y_clear = self.Mot.axis_clear(y) #boolean
                    #y_state = ["disabled", "normal"][int(y_clear)]          
                    self.run_y_btn.config(state = FC_state)
            else:
                self.run_y_btn.config(state="disabled")
        else:
            self.run_x_btn.config(state="disabled")
            self.run_y_btn.config(state="disabled")
        if self.running[0]:
            self.run_x_btn.config(state="disabled")
            self.run_y_btn.config(state="disabled")
        self.root.after(1000, self.update_run_buttons)
    
    def run_scan(self, axis):
        """
        Centers Axis, initiates a Read_and_Analyze object, and starts a number of scans (given by the user) on the selected axis.
        It then calls the display_results method and retracts the axis.
        """
        self.Mot.centering(axis)
        self.running = [True, axis]
        RnA = Emittance_scanner.Read_and_Analyze(self.Var, self.Mot)
        try: 
            scans = int([self.x_scans, self.y_scans][axis%2])
        except:
            return None
        self.scan_results = []
        for i in range(scans):
            I, filename = RnA.get_current(axis)
            E_rms, alpha, beta, gamma = RnA.emittance(axis, I)
            #RnA.phase_space_plot(filename, E_rms, alpha, beta)
            self.scan_results.append((filename, E_rms, alpha, beta, gamma))
        self.current_scan = 0
        self.display_results(axis)
        self.Mot.move_out(axis)
        self.running = [False, None]
        
    def display_results(self, axis=None, filepath=None):
        """
        Display Results from Current Scan or display results from a given data file.
        Every scan is displayed by a plot and through next and previous buttons, the user can witch to plots from other scans.
        """
        if filepath: #load an existing file to see the plot and data
            filename = filepath
            data = []
            with open(filename) as f:
                for i, line in enumerate(f):
                    if i%2 == 1:
                        try:
                            data.append(json.loads(line))
                        except:
                            data.append(line.strip())
            dic = data[0]
            for row, (var_label, var_name, var_value) in enumerate(self.variables_dict):
                setattr(self.Var, var_name, dic[var_label])
            axis = data[2]
            beam_line= data[1]
            RnA = Emittance_scanner.Read_and_Analyze(self.Var, self.Mot)
            beam_line = np.where(np.array(["VENUS", "AECR"])==beam_line)[0].item()
            axis = np.where(np.array(["X", "Y", "X", "Y"])==axis)[0][beam_line].item()
            E_rms, alpha, beta, gamma = float(data[7]), float(data[8]), float(data[9]), float(data[10])
        else:
            if not hasattr(self, 'scan_results') or not self.scan_results:
                return
            filename, E_rms, alpha, beta, gamma = self.scan_results[self.current_scan]
            RnA = Emittance_scanner.Read_and_Analyze(self.Var, self.Mot)
            
        self.canvas.delete("all")
        
        for widget in self.frame5.winfo_children():
            widget.destroy()
                
        self.canvas = tk.Canvas(self.frame5)
        self.canvas.grid(row=0, column=0, columnspan=5)

        fig, ax = plt.subplots(figsize=(4.2,3.6), dpi=100)
        #RnA = Emittance_scanner.Read_and_Analyze(self.Var, self.Mot)
        RnA.phase_space_plot(filename)
        
        fig.tight_layout
            
        plot_canvas = FigureCanvasTkAgg(fig, self.canvas)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(plot_canvas, self.canvas) #a toolbar that allows the user to zoom in on the plot and move around
        toolbar.update()
        plot_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        tk.Label(self.frame5, text=f"Epsilon: {E_rms*4*1e6:.4f} [mm mrad]", font=("Helvetica", 11), bg="lightgrey").grid(row=1, column=0)
        tk.Label(self.frame5, text=f"Alpha: {alpha:.4f}", font=("Helvetica", 11), bg="lightgrey").grid(row=1, column=1, sticky="e")
        tk.Label(self.frame5, text=f"Beta: {beta:.4f} [mm/mrad]", font=("Helvetica", 11), bg="lightgrey").grid(row=2, column=0)
        tk.Label(self.frame5, text=f"Gamma: {gamma:.4f} [mrad/mm]", font=("Helvetica", 11), bg="lightgrey").grid(row=2, column=1, sticky="e")
            
        ttk.Button(self.frame5, text="Previous", command = lambda: self.previous_scan(axis)).grid(row=2, column=0, sticky="w")
        ttk.Button(self.frame5, text="Next", command = lambda: self.next_scan(axis)).grid(row=2, column=3, sticky="e")
            
    def previous_scan(self, axis):
        """Navigate to previous Scan."""
        if self.current_scan > 0:
            self.current_scan -= 1
            self.display_results(axis) 
            
    def next_scan(self, axis):
        """Navigate to next scan"""
        if self.current_scan < len(self.scan_results) -1 :
            self.current_scan += 1 
            self.display_results(axis)
            
    
    def create_axis_status(self): 
        """
        Labels, that tell, wether the x or y axis are clear to move
        """
        self.x_status_label = ttk.Label(self.frame4, text = "X Axis: checking...", font=("Helvetica", 10))
        self.x_status_label.grid(row=0, column=0,columnspan=2, padx=5, pady=5)
        
        self.y_status_label = ttk.Label(self.frame4, text = "Y Axis: checking...", font=("helvetica", 10))
        self.y_status_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        self.update_axis_status()
        
    def update_axis_status(self): 
        """
        Updates Axis status labels every second, by calling the Motor.is_clear method. 
        """
        if self.Mot.beam_line != None:
            x = [0,2][self.Mot.beam_line]
            y = [1,3][self.Mot.beam_line]
            if self.Mot.axis_clear(x) and self.Mot.check_FC():
                self.x_status_label.config(text="X Axis: clear", foreground="green", font=("Helvetica", 10))
            else:
                self.x_status_label.config(text="X Axis: obstructed", foreground="red", font=("Helvetica", 10))
            if self.Mot.axis_clear(y) and self.Mot.check_FC():
                self.y_status_label.config(text="Y Axis: clear", foreground="green", font=("Helvetica", 10))
            else:
                self.y_status_label.config(text="Y Axis: obstructed", foreground="red", font=("Helvetica", 10))
        else:
            self.x_status_label.config(text = "Y Axis: checking...", font=("helvetica", 10), foregroun="black")
            self.y_status_label.config(text = "Y Axis: checking...", font=("helvetica", 10), foreground="black")
        self.root.after(1000, self.update_axis_status)
        
    
    def create_LEDs(self): 
        """
        Indicators that reflect the ACR74C controller's axis status LEDs. Each 'LED' can be grey, red or green.
        Grey: Drive off
        Red: Drive Faulted
        Green: Drive On, no fault
        """
        self.led_title = ttk.Label(self.frame3, text="Axis Status LEDs", font=("Helvetica", 10, "bold"))
        self.led_title.grid(row=0, column=0, padx=5, pady=5)
        self.led_canvas = tk.Canvas(self.frame3, width = 200, height = 105, bg = "lightgrey")
        self.led_canvas.grid(row=1, column=0, padx=5, pady=0)
        axes = ["X - VENUS", "Y - VENUS", "X - AECR", "Y - AECR"]
        self.leds=[]
        for i in range(4): # 4 axes
            x = 12
            y = 12 + i*24
            led = self.led_canvas.create_oval(x,y,x+12, y+12, fill="grey", outline="black")
            self.leds.append(led)
            self.led_canvas.create_text(x +22, y + 6, text=f"{axes[i]}", anchor="w", font=("Helvetica", 10))
        self.update_LEDs()
    
    def update_LEDs(self):
        for i in range(4):
            drive_status = self.Mot.send_command(f"?BIT(8465 + {i}*32)")
            fault_status = self.Motor.send_command(f"?BIT(8477 + {i}*32)")
            if bool(drive_status)and not bool(fault_status):
                color = "green3" #Drive on, no fault
            elif bool(fault_status):
                color = "red"
            else:
                color = "grey"
                
            self.led_canvas.itemconfig(self.leds[i], fill=color)
        self.root.after(1000, self.update_LEDs)
    
        
    def select_BeamLine(self, beam_line): #Buttons set beam_line either to 0 (Venus) or 1 (AECR)
        """
        Sets the Motor objects beam line variable to 0 if Button "Venus" was pressed and 1 if "AECR" was pressed.
        At the same time, both buttons are disabled after selecting a beam line.
        """
        
        self.Mot.beam_line = beam_line
        
        if self.Var.x_min != None:
            self.Var.x_min = max(self.Var.x_min, -self.Mot.mid_point_offsets[[0,2][beam_line]])
        if self.Var.y_max != None:
            self.Var.y_max = max(self.Var.y_min, -self.Mot.mid_point_offsets[[1,3][beam_line]])
            
        if beam_line:
            self.venus.config(state="disabled", style="Grey.TButton")
            self.aecr.config(state="disabled", style="Green.TButton")
            self.selected_label.config(text="Selected Beam Line: AECR", foreground="green")
        else:
            self.venus.config(state="disabled", style="Green.TButton")
            self.aecr.config(state="disabled", style="Grey.TButton")
            self.selected_label.config(text="Selected Beam Line: VENUS", foreground = "green")
        
    
    def select_file(self):
        """
        Opens explorer so user can select a Variables file to be loaded into the program.
        """
        while True:
            file_path = filedialog.askopenfilename()
            try:
                if file_path:
                    self.Var.open_and_read_file(file_path)
                    break
                else:
                    break
            except Exception as e:
                print(f"Error opening file: {e}")
                continue
            
    def set_scan_num(self, var_name, entry): #number of Scans
        """
        Sets numnber of scans if the value in entry box is an integer
        """
        value = entry.get()
        try:
            value = int(value)
            setattr(self, var_name, value)
            entry.config(bg="lightgreen")
        except ValueError:
            entry.config(bg="red")
    
    def set_variable(self, var_name, entry):
        """
        This sets the variables of the Variables class to a value entered in the textbox in the Variables window upon pressing the "Set" Button, while paying attention to a set of rules:
            x/y_min cannot be smaller than negative Midpoint offset (=Limit switch position)
            x'/y' max cannot be bigger than the maximal momentum i.e. plate Voltage at 200V for a given extraction Voltage (equivalent for x'/y'_min for -200V)
            Q, M must be integers
            steps can"t be bigger than the interval
        """
        value = entry.get()
        if var_name in ['Q', 'M']:
            try:
                value = int(value)
                setattr(self.Var, var_name, value)
                entry.config(bg="lightgreen")
            except ValueError:
                entry.config(bg="red")
        elif var_name in ["xp_max", "yp_max"]:
            try:
                value = float(value)
                try:
                    if self.Var.get_V(value*1e-3) > 200:
                        value = round(200/self.Var.d/self.Var.V_extr*self.Var.L/2*1e3,3) #if momentum too big, set to maximum
                        setattr(self.Var, var_name, value)
                        entry.delete(0, tk.END)
                        entry.insert(0, value)
                    else:
                        try:
                            value = float(value)
                            entry.config(bg="lightgreen")
                            setattr(self.Var, var_name, max(value, 0))
                            entry.delete(0, tk.END)
                            entry.insert(0, max(0, value))
                        except ValueError:
                            entry.config(bg="red")
                except TypeError:
                    messagebox.showinfo("Missing Data", "Set Extrction Voltage first")
            except ValueError:
                entry.config(bg="red")
        elif var_name in ["x_min", "y_min"]:
            if value == 'None' or value == '':
                value = -getattr(self.Var, self.variables_dict[np.where(self.variables_dict == var_name)[0]-2, [1]].item())
                setattr(self.Var, var_name, value)
                entry.delete(0, tk.END)
                entry.insert(0, value)
            else:
                try:
                    value = float(value)
                    if self.Mot.beam_line != None:
                        offset = self.Mot.mid_point_offsets[np.array([[0,2], [1,3]])[np.where(np.array(["x_min", "y_min"])==var_name)[0].item(), self.Mot.beam_line]]
                        value = min(0,max(value, -offset))
                        setattr(self.Var, var_name, value)
                        entry.delete(0, tk.END)
                        entry.insert(0, value)
                        entry.config(bg="lightgreen")
                    else:
                        value = min(0, value)
                        entry.config(bg="lightgreen")
                        setattr(self.Var, var_name, value)
                except ValueError:
                    entry.config(bg="red")
        elif var_name in ["x_max", "y_max"]:
            try:
                value = float(value)
                value = max(0,min(value, 50))
                setattr(self.Var, var_name, value)
                entry.delete(0, tk.END)
                entry.insert(0, value)
                entry.config(bg="lightgreen")
            except:
                entry.config(bg="red")
        elif var_name in ["xp_step", "yp_step", "x_step", "y_step"]:
            try:
                value = abs(float(value))
                if value > 2*getattr(self.Var, self.variables_dict[np.where(self.variables_dict == var_name)[0].item()-1][1]):
                    entry.config(bg="red")
                else:
                    try:
                        value = float(value)
                        entry.config(bg="lightgreen")
                        setattr(self.Var, var_name, value)
                        entry.delete(0, tk.END)
                        entry.insert(0, value)
                    except ValueError:
                        entry.config(bg="red")
            except ValueError:
                entry.config(bg="red")
        elif var_name in ["xp_min", "yp_min"]:
            if value == 'None' or value == '':
                value = -getattr(self.Var, self.variables_dict[np.where(self.variables_dict == var_name)[0]-2, [1]].item())
                setattr(self.Var, var_name, value)
                entry.delete(0, tk.END)
                entry.insert(0, value)
            else:
                try:
                    value= float(value)
                    try:
                        if self.Var.get_V(value*1e-3) < -200:
                            value = round(-200/self.Var.d/self.Var.V_extr*self.Var.L/2*1e3,3) #if momentum too big, set to maximum
                            setattr(self.Var, var_name, value)
                            entry.delete(0, tk.END)
                            entry.insert(0, value)
                            entry.config(bg="lightgreen")
                        else:
                            entry.config(bg="lightgreen")
                            setattr(self.Var, var_name, min(value, 0))
                            entry.delete(0, tk.END)
                            entry.insert(0, min(0, value))
                    except ValueError:
                        entry.config(bg="red")
                except TypeError:
                    entry.config(bg="red")
        elif var_name == "V_extr":
            try:
                value = max(float(value),0)
                entry.config(bg="lightgreen")
                setattr(self.Var, var_name, value)
                entry.delete(0, tk.END)
                entry.insert(0, value)
            except ValueError:
                entry.config(bg="red")
    
    def show_variables(self):#opens another window with all the variables 
        """
        Opens a window that displays the Variables Class variables and let's the user edit each variable and set it with a button (or pressing enter)
        """
        var_window = tk.Toplevel(self.root)
        var_window.title("Emittance Variables")
        
        self.variables_dict = np.array([
            ["Extraction Voltage U [V]", "V_extr", self.Var.V_extr],
            ["Maximal x' [mrad]", "xp_max", self.Var.xp_max], 
            ["x' Step Size [mrad]", "xp_step", self.Var.xp_step],
            ["Minimal x' [mm]", "xp_min", self.Var.xp_min],
            ["Maximal y' [mrad]", "yp_max", self.Var.yp_max], 
            ["y' Step Size [mrad]", "yp_step", self.Var.yp_step],
            ["Minimal y' [mm]", "yp_min", self.Var.yp_min],
            ["Maximal x [mm]", "x_max", self.Var.x_max],
            ["x Step Size [mm]", "x_step", self.Var.x_step],
            ["Minimal x [mm]", "x_min", self.Var.x_min],
            ["Maximal y [mm]", "y_max", self.Var.y_max],
            ["y Step Size [mm]", "y_step", self.Var.y_step],
            ["Minimal y [mm]", "y_min", self.Var.y_min],
            ["Charge Number Q", "Q", self.Var.Q], 
            ["Mass Number M", "M", self.Var.M]
        ])
        
        for row, (var_label, var_name, var_value) in enumerate(self.variables_dict):
            label = ttk.Label(var_window, text=var_label)
            label.grid(row=row, column=0, padx=5, pady=5)
            
            entry = tk.Entry(var_window)
            entry.insert(0, str(var_value))
            entry.grid(row=row, column=1, padx=5, pady=5)
            
            entry.bind("<Return>", lambda event, e=entry, vn=var_name: self.set_variable(vn, e))
            
            set_btn = ttk.Button(var_window, text="Set", command=lambda e=entry, vn=var_name: self.set_variable(vn, e))
            set_btn.grid(row=row, column=2, padx=5, pady=5)
    
    def save(self): #saves the variables as a dictionary in a txt file
        filename = self.Var.write_and_save_file()
        messagebox.showinfo("Saved successfully", f"File was saved as {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmittanceScanGUI(root)
    root.mainloop()
