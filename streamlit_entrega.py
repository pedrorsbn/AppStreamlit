# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:05:01 2024

@author: Noemí
"""
import streamlit as st
import pandas as pd
#from plotnine import *

st.title('Planea tu viaje')

st.write("Esta página está enfoca en facilitar la eleccion de billete de tren de renfe "+
         "en función de las necesidades de cada usuario. A continuación se detalla que indica "+
         "cada columna del dataset: \n \n"+
         "origen: Ciudad de origen del viaje. \n"+ 
         "destino: Ciudad de destino del viaje.  \n"+
         "precios: Precio del billete en euros.  \n"+
         "hora_salida: Hora a la que sale el tren \n"+
         "hora_llegada: Hora estimada de llegada del tren \n"+
         "lleno: Indicador de si el tren está lleno (1 para lleno, 0 para plazas disponibles).  \n"+ 
         "plaza_H_disponible: Indicador de si hay plazas para personas con movilidad reducida "+
         "enlace_duracion: Duración de las escalas (en minutos) para viajes con conexiones.  \n"+
         "duracion_horas: Horas que dura el trayecto (es un entero) \n"+
         "duracion_minutos: Horas que dura el trayecto (es un entero) \n"
         "dia_de_la_semana: Día de la semana en el que ocurre el viaje (Lunes, Martes, etc.).  \n"+
         "dia_numero: Día del mes en el que ocurre el viaje (1, 2, ..., 31).  \n"+
         "mes: Mes del año en el que ocurre el viaje (Enero, Febrero, etc.).  \n"+
         "duracion_total: Duración total del viaje en minutos.  \n"+
         "enlace_horas: Horas de espera entre cada tren (es un entero) \n"+
         "enlace_minutos: Minutos de espera entre cada tren (es un entero) \n"+
         "duracion_total: Duración total del viaje en minutos.  \n"
         )



# Cargar los datos
df = pd.read_csv('renfe.csv')

st.write("Busqueda habitual de billetes:")
#st.write("Primeras filas del DataFrame:", df.head())
with st.expander("Filtrar billetes por características"):
    origen = st.selectbox('Selecciona el origen', df['origen'].unique(),key="origen_selectbox")
    destino = st.selectbox('Selecciona el destino', df['destino'].unique(), key="destino_selectbox")

# Permitir al usuario seleccionar el día de la semana, con "Cualquiera" como opción
    dia_de_la_semana = st.selectbox('Selecciona el día de la semana', ['Cualquiera'] + df['dia_de_la_semana'].unique().tolist())
    
    # Permitir al usuario seleccionar el mes, con "Cualquiera" como opción
    mes = st.selectbox('Selecciona el mes', ['Cualquiera'] + df['mes'].unique().tolist())
    
    # Permitir al usuario seleccionar el día del mes, con "Cualquiera" como opción
    dia_del_mes = st.selectbox('Selecciona el día del mes', ['Cualquiera'] + df['dia_numero'].unique().tolist())
    
    filtro_lleno = st.checkbox('Filtrar por trenes con plazas libres', value=False)
    
    # Filtrar por plaza disponible para movilidad reducida
    filtro_plaza_disponible = st.checkbox('Filtrar por plazas disponibles para personas con movilidad reducida', value=False)

    filtro_sin_escalas = st.checkbox('Filtrar por viajes sin escalas', value=False)
    
    # Permitir al usuario seleccionar el criterio de ordenación por precios
    orden_precio = st.selectbox('Ordenar por precios', ['Cualquiera', 'Ascendente', 'Descendente'])
    
    orden_duracion = st.selectbox('Ordenar por duración', ['Cualquiera', 'Ascendente', 'Descendente'])
    
    precio_min = st.slider('Precio mínimo', 0, 100, 20)
    precio_max = st.slider('Precio máximo', 0, 100, 50)

    df_filtrado = df[(df['precios'] >= precio_min) & (df['precios'] <= precio_max)]
    
    # Filtrar los datos según la selección del usuario
    df_filtrado = df[(df['origen'] == origen) & (df['destino'] == destino)]
    
    # Filtrar por día de la semana, si no es "Cualquiera"
    if dia_de_la_semana != 'Cualquiera':
        df_filtrado = df_filtrado[df_filtrado['dia_de_la_semana'] == dia_de_la_semana]
    
    # Filtrar por mes, si no es "Cualquiera"
    if mes != 'Cualquiera':
        df_filtrado = df_filtrado[df_filtrado['mes'] == mes]
    
    # Filtrar por día del mes, si no es "Cualquiera"
    if dia_del_mes != 'Cualquiera':
        df_filtrado = df_filtrado[df_filtrado['dia_numero'] == dia_del_mes]
        
    if filtro_lleno:
        df_filtrado = df_filtrado[df_filtrado['lleno'] == 0]
    
    # Filtrar por plaza disponible, si se selecciona el checkbox
    if filtro_plaza_disponible:
        df_filtrado = df_filtrado[df_filtrado['plaza_H_disponible'] == 1]
        
    if filtro_sin_escalas:
        df_filtrado = df_filtrado[df_filtrado['enlace_duracion'] == '0']
        
        # Ordenar por precios, si es seleccionado
    if orden_precio == 'Ascendente':
        df_filtrado = df_filtrado.sort_values(by='precios', ascending=True)
    elif orden_precio == 'Descendente':
        df_filtrado = df_filtrado.sort_values(by='precios', ascending=False)
        
    if orden_duracion == 'Ascendente':
        df_filtrado = df_filtrado.sort_values(by='duracion_total', ascending=True)
    elif orden_duracion == 'Descendente':
        df_filtrado = df_filtrado.sort_values(by='duracion_total', ascending=False)
    
    # Mostrar el DataFrame filtrado
    st.write("Datos filtrados:")
    #st.write(df_filtrado)
    st.dataframe(df_filtrado, height=600, width=1200)
    
###################################################################################################
########################################INSIGHTS###################################################
###################################################################################################
st.write("Conocer la frecuencia de trenes a lo largo de la semana nos ayudará a decidir cuanto podemos esperar para adquirir el billete antes de que se agoten")

with st.expander("Frecuencia entre semana de viajes"):

    origen_frecuencia = st.selectbox("Selecciona el origen", df['origen'].unique(), key="origen_frecuencia_selectbox")
    destino_frecuencia = st.selectbox("Selecciona el destino", df['destino'].unique(), key="destino_frecuencia_selectbox")
    
    # Filtrar el DataFrame según el origen y destino seleccionados
    df_filtrado = df[(df['origen'] == origen_frecuencia) & (df['destino'] == destino_frecuencia)]
    
    # Si hay datos para el origen y destino seleccionados
    if not df_filtrado.empty:
        # Contar los viajes por día de la semana y ordenar por días de lunes a domingo
        viajes_por_dia = (
            df_filtrado['dia_de_la_semana']
            .value_counts()
            .reindex(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
            .fillna(0)  # Rellenar con 0 para días sin datos
            .astype(int)  # Asegurarse de que los valores sean enteros
        )
    
        # Crear un DataFrame con los datos del gráfico
        data_grafico = pd.DataFrame({
            'Día de la Semana': viajes_por_dia.index,
            'Número de Viajes': viajes_por_dia.values
        })
    
        # Mostrar el gráfico como una barra interactiva con Streamlit
        st.write(f"Cantidad de viajes por día de la semana de {origen_frecuencia} a {destino_frecuencia}")
        st.bar_chart(data_grafico.set_index('Día de la Semana'))  # Usar 'Día de la Semana' como índice para el gráfico
    
    else:
        st.write("No hay viajes disponibles para el origen y destino seleccionados.")
        
###################################################################################################
###################################################################################################
###################################################################################################
st.write("Conocer la evoución del precio mínimo a lo largo de la semana nos ayudará a saber cuando nos es más económico viajar")

with st.expander("Evolucion del precio minimo a lo largo de la semana"):

    st.write("Evolución de precios mínimos a lo largo de los días de la semana:")
    origen_precio = st.selectbox("Selecciona el origen", df['origen'].unique(), key="origen_precio")
    destino_precio = st.selectbox("Selecciona el destino", df['destino'].unique(), key="destino_precio")
    
    # Filtrar los datos por el origen y destino seleccionados
    df_precio_filtrado = df[(df['origen'] == origen_precio) & (df['destino'] == destino_precio)]
    
    # Verificar si hay datos disponibles
    if not df_precio_filtrado.empty:
        # Calcular el precio mínimo por día de la semana
        precios_minimos = (
            df_precio_filtrado.groupby('dia_de_la_semana')['precios']
            .min()
            .reset_index()
            .rename(columns={'precios': 'precio_minimo'})
            )

        # Ordenar explícitamente los días de la semana
        orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        precios_minimos['dia_de_la_semana'] = pd.Categorical(precios_minimos['dia_de_la_semana'], categories=orden_dias, ordered=True)
        precios_minimos = precios_minimos.sort_values('dia_de_la_semana')
        
        # Preparar los datos para `st.line_chart`
        precios_minimos = precios_minimos.set_index('dia_de_la_semana')  # Usar el índice para el eje X
        
        # Mostrar el gráfico con st.line_chart
        st.line_chart(precios_minimos['precio_minimo'])
    else:
        st.write("No hay datos disponibles para el origen y destino seleccionados.")
    
##################################################################################################
##################################################################################################
##################################################################################################
st.write("Aquí podemos apreciar a que destinos nos será más fácil viajar en caso de tener movilidad reducida ")

with st.expander("Inclusividad en Destinos de Viajes en función del porcentaje de billetes con plazas H disponibles"):
    st.title("Inclusividad en Destinos de Viajes")
    
    # Seleccionar el lugar de origen
    origen_seleccionado = st.selectbox("Selecciona el lugar de origen", df['origen'].unique(), key = 'origen_seleccionado')
    
    # Filtrar el DataFrame por el origen seleccionado
    df_origen = df[df['origen'] == origen_seleccionado]
    
    # Calcular el porcentaje de billetes con plaza_h por destino
    porcentaje_plaza_h = (
        df_origen.groupby('destino')['plaza_H_disponible']
        .mean()  # Media de 1s (proporción)
        .multiply(100)  # Convertir a porcentaje
        .reset_index()
        .rename(columns={'plaza_H_disponible': 'porcentaje_plaza_h'})
        .sort_values(by='porcentaje_plaza_h', ascending=False)
    )
    
    # Crear el gráfico interactivo con st.bar_chart
    st.write(f"Porcentaje de billetes con plaza para movilidad reducida desde {origen_seleccionado}:")
    st.bar_chart(data=porcentaje_plaza_h.set_index('destino'))

##################################################################################################
##################################################################################################
##################################################################################################
st.write("Aquí podemos apreciar la facilidad de movilidad entre localidades")

with st.expander("Destinos más comunes desde cada ciudad"):
    origen_seleccionado = st.selectbox("Selecciona el lugar de origen", df['origen'].unique(), key = 'origen_seleccionado_comun')
    
    df_origen = df[df['origen'] == origen_seleccionado]
    # Destinos más comunes
    destinos_comunes = df_origen['destino'].value_counts()
    
    # Mostrar el título y el gráfico de barras
    st.write(f"Destinos más comunes desde {origen_seleccionado}:")
    st.bar_chart(destinos_comunes)

##################################################################################################
##################################################################################################
##################################################################################################



