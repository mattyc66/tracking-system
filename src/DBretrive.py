import firebase_admin
from firebase_admin import db, credentials
from tkinter import *
import customtkinter as ctk

credPath = "creds.json"
cred = credentials.Certificate(credPath)
firebase_admin.initialize_app(cred, {"databaseURL": "https://tracking-system-database-default-rtdb.europe-west1.firebasedatabase.app/"})
LatData = db.reference("/GPS-data/timestamp1/Lat")
LngData = db.reference("/GPS-data/timestamp1/Lng")
print("Latitude:",LatData.get())
print("Longitude:", LatData.get())
