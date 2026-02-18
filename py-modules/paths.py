import os

# Ruta base del proyecto (donde se ejecuta el script principal)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta a la carpeta src (una carpeta arriba)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'src'))

# Rutas de archivos individuales
EXPORT_XLSX = os.path.join(SRC_DIR, 'EXPORT.XLSX')
DUPLICATES_XLSX = os.path.join(SRC_DIR, 'tmp','CLIENTES_DUPLICADOS')
#API_RESPONSE = os.path.join(SRC_DIR,'tmp', 'RESPUESTA_API.json')
#API_RESPONSE_XLSX = os.path.join(SRC_DIR,'tmp', 'RESPUESTA_API.xlsx') 

#TRACEABILITY_CUSTOMERS = os.path.join(SRC_DIR,'tmp', 'CLIENTES_TRAZABILIDAD.json')
