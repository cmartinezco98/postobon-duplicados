# Generador de Duplicados - Transacción ZBDSDQ008

Este programa en Python automatiza el procesamiento de datos extraídos de SAP, específicamente para la transacción **ZBDSDQ008**. Su función principal es tomar el archivo de origen y generar duplicados o registros procesados basados en la lógica de negocio requerida.

## 📝 Descripción
La aplicación lee el archivo de entrada denominado `EXPORT.XLSX` (proveniente de la transacción ZBDSDQ008), aplica las transformaciones necesarias y facilita la manipulación de los datos para reportes o cargas posteriores.

Crea un archivo `CLIENTES_DUPLICADOS_[timestamp].xlsx`,el cual contiene una tabla en formato plano para identificar y realizar las validaciones pertinentes.

## 🛠️ Requisitos previos

Antes de ejecutar el programa, asegúrate de tener instalado [Python](https://www.python.org) en tu sistema.

### 1. Actualizar el gestor de paquetes
Es altamente recomendable tener la última versión de `pip` para evitar problemas de compatibilidad durante la instalación de librerías:

```bash
# Actualizar pip
py -m pip install --upgrade pip

# Instalar librerías
py -m pip install pandas openpyxl

```

### 2.Ejecucion 
Sigue estos pasos para ejecutar el proceso correctamente:
1. Exportar datos: Descarga el archivo desde SAP y guárdalo con el nombre EXPORT.xlsx dentro de la carpeta ./src.
2. Ejecutar proceso: Haz doble clic en el archivo ejecutable duplicados.bat ubicado en la raíz del proyecto.
3. Obtener resultados: El archivo resultante, nombrado como CLIENTES_DUPLICADOS_[timestamp].xlsx, se generará automáticamente en la ruta ./src/tmp/.



