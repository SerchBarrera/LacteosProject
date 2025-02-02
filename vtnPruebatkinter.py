from tkinter import *






#Iniciando app
aplicacion = Tk()

#tamaño de ventana
aplicacion.geometry("1020x630+0+0")

#evitarr maximizar
aplicacion.resizable(0, 0)

#titulo ventana
aplicacion.title("Ventana Reportes")

#color de fondo de ventana
aplicacion.config(background="bisque")

#panel superior
panelSuperior = Frame(aplicacion, bd=1, relief=FLAT)
panelSuperior.pack(side=TOP)

#etiqueta tiutulo
etiquetaTitulo = Label(panelSuperior,text="Ventana de reportes",fg='azure4',
                       font=('Dosis',58), bg='burlywood',width=27)
etiquetaTitulo.grid(row=0,column=0)

#panel izquierdo
panelIzquierdo = Frame(aplicacion, bd=1,relief=FLAT)
panelIzquierdo.pack(side=LEFT)

#panel costos
panelCostos = Frame(panelIzquierdo, bd=1,relief=FLAT)
panelCostos.pack(side=BOTTOM)

#panel comidas
panelComidas = Label(panelIzquierdo,text="Comida",font=('Dosis',19,'bold'),
                                                        bd=1, relief=FLAT, fg='azure4')
panelComidas.pack(side=LEFT)
#Panel bebidas
panelBebidas = Label(panelIzquierdo,text="BebidaS",font=('Dosis',19,'bold'),
                                                        bd=1, relief=FLAT, fg='azure4')
panelBebidas.pack(side=LEFT)
#PANEL POSTRES
panelPostres = Label(panelIzquierdo,text="Postres",font=('Dosis',19,'bold'),
                                                        bd=1, relief=FLAT, fg='azure4')
panelPostres.pack(side=LEFT)

#panel derecha
panelDerecha = Frame(aplicacion,bd=1,relief=FLAT)
panelDerecha.pack(side=RIGHT)

#PANEL CALCULADORA
panelCalculadora = Frame(panelDerecha,bd=1, relief=FLAT,bg='burlywood')
panelCalculadora.pack()
#panel recibo
panelRecibo = Frame(panelDerecha,bd=1, relief=FLAT,bg='burlywood')
panelRecibo.pack()

#panel botones
panelBotones= Frame(panelDerecha,bd=1, relief=FLAT,bg='burlywood')
panelBotones.pack()

#listas productos
listasComidas = ['pollo','pollo','pollo','platanos']
listaBedibas = ['coca','coca','coca']
listaPostres = ['brownies', 'brownies', 'brownies', 'panqués']

contador = 0
for comida in listasComidas:
    comida = Checkbutton(panelComidas, text=comida.title(), font=('Dosis',19,'bold'), onvalue=1, offvalue=0)
    comida.grid(row=contador,column=0,sticky=W)
    contador += 1

# lista de productos
lista_comidas = ['pollo','platanos','salmon','kebab']
lista_bebidas = ['vino','coca-cola','agua mineral','refresco fanta']
lista_postres = ['pastel zanahoria','pastel chocolate','brownies','cheescake']

#comida dinamica
variables_comida  = []
contador = 0
for comida in lista_comidas:
    variables_comida.append('')
    variables_comida[contador] = IntVar()
    comida = Checkbutton(panelComidas, text=comida.title(), font=('Dosis',19,'bold'),
                         onvalue=1, offvalue=0, variable=variables_comida[contador])
    comida.grid(row=contador, column=0,sticky=W)
    contador += 1




#bebidasdinamica
variables_postre = []
contador = 0
for postres in lista_postres:
    variables_postre.append('')
    variables_postre[contador] = IntVar()
    postres= Checkbutton(panelPostres, text=postres.title(), font=('Dosis',19,'bold'),
                         onvalue=1, offvalue=0, variable=variables_postre[contador])
    postres.grid(row=contador, column=0,sticky=W)
    contador += 1





#Evitar que la ventana se cierre
aplicacion.mainloop()