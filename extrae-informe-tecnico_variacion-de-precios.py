import os
import re
import pandas as pd
import pdfplumber

# --- CONFIGURACIÓN ---
# ¡IMPORTANTE! Cambia esta ruta a la carpeta donde guardas tus archivos PDF del INEI.
# Ejemplo en Windows: "C:\\Users\\TuUsuario\\Documents\\Informes_INEI"
# Ejemplo en macOS/Linux: "/home/TuUsuario/Documentos/Informes_INEI"
PDF_DIRECTORY = "C:\\"

# Nombre del archivo CSV que se generará como resultado.
OUTPUT_CSV_FILE = "datos_precios_extraidos.csv"

# --- DICCIONARIOS Y EXPRESIONES REGULARES (REGEX) ---
# Mapeo para normalizar los nombres de los meses
MESES = {
    "enero": "Enero", "febrero": "Febrero", "marzo": "Marzo",
    "abril": "Abril", "mayo": "Mayo", "junio": "Junio",
    "julio": "Julio", "agosto": "Agosto", "setiembre": "Setiembre",
    "octubre": "Octubre", "noviembre": "Noviembre", "diciembre": "Diciembre"
}

# Lista de las divisiones de consumo para buscarlas en el texto
DIVISIONES_CONSUMO = [
    "Transporte",
    "Alimentos y Bebidas no Alcohólicas",
    "Alimentos y Bebidas No Alcohólicas",
    "Restaurantes y Hoteles",
    "Educación",
    "Bienes y Servicios Diversos",
    "Alojamiento, Agua, Electricidad, Gas y Otros Combustibles",
    "Salud",
    "Recreación y Cultura",
    "Bebidas Alcohólicas, Tabaco y Estupefacientes",
    "Comunicaciones"
]


def limpiar_valor(texto_valor):
    """Convierte el texto de un valor (ej. '-0,08') a un número flotante."""
    if texto_valor:
        try:
            # Reemplaza la coma decimal por un punto y convierte a float
            return float(texto_valor.strip().replace(',', '.'))
        except (ValueError, AttributeError):
            return None
    return None

def extraer_datos_pdf(ruta_archivo):
    """
    Función principal que abre un archivo PDF, extrae su texto y busca los datos
    de inflación utilizando expresiones regulares.
    """
    datos_extraidos = []
    nombre_archivo = os.path.basename(ruta_archivo)

    try:
        with pdfplumber.open(ruta_archivo) as pdf:
            # Generalmente, el resumen con los datos principales está en la primera página.
            primera_pagina = pdf.pages[0]
            texto = primera_pagina.extract_text(x_tolerance=2, y_tolerance=2)

            if not texto:
                print(f"  -> Advertencia: No se pudo extraer texto de '{nombre_archivo}'.")
                return []

            # Reemplazar saltos de línea para facilitar la búsqueda con regex en párrafos.
            texto_plano = texto.replace('\n', ' ')

            # 1. Extraer Año y Mes del informe
            # Busca un mes seguido de un año de 4 dígitos en el título.
            match_fecha = re.search(r'(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Setiembre|Octubre|Noviembre|Diciembre)\s+(\d{4})', texto, re.IGNORECASE)
            if not match_fecha:
                print(f"  -> Advertencia: No se encontró Mes/Año en '{nombre_archivo}'.")
                return [] # No podemos continuar sin la fecha.
            
            mes_str, anio_str = match_fecha.groups()
            mes = MESES.get(mes_str.lower())
            anio = int(anio_str)
            
            # --- Función auxiliar para añadir datos a la lista ---
            def registrar_dato(tipo_dato, item_nombre, item_detalle, valor_principal, valor_secundario=None):
                datos_extraidos.append({
                    "Anio": anio,
                    "Mes": mes,
                    "Tipo_Dato": tipo_dato,
                    "Item_Nombre": item_nombre,
                    "Item_Detalle": item_detalle,
                    "Valor_Principal_Porcentual": valor_principal,
                    "Valor_Secundario_Porcentual": valor_secundario,
                    "Fuente_Archivo": nombre_archivo
                })

            # 2. Extraer indicadores principales
            # Variación Mensual Nacional
            val_mensual_nac = re.search(r'Nacional (?:aumentó|disminuyó|varió|subió|decreció) en\s+(-?[\d,]+)%', texto_plano)
            if val_mensual_nac:
                registrar_dato("Variación Mensual", "Índice de Precios al Consumidor", "Nacional", limpiar_valor(val_mensual_nac.group(1)))

            # Variación Mensual Lima Metropolitana
            val_mensual_lima = re.search(r'Lima Metropolitana,.*? (?:aumentó|subió|decreció|varió en)\s+(-?[\d,]+)%', texto_plano)
            if val_mensual_lima:
                registrar_dato("Variación Mensual", "Índice de Precios al Consumidor", "Lima Metropolitana", limpiar_valor(val_mensual_lima.group(1)))

            # Variación Anual (ambos indicadores en una misma frase)
            val_anual = re.search(r'variación de ([\d,]+)% para el indicador Nacional y de ([\d,]+)% para el de Lima Metropolitana', texto_plano)
            if val_anual:
                registrar_dato("Variación Anual", "Índice de Precios al Consumidor", "Nacional", limpiar_valor(val_anual.group(1)))
                registrar_dato("Variación Anual", "Índice de Precios al Consumidor", "Lima Metropolitana", limpiar_valor(val_anual.group(2)))

            # Variación Acumulada
            # La redacción varía mucho, por lo que buscamos frases comunes
            val_acum_lima = re.search(r'variación acumulada de ([\d,]+)%', texto_plano)
            if val_acum_lima:
                 registrar_dato("Variación Acumulada", "Índice de Precios al Consumidor", "Lima Metropolitana", limpiar_valor(val_acum_lima.group(1)))

            val_acum_nac = re.search(r'acumulando.*? un alza de ([\d,]+)%', texto_plano)
            if val_acum_nac:
                 registrar_dato("Variación Acumulada", "Índice de Precios al Consumidor", "Nacional", limpiar_valor(val_acum_nac.group(1)))

            # 3. Extraer divisiones de consumo (Lima Metropolitana)
            # Busca el nombre de cada división y el primer porcentaje que aparece después.
            for division in DIVISIONES_CONSUMO:
                # Usamos re.escape para tratar caracteres especiales en el nombre de la división
                patron = re.compile(re.escape(division) + r'.*?(-?[\d,]+)%', re.IGNORECASE)
                match = patron.search(texto_plano)
                if match:
                    # Validar que no se haya añadido ya esta división para este mes
                    if not any(d['Item_Nombre'] == division.replace(" no ", " No ") and d['Mes'] == mes for d in datos_extraidos):
                        valor = limpiar_valor(match.group(1))
                        # La incidencia (valor secundario) es muy difícil de extraer con certeza, se omite por ahora.
                        registrar_dato("Variación Mensual", division.replace(" no ", " No "), "Lima Metropolitana", valor)

    except Exception as e:
        print(f"  -> ERROR procesando el archivo '{nombre_archivo}': {e}")

    return datos_extraidos

def main():
    """
    Función principal que orquesta el proceso:
    1. Verifica la ruta de los PDF.
    2. Itera sobre cada archivo.
    3. Llama a la función de extracción.
    4. Consolida los datos y los guarda en un CSV.
    """
    if not os.path.isdir(PDF_DIRECTORY) or "ruta\\a\\tus" in PDF_DIRECTORY:
        print("¡Error de configuración!")
        print(f"El directorio especificado no es válido: '{PDF_DIRECTORY}'")
        print("Por favor, edita la variable 'PDF_DIRECTORY' en el script con la ruta correcta a tu carpeta de archivos PDF.")
        return

    archivos_pdf = [os.path.join(PDF_DIRECTORY, f) for f in os.listdir(PDF_DIRECTORY) if f.lower().endswith('.pdf')]

    if not archivos_pdf:
        print(f"No se encontraron archivos PDF en '{PDF_DIRECTORY}'. Asegúrate de que los archivos estén allí.")
        return

    print(f"Se encontraron {len(archivos_pdf)} archivos PDF. Iniciando extracción...")

    todos_los_datos = []
    for ruta_pdf in archivos_pdf:
        print(f"Procesando: {os.path.basename(ruta_pdf)}")
        datos_del_archivo = extraer_datos_pdf(ruta_pdf)
        if datos_del_archivo:
            todos_los_datos.extend(datos_del_archivo)

    if not todos_los_datos:
        print("\nNo se pudo extraer ningún dato. Revisa las advertencias y errores anteriores.")
        return

    # Convertir la lista de diccionarios a un DataFrame de pandas
    df = pd.DataFrame(todos_los_datos)

    # Reordenar las columnas para que coincidan con el formato solicitado
    columnas_ordenadas = [
        "Anio", "Mes", "Tipo_Dato", "Item_Nombre", "Item_Detalle",
        "Valor_Principal_Porcentual", "Valor_Secundario_Porcentual", "Fuente_Archivo"
    ]
    df = df[columnas_ordenadas]

    # Guardar el DataFrame en un archivo CSV
    try:
        df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8-sig')
        print(f"\n¡Proceso completado con éxito!")
        print(f"Se extrajeron {len(df)} registros en total.")
        print(f"Los datos han sido guardados en: {os.path.abspath(OUTPUT_CSV_FILE)}")
    except Exception as e:
        print(f"\nError al intentar guardar el archivo CSV: {e}")

# --- Punto de entrada para ejecutar el script ---
if __name__ == "__main__":
    main()