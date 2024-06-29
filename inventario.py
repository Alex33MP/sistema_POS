import sqlite3
from tkinter import *
import tkinter as tk 
from tkinter import ttk, messagebox

#se hace la clasificacion de la funcion 
class Inventario(tk.Frame):
    db_name= "database.db"
    def __init__(self, padre):
        super().__init__(padre)
        self.pack()
        self.conn =sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.widgets()

    def widgets (self):
        frame1 = tk.Frame(self, bg="blue",highlightbackground="blue", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1000,height=100)

        titulo = tk.Label(self,text="INVENTARIO DE ARTICULOS",bg="black", fg="white", font="Arial 35 bold", anchor="center")
        titulo.pack()
        titulo.place(x=50, y=10, width=900, height=80)

        frame2 = tk.Frame(self, bg="blue",highlightbackground="black", highlightthickness=1)
        frame2.place (x=0, y=100, width=1100,height=550)
       
        #Se crea las etiquetan para la ventana inventario 

        labelframe = LabelFrame (frame2, text="ARTICULOS", font="Arial 14 bold", bg="blue", fg="black")
        labelframe.place(x=20, y=30 , width=400, height=500)

        lblnombre = Label(labelframe, text="NOMBRE:", font="Arial 12 bold")
        lblnombre.place (x=10, y=20)
        self.nombre = ttk.Entry (labelframe,font="Arial 12 bold")
        self.nombre.place (x=140, y=20, width=240, height=40)

        lblmarca= Label (labelframe, text="MARCA:",font="Arial 12 bold", bg="#dddddd")
        lblmarca.place(x=10, y=80)
        self.marca= ttk.Entry (labelframe,font="Arial 14 bold")
        self.marca.place(x=140, y=80, width=240, height=40)

        lblprecio = Label (labelframe, text="PRECIO:",font="Arial 12 bold", bg="#dddddd")
        lblprecio.place (x=10, y=140)
        self.precio= ttk.Entry (labelframe,font="Arial 14 bold")
        self.precio.place(x=140, y=140, width=240, height=40)

        lblcosto = Label (labelframe, text="COSTO:",font="Arial 12 bold", bg="#dddddd")
        lblcosto.place (x=10, y=200)
        self.costo= ttk.Entry (labelframe,font="Arial 14 bold")
        self.costo.place(x=140, y=200, width=240, height=40)

        lblstock = Label (labelframe, text="STOCK:",font="Arial 12 bold", bg="#dddddd")
        lblstock.place (x=10, y=260)
        self.stock= ttk.Entry (labelframe,font="Arial 14 bold")
        self.stock.place(x=140, y=260, width=240, height=40)

        boton_agregar=tk.Button(labelframe, text="INGRESAR",font="Arial 12 bold", bg="blue",fg="white", command= self.registrar)
        boton_agregar.place(x=80, y=310, width=100, height=40, )

        boton_editar=tk.Button(labelframe, text="EDITAR",font="Arial 12 bold", bg="blue",fg="white", command=self.editar_producto)
        boton_editar.place(x=200, y=310, width=100, height=40)
        
        #se establecen los parametros de la tabla 
        treFrame = Frame (frame2, bg="black")
        treFrame.place(x=430, y=50, width=500, height=350)

        scrol_y =ttk.Scrollbar (treFrame)
        scrol_y.pack (side=RIGHT, fill=Y)

        scrol_x =ttk.Scrollbar (treFrame, orient=HORIZONTAL)
        scrol_x.pack (side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40,
                                 columns=("ID", "PRODUCTO", "MARCA", "PRECIO", "COSTO", "STOCK"),show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("ID", text="Id")
        self.tre.heading("PRODUCTO", text="Producto")
        self.tre.heading("MARCA", text="Marca")
        self.tre.heading("PRECIO", text="Precio")
        self.tre.heading("COSTO", text="Costo")
        self.tre.heading ("STOCK", text="Stock")

        self.tre.column("ID", width=70, anchor="center")
        self.tre.column("PRODUCTO", width=100, anchor="center")
        self.tre.column("MARCA", width=100, anchor="center")
        self.tre.column("PRECIO", width=100, anchor="center")
        self.tre.column("COSTO", width=100, anchor="center")
        self.tre.column("STOCK", width=70, anchor="center")
        
        self.mostrar()

        btn_actualizar = Button(frame2, text="GUARDAR CAMBIOS", font="Arial 14 bold", bg="blue",fg="white", command=self.actualizar_inventario)
        btn_actualizar.place(x=55, y=410, width=300, height=40)

    def eje_consulta(self, consulta, parametros=()):
        print(consulta)
        print(parametros)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()
        return result
    

    def validacion(self, nombre, marca, precio, costo, stock):
        if not (nombre and marca and precio and costo and stock):
            return False 
        try: 
            float(precio)
            float(costo)
            int(stock)
        except ValueError:
            return False 
        return True 
        
 
    def mostrar(self):
        consulta= "SELECT * FROM inventario ORDER BY id DESC"

        result = self.eje_consulta(consulta)
        for elem in result: 
            try:
                precio_Bs = "{:,.2f}".format(float(elem[3])) if elem[3] else "" 
                costo_Bs = "{:,.2f} ".format(float(elem[4])) if elem[4] else ""
            except ValueError:
                precio_Bs = elem[3]
                costo_Bs = elem[4]
            self.tre.insert ("", 0, text=elem[0], values=(elem[0], elem[1], elem[2],precio_Bs, costo_Bs, elem[5] )) 

    def actualizar_inventario(self):
        for item in self.tre.get_children():
            self.tre.delete(item) 

        self.mostrar()

        messagebox.showinfo("Actualizacion exitosa.")

        
    def registrar(self):  
        result = self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        nombre = self.nombre.get()
        marca = self.marca.get()
        precio = self.precio.get()
        costo = self.costo.get()
        stock = self.stock.get()
        if self.validacion(nombre, marca, precio, costo, stock):
            try:
                consulta = "INSERT INTO inventario VALUES(?,?,?,?,?,?)"
                parametros = (None, nombre, marca, precio, costo, stock)
                self.eje_consulta(consulta, parametros)
                self.mostrar()
                self.nombre.delete(0, END)
                self.marca.delete(0, END)
                self.precio.delete(0, END)
                self.costo.delete(0, END)
                self.stock.delete(0, END)
            except Exception as e:
                messagebox.showwarning(title="Error", message= f"El registro no fue realizado: {e}")
        else:
            messagebox.showwarning(title="Error",message= f"Error al rellenar los campos") 
            self.mostrar()   

    def editar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Editar producto", "Seleccione un producto.")
            return
        item_id = self.tre.item(seleccion)["text"] 
        item_values = self.tre.item(seleccion)["values"]

        ventana_editar = Toplevel(self)
        ventana_editar.title("EDITAR PRODUCTOS")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="black")

        lbl_nombre = Label(ventana_editar, text="NOMBRE:", font= "Arial 14 bold", bg="blue", fg="white")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = Entry(ventana_editar, font= "Arial 12 bold")
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.insert(0, item_values[1])

        lbl_marca = Label (ventana_editar, text="MARCA: ",font= "Arial 14 bold", bg="blue", fg="white")
        lbl_marca.grid(row=1, column=0, padx=10, pady=10)
        entry_marca = Entry(ventana_editar, font= "Arial 12 bold")
        entry_marca.grid(row=1, column=1, padx=10, pady=10)
        entry_marca.insert(0, item_values[2])

        lbl_precio = Label (ventana_editar, text="PRECIO: ",font= "Arial 14 bold", bg="blue", fg="white")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        entry_precio = Entry(ventana_editar, font= "Arial 12 bold")
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        entry_precio.insert(0, item_values[3]) 

        lbl_costo = Label(ventana_editar, text="COSTO: ",font= "Arial 14 bold", bg="blue", fg="white")
        lbl_costo.grid(row=3, column=0, padx=10, pady=10)
        entry_costo = Entry(ventana_editar, font= "Arial 12 bold")
        entry_costo.grid(row=3, column=1, padx=10, pady=10)
        entry_costo.insert(0, item_values[4])

        lbl_stock = Label (ventana_editar, text="STOCK: ",font= "Arial 14 bold", bg="blue", fg="white")
        lbl_stock.grid(row=4, column=0, padx=10, pady=10)
        entry_stock = Entry(ventana_editar, font= "Arial 12 bold")
        entry_stock.grid(row=4, column=1, padx=10, pady=10)
        entry_stock.insert(0, item_values[5])


        def guardar_cambios():
            nombre = entry_nombre.get()
            marca = entry_marca.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()

            if not (nombre and marca and precio and costo and stock):
                messagebox.showwarning("Guardar cambios", "Rellene todos los campos.")
                return
            try:
                precio = float(precio.replace(",",""))
                costo = float(costo.replace(",",""))   
            except ValueError:
                messagebox.showwarning("Guardar cambios","Ingresen un valor correcto.")
                return

            consulta = "UPDATE inventario SET nombre=?, precio=?, precio=?, costo=?, stock=? WHERE id=?"
            parametros = (nombre, marca, precio, costo, stock, item_id)
            self.eje_consulta(consulta, parametros)

            self.actualizar_inventario()

            ventana_editar.destroy()

        btn_guardar = Button(ventana_editar, text="GUARDAR CAMBIOS",font="Arial 14 bold",bg="blue", fg="white", command=guardar_cambios)
        btn_guardar.place(x=80, y=250, width=240, height=40)           

        
               


    





        





      


        












        