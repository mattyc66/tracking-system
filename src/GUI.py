import paho.mqtt.client as mqtt
from tkinter import *
import customtkinter as ctk

ctk.set_appearance_mode("dark")

window = ctk.CTk()
window.geometry("500x600")

Boundary = {
    'lat_min': float('-inf'),  
    'lat_max': float('inf'),   
    'lng_min': float('-inf'),  
    'lng_max': float('inf')
}

gpsSat = None
gpsLat = None
gpsLng = None
canvas_width = 450
canvas_height =320

def on_connect(client, userdata, status, flags):
    client.subscribe("MC-Project-Lat")
    client.subscribe("MC-Project-Lng")
    client.subscribe("MC-Project-Sat")

def draw_tracker(latitude, longitude):
    # Calculate canvas coordinates relative to the set boundaries
    canvas_x = int((longitude - Boundary['lng_min']) / (Boundary['lng_max'] - Boundary['lng_min']) * canvas_width)
    canvas_y = int((latitude - Boundary['lat_min']) / (Boundary['lat_max'] - Boundary['lat_min']) * canvas_height)

    # Draw a red dot at the calculated position
    canvas.create_oval(canvas_x - 3, canvas_y - 3, canvas_x + 3, canvas_y + 3, fill="red")


def on_message(client, userdata, msg):
    global gpsSat, gpsLat, gpsLng
    if msg.topic == "MC-Project-Lat":
        gpsLat = msg.payload.decode("utf-8")
    elif msg.topic == "MC-Project-Lng":
        gpsLng = msg.payload.decode("utf-8")
    elif msg.topic == "MC-Project-Sat":
        gpsSat = msg.payload.decode("utf-8")
    update_labels()
    status_update()

def update_labels():
    satval.configure(text=gpsSat)
    latval.configure(text=gpsLat)
    lngVal.configure(text=gpsLng)

def set_boundaries(minLatEntry, maxLatEntry, minLngEntry, maxLngEntry):
    Boundary['lat_min'] = float(minLatEntry.get())
    Boundary['lat_max'] = float(maxLatEntry.get())
    Boundary['lng_min'] = float(minLngEntry.get())
    Boundary['lng_max'] = float(maxLngEntry.get())


def check_boundaries(latitude, longitude):
    if (Boundary['lat_min'] <= latitude <= Boundary['lat_max']) and (Boundary['lng_min'] <= longitude <= Boundary['lng_max']):
        return True
    else:
        return False
    
def status_update():
    if gpsLat is not None and gpsLng is not None:
        latitude = float(gpsLat)
        longitude = float(gpsLng)
        if check_boundaries(latitude, longitude):
            status.configure(text="In bounds", text_color="green")
        else:
            status.configure(text="Out of bounds", text_color="red")



broker_address = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)
client.loop_start()

def bound_nav():
    Bwindow = ctk.CTkToplevel(window)
    Bwindow.geometry("250x300")
    minLatEntry = ctk.CTkEntry(Bwindow, width=40)
    minLatEntry.place(x=56, y=69)
    maxLatEntry = ctk.CTkEntry(Bwindow, width=40)
    maxLatEntry.place(x=139, y=69)
    minLngEntry = ctk.CTkEntry(Bwindow, width=40)
    minLngEntry.place(x=56, y=125)
    maxLngEntry = ctk.CTkEntry(Bwindow, width=40)
    maxLngEntry.place(x=139, y=125)
    minlabel = ctk.CTkLabel(Bwindow, text="Min")
    minlabel.place(x=62, y=35)
    maxlabel = ctk.CTkLabel(Bwindow, text="Max")
    maxlabel.place(x=145, y=35)
    latlabel = ctk.CTkLabel(Bwindow, text="Lat")
    latlabel.place(x=14, y=73)
    lnglabel = ctk.CTkLabel(Bwindow, text="Lng")
    lnglabel.place(x=14, y=129)

    calculate = ctk.CTkButton(Bwindow,
                              width=1,
                              corner_radius=5,
                              command=lambda: set_boundaries(minLatEntry, maxLatEntry, minLngEntry, maxLngEntry),
                              text="Set")
    calculate.place(x=30, y=241)

    Bwindow.grab_set()




toggle = ctk.CTkButton(window,
                       width=86,
                       height=25,
                       corner_radius=5,
                       text="Toggle")
toggle.place(x=81, y=235)

bound = ctk.CTkButton(window,
                      width=69,
                      height=25,
                      corner_radius=5,
                      command=bound_nav,
                      text="Boundries")
bound.place(x=23, y=550)

Dframe = ctk.CTkFrame(window,
                      corner_radius=20,
                      width=316,
                      height=133,
                      bg_color='transparent',
                      border_width=0)
Dframe.place(x=58, y=89)
status = ctk.CTkLabel(Dframe, text="In bounds", text_color="green")
status.place(x=18, y=2)
sat = ctk.CTkLabel(Dframe, text="Satellites: ")
satval = ctk.CTkLabel(Dframe, text=gpsSat)
satval.place(x=97, y=34)
sat.place(x=18, y=34)
lat = ctk.CTkLabel(Dframe, text="Latitude: ")
latval = ctk.CTkLabel(Dframe, text=gpsLat)
lat.place(x=18, y=66)
latval.place(x=97, y=65)
lng = ctk.CTkLabel(Dframe, text="Longitude: ")
lngVal = ctk.CTkLabel(Dframe, text=gpsLng)
lngVal.place(x=97, y=97)
lng.place(x=18, y=97)

tracker_label = ctk.CTkLabel(window, text="Tracker Location:")
tracker_label.place(x=85, y=270)
canvas = ctk.CTkCanvas(window, width=canvas_width, height=canvas_height, bg='gray', highlightthickness=0)
canvas.place(x=150, y=600)
canvas.create_rectangle(0, 0, 450, 320, outline='white', width=2)
canvas.create_oval(canvas_width // 2 - 5, canvas_height // 2 - 5, canvas_width // 2 + 5, canvas_height // 2 + 5, fill="red")



window.mainloop()