### Creado por Emiliano Castro @humole.jpg

Herramienta para la graficación de datos en tiempo real de manera inalámbrica desde distintos sensores con microcontroladores mediante la lectura serial de datos.

Utiliza una frecuencia de 19200 bauds.

#### Installation
```bash
 git clone https://github.com/Humol-e/graficator.git
```
```bash
 streamlit run graficator.py
```


# ALGORITMO 
Se importan varias librerías necesarias para la visualización de datos, manejo de datos, comunicación serial y configuración de la aplicación Streamlit.
Configuración Inicial de Streamlit:

Se configura la página de Streamlit con un diseño amplio y un estado inicial de la barra lateral expandido.
Se establece el título de la aplicación y se añade una imagen en la barra lateral.
Definición de Funciones:

get_available_ports(): Obtiene y devuelve una lista de puertos seriales disponibles.
procesar_linea_serial(linea): Procesa una línea de datos recibida del puerto serial, separa los valores y los convierte en un diccionario.
leer_lote_serial(ser, lote_size): Lee un lote de líneas de datos del puerto serial.
mostrar_graficas(df, selected_tags): Muestra las gráficas seleccionadas por el usuario.
velocigaugevertical(df): Muestra un indicador de velocidad vertical.
velocigaugehorizontal(df): Muestra un indicador de velocidad horizontal.
mostrar_tabla(df): Muestra la tabla completa de datos.
mostrar_filtro(df_filtrado): Muestra la tabla filtrada de datos.
Interfaz de Usuario:

Se crean dos columnas para seleccionar el puerto COM y los datos a procesar.
Se inicializa un DataFrame con las columnas seleccionadas por el usuario.
Se crea un botón para iniciar la lectura de datos.
Lectura y Procesamiento de Datos:

Si se presiona el botón de iniciar lectura, se abre el puerto serial seleccionado.
En un bucle infinito, se leen lotes de líneas de datos del puerto serial.
Cada línea se procesa y se convierte en un diccionario de datos.
Los datos procesados se añaden al DataFrame.
Se actualizan las visualizaciones y tablas en la interfaz de usuario.
Manejo de Errores:

Se manejan posibles errores al abrir el puerto serial y al procesar las líneas de datos.
Algoritmo General:
Inicialización:

Importar librerías.
Configurar Streamlit.
Definir funciones auxiliares.
Interfaz de Usuario:

Mostrar opciones para seleccionar puerto COM y datos a procesar.
Inicializar DataFrame.
Lectura de Datos:

Abrir puerto serial.
En un bucle infinito:
Leer lote de líneas del puerto serial.
Procesar cada línea.
Añadir datos procesados al DataFrame.
Actualizar visualizaciones y tablas.
Manejo de Errores:

Capturar y mostrar errores relacionados con el puerto serial y el procesamiento de datos.
