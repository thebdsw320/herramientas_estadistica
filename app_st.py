# ---  App que automatiza los primeros ejercicios de la clase de Estadistica y Probabilidad, STREAMLIT VERSION ---

# Importar los modulos necesarios
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import io
import seaborn as sns

sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context('paper')

st.title('Estadistica y Probabilidad - Estudios Estadisticos¿?')

# Leer el archivo que alguien suba en StreamLit
file_buffer = st.file_uploader('Escoge un archivo .CSV para sacar los datos...', type='csv')
if file_buffer:
    uploaded_file = io.TextIOWrapper(file_buffer)
    if uploaded_file is not None:
# Lectura del archivo para pasarlo a un DataFrame, fija el nombre de la columna en "nums"
# y se salta el primer espacio, por lo tanto, el archivo csv debera tener un espacio extra
# arriba con las letras "nums"
        dataframe = pd.read_csv(uploaded_file, names=['nums'], skipinitialspace=True)

        # Extrae la columna de los datos, es decir, con los numeros
        datos = pd.Series(dataframe['nums'])

        # Convierte la serie a un array
        array = datos.to_numpy()
        array = np.delete(array, [0])
        array = array = array.astype('int32') # Convierte el array a ints, que originalmente eran strings
        array = np.sort(array) # Acomoda los numeros de menor a mayor

        # Escoge el valor mas grande y el mas pequeño del array
        max_v = array.max() + 1
        min_v = array.min() - 1

        rango = max_v - min_v # El valor mas grande menos el mas pequeño dan el rango de los datos
        num_datos = array.size

        # Aplicacion de la Formula de Sturges para obtener el numero de intervalos
        num_intervalos = round(1 + 3.32 * (np.log10(num_datos)))
        amp_intervalo = rango / num_intervalos

        # Inicializar el diccionario principal donde iran todos los datos y columnas
        diccionario = {}

        # Sacar los indices con el numero de intervalos que tengamos 
        i = num_intervalos
        indices = []
        while i > 0:
            indices.append(i)
            i = i - 1
        indices.sort()
        diccionario['Indice'] = indices # Poner la columna indices con sus respectivos valores Ej. [1, 2, 3, 4, 5]

        # Sacar los intervalos junto con las sumas correspondientes (232.39 - 23290.92)
        n = 0
        intervalos_clase = []
        derechas = []
        izquierdas = []

        while n <= max_v:
            if n == 0:
                n = min_v + amp_intervalo
                izquierda = min_v
                derecha = n
                izquierdas.append(izquierda)
                derechas.append(derecha)
                texto = f'{min_v} --- {n}'
                intervalos_clase.append(texto)
            else:
                if derecha <= max_v:
                    if n == min_v + amp_intervalo:
                        izquierda = n + 0.001
                        n = izquierda + amp_intervalo
                        derecha = n
                        texto = f'{izquierda} --- {derecha}'
                        izquierdas.append(izquierda)
                        derechas.append(derecha)
                        intervalos_clase.append(texto)
                    else:
                        izquierda = derecha + 0.001
                        derecha = izquierda + amp_intervalo
                        marca = izquierda - derecha / 2
                        texto = f'{izquierda} --- {derecha}'
                        izquierdas.append(izquierda)
                        derechas.append(derecha)
                        intervalos_clase.append(texto)
                else:
                    break

        diccionario['I. de Clase'] = intervalos_clase
        diccionario['Derecha'] = derechas
        diccionario['Izquierda'] = izquierdas

        # Sacar las marcas de clase, sumando y dividiendo los datos de cada intervalo de clase
        marcas_de_clase = []

        for i, num in enumerate(izquierdas):
            for i2, num2 in enumerate(derechas):
                if i == i2:
                    marca = (num + num2) / 2
                    marcas_de_clase.append(marca)
                else:
                    continue

        diccionario['Marcas de clase'] = marcas_de_clase

        
        # # Sacar las marcas de clase sumadas, es como "marcas de clase ABSOLUTAS"
        # suma_marcas_clase = []


        # for i, num in enumerate(marcas_de_clase, 1):
        #     if i == 1:
        #         n = num
        #         suma_marcas_clase.append(n)
        #     else:
        #         n = n + num
        #         suma_marcas_clase.append(n)
        

        # Obtener las frecuencias de cada intervalo de clase, es decir, cuantos numeros de lal lista hay
        # en ese intervalo
        frecuencias = []

        for i, num in enumerate(izquierdas):
            contador = 0
            for i2, num2 in enumerate(derechas):
                if i == i2:
                    for i3, num3 in enumerate(array, 1):
                        if num3 >= num and num3 <= num2:
                            contador = contador + 1
                            continue
                    frecuencias.append(contador)
                else:
                    continue

        diccionario['Fcia'] = frecuencias

        # Sacar las frecuencias absolutas, la suma continua de las frecuencias
        frecuencia_absoluta = []

        for i, num in enumerate(frecuencias, 1):
            if i == 1:
                n = num
                frecuencia_absoluta.append(n)
            else:
                n = n + num
                frecuencia_absoluta.append(n)

        diccionario['Fcia. A.'] = frecuencia_absoluta

        # Obtener las medidas de tendencia central
        # ---- Media ----
        media = 0

        for i, num in enumerate(marcas_de_clase, 1):
            for i2, num2 in enumerate(frecuencias, 1):
                if i == i2:
                    temp = num * num2
                    media += temp
                else:
                    continue

        media = media / num_datos
        # ---- Mediana ----
        mediana = np.median(array)
        # ---- Moda ----
        moda = np.bincount(array).argmax()
        # ---- Media de la Frecuencia ----
        media_frecuencia = 0

        for i, num in enumerate(frecuencia_absoluta):
            temp = num
            media_frecuencia += temp

        media_frecuencia = media_frecuencia / num_intervalos

        # Sacar la diferencia entre la marca de clase y el promedio de las mismas
        dif_media_marca = []

        for i, num in enumerate(marcas_de_clase):
            resta = num - media
            dif_media_marca.append(resta)

        diccionario['A'] = dif_media_marca

        # Sacar el cuadrado de cada valor que dió al hacer la diferencia entre la marca de clase y el promedio
        # de las mismas, es decir, sacar A cuadrada
        dif_media_marca_cuadrada = []

        for i, num in enumerate(dif_media_marca):
            valor = num ** 2
            dif_media_marca_cuadrada.append(valor)

        diccionario['A^2'] = dif_media_marca_cuadrada
        # Sacar la diferencia entre cada valor de la frecuencia absoluta y el promedio de las frecuencias
        dif_media_frecuencia = []

        for i, num in enumerate(frecuencia_absoluta):
            resta = num - media_frecuencia
            dif_media_frecuencia.append(resta)

        diccionario['B'] = dif_media_frecuencia

        # Sacar el cuadrado de cada valor que dió al hacer la diferencia entre la frecuencia absoluta y el promedio
        # de las mismas, es decir, sacar B cuadrada
        dif_media_frecuencia_cuadrada = []

        for i, num in enumerate(dif_media_frecuencia):
            valor = num ** 2
            dif_media_frecuencia_cuadrada.append(valor)

        diccionario['B^2'] = dif_media_frecuencia_cuadrada

        # Sacar los valores que se obtienen al multiplicar un valor de A y su correspondiente en B
        producto_AyB = []

        for i, num in enumerate(dif_media_marca, 1):
            for i2, num2 in enumerate(dif_media_frecuencia, 1):
                if i == i2:
                    producto = num * num2
                    producto_AyB.append(producto)
                else:
                    continue

        diccionario['A*B'] = producto_AyB

        # Configurar pandas para que muestre el DataFrame completo
        pd.set_option('display.max_rows', None, 'display.max_columns', None)

        tabla = pd.DataFrame(data=diccionario)
        tabla.set_index('Indice', inplace=True)

        tabla['Suma A*B'] = tabla['A*B'].cumsum()
        tabla['Suma A^2'] = tabla['A^2'].cumsum()
        tabla['Suma B^2'] = tabla['B^2'].cumsum()

        suma_ab = tabla.iloc[-1, tabla.columns.get_loc('Suma A*B')]
        suma_a_cuadrada = tabla.iloc[-1, tabla.columns.get_loc('Suma A^2')]
        suma_b_cuadrada = tabla.iloc[-1, tabla.columns.get_loc('Suma B^2')]

        st.dataframe(tabla)


        r = suma_ab / (math.sqrt(suma_a_cuadrada * suma_b_cuadrada))
        desv_estandar = math.sqrt(suma_a_cuadrada / num_datos)
        m = suma_ab / suma_a_cuadrada
        b = media_frecuencia - (m * media)
        ecuacion = f'{m} * x  +  {b}'

        st.header('Datos de la tabla')

        # Impresión datos extra
        st.text(f'\nMedia de Marcas de clase: {media}\nMedia de las Frecuencias: {media_frecuencia}\nNumero de Intervalos: {num_intervalos}\nRango: {rango}\nNumero de datos: {num_datos}\n\nLista de datos acomodados: {array}\n\nCoeficiente de correlacion: {r}\nDesviacion Estandar: ± {desv_estandar}\nEcuacion de la Recta:\nM = {m}\nB = {b}\nEcuacion: y = {ecuacion}')

        st.header('--- Poligono de Frecuencias ---')

        # Poligono de Frecuencias
        poligono_frec = sns.relplot(x='Marcas de clase', y='Fcia', data=tabla, kind='line', markers=True)
        poligono_frec.set(title='Poligono de Frecuencias', xlabel='Marcas de Clase', ylabel='Frecuencias')
        # fig, ax = plt.subplots()
        # ax.plot(marcas_de_clase, frecuencias)
        # ax.grid()
        # ax.set_xlabel('Marcas de Clase')
        # ax.set_ylabel('Frecuencias')
        # ax.set_title('Poligono de Frecuencias')
        st.pyplot(poligono_frec)

        # Ecuacion de la recta 
        def f(x):
                return (m * x) + b
            
        x = np.linspace(-100, 100, num=1000)
        y = f(x)

        st.header('--- Ecuacion de la Recta ---')

        ecuacion_recta = sns.relplot(x=x, y=y, kind='line')
        ecuacion_recta.set(title='Grafica de recta', xlabel=f'y = {ecuacion}', ylabel='')
        #ecuacion_recta.grid()
        # fig3, ax3 = plt.subplots()
        # ax3.plot(x, y)
        # ax3.grid()
        plt.axhline(y=0, color='r')
        plt.axvline(x=0, color='r')
        # ax3.set_title('Grafica de recta')
        # ax3.set_xlabel(f'y = {ecuacion}')
        st.pyplot(ecuacion_recta)