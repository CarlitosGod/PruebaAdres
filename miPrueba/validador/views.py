
import csv
from io import TextIOWrapper
from django.shortcuts import render
import re
from django.http import HttpResponse

# a. El archivo solo debe permitir las 5 columnas, si existen más o menos
# deberá alertar al usuario
# b. Columna 1: Solo debe permitir números enteros entre 3 y 10 caracteres
# c. Columna 2: Solo debe permitir correos electrónicos
# d. Columna 3: Solo debe permitir los valores “CC” o “TI”
# e. Columna 4: Solo debe permitir valores entre 500000 y 1500000
# f. Columna 5: Permite cualquier valor


# def index(request):

#     return render(request, 'index.html')


# def index(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         decoded_file = TextIOWrapper(file.file, encoding='utf-8')

#         # Leer el archivo CSV
#         reader = csv.reader(decoded_file, delimiter=',')
#         documento = []
        
#         # Crear un diccionario con las columnas: ID, Email, Tipo de Documento, Valor, Epígrafe
#         for row in reader:
#             documento.append({
#                 'id': row[0],
#                 'email': row[1],
#                 'tipo_doc': row[2],
#                 'valor': row[3],
#                 'epigrafe': row[4]
#             })

#         return render(request, 'index.html', {'documento': documento})
    
#     return render(request, 'index.html')


def index(request):
    errors = []
    documento = []

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        decoded_file = TextIOWrapper(file.file, encoding='utf-8')

        reader = csv.reader(decoded_file, delimiter=',')
        
        for line_number, row in enumerate(reader, start=1):
            # Validar si la cantidad de columnas es exactamente 5
            if len(row) != 5:
                errors.append(f"La línea {line_number} no tiene 5 columnas.")
                continue
            
            # Validaciones específicas para cada columna
            id_val, email, tipo_doc, valor, epigrafe = row

            # a. Columna 1: ID debe ser un número entero entre 3 y 10 caracteres
            if not (id_val.isdigit() and 3 <= len(id_val) <= 10):
                errors.append(f"Error en línea {line_number}: El ID '{id_val}' debe ser un número entre 3 y 10 caracteres.")
                continue

            # b. Columna 2: Validación de correo electrónico
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append(f"Error en línea {line_number}: El correo '{email}' no es válido.")
                continue

            # c. Columna 3: Validación del tipo de documento (CC o TI)
            if tipo_doc not in ['CC', 'TI']:
                errors.append(f"Error en línea {line_number}: El tipo de documento '{tipo_doc}' debe ser 'CC' o 'TI'.")
                continue

            # d. Columna 4: Validar que el valor esté entre 500000 y 1500000
            try:
                valor_int = int(valor)
                if not (500000 <= valor_int <= 1500000):
                    errors.append(f"Error en línea {line_number}: El valor '{valor}' debe estar entre 500000 y 1500000.")
                    continue
            except ValueError:
                errors.append(f"Error en línea {line_number}: El valor '{valor}' no es un número válido.")
                continue

            # Si todo es válido, agregar a la lista de documentos
            documento.append({
                'id': id_val,
                'email': email,
                'tipo_doc': tipo_doc,
                'valor': valor,
                'epigrafe': epigrafe
            })

    # Siempre devolver la tabla de documentos aunque existan errores
    return render(request, 'index.html', {'errors': errors, 'documento': documento})


# def index(request):
#     errors = []
#     documento = []

#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         decoded_file = TextIOWrapper(file.file, encoding='utf-8')

#         reader = csv.reader(decoded_file, delimiter=',')
        
#         for line_number, row in enumerate(reader, start=1):
#             # Validar si la cantidad de columnas es exactamente 5
#             if len(row) != 5:
#                 errors.append(f"La línea {line_number} no tiene 5 columnas.")
#                 continue
            
#             # Validaciones específicas para cada columna
#             id_val, email, tipo_doc, valor, epigrafe = row

#             # a. Columna 1: ID debe ser un número entero entre 3 y 10 caracteres
#             if not (id_val.isdigit() and 3 <= len(id_val) <= 10):
#                 errors.append(f"Error en línea {line_number}: El ID '{id_val}' debe ser un número entre 3 y 10 caracteres.")
#                 continue

#             # b. Columna 2: Validación de correo electrónico
#             if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#                 errors.append(f"Error en línea {line_number}: El correo '{email}' no es válido.")
#                 continue

#             # c. Columna 3: Validación del tipo de documento (CC o TI)
#             if tipo_doc not in ['CC', 'TI']:
#                 errors.append(f"Error en línea {line_number}: El tipo de documento '{tipo_doc}' debe ser 'CC' o 'TI'.")
#                 continue

#             # d. Columna 4: Validar que el valor esté entre 500000 y 1500000
#             try:
#                 valor_int = int(valor)
#                 if not (500000 <= valor_int <= 1500000):
#                     errors.append(f"Error en línea {line_number}: El valor '{valor}' debe estar entre 500000 y 1500000.")
#                     continue
#             except ValueError:
#                 errors.append(f"Error en línea {line_number}: El valor '{valor}' no es un número válido.")
#                 continue

#             # e. Columna 5: Permitir cualquier valor (sin validación)

#             # Si todo es válido, agregar a la lista de documentos
#             documento.append({
#                 'id': id_val,
#                 'email': email,
#                 'tipo_doc': tipo_doc,
#                 'valor': valor,
#                 'epigrafe': epigrafe
#             })

#         if errors:
#             # Si hay errores, devolver los errores y no los documentos
#             return render(request, 'index.html', {'errors': errors, 'documento': documento})

#     return render(request, 'index.html', {'documento': documento})
