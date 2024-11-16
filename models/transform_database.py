import sqlite3
import pandas as pd
ruta_archivo = r'C:\Users\joaquin.gotte\Downloads\BASE_ROBOS_SECUESTROS.xlsx'

# Cargar el archivo
df = pd.read_excel(ruta_archivo, engine='openpyxl')

# Eliminar la columna sobrante
df.drop(columns=['Unnamed: 25'], inplace=True)

# Cambiar el tipo de dato de las columnas numéricas
df = df.astype({
    'tramite_fecha': 'datetime64[ns]',
    'fecha_inscripcion_inicial': 'datetime64[ns]',
    'registro_seccional_codigo': 'Int64',
    'automotor_anio_modelo': 'Int64',
    'titular_anio_nacimiento': 'Int64',
    'titular_porcentaje_titularidad': float
})

# Convertir columnas categóricas
categorical_columns = [
    'registro_seccional_descripcion', 'registro_seccional_provincia', 
    'automotor_origen', 'automotor_tipo_descripcion', 'automotor_marca_descripcion', 
    'automotor_modelo_descripcion', 'automotor_uso_descripcion', 'titular_tipo_persona',
    'titular_domicilio_localidad', 'titular_domicilio_provincia', 'titular_genero', 
    'titular_pais_nacimiento', 'tramite_tipo', 'titular_pais_nacimiento_indec_id', 
    'automotor_modelo_codigo', 'automotor_marca_codigo'
]
for col in categorical_columns:
    df[col] = df[col].astype('category')

# Reemplazar valores nulos en columnas categóricas con "desconocido"
for col in categorical_columns:
   
    df[col] = df[col].cat.add_categories('desconocido')
  
    df[col] = df[col].fillna('desconocido')

# Reemplazar valores nulos en columnas numéricas con 0 
df['automotor_anio_modelo'] = df['automotor_anio_modelo'].fillna(0)  
df['automotor_tipo_codigo'] = df['automotor_tipo_codigo'].fillna(0)  
df['automotor_marca_codigo'] = df['automotor_marca_codigo'].fillna(0)  
df['automotor_modelo_codigo'] = df['automotor_modelo_codigo'].fillna(0)  

#Agrego nueva columnas de id 

df['ID_REGISTRO'] = range(1, len(df) + 1)

#Creo la conexion a DB

conexion = sqlite3.connect('base_datos_robos_secuestrados.db')

# Cargar el DataFrame en la base de datos
df.to_sql('robos_secuestrados', conexion, if_exists='replace', index=False)

cursor = conexion.cursor()

update_queries = [
    # Unificación de variantes de 'SEDAN'
   ("UPDATE robos_secuestrados SET automotor_marca_descripcion = 'MERCEDES-BENZ' WHERE automotor_marca_descripcion = 'MERCEDES BENZ';"),
    ("UPDATE robos_secuestrados SET automotor_marca_descripcion = 'VOLKSWAGEN' WHERE automotor_marca_descripcion IN ('VOKSWAGEN', 'WOLKSWAGEN');"),
]


# Ejecutar cada una de las queries
for query in update_queries:
    cursor.execute(query)


# Confirmar los cambios realizados
conexion.commit()

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()