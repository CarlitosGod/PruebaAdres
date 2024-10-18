from PyPDF2 import PdfReader
import re
import sqlite3
import os

# Expresión regular para extraer el CUFE
CUFE_REGEX = r'\b([0-9a-fA-F]\n*){95,100}\b'

conn = sqlite3.connect('facturas.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_archivo TEXT,
    numero_paginas INTEGER,
    cufe TEXT,
    peso REAL
)
''')

def leer_pdf_local(ruta_archivo):
    try:
        with open(ruta_archivo, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            num_pages = len(reader.pages)
            text = ''
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            
            # Buscar el CUFE usando la expresión regular
            match = re.search(CUFE_REGEX, text)
            cufe = match.group(0) if match else None
            
            # Obtener el peso del archivo en MB
            peso = os.path.getsize(ruta_archivo) / (1024 * 1024)
            
            return num_pages, cufe, peso

    except Exception as e:
        print(f"Error al leer el PDF: {ruta_archivo}. Detalle: {e}")
        return 0, None, 0  
    
# Carpeta donde están los archivos PDF--------------------------------------------------------------------------------------------
carpeta_archivos = r'C:\Users\carlo\Documents\PruebaAdres\Cap2\archivos' 

# Usar os para listar y procesar cada archivo PDF en la carpeta
for archivo in os.listdir(carpeta_archivos):
    # Verificar que el archivo sea un PDF
    if archivo.endswith('.PDF'):

        ruta_archivo = os.path.join(carpeta_archivos, archivo)  
        print("Ruta: " + ruta_archivo)
        num_pages, cufe, peso = leer_pdf_local(ruta_archivo)

        # Mensajes de depuración
        print(f"Archivo: {archivo}, Número de páginas: {num_pages}, CUFE: {cufe}, Peso: {peso:.2f} MB")
        
        if num_pages > 0 and cufe: 
            # Insertar los datos en la base de datos
            cursor.execute('''
            INSERT INTO facturas (nombre_archivo, numero_paginas, cufe, peso)
            VALUES (?, ?, ?, ?)
            ''', (archivo, num_pages, cufe, peso))
            print(f"Datos de {archivo} guardados en la base de datos.")
        else:
            print(f"No se guardaron los datos para {archivo} porque no se obtuvo CUFE.")

conn.commit()
conn.close()

print("Extracción de CUFE completada y almacenada en la base de datos.")
