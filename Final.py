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
paginas = ['🏠 Inicio', '🔍 Buscador', 'Juego']
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)

# Paso 4: Hacemos condicionales con la selección del panel lateral
if pagina_seleccionada == '🏠 Inicio':
    st.markdown("<h1 style='text-align: center;'>SPOTIFY USER DATA 2023</h1>", unsafe_allow_html=True)
    textoinicio = """
    SPOTIFY USER DATA 2023 consiste en una plataforma informativa sobre los datos de los usuarios en Spotify.
    """
    st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{textoinicio}</div>", unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    
    with col1:
        # Contar ocurrencias por género
        conteo_genero = SUserBehavior["genero"].value_counts().reset_index()
        conteo_genero.columns = ["Género", "Cantidad"]

        # Crear gráfico circular
        fig1 = px.pie(
            conteo_genero,
            names="Género",
            values="Cantidad",
            title="Distribución por género de usuarios",
        )
        # Actualizamos las trazas para mostrar etiquetas dentro del gráfico
        # 'textposition' define la posición del texto (dentro)
        # 'textinfo' muestra el porcentaje y la etiqueta (nombre del país)
        fig1.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig1)
    with col2:
        # Gráfico circular interactivo
        # Contamos los tiempos de escucha por cada usuario
        # 'value_counts' devuelve la frecuencia de cada valor en la columna 'momento_escucha_música'
        # 'reset_index' convierte la serie resultante en un DataFrame
        momentoescucha = SUserBehavior['momento_escucha_música'].value_counts().reset_index()

        # Renombramos las columnas para mayor claridad
        momentoescucha.columns = ['Tiempo de escucha', 'Cantidad']

        # Creamos un gráfico de torta (pie chart) con plotly express
        fig2 = px.pie(
            momentoescucha,           # Datos de entrada (DataFrame)
            names='Tiempo de escucha',          # La categoría que define las porciones
            values='Cantidad',        # Tamaño de cada porción
            title='Distribución de tiempo de escucha',  # Título del gráfico
            color_discrete_sequence=px.colors.qualitative.Pastel  # Paleta de colores pastel para las porciones
        )

        # Actualizamos las trazas para mostrar etiquetas dentro del gráfico
        # 'textposition' define la posición del texto (dentro)
        # 'textinfo' muestra el porcentaje y la etiqueta (nombre del país)
        fig2.update_traces(textposition='inside', textinfo='percent+label')

        # Mostramos el gráfico interactivo
        st.plotly_chart(fig2)
#------------------------grafico3------------------------
    conteo = SUserBehavior['género_musical_favorito'].value_counts().reset_index()

    # Renombrar las columnas para que sean más descriptivas
    conteo.columns = ['Géneros preferidos', 'N° de usuarios']

    # Seleccionar una paleta de colores pastel para el gráfico (colores discretos para categorías)
    colores = px.colors.qualitative.Pastel

    # Crear un gráfico de barras con Plotly Express
    # - eje x: nombre de los géneros favoritos
    # - eje y: cantidad de usuarios que prefieren el género
    # - color: asigna un color distinto a cada barra según la escudería
    fig3 = px.bar(
        conteo,
        x='Géneros preferidos',
        y='N° de usuarios',
        title='Cantidad de usuarios según géneros musicales preferidos',
        color='Géneros preferidos',
        color_discrete_sequence=colores
    )

    # Mostrar el gráfico interactivo
    st.plotly_chart(fig3)
#----------------------grafico 4-----------------------
    # Clasificar tipo de plan: Gratis o Premium
    SUserBehavior["tipo_plan"] = SUserBehavior["plan_spotify"].apply(
        lambda x: "Gratis" if "Gratis" in x else "Premium"
    )

    # Agrupar por plan y tiempo en Spotify
    tiempo_vs_plan = SUserBehavior.groupby(
        ["tipo_plan", "tiempo_uso_spotify"]
    ).size().reset_index(name="Usuarios")

    # Eliminar respuestas muy raras o poco frecuentes
    tiempo_vs_plan = tiempo_vs_plan[tiempo_vs_plan["Usuarios"] > 2]

    # Crear gráfico de barras agrupadas
    fig = px.bar(
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
        color_discrete_map={"Gratis": "#EF553B", "Premium": "#636EFA"}
    )

    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)

    
elif pagina_seleccionada == '🔍 Buscador':
    st.markdown("<h1 style='text-align: center;'>🎧 Las Mejores Canciones</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 25px;'>{"Top 30 canciones 2023"}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 70px;'>{""}</div>", unsafe_allow_html=True)

    # Filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        nombre = st.text_input("🔍 Buscar por nombre de canción")

    with col2:
        artistas = sorted(SMostStreamed["artist_name"].unique().tolist())
        artista = st.selectbox("🎤 Filtrar por artista", options=["Todos"] + artistas)

    with col3:
        años = sorted(SMostStreamed["released_year"].unique().tolist())
        año = st.selectbox("📅 Filtrar por año", options=["Todos"] + años)

    # Filtrado
    resultados = SMostStreamed.copy()

    if nombre:
        resultados = resultados[resultados["track_name"].str.contains(nombre, case=False, na=False)]

    if artista != "Todos":
        resultados = resultados[resultados["artist_name"] == artista]

    if año != "Todos":
        resultados = resultados[resultados["released_year"] == año]

    # Mostrar resultados
    st.markdown("### 🎵 Resultados")

    if not resultados.empty:
        for _, row in resultados.iterrows():
            with st.container():
                st.image(row["url_imagen"], width=100)
                st.subheader(row["track_name"])
                st.write(f"**Artista:** {row['artist_name']}")
                st.write(f"**Año de lanzamiento:** {row['released_year']}")
                st.write(f"**Reproducciones:** {row['streams']:,}")
                st.markdown("---")
    else:
        st.warning("No se encontraron resultados con los filtros aplicados.")
elif pagina_seleccionada == 'Juego': 
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