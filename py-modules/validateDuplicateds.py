import pandas as pd
import paths as p
import openpyxl
from datetime import datetime


def get_duplicateds():
    
    try:    
         # Leer archivo original
        df = pd.read_excel(p.EXPORT_XLSX, engine='openpyxl')
    except FileNotFoundError:
        return(f"Error: El archivo '{p.EXPORT_XLSX}' no se encontró.")

    # Diccionario para guardar los pedidos duplicados por cliente
    pedidos_duplicados = []

    try:
        # Agrupar por cliente
        clientes = df.groupby('Solic.')

        for cod_cliente, grupo_cliente in clientes:
            pedidos = grupo_cliente.groupby('Nro Pedido Canal')
            pedidos_dict = {}

            for cod_pedido, grupo_pedido in pedidos:
                productos = set(zip(grupo_pedido['Material introducido'], grupo_pedido['Cantidad de pedido']))
                pedidos_dict[cod_pedido] = productos

            codigos_pedido = list(pedidos_dict.keys())
            duplicado_pedidos = set()

            for i in range(len(codigos_pedido)):
                for j in range(i + 1, len(codigos_pedido)):
                    pedido_1 = pedidos_dict[codigos_pedido[i]]
                    pedido_2 = pedidos_dict[codigos_pedido[j]]

                    productos_comunes = pedido_1 & pedido_2

                    if len(productos_comunes) >= 2:
                        duplicado_pedidos.add(codigos_pedido[i])
                        duplicado_pedidos.add(codigos_pedido[j])

            # Guardar los pedidos que fueron marcados como duplicados
            if duplicado_pedidos:
                duplicados_df = grupo_cliente[grupo_cliente['Nro Pedido Canal'].isin(duplicado_pedidos)]
                pedidos_duplicados.append(duplicados_df)

    except Exception as e:
        return(f"Error: Valide la disposición de los datos {str(e)}")
    
    if not pedidos_duplicados:
        print("No se encontraron pedidos duplicados.")
        return 0

    
    # Concatenar todos los pedidos duplicados en un solo DataFrame
    df_resultado = pd.concat(pedidos_duplicados)

    try:
        # Seleccionar las columnas que nos interesan
        df_resultado = df_resultado[['Clase de documento de ventas','Orden Compra','Representante', 'Solic.','Solicitante', 'Nro Pedido Canal', 'Material introducido', 'Cantidad de pedido','UM','Total Cajas','UMA','Motivo','Número de material','Estado del pedido en DSD','Total']]

        # Convertir DataFrame en un JSON
        # Agrupamos por "Solic." y "Solicitante"
        json_data = []

        for (solic, solicitante), df_solic in df_resultado.groupby(["Solic.", "Solicitante"]):
            trazabilidad = []

            for representante, df_repr in df_solic.groupby("Representante"):
                pedidos = []

                for (orden, pedido_canal, estado_pedido, clase_doc), df_pedido in df_repr.groupby([
                    "Orden Compra", "Nro Pedido Canal", "Estado del pedido en DSD", "Clase de documento de ventas"
                ]):
                    # Reemplazar NaN por None
                    df_pedido = df_pedido.where(pd.notnull(df_pedido), None)
                    productos = df_pedido[[
                        "Material introducido",
                        "Cantidad de pedido",
                        "UM",
                        "Total Cajas",
                        "UMA",
                        "Motivo",
                        "Número de material",
                        "Total"
                    ]].to_dict(orient="records")

                    pedidos.append({
                        "Orden Compra": orden,
                        "Nro Pedido Canal": pedido_canal,
                        "Estado del pedido en DSD": estado_pedido,
                        "Clase de documento de ventas": clase_doc,
                        "Productos": productos
                    })

                trazabilidad.append({
                    "Representante": representante,
                    "Pedidos": pedidos
                })

            json_data.append({
                "Solic.": solic,
                "Solicitante": solicitante,
                "Trazabilidad": trazabilidad
            })
    except Exception as e:
        return(f"Error al procesar los datos: {str(e)}")
    
    # Guardar como JSON
    #with open(p.TRACEABILITY_CUSTOMERS, "w", encoding="utf-8") as f:
    #    json.dump(json_data, f, indent=4, ensure_ascii=False)

    #print("✅ JSON generado correctamente en 'clientes_trazabilidad.json'")

    # Obtener fecha y hora actual
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    print(f"✅ Archivo '{p.DUPLICATES_XLSX}_{timestamp}.xlsx' generado con éxito.")
    # Exportar a Excel
    df_resultado.to_excel(f"{p.DUPLICATES_XLSX}_{timestamp}.xlsx" , index=False)

    #print("✅ Archivo 'PEDIDOS_DUPLICADOS.xlsx' generado con éxito.")
    df_pedidos_duplicados = pd.read_excel(f"{p.DUPLICATES_XLSX}_{timestamp}.xlsx")

    # Generar tabla dinámica interactiva (usa JavaScript, como en Excel)
    # pivot_ui(df_pedidos_duplicados, outfile_path=PATH_SRC+'tabla_interactiva.html')

    # Supongamos que la columna se llama 'clienteId'
    lista_clientes = df_pedidos_duplicados['Solic.'].dropna().astype(str).drop_duplicates().tolist()

    return len(lista_clientes);
    # getOrders.requestsOrders(lista_clientes)