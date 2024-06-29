from tkinter import *
import tkinter as tk 
from ventas import Ventas
from inventario import Inventario
from PIL import Image, ImageTk

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0,y=0,width=475,height=500)
        self.config(bg="black")
        self.widgets()

    def show_frames(self, container):
        top_level= tk.Toplevel(self)  
        frame= container(top_level)
        frame.config(bg="#C6D9E3")
        frame.pack(fill="both", expand=True)  
        top_level.geometry("1000x600+5+5")
        top_level.resizable (False,False) 
        
        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set
        top_level.lift()

    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        self.show_frames(Inventario)

    def salir(self):
        self.show_frames

    def widgets (self):

        frame1 = tk.Frame(self, bg="black") 
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=500)

        btnventas = Button(frame1,bg="blue", fg="white", font="Arial 14 bold",text="V E N T A S", command=self.ventas)
        btnventas.place(x=10, y=340, width=120, height=50)
        
        btninventario=Button(frame1,bg="blue",fg="white",font="Arial 14 bold",text="INVENTARIO", command=self.inventario)
        btninventario.place(x=335, y=340, width=120, height=50)

        
        btnsalir=Button(frame1,bg="blue",fg="white",font="Arial 14 bold",text="SALIR", command=self.salir)
        btnsalir.place(x=170, y=410, width=120, height=50)


        self.logo_image = Image.open("logo.png")
        self.logo_image = self.logo_image.resize((280,280))
        self.logo_image= ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1, image=self.logo_image, bg="#C6D9E3")
        self.logo_label.place(x=100, y=50)

        derechos_de_autor_label= tk.Label(frame1,text="SISTEMA POS 1.0 UNEFA", font="Arial 10 bold",bg= "black", fg="white")
        derechos_de_autor_label.place(x=143, y=480)

        derechos_de_autor_label= tk.Label(frame1,text="UNEFA SPORT", font="Arial 20 bold",bg= "black", fg="white")
        derechos_de_autor_label.place(x=150, y=10)

