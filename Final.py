# Paso 1: Importar bibliotecas requeridas
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import random


#Paso colab: Importamos archivos datos .xlsx (colab)
#from google.colab import files
#uploaded = files.upload()

#Paso 2: Asignar varibles a los archivos .xlsx
SMostStreamed = pd.read_excel("MostStreamedSpotifySongs2023.xlsx")
SUserBehavior = pd.read_excel("SpotifyUserBehaviorDataset.xlsx")

# Paso 3: Crear páginas interactivas en el panel lateral del sitio web
paginas = ['🏠 Inicio', '🔍 Buscador', '🎮 Juego']
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)

# Paso 4: Hacemos condicionales con la selección del panel lateral
if pagina_seleccionada == '🏠 Inicio':
    # Paso 5: Crear título de la página y un párrafo
    st.markdown("<h1 style='text-align: center;'>SPOTIFY USER DATA 2023</h1>", unsafe_allow_html=True)
    textoinicio = """
    SPOTIFY USER DATA 2023 consiste en una plataforma informativa sobre los datos de los usuarios en Spotify.
    """
    st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{textoinicio}</div>", unsafe_allow_html=True)
    # Paso 6: Crear división en dos columnas
    col1,col2 = st.columns(2)
    with col1:
        #Paso 7: Contar personas según género
        conteo_genero = SUserBehavior["genero"].value_counts().reset_index()
        conteo_genero.columns = ["Género", "Cantidad"]

        # Paso 8: Crear gráfico circular
        fig1 = px.pie(
            conteo_genero,
            names="Género",
            values="Cantidad",
            title="Distribución por género de usuarios",
        )
        # Paso 9: Agregar etiquetas dentro del gráfico
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        # Paso 10: Mostrar el gráfico
        st.plotly_chart(fig1)
        # Paso 11: Agregar interpretación del gráfico
        st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{La mayoría de los usuarios encuestados para la base de datos fueron del género femenino, lo que demuestra su relevancia dentro del público objetivo. Este dato sugiere una mayor participación en ciertos hábitos de consumo musical, preferencias de contenido de la plataforma y comportamientos digitales más activos que otros grupos.
}</div>", unsafe_allow_html=True)
    
    with col2:
        # Paso 10: Contar momentos de escucha de cada usuario y asignar columnas
        momentoescucha = SUserBehavior['momento_escucha_música'].value_counts().reset_index()
        momentoescucha.columns = ['Tiempo de escucha', 'Cantidad']

        # Paso 11: Crear grafico circular
        fig2 = px.pie(
            momentoescucha,
            names='Tiempo de escucha',
            values='Cantidad',
            title='Distribución de tiempo de escucha',
            color_discrete_sequence=px.colors.qualitative.Pastel  #Asignar colores pastel
        )
        # Paso 12: Agregar etiquetas dentro del gráfico
        fig2.update_traces(textposition='inside', textinfo='percent+label')

        # Paso 13: Mostrar el gráfico
        st.plotly_chart(fig2)
    # Paso 14: Contar géneros musicales favoritos de los usuarios y asignar columnas
    conteo = SUserBehavior['género_musical_favorito'].value_counts().reset_index()
    conteo.columns = ['Géneros preferidos', 'N° de usuarios']
    # Paso 15: Crear gráfico de barras
    fig3 = px.bar(
        conteo,
        x='Géneros preferidos',
        y='N° de usuarios',
        title='Cantidad de usuarios según géneros musicales preferidos',
        color='Géneros preferidos',
        color_discrete_sequence=px.colors.qualitative.Pastel #Asignar colores pastel
    )

    # Paso 16: Mostrar el gráfico
    st.plotly_chart(fig3)

    # Paso 17: Renombrar columna plan_spotify
    SUserBehavior["tipo_plan"] = SUserBehavior["plan_spotify"].apply(
        lambda x: "Gratis" if "Gratis" in x else "Premium"
    )

    # Paso 18: Agrupar por plan y tiempo
    tiempo_vs_plan = SUserBehavior.groupby(
        ["tipo_plan", "tiempo_uso_spotify"]
    ).size().reset_index(name="Usuarios")

    # Paso 19: Eliminar respuestas muy raras o poco frecuentes
    tiempo_vs_plan = tiempo_vs_plan[tiempo_vs_plan["Usuarios"] > 2]

    # Paso 20: Crear gráfico de barras
    fig3 = px.bar(
        tiempo_vs_plan,
        x="tiempo_uso_spotify",
        y="Usuarios",
        color="tipo_plan",
        barmode="group",
        title="Tiempo de uso de Spotify según el tipo de plan",
        labels={
            "tiempo_uso_spotify": "Tiempo de uso de Spotify",
            "Usuarios": "Cantidad de usuarios",
            "tipo_plan": "Tipo de plan"
        },
        color_discrete_map={"Gratis": "#EF553B", "Premium": "#636EFA"} #Asignar colores rojo y azul
    )
    # Paso 21: Agregar rotación a los títulos de barras
    fig.update_layout(xaxis_tickangle=-45)
    # Paso 22: Agregar el gráfico, ajustar su anchura
    st.plotly_chart(fig3, use_container_width=True)

elif pagina_seleccionada == '🔍 Buscador':
    # Paso 23: Agregar título, subtítulo y espaciado mediante markdown
    st.markdown("<h1 style='text-align: center;'>🎧 Las Mejores Canciones</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 25px;'>{"Top 30 canciones 2023"}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 70px;'>{""}</div>", unsafe_allow_html=True)

    # Paso 24: Crear división en tres columnas
    col1, col2, col3 = st.columns(3)
    # Paso 25: Crear caja de texto como buscador
    with col1:
        nombre = st.text_input("🔍 Buscar por nombre de canción") #busca por nombre de canción en el paso 29
    # Paso 26: Crear buscador mediante selectbox (widget de selección)
    with col2:
        artistas = sorted(SMostStreamed["artist_name"].unique().tolist()) #busca mediante nombre de artista(s) en el paso 29
        artista = st.selectbox("🎤 Filtrar por artista", options=["Todos"] + artistas)
    # Paso 27: Crear buscador mediante selectbox (widget de selección)
    with col3:
        años = sorted(SMostStreamed["released_year"].unique().tolist()) #busca mediante año de lanzamiento en el paso 29
        año = st.selectbox("📅 Filtrar por año", options=["Todos"] + años)

    # Paso 28: Crear variable con el contenido del .xlsl
    resultados = SMostStreamed.copy()
    
    # Paso 29: Crear condicionales según cada buscador
    if nombre:
        resultados = resultados[resultados["track_name"].str.contains(nombre, case=False, na=False)] #utilizar columna track_name para el buscador

    if artista != "Todos":
        resultados = resultados[resultados["artist_name"] == artista] #utilizar columna artist_name para el selectbox

    if año != "Todos":
        resultados = resultados[resultados["released_year"] == año] #utilizar columna released_year para el selectbox

    # Paso 30: Mostrar resultados de las canciones
    st.markdown("### 🎵 Resultados")

    # Paso 31: Crear condicional en caso de encontrar resultados
    if not resultados.empty:
        for _, row in resultados.iterrows():
            with st.container():
                st.image(row["url_imagen"], width=100) #mostrar imagen con 100px de anchura
                st.subheader(row["track_name"]) #mostrar nombre de la canción
                st.write(f"**Artista:** {row['artist_name']}") #mostrar nombre del artista
                st.write(f"**Año de lanzamiento:** {row['released_year']}") #mostrar año de lanzamiento
                st.write(f"**Reproducciones:** {row['streams']:,}") #mostrar número de reproducciones
                st.markdown("---") #separar canciones
    # Paso 32: Finalizar condicional en caso de no encontrar resultados
    else:
        st.warning("No se encontraron resultados con los filtros aplicados.")
        
elif pagina_seleccionada == '🎮 Juego': 
    # Paso 33: Interpretar 
    @st.cache_data
    def cargar_canciones(ruta):
        df = pd.read_excel(ruta, sheet_name="Hoja 1")
        df = df[["track_name", "artist_name"]].dropna()
        return df.to_dict(orient="records")

    # Iniciar nueva partida
    def nueva_partida(canciones):
        seleccion = random.choice(canciones)
        st.session_state.titulo = seleccion["track_name"].upper()
        st.session_state.artista = seleccion["artist_name"]
        st.session_state.adivinadas = []
        st.session_state.intentos = 6
        st.session_state.estado = "jugando"

    # Mostrar palabra actual
    def palabra_actual(titulo, adivinadas):
        resultado = ""
        for letra in titulo:
            if not letra.isalpha():         # muestra espacios y signos tal cual
                resultado += letra
            elif letra in adivinadas:
                resultado += letra
            else:
                resultado += "_"
        return resultado

    # Procesar entrada del usuario
    def procesar_entrada(entrada):
        entrada = entrada.strip().upper()
        titulo = st.session_state.titulo
        adivinadas = st.session_state.adivinadas

        if not entrada.replace(" ", "").isalpha():
            st.warning("Ingresa solo letras.")
            return
        elif len(entrada) == 1:
            if entrada in adivinadas:
                st.info("Ya escribiste esa letra.")
            elif entrada in titulo:
                st.session_state.adivinadas.append(entrada)
                st.success("¡Correcto!")
            else:
                st.session_state.adivinadas.append(entrada)
                st.session_state.intentos -= 1
                st.error("Incorrecto.")
        else:
            if entrada == titulo.strip():
                st.session_state.estado = "ganado"
                # Mostrar todo el título: agregar todas las letras a adivinadas
                st.session_state.adivinadas.extend([letra for letra in titulo if letra.isalpha()])
            else:
                st.session_state.intentos -= 1
                st.error("Título incorrecto.")

        # Verificar fin del juego
        if all(letra in st.session_state.adivinadas or not letra.isalpha() for letra in titulo):
            st.session_state.estado = "ganado"
        elif st.session_state.intentos <= 0:
            st.session_state.estado = "perdido"

        st.rerun()

    # Cargar canciones
    canciones = cargar_canciones("MostStreamedSpotifySongs2023.xlsx")

    # Título del juego
    st.title("🎧 Juego del Ahorcado - Canciones de Spotify")

    # Inicializar partida si es la primera vez
    if "estado" not in st.session_state:
        nueva_partida(canciones)

    # Mostrar pista
    st.write(f"🎤 *Artista:* {st.session_state.artista}")

    # Mostrar palabra oculta
    palabra = palabra_actual(st.session_state.titulo, st.session_state.adivinadas)
    st.markdown(f"<h3 style='letter-spacing: 4px;'>{palabra}</h3>", unsafe_allow_html=True)

    # Intentos
    st.write(f"🧠 Intentos restantes: {st.session_state.intentos}")

    # Entrada del jugador
    if st.session_state.estado == "jugando":
        entrada = st.text_input("🔡 Escribe una letra o el título completo (solo un intento) y presiona Enter:")
        if entrada:
            procesar_entrada(entrada)

    # Mostrar resultado
    if st.session_state.estado == "ganado":
        st.success(f"🎉 ¡Ganaste! El título era: **{st.session_state.titulo}**")
    elif st.session_state.estado == "perdido":
        st.error(f"❌ Perdiste. El título era: **{st.session_state.titulo}**")

    # Botón para reiniciar
    if st.button("🔁 Jugar de nuevo"):
        nueva_partida(canciones)
        st.rerun()
