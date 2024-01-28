import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
import re


# Función para cargar archivo a leer
def cargar_archivo():
    archivo_path = filedialog.askopenfilename(title="Seleccionar archivo")  # Abre cuadro de dialogo para seleccionar archivo
    if archivo_path and os.path.isfile(archivo_path):  # Si se selecciono un archivo y la ruta del archivo es correcta, entonces
        txt_nombre_archivo.delete(1.0, tk.END)  # Elimina el contenido de este widget (txt_nombre_archivo), de inicio a fin
        txt_nombre_archivo.insert(tk.END, archivo_path)  # Inserta ruta del archivo al final del widget txt_nombre_archivo
        txt_nombre_archivo.see(tk.END)  # Ajusta la vista al final del texto


# Función para guardar archivo CSV resultante en un directorio deseado
def guardar_en():
    carpeta_path = filedialog.askdirectory(title="Seleccionar carpeta para guardar archivos CSV")  # Abre un cuadro de dialogo para seleccionar una carpeta. La ruta de la carpeta se almacena en carpeta_path
    if carpeta_path:  # Si se selecciono una carpeta, es decir, si la variable tiene valor, entonces:
        txt_ruta_guardado.delete(1.0, tk.END)  # Elimina el contenido de este widget (txt_ruta_guardado), de inicio a fin
        txt_ruta_guardado.insert(tk.END, carpeta_path)  # Inserta ruta del directorio seleccionado al final del widget txt_ruta_guardado
        txt_ruta_guardado.see(tk.END)


# Función en donde se realizan acciones en las etiquetas, creaciónde CSV y manejo de errores
def opciones_Realizar():
    # Obteniendo contenido de widgets, es decir, rutas de archivo cargado y de directorio de guardado
    archivo_path = txt_nombre_archivo.get(1.0, tk.END).strip()  # El .strip() elimina el espacio en blanco al principio o al final de la cadena.
    carpeta_path = txt_ruta_guardado.get(1.0, tk.END).strip()

    # Si cualquiera de los widgets no tiene contenido, es decir, si no hay ruta de archivo cargado o no hay ruta de directorio de guardado, entonces:
    if not archivo_path or not carpeta_path:
        messagebox.showerror("Error", "Por favor, seleccione el archivo a leer y la carpeta de destino de guardado.") # Da mensaje de error
        return

    # Creando manejo de errores
    try:
        # Abre cuadro de dialogo para nombrar y guardar el archivo CVS resultante en la carpeta elegida
        resultado_path = filedialog.asksaveasfilename(title="Guardar CSV", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if resultado_path:  # Si este widget tiene un valor, entonces
            opciones_seleccionadas = txt_opciones_usadas.get(1.0, tk.END).strip().split(", ")  # Variable que obtiene las opciones seleccionadas del widget txt_opciones_usadas, es decir, del boton Opciones
            opciones_mostrar = txt_mostrar_datos.get(1.0, tk.END).strip().split(", ")   # Nuevas opciones seleccionadas para mostrar
            resultado_path = resultado_path  # Se asegura de que el archivo tenga la extensión .csv

            # Creando error para FQDN, verificar si "fqdn" está presente en opciones_buscar
            if "fqdn" in opciones_seleccionadas:
                # Verificar si "ip-address", "subnet-mask" o "subnet-mask(variado)" están en opciones_mostrar
                opciones_invalidas = {"ip-address", "subnet-mask", "subnet-mask(variado)"} & set(opciones_seleccionadas)
                if opciones_invalidas: # Si esta alguna de estas opciones junto a fqdn, muestra error
                    raise ValueError(
                        f"Si selecciona 'fqdn' en 'Datos a buscar', no puede seleccionar '{', '.join(opciones_invalidas)}' en 'Datos a mostrar'.")

            # Se cargan parametros a la función procesar_archivo, este usara los sig.: ruta completa del archivo cargado (por eso el .strip), la variable opciones_seleccionadas, ruta con el nombre del archivo a guardar y la función opciones_mostrar)
            procesar_archivo(txt_nombre_archivo.get(1.0, tk.END).strip(), opciones_seleccionadas, resultado_path, opciones_mostrar)

            # Limpiando el texto de las etiquetas
            txt_nombre_archivo.delete(1.0, tk.END)
            txt_ruta_guardado.delete(1.0, tk.END)

            txt_opciones_usadas.config(state=tk.NORMAL)
            txt_opciones_usadas.delete(1.0, tk.END)
            txt_opciones_usadas.config(state=tk.DISABLED)

            txt_mostrar_datos.config(state=tk.NORMAL)
            txt_mostrar_datos.delete(1.0, tk.END)
            txt_mostrar_datos.config(state=tk.DISABLED)

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Se ha generado el archivo CSV correctamente: {resultado_path}")

    # Creando excepción para cualquier error
    except FileNotFoundError as e:
        messagebox.showinfo("Error", "No se encontro el archivo cargado")
    except ValueError as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")
        return


# Función para guardar las opciones usadas del botón Datos a buscar
def actualizar_opciones_usadas(opcion):  # Actualiza el contenido del widget txt_opciones_usadas y muestra las opciones usadas en la etiqueta opciones_usadas
    opciones_actuales = txt_opciones_usadas.get(1.0, tk.END).strip()  # Obtiene el contenido del widget txt_opciones_usadas y lo guarda en esta variable
    opciones_nuevas = f"{opciones_actuales}, {opcion}" if opciones_actuales else opcion  # Construye nueva cadena, usando el contenido de la variable opciones_actuales y le agrega la siguiente opción que el usuario escoja, separandolas por comas y un espacio
    txt_opciones_usadas.config(state=tk.NORMAL)  # Habilitar la modificación
    txt_opciones_usadas.delete(1.0, tk.END)  # Limpiar el contenido existente
    txt_opciones_usadas.insert(tk.END, opciones_nuevas)  # Insertar nuevas opciones
    txt_opciones_usadas.config(state=tk.DISABLED)  # Deshabilitar la modificación
    txt_opciones_usadas.see(tk.END)  # Ajusta la vista al final del texto


# Función para borrar las opciones usadas del botón Datos a buscar
def borrar_opciones_usadas():
    txt_opciones_usadas.config(state=tk.NORMAL)
    txt_opciones_usadas.delete(1.0, tk.END)
    txt_opciones_usadas.config(state=tk.DISABLED)


# Función para guardar las opciones usadas del botón Datos a mostrar
def actualizar_mostrar_datos(opcion): # Actualiza el contenido del widget txt_opciones_usadas y muestra las opciones usadas en la etiqueta opciones_usadas
    datos_actuales = txt_mostrar_datos.get(1.0, tk.END).strip()  # Obtiene el contenido del widget txt_opciones_usadas y lo guarda en esta variable
    datos_nuevos = f"{datos_actuales}, {opcion}" if datos_actuales else opcion  # Construye nueva cadena, usando el contenido de la variable opciones_actuales y le agrega la siguiente opción que el usuario escoja, separandolas por comas y un espacio
    txt_mostrar_datos.config(state=tk.NORMAL)  # Habilitar la modificación
    txt_mostrar_datos.delete(1.0, tk.END)  # Limpiar el contenido existente
    txt_mostrar_datos.insert(tk.END, datos_nuevos)  # Insertar nuevas opciones
    txt_mostrar_datos.config(state=tk.DISABLED)  # Deshabilitar la modificación
    txt_mostrar_datos.see(tk.END)  # Ajusta la vista al final del texto


# Función para borrar las opciones usadas en el botón Datos a mostrar
def borrar_mostrar_datos():
    txt_mostrar_datos.config(state=tk.NORMAL)
    txt_mostrar_datos.delete(1.0, tk.END)
    txt_mostrar_datos.config(state=tk.DISABLED)


# Función para mostrar mensaje de si desea salir del programa, si lo hace, termina el programa
def cerrar_ventana():
    respuesta = messagebox.askyesno("Salir", "¿Desea salir del programa?")
    if respuesta:
        ventana.destroy()


# Función que aplica la logica de procesamiento de datos para obtener los que desea obtener y mostrar el usuario
def procesar_archivo(archivo_path, opciones_seleccionadas, resultado_path, opciones_mostrar):
    with open(archivo_path, 'r', encoding='utf-8') as archivo:  # Abre archivo cargado en modo lectura
        datos = archivo.read()

    # Dividir datos por conjuntos (asumiendo que cada conjunto de datos comienza con 'edit')
    conjuntos = re.split(r'(?=edit)', datos)

    datos_procesados = []  # Lista que guarda datos deseados

    # Bucle que recorre los conjuntos de datos en busca de los datos deseados por el usuario
    for i, conjunto in enumerate(conjuntos):
        conjunto_dict = {}  # Diccionario que guarda los datos recopilados, ejemplo {"edit": "dato encontrado", "fqdn": "dato encontrado", etc}

        # Si "edit" esta dentro de la variable opciones_seleccionadas, entonces
        if "edit" in opciones_seleccionadas:
            match_edit = re.search(r'edit "(.*?)"', conjunto)  # Busca dato entre comillas con expresión regex, group(1)
            if match_edit:  # Si encuentra el dato
                conjunto_dict["edit"] = match_edit.group(1)  # Guarda en diccionario, nombre opción y dato encontrado entre comillas, ej. {"edit": "dato encontrado"}

        # Si "fqdn" esta dentro de la variable opciones_seleccionadas, entonces
        if "fqdn" in opciones_seleccionadas:
            match_type_fqdn = re.search(r'set type fqdn', conjunto)  # Busca que exista este dato en el conjunto de datos
            if match_type_fqdn:  # Si existe, entonces
                match_fqdn = re.search(r'set fqdn "(.*?)"', conjunto) # Busca dato entre comillas con expresión regex, group(1)
                if match_fqdn:  # Si existe, entonces
                    conjunto_dict["fqdn"] = match_fqdn.group(1) # Guarda en diccionario, nombre opción y dato encontrado entre comillas, ej. {"fqdn": "dato encontrado"}
                else:  # Si no existe, entonces
                    messagebox.showerror("Error", "No se encontro ningún FQDN")  # Mensaje de error

        # Si "color" esta dentro de la variable opciones_seleccionadas, entonces
        if "color" in opciones_seleccionadas:
            conjunto_dict["color"] = "black"  # Agrega directamente al diccionario {"color": "black"}

        # Si "comments" esta dentro de la variable opciones_seleccionadas, entonces
        if "comments" in opciones_seleccionadas:
            match_comments = re.search(r'set comment "(.*?)"', conjunto)  # Busca dato entre comillas con expresión regex, group(1)
            if match_comments:  # Si existe, entonces
                conjunto_dict["comments"] = match_comments.group(1)  # Guarda en diccionario, nombre opción y dato encontrado entre comillas, ej. {"comments": "dato encontrado"}
            else:  # Si no existe, entonces
                # Agregamos una entrada vacía para indicar la ausencia de comentarios
                conjunto_dict["comments"] = ""  # Guarda en diccionario, nombre opción y cadena vacia, ej. {"comments": ""}

        # Si "ip-address" esta dentro de la variable opciones_seleccionadas, entonces
        if "ip-address" in opciones_seleccionadas:
            match_subnet = re.search(r'set subnet (\d+\.\d+\.\d+\.\d+) \d+\.\d+\.\d+\.\d+', conjunto) # Busca dato entre parentesis con expresión regex, group(1)
            if match_subnet:  # Si existe, entonces
                conjunto_dict["ip-address"] = match_subnet.group(1)  # Guarda en diccionario, nombre opción y dato encontrado entre parentesis, ej. {"ip-address": "dato encontrado"}

        # Si "subnet-mask" esta dentro de la variable opciones_seleccionadas, entonces
        if "subnet-mask" in opciones_seleccionadas:
            match_subnet = re.search(r'set subnet (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', conjunto)  # Busca dato entre parentesis con expresión regex, aquí hay 2 datos, se necesita el segundo, group(2)
            if match_subnet:  # Si existe, entonces
                subnet_mask = match_subnet.group(2)  # Nueva variable guarda la mascara de red
                if subnet_mask == "255.255.255.255":  # Si la mascara es distinta de 255.255.255.255, entonces
                    conjunto_dict["subnet-mask"] = subnet_mask  # Guarda en diccionario, nombre opción y dato almacenado en variable, ej. {"subnet-mask": "dato encontrado"}

        # Si "subnet-mask(variado)" esta dentro de la variable opciones_seleccionadas, entonces
        if "subnet-mask(variado)" in opciones_seleccionadas:
            match_subnet_variado = re.search(r'set subnet (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', conjunto) # Busca dato entre parentesis con expresión regex, aquí hay 2 datos, se necesita el segundo, group(2)
            if match_subnet_variado:  # Si existe, entonces
                subnet_mask_variada = match_subnet_variado.group(2)  # Nueva variable guarda la mascara de red
                if subnet_mask_variada != "255.255.255.255":  # Si la mascara es distinta de 255.255.255.255, entonces
                    conjunto_dict["subnet-mask(variado)"] = subnet_mask_variada  # Guarda en diccionario, nombre opción y dato almacenado en variable, ej. {"subnet-mask(variado)": "dato encontrado"}

        # Verificar que todos los campos requeridos estén presentes
        if all(opcion in conjunto_dict for opcion in opciones_seleccionadas):
            datos_procesados.append(conjunto_dict) # Guarda los datos recopilados en la lista

    guardar_en_csv(datos_procesados, resultado_path, opciones_mostrar)  # La función guardar_en_csv usara estos datos


# Función para guardar los datos recopilados en un archivo CSV
def guardar_en_csv(datos, archivo_csv, opciones_mostrar):
    with open(archivo_csv, 'w', newline='') as archivo:  # Abre el nuevo archivo en blanco en modo escritura
        escritor_csv = csv.writer(archivo) # Escribe el archivo en formato CSV

        # Modificar la cabecera para mostrar "subnet-mask" en lugar de "subnet-mask(variado)"
        opciones_mostrar_cabecera = [opcion.replace("(variado)", "") for opcion in opciones_mostrar]
        escritor_csv.writerow(opciones_mostrar_cabecera)  # Escribe las cabeceras de las opciones almacenadas en opciones_mostrar

        # Bucle for que va a leer los datos procesados y los guardar en filas
        for conjunto in datos:
            fila = []  # Lista que almacena los datos procesados

            # Bucle que lee las cabeceras
            for opcion in opciones_mostrar_cabecera:
                # Si en opción esta "subnet-mask" y "subnet-mask(variado) dentro de los datos procesados, entonces
                if opcion == "subnet-mask" and "subnet-mask(variado)" in conjunto:
                    fila.append(conjunto["subnet-mask(variado)"])  # Agrega el valor de subnet-mask(variado)
                else:  # Si no
                    fila.append(conjunto.get(opcion, ''))  # Agrega el valor correspondiente o una cadena vacia

            escritor_csv.writerow(fila)  # Guarda los datos procesados en la lista


# Función para ordenar el diccionario y las claves
def _dict_to_list(diccionario, orden):
    return [diccionario.get(clave, '') for clave in orden]  # Devuelve lista con los valores ordenados, si no hay clave se agrega cadena vacia


if __name__ == "__main__":

    ventana = tk.Tk()  # Iniciando interfaz
    ventana.title("Convertor CSV")  # Nombrando interfaz

    ventana.geometry("550x380")  # Asignando tamaño de interfaz
    ventana.resizable(False, False)  # Evitando cambio de tamaño de interfaz

    # Creando botones los primeros botones
    # Botón para cargar archivo
    btn_cargar = tk.Button(ventana, text="Cargar archivo", command=cargar_archivo)
    btn_cargar.pack(pady=10, padx=20)

    # Botón para guardar archivo
    btn_guardar = tk.Button(ventana, text="Guardar archivos en", command=guardar_en)
    btn_guardar.pack(pady=10, padx=20)

    # Botón con menu de opciones para buscar datos en base a esas opciones, Datos a buscar
    mb_opciones = tk.Menubutton(ventana, text="Datos a buscar")
    mb_opciones.pack(pady=10, padx=20)

    # Creando menu de opciones del botón Datos a buscar
    submenu_opciones = tk.Menu(mb_opciones, tearoff=0) # Asignando menu de opciones a botón Datos a buscar
    submenu_opciones.add_command(label="edit", command=lambda: actualizar_opciones_usadas("edit"))  # Nombrando opciones y dandoles comandos
    submenu_opciones.add_command(label="fqdn", command=lambda: actualizar_opciones_usadas("fqdn"))
    submenu_opciones.add_command(label="ip-address", command=lambda: actualizar_opciones_usadas("ip-address"))
    submenu_opciones.add_command(label="subnet-mask", command=lambda: actualizar_opciones_usadas("subnet-mask"))
    submenu_opciones.add_command(label="subnet-mask(variado)", command=lambda: actualizar_opciones_usadas("subnet-mask(variado)"))
    submenu_opciones.add_command(label="color", command=lambda: actualizar_opciones_usadas("color"))
    submenu_opciones.add_command(label="comments", command=lambda: actualizar_opciones_usadas("comments"))
    mb_opciones["menu"] = submenu_opciones

    # Botón con menu de opciones para mostrar datos en base a esas opciones, Datos a mostrar
    mb_mostrar = tk.Menubutton(ventana, text="Datos a mostrar")
    mb_mostrar.pack(pady=10, padx=20)

    # Creando menu de opciones del botón Datos a mostrar
    submenu_mostrar = tk.Menu(mb_mostrar, tearoff=0)
    submenu_mostrar.add_command(label="edit", command=lambda: actualizar_mostrar_datos("edit"))
    submenu_mostrar.add_command(label="fqdn", command=lambda: actualizar_mostrar_datos("fqdn"))
    submenu_mostrar.add_command(label="ip-address", command=lambda: actualizar_mostrar_datos("ip-address"))
    submenu_mostrar.add_command(label="subnet-mask", command=lambda: actualizar_mostrar_datos("subnet-mask"))
    submenu_mostrar.add_command(label="color", command=lambda: actualizar_mostrar_datos("color"))
    submenu_mostrar.add_command(label="comments", command=lambda: actualizar_mostrar_datos("comments"))
    mb_mostrar["menu"] = submenu_mostrar

    # Creando contenedores para etiquetas y creando etiquetas
    # Creando contenedor para etiqueta de archivo_cargado
    contenedor_archivo_cargado = tk.Frame(ventana)
    contenedor_archivo_cargado.pack(pady=5, fill=tk.X, anchor=tk.W)

    # Creando etiqueta de archivo_cargado
    etiqueta_archivo_cargado = tk.Label(contenedor_archivo_cargado, text="Archivo cargado:")
    etiqueta_archivo_cargado.pack(side=tk.LEFT, fill=tk.X)

    # Mostrando texto en etiqueta archivo_cargado
    txt_nombre_archivo = tk.Text(contenedor_archivo_cargado, height=1, width=40, wrap=tk.NONE)
    txt_nombre_archivo.pack(side=tk.LEFT, fill=tk.X)

    # Creando contenedor para etiqueta de ruta_guardado
    contenedor_ruta_guardado = tk.Frame(ventana)
    contenedor_ruta_guardado.pack(pady=5, fill=tk.X, anchor=tk.W)

    # Creando etiqueta de ruta_guardado
    etiqueta_ruta_guardado = tk.Label(contenedor_ruta_guardado, text="Ruta de Guardado:")
    etiqueta_ruta_guardado.pack(side=tk.LEFT, fill=tk.X)

    # Mostrando texto en etiqueta ruta_guardado
    txt_ruta_guardado = tk.Text(contenedor_ruta_guardado, height=1, width=40, wrap=tk.NONE)
    txt_ruta_guardado.pack(side=tk.LEFT, fill=tk.X)

    # Creando contenedor para etiqueta de opciones_usadas
    contenedor_opciones_usadas = tk.Frame(ventana)
    contenedor_opciones_usadas.pack(pady=5, fill=tk.X, anchor=tk.W)

    # Creando etiqueta de opciones_usadas
    etiqueta_opciones_usadas = tk.Label(contenedor_opciones_usadas, text="Opciones usadas:")
    etiqueta_opciones_usadas.pack(side=tk.LEFT, fill=tk.X)

    # Mostrando texto en etiqueta opciones_usadas
    txt_opciones_usadas = tk.Text(contenedor_opciones_usadas, height=1, width=40, wrap=tk.NONE, state=tk.DISABLED)
    txt_opciones_usadas.pack(side=tk.LEFT, fill=tk.X)

    # Creando un botón para etiqueta opciones_usadas, borrar opciones
    btn_borrar_opciones = tk.Button(contenedor_opciones_usadas, text="Borrar Opciones", command=borrar_opciones_usadas)
    btn_borrar_opciones.pack(side=tk.LEFT, padx=10)

    # Creando contenedor para etiqueta de mostrar_datos
    contenedor_mostrar_datos = tk.Frame(ventana)
    contenedor_mostrar_datos.pack(pady=5, fill=tk.X, anchor=tk.W)

    # Creando etiqueta de mostar_opciones
    etiqueta_mostrar_datos = tk.Label(contenedor_mostrar_datos, text="Mostrar en CSV:")
    etiqueta_mostrar_datos.pack(side=tk.LEFT, fill=tk.X)

    # Mostrando texto en etiqueta mostrar_opciones
    txt_mostrar_datos = tk.Text(contenedor_mostrar_datos, height=1, width=40, wrap=tk.NONE, state=tk.DISABLED)
    txt_mostrar_datos.pack(side=tk.LEFT, fill=tk.X)

    # Creando botón para etiqueta mostrar_opciones
    btn_borrar_mostrar_datos = tk.Button(contenedor_mostrar_datos, text="Borrar Opciones", command=borrar_mostrar_datos)
    btn_borrar_mostrar_datos.pack(side=tk.LEFT, padx=10)

    # Creando botón para iniciar proceso de creación de CSV
    btn_iniciar = tk.Button(ventana, text="Generar CSV", command=opciones_Realizar)
    btn_iniciar.pack(pady=10)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)  # metodo para cerrar la ventana de manera correcta

    ventana.mainloop()  # Creando bucle para la interfaz
