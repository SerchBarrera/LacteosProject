from customtkinter import *
from tkinter import messagebox
from PIL import Image
import Menu


def verificar_credenciales():
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()

    if usuario == "admin" and contrasena == "admin":
        messagebox.showinfo("Inicio de sesión exitoso", "Bienvenido al sistema")
        app.destroy()  # Cierra la ventana de inicio de sesión
        abrir_menu()  # Abre la ventana del menú
    else:
        messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos")


def abrir_menu():
    menu_root = CTk()
    app = Menu.MenuApp(menu_root)
    menu_root.mainloop()


app = CTk()
app.geometry("600x480")
app.resizable(0, 0)
app.title("Iniciar Sesión-MilkShop")

side_img_data = Image.open('C:\\Users\\sbarr\\PycharmProjects\\ProjectCompleto_V1\\ProjectCompleto_V1\\imagenes\\imgFondoDef.jpg')
email_icon_data = Image.open("C:\\Users\\sbarr\\PycharmProjects\\ProjectCompleto_V1\\ProjectCompleto_V1\\imagenes\\icon_user_color.png")
password_icon_data = Image.open("C:\\Users\\sbarr\\PycharmProjects\\ProjectCompleto_V1\\ProjectCompleto_V1\\imagenes\\pwd_user_color.png")


side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="!Bienvenido de vuelta!", text_color="#A23C26", anchor="w", justify="left",
         font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(master=frame, text="Ingresa con tu usuario", text_color="#A23C26", anchor="w", justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Usuario:", text_color="#A23C26", anchor="w", justify="left", font=("Arial Bold", 14),
         image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
entrada_usuario = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                           text_color="#000000")
entrada_usuario.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Contraseña:", text_color="#A23C26", anchor="w", justify="left", font=("Arial Bold", 14),
         image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
entrada_contrasena = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                              text_color="#000000", show="*")
entrada_contrasena.pack(anchor="w", padx=(25, 0))

CTkButton(master=frame, text="Iniciar Sesión", fg_color="#A23C26", hover_color="#E85636", font=("Arial Bold", 12),
          text_color="#ffffff", width=225, command=verificar_credenciales).pack(anchor="w", pady=(40, 0), padx=(25, 0))


app.mainloop()

"""
import Inventario
import Pedidos
import Empresas
import Reporte
from PIL import ImageTk, Image
"""
"""
user={'username':'admin','password':'admin'}
def authenticate(username,password):
      if user['username'] == username and user['password'] == password:
            messagebox.showinfo("Inicio de Sesión","Inicio de sesión existoso")
            return user
      else :
          messagebox.showerror("Error","Nombre de usuario o contraseña incorrectos")
          return None

def iniciar_sesion():
    usuario = entrada_usuario.get()
    contraseña = entrada_contraseña.get()
    authenticate(usuario,contraseña)


vtnInicial = tk.Tk()
vtnInicial.title("Inicio de Sesión")
vtnInicial.geometry("400x300")

imagen = Image.open("C:\\Users\\sbarr\\Downloads\\imgFondo.jpg")
imagen = imagen.resize((400,150))
imagenTk = ImageTk.PhotoImage(imagen)

label_imagen = tk.Label(vtnInicial,image=imagenTk)
label_imagen.pack()

frame = tk.Frame(vtnInicial)
frame.pack(pady=20)

label_usuario = tk.Label(frame, text="Ingrese su usuario: ", font=('Dosis',19,'bold'))
label_usuario.grid(row=0,column=0, padx=10, pady=5)
entrada_usuario = tk.Entry(frame)
entrada_usuario.grid(row=0,column=1, padx=10, pady=5)

label_contraseña = tk.Label(frame, text="Ingrese su contraseña: ", font=('Dosis',19,'bold'))
label_contraseña.grid(row=1,column=0, padx=10, pady=5)
entrada_contraseña = tk.Entry(frame,show="*")
entrada_contraseña.grid(row=1,column=1, padx=10, pady=5)

btnIniciarSesion = tk.Button(frame,text="Iniciar Sesion",command=iniciar_sesion)
btnIniciarSesion.grid(row=2,columnspan=2,pady=5)

vtnInicial.mainloop()






def login():
    while True:
        print("\n******Bienvenido a MilkyShop*****")
        print("1. Iniciar sesion")
        print("2. Salir")
        option = input("Seleccione una opción: ")
        match option:
            case "1":
                username = input("Ingrese usuario: ")
                password = input("Ingrese contraseña: ")
                #password = getpass.getpass("password")
                user = authenticate(username,password)
                if user:
                    print("usuario y contraseña validos")
                    Menu()
                else:
                    print("Datos inválidos, favor de ingresarlos nuevamente")
            case "2":
                print("Saliendo......")
                break
            case _:
                print("Datos ingresados no validos, favor de intentarlo nuevamente")


def Menu():
    print("*****Bienvenido a nuestro menu principal*****")
    while True:
        print("1. Reportes")
        print("2. Pedidos")
        print("3. Inventario")
        print("4. Empresas")
        print("5. Salir")
        option = input("Favor de seleccionar una opcion: ")
        match option:
            case "1":
                Reporte.menuReporte()
            case "2":
                Pedidos.menuPedidos()
            case "3":
                Inventario.menuInventario()
            case "4":
                Empresas.menuEmpresas()
            case "5":
                print("Saliendo......")
                break

login()
"""

