import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os
from datetime import datetime, timedelta

LIBROS_JSON = "libros.json"
USUARIO_JSON = "usuario.json"

class Libro:
    
    Lista_libros = []

    def __init__(self, titulo, codigo, autor, genero, categoria, editorial, anio_publicacion):
        self.titulo = titulo
        self.codigo = codigo
        self.autor = autor
        self.categoria = categoria
        self.genero = genero
        self.editorial = editorial
        self.anio_publicacion = anio_publicacion
        self.disponible = True
        Libro.Lista_libros.append(self)

    @classmethod
    def cargar_libros(cls):
        if os.path.exists(LIBROS_JSON):
            with open(LIBROS_JSON, "r") as file:
                data = json.load(file)
                for libro_data in data:
                    Libro(
                        libro_data["titulo"],
                        libro_data["codigo"],
                        libro_data["autor"],
                        libro_data["categoria"],
                        libro_data["genero"],
                        libro_data["editorial"],
                        libro_data["anio_publicacion"]
                    )
        return Libro.Lista_libros

    @classmethod
    def guardar_libros(cls):
        data = []
        for libro in Libro.Lista_libros:
            data.append({
                "titulo": libro.titulo,
                "codigo": libro.codigo,
                "autor": libro.autor,
                "categoria": libro.categoria,
                "genero": libro.genero,
                "editorial": libro.editorial,
                "anio_publicacion": libro.anio_publicacion
            })
        with open(LIBROS_JSON, "w") as file:
            json.dump(data, file, indent=4)

class Usuario:
    
    Lista_usuario = []

    def __init__(self, id_usuario, nombre, email):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        Usuario.Lista_usuario.append(self)

    @classmethod
    def cargar_usuarios(cls):
        if os.path.exists(USUARIO_JSON):
            with open(USUARIO_JSON, "r") as archivo:
                data = json.load(archivo)
                for usuario_data in data:
                    Usuario(
                        usuario_data["id_usuario"],
                        usuario_data["nombre"],
                        usuario_data["email"],
                    )
        return Usuario.Lista_usuario

    @classmethod
    def guardar_usuarios(cls):
        data = []
        for usuario in Usuario.Lista_usuario:
            data.append({
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "email": usuario.email,
            })
        with open(USUARIO_JSON, "w") as archivo:
            json.dump(data, archivo, indent=4)

class Biblioteca:
    
    def __init__(self):
        self.prestamos = []
        
    def realizar_prestamo(self, libro, usuario, fecha):
        libro.disponible = False
        self.prestamos.append((libro, usuario, fecha))
        Libro.guardar_libros()

class SistemaBibliotecaApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.centrar_ventana(self.root, 1400, 650)
        
        Libro.cargar_libros()
        Usuario.cargar_usuarios()
        
        self.biblioteca = Biblioteca()
        self.pantalla_principal()
        
    def centrar_ventana(self, ventana, ancho, alto):
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
       
    def pantalla_principal(self):
        self.root.iconbitmap("iconobiblioteca.ico")
        self.root.configure(bg="white")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Botondepantallaprincipal.TButton", background="antiquewhite", foreground="black", font=("Arial", 10, "bold"))
        style.configure("Botondepantallasecundaria.TButton", background="wheat3", foreground="black", font=("Arial", 10, "bold"))
        
        tk.Label(self.root, text="Sistema de Biblioteca", font=("Arial", 24, "bold"), bg="antiquewhite", fg="black").pack(pady=28)

        image = Image.open("biblioteca.png")
        image = image.resize((1400, 650), Image.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(image)

        label_imagen = tk.Label(self.root, image=imagen_tk)
        label_imagen.image = imagen_tk
        label_imagen.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        label_imagen.lower()

        frame_botones = tk.Frame(self.root, bg="", padx=10, pady=10)
        frame_botones.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        botones = [
            ("Lista de Usuarios", self.mostrar_lista_usuarios),
            ("Lista de Libros", self.mostrar_lista_libros),
            ("Buscar Usuario", self.buscar_usuario),
            ("Búsqueda Avanzada", self.buscar_avanzado),
            ("Realizar Préstamo", self.realizar_prestamo),
            ("Registrar Devolución", self.registrar_devolucion),
            ("Administrar Catálogo", self.administrar_catalogo),
        ]

        for texto, comando in botones:
            ttk.Button(frame_botones, text=texto, command=comando, style="Botondepantallaprincipal.TButton").pack(pady=15)

        ttk.Button(self.root, text="Salir", command=self.salir, style="Botondepantallaprincipal.TButton").pack(side=tk.BOTTOM, pady=15)
        
    def mostrar_lista_usuarios(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Lista de Usuarios")
        self.centrar_ventana(ventana, 600, 450)
        ventana.configure(bg="antiquewhite")
        
        ventana.iconbitmap("usuarioicono.ico")
        
        tk.Label(ventana, text="Lista de Usuarios", font=("Arial", 18, "bold", "underline"), bg="antiquewhite", fg="black").pack(pady=20)
        
        frame_texto = tk.Frame(ventana)
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10)
        
        scrollbar_y = tk.Scrollbar(frame_texto, orient=tk.VERTICAL)
        texto = tk.Text(frame_texto, height=20, width=50, wrap=tk.NONE, yscrollcommand=scrollbar_y.set)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y.config(command=texto.yview)
        
        usuarios = Usuario.Lista_usuario
        
        if not usuarios:
            texto.insert(tk.END, "No hay usuarios registrados.\n")
        else:
            texto.insert(tk.END, f"{'ID':<10}{'Nombre':<25}{'Correo':<30}\n")
            texto.insert(tk.END, "-" * 70 + "\n")
            for usuario in usuarios:
                id_usuario = getattr(usuario, "id_usuario","")
                nombre = getattr(usuario, "nombre","")
                email = getattr(usuario, "email","")
                texto.insert(tk.END, f"{id_usuario:<10}{nombre:<25}{email:<30}\n")
                
        texto.config(state=tk.DISABLED)
        
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy, style="Botondepantallasecundaria.TButton").pack(pady=10)
        
    def mostrar_lista_libros(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Lista de Libros")
        self.centrar_ventana(ventana, 1250, 550)
        ventana.configure(bg="antiquewhite")
        
        ventana.iconbitmap("estanteicono.ico")

        tk.Label(ventana, text="Lista de Libros", font=("Arial", 18, "bold", "underline"), bg="antiquewhite", fg="black").pack(pady=20)

        frame_texto = tk.Frame(ventana)
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10)

        scrollbar_y = tk.Scrollbar(frame_texto, orient=tk.VERTICAL)
        texto = tk.Text(frame_texto, height=20, width=140, wrap=tk.NONE, yscrollcommand=scrollbar_y.set)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y.config(command=texto.yview)

        libros = Libro.Lista_libros
        if not libros:
            texto.insert(tk.END, "No hay libros disponibles.\n")
        else:
            texto.insert(tk.END, f"{'Código':<10} {'Título':<60} {'Autor':<30} {'Genero':<25} {'Estado':<10}\n")
            texto.insert(tk.END, "-" * 151 + "\n")
            for libro in libros:
                codigo = getattr(libro, "codigo", "")
                titulo = getattr(libro, "titulo", "")
                autor = getattr(libro, "autor", "")
                categoria = getattr(libro, "categoria", "")
                editorial = getattr(libro, "editorial", "")
                estado = "Disponible" if getattr(libro, "disponible", True) else "Prestado"

                texto.insert(tk.END, f"{codigo:<10} {titulo:<60} {autor:<30} {categoria:<25}  {estado:<10}\n")

        texto.config(state=tk.DISABLED)

        ttk.Button(ventana, text="Cerrar", command=ventana.destroy, style="Botondepantallasecundaria.TButton").pack(pady=20)

    def buscar_usuario(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Buscar Usuario")
        self.centrar_ventana(ventana, 500, 450)
        ventana.configure(bg="antiquewhite")
        
        ventana.iconbitmap("usuarioicono.ico")
        
        tk.Label(ventana, text="Buscar Usuario", font=("Arial", 18, "bold", "underline"), bg="antiquewhite", fg="black").pack(pady=20)

        tk.Label(ventana, text="Nombre del Usuario:", font=("Arial", 12), bg="antiquewhite").pack()
        entrada_busqueda = tk.Entry(ventana, font=("Arial", 12))
        entrada_busqueda.pack(pady=10)

        frame_resultado = tk.Frame(ventana)
        frame_resultado.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar_y = tk.Scrollbar(frame_resultado, orient=tk.VERTICAL)
        resultado_texto = tk.Text(frame_resultado, height=10, width=55, wrap=tk.WORD, yscrollcommand=scrollbar_y.set, font=("Arial", 11), bg="white")
        scrollbar_y.config(command=resultado_texto.yview)

        resultado_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        resultado_texto.config(state=tk.DISABLED)

        def realizar_busqueda():
            texto = entrada_busqueda.get().lower()
            coincidencias = [
                usuario for usuario in Usuario.Lista_usuario if texto in usuario.nombre.lower()
            ]

            resultado_texto.config(state=tk.NORMAL)
            resultado_texto.delete(1.0, tk.END)

            if coincidencias:
                for usuario in coincidencias:
                    resultado_texto.insert(tk.END, f"🪪 ID: {usuario.id_usuario}\n")
                    resultado_texto.insert(tk.END, f"👤 Nombre: {usuario.nombre}\n")
                    resultado_texto.insert(tk.END, f"📧 Correo: {usuario.email}\n")
                    resultado_texto.insert(tk.END, "-" * 40 + "\n")
            else:
                resultado_texto.insert(tk.END, "❌ No se encontró ningún usuario.")

            resultado_texto.config(state=tk.DISABLED)

        # Botones
        ttk.Button(ventana, text="Buscar", command=realizar_busqueda, style="Botondepantallasecundaria.TButton").pack(pady=5)
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy, style="Botondepantallasecundaria.TButton").pack(pady=10)
        
    def buscar_avanzado(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Búsqueda Avanzada")
        self.centrar_ventana(ventana, 1350, 450)
        ventana.configure(bg="antiquewhite")
        
        ventana.iconbitmap("estanteicono.ico")

        tk.Label(ventana, text="Buscar Libro", font=("Arial", 18, "bold", "underline"),
                bg="antiquewhite").pack(pady=20)

        frame = tk.Frame(ventana, bg="antiquewhite")
        frame.pack(pady=10)

        # Campos alineados horizontalmente
        campos = [
            ("titulo", "Título"), ("codigo", "Código"), ("autor", "Autor"),
            ("categoria", "Género"), ("genero", "Categoría"), ("editorial", "Editorial"), ("anio", "Año")
        ]
        entradas = {}

        for i, (clave, etiqueta) in enumerate(campos):
            col = i * 2
            tk.Label(frame, text=etiqueta + ":", bg="antiquewhite", font=("Arial", 10)).grid(
                row=0, column=col, padx=5, pady=5, sticky="e")
            entrada = tk.Entry(frame, width=15, font=("Arial", 10))
            entrada.grid(row=0, column=col + 1, padx=5, pady=5)
            entradas[clave] = entrada

        # Área de resultados
        result_frame = tk.Frame(ventana)
        result_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(result_frame)
        result_text = tk.Text(result_frame, height=12, width=160, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        scrollbar.config(command=result_text.yview)

        result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def filtrar_libros():
            criterios = {k: entradas[k].get().lower() for k in entradas}
            result_text.delete("1.0", tk.END)
            encontrados = []

            for libro in Libro.Lista_libros:
                if (
                    (criterios["titulo"] and criterios["titulo"] in libro.titulo.lower()) or
                    (criterios["codigo"] and criterios["codigo"] in libro.codigo.lower()) or
                    (criterios["autor"] and criterios["autor"] in libro.autor.lower()) or
                    (criterios["genero"] and criterios["genero"] in libro.genero.lower()) or
                    (criterios["categoria"] and criterios["categoria"] in libro.categoria.lower()) or
                    (criterios["editorial"] and criterios["editorial"] in libro.editorial.lower()) or
                    (criterios["anio"] and criterios["anio"] in str(libro.anio_publicacion))
                ):
                    estado = "Disponible" if libro.disponible else "Prestado"
                    encontrados.append(
                        f"📚 Título: {libro.titulo}\n"
                        f"📘 Código: {libro.codigo}\n"
                        f"✍ Autor: {libro.autor}\n"
                        f"🎭 Género: {libro.categoria}\n"
                        f"📖 Categoría:{libro.genero}\n"
                        f"🏢 Editorial: {libro.editorial}\n"
                        f"📅 Año: {libro.anio_publicacion}\n"
                        f"📌 Estado: {estado}\n"
                        f"{'-'*80}\n"
                    )

            if encontrados:
                result_text.insert(tk.END, "\n".join(encontrados))
            else:
                result_text.insert(tk.END, "❌ No se encontraron libros con esos criterios.")

        ttk.Button(ventana, text="Buscar", command=filtrar_libros,
                style="Botondepantallasecundaria.TButton").pack(pady=5)
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy,
                style="Botondepantallasecundaria.TButton").pack(pady=5)
        
    def realizar_prestamo(self):
        ventana=tk.Toplevel(self.root)
        ventana.title("Realizar Préstamo")
        self.centrar_ventana(ventana, 400, 350)
        ventana.configure(bg="antiquewhite")
        
        ventana.iconbitmap("librosicono.ico")
        
        tk.Label(ventana, text="Préstamo", font=("Arial", 18, "bold", "underline"), bg="antiquewhite").pack(pady=20)
        
        tk.Label(ventana, text="ID de Usuario", font=("Arial", 12, "bold"), bg="antiquewhite").pack(pady=5)
        user_id_entry = ttk.Entry(ventana)
        user_id_entry.pack(pady=10)
        
        tk.Label(ventana, text="Código del Libro", font=("Arial", 12, "bold"), bg="antiquewhite").pack(pady=5)
        book_code_entry = ttk.Entry(ventana)
        book_code_entry.pack(pady=10)
        
        def procesar_prestamo():
            user_id = user_id_entry.get()
            book_code = book_code_entry.get()
            
            usuario = next((u for u in Usuario.Lista_usuario if u.id_usuario == user_id), None)
            libro = next((l for l in Libro.Lista_libros if l.codigo == book_code), None)
            
            if not usuario or not libro:
                messagebox.showerror("Error", "Usuario o Libro no encontrado.")
                return
    
            if not libro.disponible:
                if libro.fecha_devolucion and datetime.now() > libro.fecha_devolucion:
                    dias_retraso = (datetime.now() - libro.fecha_devolucion).days
                    messagebox.showwarning("Retraso", f"El libro '{libro.titulo}' esta retrasado {dias_retraso} dias desde su fecha de devolucion.")
                else:
                    messagebox.showwarning("Advertencia", "El libro ya esta prestado.")
                return
            
            fecha_prestamo = datetime.now()
            fecha_devolucion = fecha_prestamo + timedelta(days=7)
            libro.disponible = False
            libro.fecha_prestamo = fecha_prestamo
            libro.fecha_devolucion = fecha_devolucion
            self.prestamos.append((libro, usuario, fecha_devolucion))
            
            messagebox.showinfo("Éxito", f"Préstamo realizado para el libro '{libro.titulo}' a {usuario.nombre}.")
            ventana.destroy()
            
        ttk.Button(ventana, text="Realizar Préstamo", command=procesar_prestamo, style="Botondepantallasecundaria.TButton").pack(pady=10)
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy, style="Botondepantallasecundaria.TButton").pack(pady=10)
        
    def registrar_devolucion(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Devolución")
        self.centrar_ventana(ventana, 300, 200)
        ventana.configure(bg="antiquewhite")
        
        ventana.iconbitmap("librosicono.ico")
        
        tk.Label(ventana, text="Código del Libro", font=("Arial", 18, "bold", "underline"), bg="antiquewhite").pack(pady=10)
        book_code_entry = tk.Entry(ventana)
        book_code_entry.pack(pady=10)
        
        def procesar_devolucion():
            book_code = book_code_entry.get()
            
            libro = next((l for l in Libro.Lista_libros if l.codigo == book_code), None)
            
            if not libro:
                messagebox.showerror("Error", "Libro no encontrado.")
                return
            if not libro.fecha_devolucion:
                messagebox.showwarning("Advertencia", "El libro no tiene una fecha de devolución registrada.")
            elif datetime.now() > libro.fecha_devolucion:
                dias_retraso = (datetime.now() - libro.fecha_devolucion).days
                multa = dias_retraso * 1 
                messagebox.showwarning("Penalizacion", f"El libro '{libro.titulo}' esta retrasado {dias_retraso} dias desde su fecha de devolucion. \nSe le aplicara una multa de ${multa}.")
            else:
                messagebox.showinfo("Éxito", f"Devolución registrada para el libro '{libro.titulo}'.")
    
            libro.disponible = True
            libro.fecha_devolucion = None
            libro.fecha_prestamo = None
            libro.guardar_libros()
            ventana.destroy()
            
        ttk.Button(ventana, text="Registrar Devolución", command=procesar_devolucion, style="Botondepantallasecundaria.TButton").pack(pady=10)
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy, style="Botondepantallasecundaria.TButton").pack(pady=10)
    
    def administrar_catalogo(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Administrar Catálogo de Libros")
        self.centrar_ventana(ventana, 500, 550)
        ventana.configure(bg="antiquewhite")
        
        ventana.iconbitmap("estanteicono.ico")

        tk.Label(ventana, text="Administrar Catálogo", font=("Arial", 18, "bold", "underline"), bg="antiquewhite").pack(pady=10)

        def abrir_ventana_agregar():
            win = tk.Toplevel(ventana)
            win.title("Agregar Libro")
            self.centrar_ventana(win, 400, 400)
            win.configure(bg="antiquewhite")
            
            win.iconbitmap("librosicono.ico")  # Icono de la ventana agregar libro

            tk.Label(win, text="Agregar Libro", font=("Arial", 14, "bold", "underline"), bg="antiquewhite").pack(pady=10)
            frame = tk.Frame(win, bg="antiquewhite")
            frame.pack(pady=10)

            campos = {
                "Título": tk.StringVar(),
                "Autor": tk.StringVar(),
                "Categoría": tk.StringVar(),
                "Genero": tk.StringVar(),
                "Editorial": tk.StringVar(),
                "Año de Publicación": tk.StringVar()
            }

            for i, (label, var) in enumerate(campos.items()):
                ttk.Label(frame, text=f"{label}:").grid(row=i, column=0, sticky="e", padx=5, pady=2)
                ttk.Entry(frame, textvariable=var).grid(row=i, column=1, padx=5)

            def generar_codigo_personalizado(titulo):
                palabras = titulo.strip().split()
                if len(palabras) == 1:
                    prefijo = palabras[0][:3].upper()
                else:
                    prefijo = ''.join(p[0].upper() for p in palabras[:2])
                contador = 1
                codigos_existentes = [libro.codigo for libro in Libro.Lista_libros if libro.codigo.startswith(prefijo)]
                while True:
                    codigo = f"{prefijo}{contador:03d}"
                    if codigo not in codigos_existentes:
                        return codigo
                    contador += 1

            def guardar_libro():
                datos = {k: v.get().strip() for k, v in campos.items()}
                if not all(datos.values()):
                    messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios.")
                    return

                codigo = generar_codigo_personalizado(datos["Título"])
                if any(libro.codigo == codigo for libro in Libro.Lista_libros):
                    messagebox.showerror("Duplicado", "Ya existe un libro con ese código.")
                    return

                nuevo_libro = Libro(
                    datos["Título"],
                    codigo,
                    datos["Autor"],
                    datos["Genero"],
                    datos["Categoría"],
                    datos["Editorial"],
                    datos["Año de Publicación"]
                )

                Libro.Lista_libros.append(nuevo_libro)
                Libro.guardar_libros()
                messagebox.showinfo("Éxito", "Libro agregado correctamente.")
                win.destroy()

            ttk.Button(win, text="Guardar Libro", command=guardar_libro, style="Botondepantallasecundaria.TButton").pack(pady=15)

        ttk.Button(ventana, text="Agregar Libro", command=abrir_ventana_agregar, style="Botondepantallasecundaria.TButton").pack(pady=10)

        # Eliminar libros
        tk.Label(ventana, text="Eliminar Libro", font=("Arial", 12, "bold", "underline"), bg="antiquewhite").pack(pady=10)
        frame_eliminar = tk.Frame(ventana)
        frame_eliminar.pack()

        tk.Label(frame_eliminar, text="Código:", bg="antiquewhite", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        eliminar_entry = tk.Entry(frame_eliminar)
        eliminar_entry.grid(row=0, column=1, padx=5, pady=5)

        def eliminar_libro():
            codigo = eliminar_entry.get().strip()
            for libro in Libro.Lista_libros:
                if libro.codigo == codigo:
                    Libro.Lista_libros.remove(libro)
                    Libro.guardar_libros()
                    messagebox.showinfo("Eliminado", f"Libro '{libro.titulo}' eliminado.")
                    eliminar_entry.delete(0, tk.END)
                    return
            messagebox.showerror("No encontrado", "Libro no encontrado.")

        ttk.Button(ventana, text="Eliminar Libro", command=eliminar_libro, style="Botondepantallasecundaria.TButton").pack(pady=10)

        # Editar libros
        tk.Label(ventana, text="Editar Libro", font=("Arial", 12, "bold", "underline"), bg="antiquewhite").pack(pady=10)
        frame_editar = tk.Frame(ventana, bg="antiquewhite")
        frame_editar.pack(pady=5)

        tk.Label(frame_editar, text="Código:", bg="antiquewhite", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        editar_codigo_entry = ttk.Entry(frame_editar)
        editar_codigo_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_editar, text="Nuevo Título:", bg="antiquewhite", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5)
        nuevo_titulo_entry = ttk.Entry(frame_editar)
        nuevo_titulo_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_editar, text="Nueva Categoría:", bg="antiquewhite", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=5)
        nueva_categoria_entry = ttk.Entry(frame_editar)
        nueva_categoria_entry.grid(row=2, column=1, padx=5, pady=5)

        def editar_libro():
            codigo = editar_codigo_entry.get().strip()
            nuevo_titulo = nuevo_titulo_entry.get().strip()
            nueva_categoria = nueva_categoria_entry.get().strip()

            libro = next((l for l in Libro.Lista_libros if l.codigo == codigo), None)
            if not libro:
                messagebox.showerror("Error", "Libro no encontrado.")
                return

            if nuevo_titulo:
                libro.titulo = nuevo_titulo
            if nueva_categoria:
                libro.categoria = nueva_categoria

            Libro.guardar_libros()
            messagebox.showinfo("Éxito", "Libro editado correctamente.")
            editar_codigo_entry.delete(0, tk.END)
            nuevo_titulo_entry.delete(0, tk.END)
            nueva_categoria_entry.delete(0, tk.END)

        ttk.Button(ventana, text="Editar Libro", command=editar_libro, style="Botondepantallasecundaria.TButton").pack(pady=10)

        ttk.Button(ventana, text="Cerrar", command=ventana.destroy, style="Botondepantallasecundaria.TButton").pack(pady=10)

    def salir(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaBibliotecaApp(root)
    root.mainloop()