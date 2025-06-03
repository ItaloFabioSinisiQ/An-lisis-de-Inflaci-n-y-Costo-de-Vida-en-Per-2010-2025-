import pandas as pd

# Ruta al archivo
archivo = "C:\\"

# Cargar hojas
vbp_df = pd.read_excel(archivo, sheet_name='INDICES VBP', skiprows=4)
indice_df = pd.read_excel(archivo, sheet_name='Indice Total 8 sb07', skiprows=3)

# Limpiar columnas vacías
vbp_df = vbp_df.dropna(how='all', axis=1)
indice_df = indice_df.dropna(how='all', axis=1)

# Renombrar la primera columna como fecha o periodo
vbp_df.rename(columns={vbp_df.columns[0]: "Periodo"}, inplace=True)
indice_df.rename(columns={indice_df.columns[0]: "Periodo"}, inplace=True)

# Convertir el periodo a fecha si es YYYYMM
try:
    vbp_df["Periodo"] = pd.to_datetime(vbp_df["Periodo"], format="%Y%m")
except:
    pass

# Mostrar primeras filas
print("=== INDICES VBP (Producción por sector) ===")
print(vbp_df.head())

print("\n=== INDICE TOTAL (Producción Nacional Global) ===")
print(indice_df.head())

# Guardar como CSV si deseas
vbp_df.to_csv("produccion_sectorial_limpio.csv", index=False)
indice_df.to_csv("produccion_global_limpio.csv", index=False)
