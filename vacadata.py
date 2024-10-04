import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# Archivo para almacenar usuarios y contraseñas
FILE_USERS = "usuarios.txt"
# Directorios para almacenar historias clínicas y producción
HISTORIAS_CLINICAS_DIR = "historias_clinicas"
PRODUCCION_DIR = "produccion"

# Crear los directorios si no existen
os.makedirs(HISTORIAS_CLINICAS_DIR, exist_ok=True)
os.makedirs(PRODUCCION_DIR, exist_ok=True)

# Función para registrar un nuevo usuario
def registrar():
    usuario = simpledialog.askstring("Registro", "Ingrese su nombre de usuario:")
    contrasena = simpledialog.askstring("Registro", "Ingrese su contraseña:", show='*')

    if not usuario or not contrasena:
        messagebox.showwarning("Advertencia", "Usuario y contraseña no pueden estar vacíos.")
        return

    # Verificar si el usuario ya existe
    if os.path.exists(FILE_USERS):
        with open(FILE_USERS, "r") as file:
            for linea in file:
                nombre, _ = linea.strip().split(",")
                if nombre == usuario:
                    messagebox.showwarning("Advertencia", "El usuario ya existe. Intente con otro nombre.")
                    return

    # Guardar el nuevo usuario
    with open(FILE_USERS, "a") as file:
        file.write(f"{usuario},{contrasena}\n")
    messagebox.showinfo("Registro", "Usuario registrado con éxito.")

# Función para iniciar sesión
def login():
    usuario = simpledialog.askstring("Iniciar Sesión", "Ingrese su nombre de usuario:")
    contrasena = simpledialog.askstring("Iniciar Sesión", "Ingrese su contraseña:", show='*')

    if not usuario or not contrasena:
        messagebox.showwarning("Advertencia", "Usuario y contraseña no pueden estar vacíos.")
        return False

    # Comprobar si el usuario existe y la contraseña es correcta
    if os.path.exists(FILE_USERS):
        with open(FILE_USERS, "r") as file:
            for linea in file:
                nombre, passw = linea.strip().split(",")
                if nombre == usuario and passw == contrasena:
                    messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso.")
                    mostrar_frame(frame_menu_principal)
                    return True
    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    return False

# Función para cambiar entre diferentes secciones (frames)
def mostrar_frame(frame):
    frame.tkraise()

# Función para la historia clínica de la vaca
def historia_clinica():
    nombre_vaca = simpledialog.askstring("Historia Clínica", "Ingrese el nombre o ID de la vaca:")
    if not nombre_vaca:
        return
    global archivo_vaca
    archivo_vaca = os.path.join(HISTORIAS_CLINICAS_DIR, f"{nombre_vaca}.txt")
    label_historia_clinica.config(text=f"--- Historia Clínica de {nombre_vaca} ---")
    mostrar_frame(frame_historia_clinica)
    actualizar_lista_registros_clinicos()

# Función para agregar un registro clínico en el mismo frame
def agregar_registro_clinico():
    fecha = entry_fecha_clinica.get()
    descripcion = entry_descripcion_clinica.get()

    if not fecha or not descripcion:
        messagebox.showwarning("Advertencia", "Fecha y descripción no pueden estar vacíos.")
        return

    with open(archivo_vaca, "a") as file:
        file.write(f"Fecha: {fecha}\nDescripción: {descripcion}\n---\n")
    
    messagebox.showinfo("Registro Clínico", "Registro agregado con éxito.")
    entry_fecha_clinica.delete(0, tk.END)
    entry_descripcion_clinica.delete(0, tk.END)
    actualizar_lista_registros_clinicos()

# Función para actualizar la lista de registros clínicos en el frame
def actualizar_lista_registros_clinicos():
    listbox_clinica.delete(0, tk.END)
    if os.path.exists(archivo_vaca):
        with open(archivo_vaca, "r") as file:
            registros = file.readlines()
        registros_completos = ["".join(registros[i:i+3]).strip() for i in range(0, len(registros), 3)]
        for registro in registros_completos:
            listbox_clinica.insert(tk.END, registro)
    else:
        listbox_clinica.insert(tk.END, "No hay registros clínicos.")

# Función para eliminar un registro clínico
def eliminar_registro_clinico():
    seleccion = listbox_clinica.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")
        return

    # Obtener el índice del registro seleccionado
    index = seleccion[0]

    # Leer todos los registros
    with open(archivo_vaca, "r") as file:
        registros = file.readlines()

    # Identificar el inicio y fin del registro seleccionado
    inicio = index * 3
    fin = inicio + 3

    # Eliminar el registro seleccionado
    del registros[inicio:fin]

    # Escribir de nuevo el archivo sin el registro eliminado
    with open(archivo_vaca, "w") as file:
        file.writelines(registros)

    messagebox.showinfo("Eliminar Registro", "Registro eliminado con éxito.")
    actualizar_lista_registros_clinicos()

# Función para la producción de la vaca
def produccion():
    nombre_vaca = simpledialog.askstring("Producción", "Ingrese el nombre o ID de la vaca:")
    if not nombre_vaca:
        return
    global archivo_produccion
    archivo_produccion = os.path.join(PRODUCCION_DIR, f"{nombre_vaca}.txt")
    label_produccion.config(text=f"--- Producción de {nombre_vaca} ---")
    mostrar_frame(frame_produccion)
    actualizar_lista_registros_produccion()

# Función para agregar un registro de producción en el mismo frame
def agregar_registro_produccion():
    fecha = entry_fecha_produccion.get()
    tipo = entry_tipo_produccion.get().lower()
    cantidad = entry_cantidad_produccion.get()

    if tipo not in ["leche", "carne", "doble proposito", "doble propósito"]:
        messagebox.showwarning("Advertencia", "Tipo de producción no válido. Intente nuevamente.")
        return

    if not fecha or not cantidad:
        messagebox.showwarning("Advertencia", "Fecha y cantidad no pueden estar vacíos.")
        return

    with open(archivo_produccion, "a") as file:
        file.write(f"Fecha: {fecha}\nTipo: {tipo.capitalize()}\nCantidad: {cantidad}\n---\n")

    messagebox.showinfo("Registro de Producción", "Registro de producción agregado con éxito.")
    entry_fecha_produccion.delete(0, tk.END)
    entry_tipo_produccion.delete(0, tk.END)
    entry_cantidad_produccion.delete(0, tk.END)
    actualizar_lista_registros_produccion()

# Función para actualizar la lista de registros de producción en el frame
def actualizar_lista_registros_produccion():
    listbox_produccion.delete(0, tk.END)
    if os.path.exists(archivo_produccion):
        with open(archivo_produccion, "r") as file:
            registros = file.readlines()
        registros_completos = ["".join(registros[i:i+3]).strip() for i in range(0, len(registros), 3)]
        for registro in registros_completos:
            listbox_produccion.insert(tk.END, registro)
    else:
        listbox_produccion.insert(tk.END, "No hay registros de producción.")

# Función para eliminar un registro de producción
def eliminar_registro_produccion():
    seleccion = listbox_produccion.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")
        return

    # Obtener el índice del registro seleccionado
    index = seleccion[0]

    # Leer todos los registros
    with open(archivo_produccion, "r") as file:
        registros = file.readlines()

    # Identificar el inicio y fin del registro seleccionado
    inicio = index * 3
    fin = inicio + 3

    # Eliminar el registro seleccionado
    del registros[inicio:fin]

    # Escribir de nuevo el archivo sin el registro eliminado
    with open(archivo_produccion, "w") as file:
        file.writelines(registros)

    messagebox.showinfo("Eliminar Registro", "Registro eliminado con éxito.")
    actualizar_lista_registros_produccion()

# Crear la interfaz principal
root = tk.Tk()
root.title("Sistema de Gestión de Vacas")

# Crear los frames para cada sección
frame_login = tk.Frame(root)
frame_menu_principal = tk.Frame(root)
frame_historia_clinica = tk.Frame(root)
frame_produccion = tk.Frame(root)

for frame in (frame_login, frame_menu_principal, frame_historia_clinica, frame_produccion):
    frame.grid(row=0, column=0, sticky='nsew')

# --- Frame Login ---    
tk.Label(frame_login, text="--- Iniciar Sesión ---").pack(pady=10)
tk.Button(frame_login, text="Registrar", command=registrar).pack(pady=5)
tk.Button(frame_login, text="Iniciar Sesión", command=login).pack(pady=5)
tk.Button(frame_login, text="Salir", command=root.quit).pack(pady=10)

# --- Frame Menú Principal ---    
tk.Label(frame_menu_principal, text="--- Menú Principal ---").pack(pady=10)
tk.Button(frame_menu_principal, text="Historia Clínica de la Vaca", command=historia_clinica).pack(pady=5)
tk.Button(frame_menu_principal, text="Producción", command=produccion).pack(pady=5)
tk.Button(frame_menu_principal, text="Cerrar", command=root.quit).pack(pady=10)

# --- Frame Historia Clínica ---    
label_historia_clinica = tk.Label(frame_historia_clinica, text="--- Historia Clínica ---")
label_historia_clinica.pack(pady=10)

# Campos para agregar registro clínico
tk.Label(frame_historia_clinica, text="Fecha (dd/mm/aaaa):").pack()
entry_fecha_clinica = tk.Entry(frame_historia_clinica)
entry_fecha_clinica.pack()

tk.Label(frame_historia_clinica, text="Descripción:").pack()
entry_descripcion_clinica = tk.Entry(frame_historia_clinica)
entry_descripcion_clinica.pack()

tk.Button(frame_historia_clinica, text="Agregar registro clínico", command=agregar_registro_clinico).pack(pady=5)
tk.Button(frame_historia_clinica, text="Eliminar registro clínico", command=eliminar_registro_clinico).pack(pady=5)

# Lista de registros clínicos
listbox_clinica = tk.Listbox(frame_historia_clinica, height=10, width=50)
listbox_clinica.pack(pady=5)

tk.Button(frame_historia_clinica, text="Volver al Menú Principal", command=lambda: mostrar_frame(frame_menu_principal)).pack(pady=10)

# --- Frame Producción ---    
label_produccion = tk.Label(frame_produccion, text="--- Producción ---")
label_produccion.pack(pady=10)

# Campos para agregar registro de producción
tk.Label(frame_produccion, text="Fecha (dd/mm/aaaa):").pack()
entry_fecha_produccion = tk.Entry(frame_produccion)
entry_fecha_produccion.pack()

tk.Label(frame_produccion, text="Tipo (leche, carne, doble propósito):").pack()
entry_tipo_produccion = tk.Entry(frame_produccion)
entry_tipo_produccion.pack() 

tk.Label(frame_produccion, text="Cantidad: para leche (litros), para carne (kg)").pack()
entry_cantidad_produccion = tk.Entry(frame_produccion)
entry_cantidad_produccion.pack()

tk.Button(frame_produccion, text="Agregar registro de producción", command=agregar_registro_produccion).pack(pady=5)
tk.Button(frame_produccion, text="Eliminar registro de producción", command=eliminar_registro_produccion).pack(pady=5)

# Lista de registros de producción
listbox_produccion = tk.Listbox(frame_produccion, height=10, width=50)
listbox_produccion.pack(pady=5)

tk.Button(frame_produccion, text="Volver al Menú Principal", command=lambda: mostrar_frame(frame_menu_principal)).pack(pady=10)

# Mostrar el frame de inicio de sesión al iniciar
mostrar_frame(frame_login)

root.mainloop()


