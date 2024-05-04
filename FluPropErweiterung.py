# -*- coding: utf-8 -*-

# Import Packages
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import BooleanVar
from tkinter import LabelFrame
from CoolProp import CoolProp
from CoolProp.Plots import PropertyPlot, StateContainer
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import MouseButton
import matplotlib.pylab as plt

# Create Window
window = tk.Tk()
window.title("FluProp 2")
window.geometry("1280x700")
window.resizable(False, False)
window.columnconfigure(0, minsize=100)
window.columnconfigure(1, minsize=100)
window.columnconfigure(2, minsize=75)
window.columnconfigure(3, minsize=150)

# Open window on top
window.attributes('-topmost', True)
window.update()
window.attributes('-topmost', False)

## Variables
#Edit Isolines
isobar_var = BooleanVar()
isotherm_var = BooleanVar()
isochor_var = BooleanVar()
isentropic_var = BooleanVar()
isenthalpic_var = BooleanVar()
isovapore_var = BooleanVar()

# Set initial state for checkboxes
isobar_var.set = False
isotherm_var.set = False
isochor_var.set = False
isentropic_var.set = False
isenthalpic_var.set = False
isovapore_var.set = False

# Set number of Isolines
isobar_num = float()
isotherm_num = float()
isochor_num = float()
isentropic_num = float()
isenthalpic_num = float()
isovapore_num = float()

# Additional states
point1 = BooleanVar()
point2 = BooleanVar()
point3 = BooleanVar()

# Punkt 1 wird als default gesetzt
point1.set(True)
point2.set(False)
point3.set(False)


## Place LabelFrames
#LabelFrames dienen als Master der einzelnen Widgets

# Values Frame
values_frame = ttk.LabelFrame(window, text="Berechnete Fluidwerte", width=71, relief="flat")
values_frame.grid(row=1, column=0, columnspan=3, padx=10, sticky="NW")

# Infos Frame
infos_frame = ttk.LabelFrame(window)
infos_frame.grid(row=0, column=3, columnspan=4, padx=25, sticky="NW")

# Input Frame
input_frame = ttk.LabelFrame(window)
input_frame.grid(row=0, column=0, columnspan=3, rowspan=2, padx=10, sticky="NW")

# Diagram Frame
diagram_frame = ttk.LabelFrame(window)
diagram_frame.grid(row=0, column=7, columnspan=5, padx=25, sticky="NW")

# Toolbar Frame
toolbar_frame = ttk.LabelFrame(window, borderwidth=0, relief="flat")
toolbar_frame.grid(row=1, column=7, padx=25, sticky="NW")

# Combobox Frame
frame = LabelFrame(window, text="Isolinien Ein-/Ausblenden")
frame.grid(row=1, column=7, columnspan=5, padx=25, sticky="W")

# Create Label (Textfelder oben links)
fluid_label = ttk.Label(input_frame, text="Fluid-Auswahl:", font="bold")
fluid_label.grid(row=0, column=0, pady=5, sticky="E")

# Edit isolines at Checkbox Change
# Ruft nur diagram() auf. War für Testzwecke sinnvoll
def on_select_check():
    diagram(selected_diagram.get())

# Checkboxes Isolines
isobar_check = ttk.Checkbutton(frame, text="Isobare", variable=isobar_var, onvalue=True, offvalue=False, command=on_select_check)
isotherm_check = ttk.Checkbutton(frame, text="Isotherme", variable=isotherm_var, onvalue=True, offvalue=False,  command=on_select_check)
isochor_check = ttk.Checkbutton(frame, text="Isochore", variable=isochor_var, onvalue=True, offvalue=False,  command=on_select_check)
isentropic_check = ttk.Checkbutton(frame, text="Isentrope", variable=isentropic_var, onvalue=True, offvalue=False,  command=on_select_check)
isenthalpic_check = ttk.Checkbutton(frame, text="Isenthalpe", variable=isenthalpic_var, onvalue=True, offvalue=False,  command=on_select_check)
isovapore_check = ttk.Checkbutton(frame, text="Isovapore", variable=isovapore_var, onvalue=True, offvalue=False, command=on_select_check)

# Erstelle die Eingabefelder
isobar_entry = ttk.Entry(frame, textvariable=isobar_num, width=5)
isotherm_entry = ttk.Entry(frame, textvariable=isobar_num, width=5)
isochor_entry = ttk.Entry(frame, textvariable=isochor_num, width=5)
isentropic_entry = ttk.Entry(frame, textvariable=isobar_num, width=5)
isenthalpic_entry = ttk.Entry(frame, textvariable=isobar_num, width=5)
isovapore_entry = ttk.Entry(frame, textvariable=isovapore_num, width=5)

## Erstellt drei Buttons für die Auswahl der Zustandspunkte
# Stand jetzt wird hier nur die zugehoerige Variable aktiviert
# es fehlt der Befehl, damit berechnete Fluidwerte für den aktivierten Punkt angezeigt werden   

# Point 1
input1_label = ttk.Label(input_frame, text="Input-Variable 1:")
input1_label.grid(row=1, column=0, sticky="E") 

input2_label = ttk.Label(input_frame, text="Input-Variable 2:")
input2_label.grid(row=2, column=0, pady=5, sticky="E")

def on_button1():
    try: 
        point1.set(True)
        point2.set(False)
        point3.set(False)
        calc()
    except Exception as e:
        print("Error while plotting points:", e)

# Choose which Point to change in diagram
point1_button = ttk.Button(input_frame, text="1", width=2, command=on_button1)
point1_button.grid(row=1, rowspan=2, column=0, pady=5, padx=10, sticky="W")


# Point 2
input3_label = ttk.Label(input_frame, text="Input-Variable 1:")
input3_label.grid(row=4, column=0, sticky="E") 

input4_label = ttk.Label(input_frame, text="Input-Variable 2:")
input4_label.grid(row=5, column=0, pady=5, sticky="E")

def on_button2():
    try: 
        point1.set(False)
        point2.set(True)
        point3.set(False)
        calc()
    except Exception as e:
        print("Error while plotting points:", e)
    
    
# Choose which Point to change in diagram
point2_button = ttk.Button(input_frame, text="2", width=2, command=on_button2)
point2_button.grid(row=4, rowspan=2, column=0, pady=5, padx=10, sticky="W")

# Point 3
input5_label = ttk.Label(input_frame, text="Input-Variable 1:")
input5_label.grid(row=7, column=0, sticky="E") 

input6_label = ttk.Label(input_frame, text="Input-Variable 2:")
input6_label.grid(row=8, column=0, pady=5, sticky="E")

def on_button3():
    try: 
        point1.set(False)
        point2.set(False)
        point3.set(True)
        point3_button.config(bg="red")
        calc()
    except Exception as e:
        print("Error while plotting points:", e)
    

# Choose which Point to change in diagram
point3_button = ttk.Button(input_frame, text="3", width=2, command=on_button3)
point3_button.grid(row=7, rowspan=2, column=0, padx=10, sticky="W")


# Platzhalter
empty_label = ttk.Label(input_frame, text=" ")
empty_label2 = ttk.Label(input_frame, text=" ")
empty_label.grid(row=3, column=0)
empty_label2.grid(row=6, column=0)


# Fluid Info Label (Textfelder mitte)
fluidinfo_label = ttk.Label(infos_frame, text="Fluidinformationen:", font="bold")
fluidinfo_label.grid(row=0, column=4, columnspan=2, sticky="W")

pure_info_label = ttk.Label(infos_frame)
pure_info_label.grid(row=1, column=4, columnspan=2, sticky="W")
molarmass_info_label = ttk.Label(infos_frame)
molarmass_info_label.grid(row=2, column=4, columnspan=2, sticky="W")
gasconstant_info_label = ttk.Label(infos_frame)
gasconstant_info_label.grid(row=3, column=4, columnspan=2, sticky="W")

# Critical Point Label
ctp_label = ttk.Label(infos_frame, text="Kritischer Punkt:", font="bold")
ctp_label.grid(row=4, column=4, sticky="E")
ctp_pressure_label = ttk.Label(infos_frame)
ctp_pressure_label.grid(row=4, column=5, columnspan=1, sticky="W")
ctp_temp_label = ttk.Label(infos_frame)
ctp_temp_label.grid(row=5, column=5, sticky="W")
ctp_den_label = ttk.Label(infos_frame)
ctp_den_label.grid(row=6, column=5, sticky="W")

# Triple Point Label
tp_label = ttk.Label(infos_frame, text="Tripelpunkt:", font="bold")
tp_label.grid(row=7, column=4, sticky="E")
tp_pressure_label = ttk.Label(infos_frame)
tp_pressure_label.grid(row=7, column=5, sticky="W")
tp_temp_label = ttk.Label(infos_frame)
tp_temp_label.grid(row=8, column=5, sticky="W")

# Fluidlimits Label
limit_label = ttk.Label(infos_frame, text="Fluidgrenzen:", font="bold")
limit_label.grid(row=9, column=4, sticky="E")
maxtemp_label = ttk.Label(infos_frame)
maxtemp_label.grid(row=9, column=5, sticky="W")
mfloatemp_label = ttk.Label(infos_frame)
mfloatemp_label.grid(row=10, column=5, sticky="W")
maxp_label = ttk.Label(infos_frame)
maxp_label.grid(row=11, column=5, sticky="W")
minp_label = ttk.Label(infos_frame)
minp_label.grid(row=12, column=5, sticky="W")


# Define Calculated Prop Label
# Zugehoerige Werte werden erst spaeter gesetzt

calc_temp_label = ttk.Label(values_frame)
calc_p_label = ttk.Label(values_frame)
calc_vq_label = ttk.Label(values_frame)
calc_sound_label = ttk.Label(values_frame)
calc_d_label = ttk.Label(values_frame)
calc_h_label = ttk.Label(values_frame)
calc_s_label = ttk.Label(values_frame)
calc_u_label = ttk.Label(values_frame)
calc_v_label = ttk.Label(values_frame)
calc_st_label = ttk.Label(values_frame)
calc_cp_label = ttk.Label(values_frame)
calc_cv_label = ttk.Label(values_frame)

# Pack Calculated Prop Label
calc_temp_label.pack(anchor="w")
calc_p_label.pack(anchor="w")
calc_vq_label.pack(anchor="w")
calc_sound_label.pack(anchor="w")
calc_d_label.pack(anchor="w")
calc_h_label.pack(anchor="w")
calc_s_label.pack(anchor="w")
calc_u_label.pack(anchor="w")
calc_v_label.pack(anchor="w")
calc_st_label.pack(anchor="w")
calc_cp_label.pack(anchor="w")
calc_cv_label.pack(anchor="w")

# Fluid Combobox (Auswahl des Stoffes. Default ist Wasser)
selected_fluid = tk.StringVar()
cp_fluids = CoolProp.FluidsList()
fluid_combobox = ttk.Combobox(input_frame, width=50, textvariable=selected_fluid, values=cp_fluids, state="readonly")
fluid_combobox.grid(row=0, column=1, columnspan=2, sticky="W")
fluid_combobox.set("Water")

# Variables (Mögliche Eingangsvariabeln)
variables = ["Dichte ρ", "Druck p", "Temperatur T", "Spezifische Enthalpie h", "Spezifische Entropie s",
             "Dampfqualität x"]

state = StateContainer() 
# Draw first state point (very far outside)
state[0, "T"] = -10e100
state[0, "S"] = -10e100
state[0, "P"] = -10e100
state[0, "H"] = -10e100
state[0, "D"] = -10e100

diagrams = ["T-s-Diagramm", "p-h-Diagramm", "h-s-Diagramm", "p-s-Diagram", "p-T-Diagramm", "T-ρ-Diagramm"]
diagram_get = []

# Diagramm Combobox (Auswahl Diagramm)
selected_diagram = tk.StringVar()
diagram_combobox = ttk.Combobox(diagram_frame, width=
40, textvariable=selected_diagram, values=diagrams, state="readonly")
diagram_combobox.grid(row=0, column=0, padx=15, sticky="NW")
diagram_combobox.set("T-s-Diagramm")




# Input1 (Textfeld zu Variable 1)
def on_select_inpu1(event):
    selected_input1 = event.widget.get()
    if selected_input1 == "Dichte ρ":
        input1unit_label["text"] = "kg/m^3"
    elif selected_input1 == "Druck p":
        input1unit_label["text"] = "Pa"
    elif selected_input1 == "Temperatur T":
        input1unit_label["text"] = "K"
    elif selected_input1 == "Spezifische Enthalpie h":
        input1unit_label["text"] = "J/kg"
    elif selected_input1 == "Spezifische Entropie s":
        input1unit_label["text"] = "J/(kg·K)"
    elif selected_input1 == "Dampfqualität x":
        input1unit_label["text"] = "kg/kg)"


# Input1 Combobox (Auswahlbox Variable 1, per Default auf Druck)
selected_variable1 = tk.StringVar()
input1_combobox = ttk.Combobox(input_frame, width=29, textvariable=selected_variable1, values=variables, state="readonly")
input1_combobox.grid(row=1, column=1, sticky="W")
input1_combobox.set("Druck p")
input1_combobox.bind("<<ComboboxSelected>>", on_select_inpu1)

# Label Input1 Unit
input1unit_label = ttk.Label(input_frame, text="Pa")
input1unit_label.grid(row=1, column=3, sticky="W")

# Entry Input1
input1_var = tk.StringVar()
input1_entry = ttk.Entry(input_frame, textvariable=input1_var)
input1_entry.grid(row=1, column=2)


# Input2
def on_select_inpu2(event):
    selected_input2 = event.widget.get()
    if selected_input2 == "Dichte ρ":
        input2unit_label["text"] = "kg/m^3"
    elif selected_input2 == "Druck p":
        input2unit_label["text"] = "Pa"
    elif selected_input2 == "Temperatur T":
        input2unit_label["text"] = "K"
    elif selected_input2 == "Spezifische Enthalpie h":
        input2unit_label["text"] = "J/kg"
    elif selected_input2 == "Spezifische Entropie s":
        input2unit_label["text"] = "J/(kg·K)"
    elif selected_input2 == "Dampfqualität x":
        input2unit_label["text"] = "kg/kg)"


# Input2 Combobox
selected_variable2 = tk.StringVar()
input2_combobox = ttk.Combobox(input_frame, width=29, textvariable=selected_variable2, values=variables, state="readonly")
input2_combobox.grid(row=2, column=1, sticky="W")
input2_combobox.set("Temperatur T")
input2_combobox.bind("<<ComboboxSelected>>", on_select_inpu2)

# Label Input2 Unit
input2unit_label = ttk.Label(input_frame, text="K")
input2unit_label.grid(row=2, column=3, sticky="W")

# Entry Input2
input2_var = tk.StringVar()
input2_entry = ttk.Entry(input_frame, textvariable=input2_var)
input2_entry.grid(row=2, column=2)


# Input3
def on_select_inpu3(event):
    selected_input3 = event.widget.get()
    if selected_input3 == "Dichte ρ":
        input3unit_label["text"] = "kg/m^3"
    elif selected_input3 == "Druck p":
        input3unit_label["text"] = "Pa"
    elif selected_input3 == "Temperatur T":
        input3unit_label["text"] = "K"
    elif selected_input3 == "Spezifische Enthalpie h":
        input3unit_label["text"] = "J/kg"
    elif selected_input3 == "Spezifische Entropie s":
        input3unit_label["text"] = "J/(kg·K)"
    elif selected_input3 == "Dampfqualität x":
        input3unit_label["text"] = "kg/kg)"


# Input3 Combobox
selected_variable3 = tk.StringVar()
input3_combobox = ttk.Combobox(input_frame, width=29, textvariable=selected_variable3, values=variables, state="readonly")
input3_combobox.grid(row=4, column=1, sticky="W")
input3_combobox.set("Druck p")
input3_combobox.bind("<<ComboboxSelected>>", on_select_inpu3)

# Label Input3 Unit
input3unit_label = ttk.Label(input_frame, text="Pa")
input3unit_label.grid(row=4, column=3, sticky="W")

# Entry Input3
input3_var = tk.StringVar()
input3_entry = ttk.Entry(input_frame, textvariable=input3_var)
input3_entry.grid(row=4, column=2)

# Input4
def on_select_inpu4(event):
    selected_input4 = event.widget.get()
    if selected_input4 == "Dichte ρ":
        input4unit_label["text"] = "kg/m^3"
    elif selected_input4 == "Druck p":
        input4unit_label["text"] = "Pa"
    elif selected_input4 == "Temperatur T":
        input4unit_label["text"] = "K"
    elif selected_input4 == "Spezifische Enthalpie h":
        input4unit_label["text"] = "J/kg"
    elif selected_input4 == "Spezifische Entropie s":
        input4unit_label["text"] = "J/(kg·K)"
    elif selected_input4 == "Dampfqualität x":
        input4unit_label["text"] = "kg/kg)"


# Input4 Combobox
selected_variable4 = tk.StringVar()
input4_combobox = ttk.Combobox(input_frame, width=29, textvariable=selected_variable4, values=variables, state="readonly")
input4_combobox.grid(row=5, column=1, sticky="W")
input4_combobox.set("Temperatur T")
input4_combobox.bind("<<ComboboxSelected>>", on_select_inpu4)

# Label Input4 Unit
input4unit_label = ttk.Label(input_frame, text="K")
input4unit_label.grid(row=5, column=3, sticky="W")

# Entry Input4
input4_var = tk.StringVar()
input4_entry = ttk.Entry(input_frame, textvariable=input4_var)
input4_entry.grid(row=5, column=2)

# Input5
def on_select_inpu5(event):
    selected_input5 = event.widget.get()
    if selected_input5 == "Dichte ρ":
        input5unit_label["text"] = "kg/m^3"
    elif selected_input5 == "Druck p":
        input5unit_label["text"] = "Pa"
    elif selected_input5 == "Temperatur T":
        input5unit_label["text"] = "K"
    elif selected_input5 == "Spezifische Enthalpie h":
        input5unit_label["text"] = "J/kg"
    elif selected_input5 == "Spezifische Entropie s":
        input5unit_label["text"] = "J/(kg·K)"
    elif selected_input5 == "Dampfqualität x":
        input5unit_label["text"] = "kg/kg)"


# Input5 Combobox
selected_variable5 = tk.StringVar()
input5_combobox = ttk.Combobox(input_frame, width=29, textvariable=selected_variable5, values=variables, state="readonly")
input5_combobox.grid(row=7, column=1, sticky="W")
input5_combobox.set("Druck p")
input5_combobox.bind("<<ComboboxSelected>>", on_select_inpu5)

# Label Input5 Unit
input5unit_label = ttk.Label(input_frame, text="Pa")
input5unit_label.grid(row=7, column=3, sticky="W")

# Entry Input5
input5_var = tk.StringVar()
input5_entry = ttk.Entry(input_frame, textvariable=input5_var)
input5_entry.grid(row=7, column=2)

# Input6
def on_select_inpu6(event):
    selected_input6 = event.widget.get()
    if selected_input6 == "Dichte ρ":
        input6unit_label["text"] = "kg/m^3"
    elif selected_input6 == "Druck p":
        input6unit_label["text"] = "Pa"
    elif selected_input6 == "Temperatur T":
        input6unit_label["text"] = "K"
    elif selected_input6 == "Spezifische Enthalpie h":
        input6unit_label["text"] = "J/kg"
    elif selected_input6 == "Spezifische Entropie s":
        input6unit_label["text"] = "J/(kg·K)"
    elif selected_input6 == "Dampfqualität x":
        input6unit_label["text"] = "kg/kg)"


# Input6 Combobox
selected_variable6 = tk.StringVar()
input6_combobox = ttk.Combobox(input_frame, width=29, textvariable=selected_variable6, values=variables, state="readonly")
input6_combobox.grid(row=8, column=1, sticky="W")
input6_combobox.set("Temperatur T")
input6_combobox.bind("<<ComboboxSelected>>", on_select_inpu6)

# Label Input6 Unit
input6unit_label = ttk.Label(input_frame, text="K")
input6unit_label.grid(row=8, column=3, sticky="W")

# Entry Input6
input6_var = tk.StringVar()
input6_entry = ttk.Entry(input_frame, textvariable=input6_var)
input6_entry.grid(row=8, column=2)

# Fluid Info refresh
# Setzt Werte der Labels für Fluidvalues
def fluid_info(fluidselected):
    pure_info = CoolProp.get_fluid_param_string(fluidselected, "pure")
    if pure_info == "true":
        pure_info_label["text"] = "Reines Fluid: Ja"
    elif pure_info == "false":
        pure_info_label["text"] = "Reines Fluid: Nein"

    # Molar Mass
    molarmass_info = CoolProp.PropsSI("M", fluidselected)
    molarmass_info_label["text"] = "Molare Masse: " + str(round(molarmass_info * 1000, 4)) + " g/mol"    #mol masse auf 4 Stellen nach Komma
    gascostant = CoolProp.PropsSI("gas_constant", fluidselected)
    gasconstant_info_label["text"] = "Spezifische Gaskonstante: " + str(
        round(gascostant / molarmass_info, 1)) + " J/kg/K"    #Gaskonstante auf eine Nachkommastelle genau

    # Critical Point
    ctp_pressure = CoolProp.PropsSI("pcrit", fluidselected)
    ctp_pressure_label["text"] = "Druck: " + str(ctp_pressure) + " Pa"
    ctp_temp = CoolProp.PropsSI("Tcrit", fluidselected)
    ctp_temp_label["text"] = "Temperatur: " + str(ctp_temp) + " K"
    ctp_den = CoolProp.PropsSI("rhocrit", fluidselected)
    ctp_den_label["text"] = "Dichte: " + str(round(ctp_den, 1)) + " kg/m^3"

    # Triple Point
    tp_pressure = CoolProp.PropsSI("ptriple", fluidselected)
    tp_pressure_label["text"] = "Druck: " + str(tp_pressure) + " Pa"
    tp_temp = CoolProp.PropsSI("Ttriple", fluidselected)
    tp_temp_label["text"] = "Temperatur: " + str(tp_temp) + " K"

    # Fluidlimits
    maxp = CoolProp.PropsSI("pmax", fluidselected)
    maxp_label["text"] = "Max. Druck: " + str(maxp) + " Pa"
    maxtemp = CoolProp.PropsSI("Tmax", fluidselected)
    maxtemp_label["text"] = "Max. Temperatur: " + str(maxtemp) + " K"
    minp = CoolProp.PropsSI("pmin", fluidselected)
    minp_label["text"] = "Min. Druck: " + str(round(minp, 2)) + " Pa"
    mfloatemp = CoolProp.PropsSI("Tmin", fluidselected)
    mfloatemp_label["text"] = "Min. Temperatur: " + str(round(mfloatemp, 3)) + " K"

    diagram(selected_diagram.get())


# Fluid Info at Combobox Change (Aktualisiert Fluidinfos und Diagramm, wenn neues Fluid gewählt)
def on_select_fluid(event):
    fluid_info(event.widget.get())
    calc()

# Diagramm at Combobox Change
def on_select_diagram(event):
    diagram(event.widget.get())

# Click Event Diagram
# Setzt Variablen bei Klick in Diagramm und markiert den Punkt
def mouse_event(event):
    x = round(event.xdata, 2)
    y = round(event.ydata, 2)
    
    if selected_diagram.get() =="T-s-Diagramm":
        prop_output("S", "T", x, y)
        
        if point1.get()==True:
            input1_combobox.set("Temperatur T")
            input1unit_label["text"] = "K"       
            input2_combobox.set("Spezifische Entropie s")
            input2unit_label["text"] = "J/(kg·K)"
            
        elif point2.get()==True:
            input3_combobox.set("Temperatur T")
            input3unit_label["text"] = "K"       
            input4_combobox.set("Spezifische Entropie s")
            input4unit_label["text"] = "J/(kg·K)"
            
        elif point3.get()==True:
            input5_combobox.set("Temperatur T")
            input5unit_label["text"] = "K"       
            input6_combobox.set("Spezifische Entropie s")
            input6unit_label["text"] = "J/(kg·K)"
                       
    elif selected_diagram.get() == "p-h-Diagramm":
        prop_output("H", "P", x, y)
        
        if point1.get()==True:
            input1_combobox.set("Druck p")
            input1unit_label["text"] = "Pa"       
            input2_combobox.set("Spezifische Enthalpie h")
            input2unit_label["text"] = "J/kg"
            
        elif point2.get()==True:
            input3_combobox.set("Druck p")
            input3unit_label["text"] = "Pa"       
            input4_combobox.set("Spezifische Enthalpie h")
            input4unit_label["text"] = "J/kg"
            
        elif point3.get()==True:
            input5_combobox.set("Druck p")
            input5unit_label["text"] = "Pa"       
            input6_combobox.set("Spezifische Enthalpie h")
            input6unit_label["text"] = "J/kg"
        
    elif selected_diagram.get() == "h-s-Diagramm":
        prop_output("S", "H", x, y)
        
        if point1.get()==True:
            input1_combobox.set("Spezifische Enthalpie h")
            input1unit_label["text"] = "J/kg"    
            input2_combobox.set("Spezifische Entropie s")
            input2unit_label["text"] = "J/(kg·K)"
            
        elif point2.get()==True:
            input3_combobox.set("Spezifische Enthalpie h")
            input3unit_label["text"] = "J/kg"    
            input4_combobox.set("Spezifische Entropie s")
            input4unit_label["text"] = "J/(kg·K)"
            
        elif point3.get()==True:
            input5_combobox.set("Spezifische Enthalpie h")
            input5unit_label["text"] = "J/kg"    
            input6_combobox.set("Spezifische Entropie s")
            input6unit_label["text"] = "J/(kg·K)"
        
    elif selected_diagram.get() == "p-s-Diagram":
        prop_output("S", "P", x, y)
        
        if point1.get()==True:
            input1_combobox.set("Druck p")
            input1unit_label["text"] = "Pa"      
            input2_combobox.set("Spezifische Entropie s")
            input2unit_label["text"] = "J/(kg·K)"
            
        elif point2.get()==True:
            input3_combobox.set("Druck p")
            input3unit_label["text"] = "Pa"      
            input4_combobox.set("Spezifische Entropie s")
            input4unit_label["text"] = "J/(kg·K)"
            
        elif point3.get()==True:
            input5_combobox.set("Druck p")
            input5unit_label["text"] = "Pa"      
            input6_combobox.set("Spezifische Entropie s")
            input6unit_label["text"] = "J/(kg·K)"
             
    elif selected_diagram.get() == "p-T-Diagramm":
        prop_output("T", "P", x, y)
        
        if point1.get()==True:
            input1_combobox.set("Druck p")
            input1unit_label["text"] = "Pa"        
            input2_combobox.set("Temperatur T")
            input2unit_label["text"] = "K"
            
        elif point2.get()==True:
            input3_combobox.set("Druck p")
            input3unit_label["text"] = "Pa"        
            input4_combobox.set("Temperatur T")
            input4unit_label["text"] = "K"
            
        elif point3.get()==True:
            input5_combobox.set("Druck p")
            input5unit_label["text"] = "Pa"        
            input6_combobox.set("Temperatur T")
            input6unit_label["text"] = "K"
        
    elif selected_diagram.get() == "T-ρ-Diagramm":
        prop_output("D", "T", x, y)
        
        if point1.get()==True:
            input1_combobox.set("Temperatur T")
            input1unit_label["text"] = "K"       
            input2_combobox.set("Dichte ρ")
            input2unit_label["text"] = "kg/m^3"
            
        elif point2.get()==True:
            input3_combobox.set("Temperatur T")
            input3unit_label["text"] = "K"       
            input4_combobox.set("Dichte ρ")
            input4unit_label["text"] = "kg/m^3"
            
        elif point3.get()==True:
            input5_combobox.set("Temperatur T")
            input5unit_label["text"] = "K"       
            input6_combobox.set("Dichte ρ")
            input6unit_label["text"] = "kg/m^3"
    
    if point1.get()==True:
        input1_var.set(y)
        input2_var.set(x)
    
    elif point2.get()==True:
        input3_var.set(y)
        input4_var.set(x)
    
    elif point3.get()==True:
        input5_var.set(y)
        input6_var.set(x)
        
    diagram(selected_diagram.get())

# Creating Plots
fluidselected = selected_fluid.get()

fig_ts_plot = Figure(figsize=(4, 4))
ts_plot = PropertyPlot(fluidselected, 'Ts', tp_limits='ORC', figure=fig_ts_plot, unit_system="EUR")

fig_ph_plot = Figure(figsize=(4, 4))
ph_plot = PropertyPlot(fluidselected, 'ph', figure=fig_ph_plot, unit_system="EUR")

fig_hs_plot = Figure(figsize=(4, 4))
hs_plot = PropertyPlot(fluidselected, 'hs', figure=fig_hs_plot, unit_system="EUR")

fig_ps_plot = Figure(figsize=(4, 4))
ps_plot = PropertyPlot(fluidselected, 'ps', figure=fig_ps_plot, unit_system="EUR")

fig_td_plot = Figure(figsize=(4, 4))
td_plot = PropertyPlot(fluidselected, 'td', figure=fig_td_plot, unit_system="EUR")

fig_pT_plot = Figure(figsize=(4, 4))
pT_plot = PropertyPlot(fluidselected, 'pT', figure=fig_pT_plot, unit_system="EUR")

# Mouseover, um Koordinaten in Diagramm zu sehen
# Gibt derzeit die Daten nur in der Konsole wieder, nicht neben dem Cursor
# Callbacks momentan nur in TS-Diagramm hinterlegt
# Aufgerufen wird Klasse um Zeile 1000 rum (on_move(event))

class CursorAnnotation:
    def __init__(self, ax):
        self.ax = ax
        self.annotation = ax.annotate('', xy=(0, 0), xytext=(10, -10),
                                        textcoords='offset points',
                                        bbox=dict(boxstyle="round", fc="w"),
                                        arrowprops=dict(arrowstyle="->"))
        self.annotation.set_visible(False)

    def update(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                self.annotation.set_text(f'x={x:.2f}, y={y:.2f}')
                self.annotation.xy = (x, y)
                self.annotation.set_visible(True)
                event.canvas.draw()
            else:
                self.annotation.set_visible(False)
                event.canvas.draw()

def on_move(event):
    cursor_annotation.update(event)

# Keep Diagrams up-to-date
def diagram(diagram_select):
    fluidselected = selected_fluid.get()
      
    # Delete existing Checkboxes
    try:
        isobar_check.grid_remove()
        isotherm_check.grid_remove()
        isochor_check.grid_remove()
        isentropic_check.grid_remove()
        isenthalpic_check.grid_remove()
        isovapore_check.grid_remove()
    except:
        pass
    
    if diagram_select == "T-s-Diagramm":
        fig_ts_plot = Figure(figsize=(4, 4))
        ts_plot = PropertyPlot(fluidselected, 'Ts', tp_limits='ORC', figure=fig_ts_plot, unit_system="SI")
        ts_plot.calc_isolines(CoolProp.iQ, num=2)
        

        try:
            isobar_check.grid(row=0, column=0, sticky = "W")
            isovapore_check.grid(row=5, column=0, sticky = "W")
            isochor_check.grid(row=2, column=0, sticky = "W")
        
        except Exception as e:
            print("Error while plotting points:", e)
        

        # If Checkbox is activated plot Isolines
        try:
            if isobar_var.get():
                ts_plot.calc_isolines(CoolProp.iP, num=10)
            if isovapore_var.get():
                ts_plot.calc_isolines(CoolProp.iQ, num=6)
            if isochor_var.get():
                ts_plot.calc_isolines(CoolProp.iDmass, num=10)
                
        except Exception as e:
            print("Error while plotting points:", e)
            
        # try:
        #     if isobar_var.get():
        #         if isobar_num == 0:
        #             ts_plot.calc_isolines(CoolProp.iP, num=10)
        #         else:
        #             ts_plot.calc_isolines(CoolProp.iP, num=isobar_num)
                    
        #     if isovapore_var.get():
        #         if isovapore_num == 0 or isovapore_num == 1:
        #             ts_plot.calc_isolines(CoolProp.iQ, num=6)
        #         else:
        #             ts_plot.calc_isolines(CoolProp.iQ, num=isovapore_num)
        #     if isochor_var.get():
        #         if isochor_num == 0:
        #             ts_plot.calc_isolines(CoolProp.iDmass, num=10)
        #         else:
        #             ts_plot.calc_isolines(CoolProp.iDmass, num=isochor_num)
        
        ts_plot.draw()

        canvas_ts = FigureCanvasTkAgg(fig_ts_plot, master=diagram_frame)
        canvas_ts.draw()
        canvas_ts.get_tk_widget().grid(row=1, column=0, rowspan=16, pady=10, sticky="NW")

        toolbar = NavigationToolbar2Tk(canvas_ts, toolbar_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=0, column=0, sticky="WE")

        fig_ts_plot.tight_layout()

        cid = fig_ts_plot.canvas.mpl_connect("button_press_event", mouse_event)
        
        # Übergibt Koordinaten an CursorAnnotation
        cursor_annotation = CursorAnnotation(fig_ts_plot.gca())

        # Verbindet Funktion mit Event
        fig_ts_plot.canvas.mpl_connect('motion_notify_event', on_move)
        
        diagram_get = ts_plot

        ts_plot.draw_process(state)
    if diagram_select == "p-h-Diagramm":
        fig_ph_plot = Figure(figsize=(4, 4))
        ph_plot = PropertyPlot(fluidselected, 'ph', figure=fig_ph_plot, unit_system="SI")
        ph_plot.calc_isolines(CoolProp.iQ, num=2)
        
        try:
            isotherm_check.grid(row=1, column=0, sticky = "W")
            isochor_check.grid(row=2, column=0, sticky = "W")
            isentropic_check.grid(row=3, column=0, sticky = "W")
            isovapore_check.grid(row=5, column=0, sticky = "W")
        except:
            pass
        
        try:
            if isentropic_var.get():
                ph_plot.calc_isolines(CoolProp.iSmass, num=15)
            
            if isotherm_var.get():
                ph_plot.calc_isolines(CoolProp.iT, num=15)
            
            if isovapore_var.get():
                ph_plot.calc_isolines(CoolProp.iQ, num=6)
                
            if isochor_var.get():
                ph_plot.calc_isolines(CoolProp.iDmass, num=10)

        except:
            pass 
            
        ph_plot.draw()

        canvas_ph = FigureCanvasTkAgg(fig_ph_plot, master=diagram_frame)
        canvas_ph.draw()
        canvas_ph.get_tk_widget().grid(row=1, column=0, rowspan=16, pady=10, sticky="NW")

        toolbar = NavigationToolbar2Tk(canvas_ph, toolbar_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=0, column=0, sticky="W")

        fig_ph_plot.tight_layout()

        cid = fig_ph_plot.canvas.mpl_connect("button_press_event", mouse_event)
        
        diagram_get = ph_plot

        ph_plot.draw_process(state)
    if diagram_select == "h-s-Diagramm":
        fig_hs_plot = Figure(figsize=(4, 4))
        hs_plot = PropertyPlot(fluidselected, 'hs', figure=fig_hs_plot, unit_system="SI")
        hs_plot.calc_isolines(CoolProp.iQ, num=2)
        
        try:
            isobar_check.grid(row=0, column=0, sticky = "W")
            isotherm_check.grid(row=1, column=0, sticky = "W")
            isochor_check.grid(row=2, column=0, sticky = "W")
            isovapore_check.grid(row=5, column=0, sticky = "W")
        except:
            pass
        
        try:
            if isobar_var.get():
                hs_plot.calc_isolines(CoolProp.iP, num=10)
                
            if isotherm_var.get():
                hs_plot.calc_isolines(CoolProp.iT, num=15)
            
            if isovapore_var.get():
                hs_plot.calc_isolines(CoolProp.iQ, num=11)
                
            if isochor_var.get():
                hs_plot.calc_isolines(CoolProp.iDmass, num=10)
                

        except:
            pass
        
        hs_plot.draw()

        canvas_hs = FigureCanvasTkAgg(fig_hs_plot, master=diagram_frame)
        canvas_hs.draw()
        canvas_hs.get_tk_widget().grid(row=1, column=0, rowspan=16, pady=10, sticky="NW")

        toolbar = NavigationToolbar2Tk(canvas_hs, toolbar_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=0, column=0, sticky="W")

        fig_hs_plot.tight_layout()

        cid = fig_hs_plot.canvas.mpl_connect("button_press_event", mouse_event)
        
        diagram_get = hs_plot

        hs_plot.draw_process(state)
    if diagram_select == "p-s-Diagram":
        fig_ps_plot = Figure(figsize=(4, 4))
        ps_plot = PropertyPlot(fluidselected, 'ps', figure=fig_ps_plot, unit_system="SI")
        ps_plot.calc_isolines(CoolProp.iQ, num=2)
        
        try:
            isotherm_check.grid(row=1, column=0, sticky = "W")
            isochor_check.grid(row=2, column=0, sticky = "W")
            isovapore_check.grid(row=5, column=0, sticky = "W")
        except:
            pass
        
        try:
            if isotherm_var.get():
                ps_plot.calc_isolines(CoolProp.iT, num=15)
            
            if isovapore_var.get():
                ps_plot.calc_isolines(CoolProp.iQ, num=11)
                
            if isochor_var.get():
                ps_plot.calc_isolines(CoolProp.iDmass, num=10)
                
        except:
            pass
            
        ps_plot.draw()

        canvas_ps = FigureCanvasTkAgg(fig_ps_plot, master=diagram_frame)
        canvas_ps.draw()
        canvas_ps.get_tk_widget().grid(row=1, column=0, rowspan=16, pady=10, sticky="NW")

        toolbar = NavigationToolbar2Tk(canvas_ps, toolbar_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=0, column=0, sticky="W")

        fig_ps_plot.tight_layout()

        cid = fig_ps_plot.canvas.mpl_connect("button_press_event", mouse_event)
        
        diagram_get = ps_plot

        ps_plot.draw_process(state)

    if diagram_select == "p-T-Diagramm":
        fig_pT_plot = Figure(figsize=(4, 4))
        pT_plot = PropertyPlot(fluidselected, 'pT', figure=fig_pT_plot, unit_system="SI")
        pT_plot.calc_isolines(CoolProp.iQ, [0.5, 1])
        
        try:
            isochor_check.grid(row=2, column=0, sticky = "W")
        except:
            pass
        
        try:
            if isochor_var.get():
                pT_plot.calc_isolines(CoolProp.iDmass, num=10)     
        except:
            pass
        
        # Bei zusätzlicher Zeit Aggregatzustände einblenden
        
        pT_plot.draw()

        canvas_pT = FigureCanvasTkAgg(fig_pT_plot, master=diagram_frame)
        canvas_pT.draw()
        canvas_pT.get_tk_widget().grid(row=1, column=0, rowspan=16, pady=10, sticky="NW")

        toolbar = NavigationToolbar2Tk(canvas_pT, toolbar_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=0, column=0, sticky="W")

        fig_pT_plot.tight_layout()

        cid = fig_pT_plot.canvas.mpl_connect("button_press_event", mouse_event)
        
        diagram_get = pT_plot

        pT_plot.draw_process(state)
        
    if diagram_select == "T-ρ-Diagramm":
        fig_td_plot = Figure(figsize=(4, 4))
        td_plot = PropertyPlot(fluidselected, 'td', figure=fig_td_plot, unit_system="SI")
        td_plot.calc_isolines(CoolProp.iQ, num=2)
        
        try:
            isobar_check.grid(row=0, column=0, sticky = "W")
            isentropic_check.grid(row=3, column=0, sticky = "W")
            isenthalpic_check.grid(row=4, column=0, sticky = "W")
            isovapore_check.grid(row=5, column=0, sticky = "W")
    
        except:
            pass
        
        try:
            if isobar_var.get():
                td_plot.calc_isolines(CoolProp.iP, num=10)
            
            if isentropic_var.get():
                td_plot.calc_isolines(CoolProp.iSmass, num=15)
                
            if isenthalpic_var.get():
                td_plot.calc_isolines(CoolProp.iHmass)
            
            if isovapore_var.get():
                td_plot.calc_isolines(CoolProp.iQ, num=11)
         
        except:
            pass 
            
        td_plot.draw()

        canvas_td = FigureCanvasTkAgg(fig_td_plot, master=diagram_frame)
        canvas_td.draw()
        canvas_td.get_tk_widget().grid(row=1, column=0, rowspan=16, pady=10, sticky="NW")

        toolbar = NavigationToolbar2Tk(canvas_td, toolbar_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=0, column=0, sticky="W")

        fig_td_plot.tight_layout()

        cid = fig_td_plot.canvas.mpl_connect("button_press_event", mouse_event)
        
        diagram_get = td_plot

        td_plot.draw_process(state)
        

# At Start Output Fluid Info
fluid_info("water")


# # Coordinates Mouse
# def on_move(event):
#     if event.inaxes:
#         #print(f'data coords {event.xdata} {event.ydata},',
#              #f'pixel coords {event.x} {event.y}')
#         ax = event.inaxes
#         ax.format_coord = lambda x, y: f'x={x:.2f}, y={y:.2f}'
        
# Erstelle CursorAnnotation
cursor_annotation = CursorAnnotation(fig_ts_plot.gca())

# Verbinde die Funktion mit dem Mausbewegungs-Event
fig_ts_plot.canvas.mpl_connect('motion_notify_event', on_move)


def on_click(event):
    if event.button is MouseButton.LEFT:
        print('disconnecting callback')
        plt.disconnect(binding_id)


binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', on_click)

# At Combobox Change call Function
diagram_combobox.bind("<<ComboboxSelected>>", on_select_diagram)
fluid_combobox.bind("<<ComboboxSelected>>", on_select_fluid)


# On Input Nr. Select
    

# Calc Function for the Properties
def calc():
    #Berechne Punkt 1
    if selected_variable1.get() == "Dichte ρ":
        if selected_variable2.get() == "Dichte ρ":
            tkinter.messagebox.showwarning("Warnung", "Bitte zwei unterschiedliche Variablen zur Berechnung wählen!")
        elif selected_variable2.get() == "Druck p":
            tkinter.messagebox.showwarning("Warnung",
                                           "Dieses Paar von Eingabevariablen ist nicht möglich! Bitte eine andere Kombination wählen.")
        elif selected_variable2.get() == "Temperatur T":
            prop_output("D", "T", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Spezifische Enthalpie h":
            prop_output("D", "H", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Spezifische Entropie s":
            prop_output("D", "S", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Dampfqualität x":
            prop_output("D", "Q", float(input1_var.get()), float(input2_var.get()))

    if selected_variable1.get() == "Druck p":
        if selected_variable2.get() == "Dichte ρ":
            prop_output("P", "D", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Druck p":
            tkinter.messagebox.showwarning("Warnung", "Bitte zwei unterschiedliche Variablen zur Berechnung wählen!")
        elif selected_variable2.get() == "Temperatur T":
            prop_output("P", "T", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Spezifische Enthalpie h":
            prop_output("P", "H", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Spezifische Entropie s":
            prop_output("P", "S", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Dampfqualität x":
            prop_output("P", "Q", float(input1_var.get()), float(input2_var.get()))

    if selected_variable1.get() == "Temperatur T":
        
        if selected_variable2.get() == "Dichte ρ":
            prop_output("T", "D", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Druck p":
            prop_output("T", "P", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Temperatur T":
            tkinter.messagebox.showwarning("Warnung", "Bitte zwei unterschiedliche Variablen zur Berechnung wählen!")
        elif selected_variable2.get() == "Spezifische Enthalpie h":
            tkinter.messagebox.showwarning("Warnung",
                                           "Dieses Paar von Eingabevariablen ist nicht möglich! Bitte eine andere Kombination wählen.")
        elif selected_variable2.get() == "Spezifische Entropie s":
            prop_output("T", "S", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Dampfqualität x":
            prop_output("T", "Q", float(input1_var.get()), float(input2_var.get()))

    if selected_variable1.get() == "Spezifische Enthalpie h":
        if selected_variable2.get() == "Dichte ρ":
            prop_output("H", "D", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Druck p":
            prop_output("H", "P", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Temperatur T":
            tkinter.messagebox.showwarning("Warnung",
                                           "Dieses Paar von Eingabevariablen ist nicht möglich! Bitte eine andere Kombination wählen.")
        elif selected_variable2.get() == "Spezifische Enthalpie h":
            tkinter.messagebox.showwarning("Warnung", "Bitte zwei unterschiedliche Variablen zur Berechnung wählen!")
        elif selected_variable2.get() == "Spezifische Entropie s":
            prop_output("H", "S", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Dampfqualität x":
            tkinter.messagebox.showwarning("Warnung",
                                           "Dieses Paar von Eingabevariablen ist nicht möglich! Bitte eine andere Kombination wählen.")

    if selected_variable1.get() == "Spezifische Entropie s":
        if selected_variable2.get() == "Dichte ρ":
            prop_output("S", "D", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Druck p":
            prop_output("S", "P", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Temperatur T":
            prop_output("S", "T", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Spezifische Enthalpie h":
            prop_output("S", "H", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Spezifische Entropie s":
            tkinter.messagebox.showwarning("Warnung", "Bitte zwei unterschiedliche Variablen zur Berechnung wählen!")
        elif selected_variable2.get() == "Dampfqualität x":
            tkinter.messagebox.showwarning("Warnung",
                                           "Dieses Paar von Eingabevariablen ist nicht möglich! Bitte eine andere Kombination wählen.")

    if selected_variable1.get() == "Dampfqualität x":
        if selected_variable2.get() == "Dichte ρ":
            prop_output("Q", "D", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Druck p":
            prop_output("Q", "P", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Temperatur T":
            prop_output("Q", "T", float(input1_var.get()), float(input2_var.get()))
        elif selected_variable2.get() == "Spezifische Enthalpie h":
            tkinter.messagebox.showwarning("Warnung",
                                           "Dieses Paar von Eingabevariablen ist nicht möglich! Bitte eine andere Kombination wählen.")
        elif selected_variable2.get() == "Spezifische Entropie s":
            tkinter.messagebox.showwarning("Warnung",
                                           "Dieses Paar von Eingabevariablen ist nicht möglich! Bitte eine andere Kombination wählen.")
        elif selected_variable2.get() == "Dampfqualität x":
            tkinter.messagebox.showwarning("Warnung", "Bitte zwei unterschiedliche Variablen zur Berechnung wählen!")
     
            
     #Berechne Punkt 2
            
    # if selected_variable3.get() == "Temperatur T":
        
    #     if selected_variable4.get() == "Dichte ρ":
    #         prop_output("T", "D", float(input3_var.get()), float(input4_var.get()))
    #     elif selected_variable4.get() == "Druck p":
    #         prop_output("T", "P", float(input3_var.get()), float(input4_var.get()))
    #     elif selected_variable4.get() == "Temperatur T":
    #         tkinter.messagebox.showwarning("Warnung", "Bitte zwei unterschiedliche Variablen zur Berechnung wählen!")
    #     elif selected_variable4.get() == "Spezifische Enthalpie h":
    #         tkinter.messagebox.showwarning("Warnung",
    #                                        "Dieses Paar von Eingabevariablen ist nicht möglich! Bitte eine andere Kombination wählen.")
    #     elif selected_variable4.get() == "Spezifische Entropie s":
    #         prop_output("T", "S", float(input3_var.get()), float(input4_var.get()))
    #     elif selected_variable4.get() == "Dampfqualität x":
    #         prop_output("T", "Q", float(input3_var.get()), float(input4_var.get()))       

    diagram(selected_diagram.get())


# Output to the Labels
def prop_output(input1, input2, var1, var2):
    calc_temp = CoolProp.PropsSI("T", input1, var1,
                                 input2, var2,
                                 selected_fluid.get())
    calc_s = CoolProp.PropsSI("S", input1,
                              var1, input2,
                              var2,
                              selected_fluid.get())
    calc_p = CoolProp.PropsSI("P", input1, var1, input2,
                              var2,
                              selected_fluid.get())
    calc_h = CoolProp.PropsSI("H", input1,
                              var1, input2,
                              var2,
                              selected_fluid.get())
    calc_d = CoolProp.PropsSI("D", input1, var1,
                              input2, var2,
                              selected_fluid.get())


    state[0, "T"] = calc_temp
    state[0, "S"] = calc_s
    state[0, "P"] = calc_p
    state[0, "H"] = calc_h
    state[0, "D"] = calc_d

    try:
        calc_temp_label["text"] = "Temperatur T= " + str(calc_temp) + " K"
    except:
        calc_temp_label["text"] = "Temperatur T="
    try:
        calc_p_label["text"] = "Druck p= " + str(CoolProp.PropsSI("P", input1, var1, input2,
                                                                  var2,
                                                                  selected_fluid.get())) + " Pa"
    except:
        calc_p_label["text"] = "Druck p="
    try:
        calc_vq_label["text"] = "Dampfqualität x= " + str(round(calc_p, 6)) + " kg/kg"
    except:
        calc_vq_label["text"] = "Dampfqualität x="
    try:
        calc_sound_label["text"] = "Schallgeschwindigkeit c= " + str(round(CoolProp.PropsSI("A", input1,
                                                                                            var1,
                                                                                            input2,
                                                                                            var2,
                                                                                            selected_fluid.get()),
                                                                           6)) + " m/s"
    except:
        calc_sound_label["text"] = "Schallgeschwindigkeit c="
    try:
        calc_d_label["text"] = "Dichte ρ= " + str(round(calc_d, 6)) + " kg/m^3"
    except:
        calc_d_label["text"] = "Dichte ρ="
    try:
        calc_h_label["text"] = "Spezifische Enthalpie h= " + str(round(calc_h,
                                                                       6)) + " J/kg"
    except:
        calc_h_label["text"] = "Spezifische Enthalpie h="
    try:
        calc_s_label["text"] = "Spezifische Entropie s= " + str(round(calc_s, 6)) + " J/kg/K"
    except:
        calc_s_label["text"] = "Spezifische Entropie s="
    try:
        calc_u_label["text"] = "Spezifische innere Energie u= " + str(round(CoolProp.PropsSI("U", input1,
                                                                                             var1,
                                                                                             input2,
                                                                                             var2,
                                                                                             selected_fluid.get()),
                                                                            6)) + " J/kg"
    except:
        calc_u_label["text"] = "Spezifische innere Energie u="
    try:
        calc_v_label["text"] = "Viskosität η= " + str(round(CoolProp.PropsSI("V", input1, var1,
                                                                             input2, var2,
                                                                             selected_fluid.get()), 6)) + " Pa·s"
    except:
        calc_v_label["text"] = "Viskosität η="
    try:
        calc_st_label["text"] = "Oberflächenspannung σ= " + str(round(CoolProp.PropsSI("surface_tension",
                                                                                       input1, var1,
                                                                                       input2, var2,
                                                                                       selected_fluid.get()),
                                                                      6)) + " N/m"
    except:
        calc_st_label["text"] = "Oberflächenspannung σ="
    try:
        calc_cp_label["text"] = "Spezifische Wärmekapazität (Druck konstant) cp= " + str(round(
            CoolProp.PropsSI("Cpmass", input1, var1, input2, var2,
                             selected_fluid.get()), 6)) + " J/kg/K"
    except:
        calc_cp_label["text"] = "Spezifische Wärmekapazität (Druck konstant) cp="
    try:
        calc_cv_label["text"] = "Spezifische Wärmekapazität (Volumen konstant) cv= " + str(round(
            CoolProp.PropsSI("Cvmass", input1, var1, input2, var2,
                             selected_fluid.get()), 6)) + " J/kg/K"
    except:
        calc_cv_label["text"] = "Spezifische Wärmekapazität (Volumen konstant) cv="


# Use of Return Key
def return_calc(event):
    calc()

diagram(selected_diagram.get())


# Create Calc Button
calc_btn = ttk.Button(input_frame, text="Berechnen", command=calc, width=15)
calc_btn.grid(row=10, column=0, sticky="N", columnspan=3, padx = 15, pady=10)
window.bind("<Return>", return_calc)


# Infinite Loop & Close Window
def on_closing():
    if tkinter.messagebox.askyesno("FluProp schließen", "Möchtest du FluProp beenden?"):
        window.destroy()
        plt.close("all")


window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()