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
    st.markdown("<h1 style='text-align: center;'>Bits & Beats: Análisis de usuarios Spotify 2023</h1>", unsafe_allow_html=True)
    textoinicio = """
    ¡Bienvenidos a Bits & Beats! Dentro de esta plataforma van a poder encontrar información sobre los datos de los usuarios en Spotify, las canciones más populares del 2023 y un juego de ahorcado de dichas piezas musicales.
    A través de este espacio, podrán conocer cómo se comportan los oyentes en la plataforma, qué géneros y artistas dominaron el año, y además entretenerse poniendo a prueba su memoria musical. Todo esto mientras navegan por contenidos dinámicos y gráficos que hacen más fácil y entretenido el análisis de datos.
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
            title="Distribución por género",
        )
        # Paso 9: Agregar etiquetas dentro del gráfico
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        # Paso 10: Mostrar el gráfico
        st.plotly_chart(fig1)
        # Paso 11: Agregar interpretación del gráfico
        textograf1 = """
        La mayoría de los usuarios encuestados para la base de datos fueron del género femenino, lo que demuestra su relevancia dentro del público objetivo. Este dato sugiere una mayor participación en ciertos hábitos de consumo musical, preferencias de contenido de la plataforma y comportamientos digitales más activos que otros grupos.
        """
        st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{textograf1}</div>", unsafe_allow_html=True)
    
    with col2:
        # Paso 12: Contar momentos de escucha de cada usuario y asignar columnas
        momentoescucha = SUserBehavior['momento_escucha_música'].value_counts().reset_index()
        momentoescucha.columns = ['Tiempo de escucha', 'Cantidad']

        # Paso 13: Crear grafico circular
        fig2 = px.pie(
            momentoescucha,
            names='Tiempo de escucha',
            values='Cantidad',
            title='Distribución por tiempo de escucha',
            color_discrete_sequence=px.colors.qualitative.Pastel  #Asignar colores pastel
        )
        # Paso 14: Agregar etiquetas dentro del gráfico
        fig2.update_traces(textposition='inside', textinfo='percent+label')

        # Paso 15: Mostrar el gráfico
        st.plotly_chart(fig2)
        # Paso 16: Agregar interpretación del gráfico
        textograf2 = """
        Una mayor distribución en el tiempo de escucha en la noche indica una preferencia por los usuarios a tiempos más reservados dónde puedan disfrutar de mejor manera el consumo musical. Asimismo, nos resalta la importancia la importancia de adaptar las recomendaciones algorítmicas y las campañas promocionales a estos horarios de mayor actividad.
        """
        st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{textograf2}</div>", unsafe_allow_html=True)
    # Paso 17: Contar géneros musicales favoritos de los usuarios y asignar columnas
    conteo = SUserBehavior['género_musical_favorito'].value_counts().reset_index()
    conteo.columns = ['Géneros preferidos', 'N° de usuarios']
    # Paso 18: Crear gráfico de barras
    fig3 = px.bar(
        conteo,
        x='Géneros preferidos',
        y='N° de usuarios',
        title='Cantidad de usuarios según géneros musicales preferidos',
        color='Géneros preferidos',
        color_discrete_sequence=px.colors.qualitative.Pastel #Asignar colores pastel
    )

    # Paso 19: Mostrar el gráfico
    st.plotly_chart(fig3)
    # Paso 20: Agregar interpretación del gráfico
    textograf3 = """
    La mayoría de los usuarios prefieren escuchar melodía por encima de otros géneros, ya que ofrece un efecto de relajación y acompañamiento emocional que se adapta a distintas actividades cotidianas sin interferir en momentos de concentración. Este tipo de música genera una atmósfera tranquila y se distingue por su carácter versátil. De manera similar, el segundo género más escuchado es la música clásica, que comparte estas cualidades al favorecer la calma y el enfoque. Su estructura instrumental, sin letra, facilita la introspección, lo que la convierte en una opción popular durante sesiones de estudio, lectura o meditación.
    Esta preferencia revela una tendencia hacia géneros que no solo entretienen, sino que también cumplen una función práctica dentro de la rutina diaria. En contraste, otros géneros presentes en la gráfica se caracterizan por ritmos más enérgicos y letras que invitan al movimiento o la celebración, siendo más comunes en contextos sociales o recreativos. Esta diversidad en los hábitos de escucha demuestra cómo los usuarios adaptan sus elecciones musicales según el momento y la necesidad emocional o funcional del día.
    """
    st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{textograf3}</div>", unsafe_allow_html=True)

    # Paso 21: Renombrar columna plan_spotify
    SUserBehavior["tipo_plan"] = SUserBehavior["plan_spotify"].apply(
        lambda x: "Gratis" if "Gratis" in x else "Premium"
    )

    # Paso 22: Agrupar por plan y tiempo
    tiempo_vs_plan = SUserBehavior.groupby(
        ["tipo_plan", "tiempo_uso_spotify"]
    ).size().reset_index(name="Usuarios")

    # Paso 23: Eliminar respuestas muy raras o poco frecuentes
    tiempo_vs_plan = tiempo_vs_plan[tiempo_vs_plan["Usuarios"] > 2]

    # Paso 24: Crear gráfico de barras
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
    # Paso 25: Agregar rotación a los títulos de barras
    fig3.update_layout(xaxis_tickangle=-45)
    # Paso 26: Agregar el gráfico, ajustar su anchura
    st.plotly_chart(fig3, use_container_width=True)
    # Paso 27: Agregar interpretación del grafico
    textograf4 = """
    A partir del gráfico, se puede evidenciar una mayor fidelización entre los usuarios que acceden gratuitamente a Spotify en comparación con aquellos que cuentan con un plan Premium. Esto se debe a que, a pesar de las limitaciones de la versión gratuita —como los anuncios y la reproducción aleatoria—, muchos usuarios valoran la posibilidad de acceder sin costo a un amplio catálogo musical. Esta accesibilidad favorece una conexión constante con la plataforma, lo que contribuye a generar hábitos de uso sostenidos en el tiempo. Además, elementos como la facilidad de navegación, la creación automática de playlists y las recomendaciones personalizadas influyen en que estos usuarios se mantengan activos sin necesidad de pagar por el servicio.

Por otro lado, los usuarios Premium, aunque disfrutan de una experiencia optimizada y sin interrupciones, representan una proporción menor dentro del total de usuarios. No obstante, es importante destacar que la mayoría de quienes cuentan con esta suscripción llevan más de dos años en la plataforma, lo que refleja un alto nivel de compromiso y satisfacción tras un uso prolongado. Esto sugiere que, si bien el modelo gratuito capta a más usuarios, el modelo Premium logra consolidar una base leal a largo plazo.
    """
    st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{textograf4}</div>", unsafe_allow_html=True)

#siguiente página del panel lateral
elif pagina_seleccionada == '🔍 Buscador':
    # Paso 28: Agregar título, subtítulo y espaciado mediante markdown
    st.markdown("<h1 style='text-align: center;'>🎧 Las Mejores Canciones</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 25px;'>{"Top 30 canciones 2023"}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 70px;'>{""}</div>", unsafe_allow_html=True)

    # Paso 29: Crear división en tres columnas
    col1, col2, col3 = st.columns(3)
    # Paso 30: Crear caja de texto como buscador
    with col1:
        nombre = st.text_input("🔍 Buscar por nombre de canción") #busca por nombre de canción en el paso 29
    # Paso 31: Crear buscador mediante selectbox (widget de selección)
    with col2:
        artistas = sorted(SMostStreamed["artist_name"].unique().tolist()) #busca mediante nombre de artista(s) en el paso 29
        artista = st.selectbox("🎤 Filtrar por artista", options=["Todos"] + artistas)
    # Paso 32: Crear buscador mediante selectbox (widget de selección)
    with col3:
        años = sorted(SMostStreamed["released_year"].unique().tolist()) #busca mediante año de lanzamiento en el paso 29
        año = st.selectbox("📅 Filtrar por año", options=["Todos"] + años)

    # Paso 33: Crear variable con el contenido del .xlsx
    resultados = SMostStreamed.copy()
    
    # Paso 34: Crear condicionales según cada buscador
    if nombre:
        resultados = resultados[resultados["track_name"].str.contains(nombre, case=False, na=False)] #utilizar columna track_name para el buscador

    if artista != "Todos":
        resultados = resultados[resultados["artist_name"] == artista] #utilizar columna artist_name para el selectbox

    if año != "Todos":
        resultados = resultados[resultados["released_year"] == año] #utilizar columna released_year para el selectbox

    # Paso 35: Mostrar resultados de las canciones
    st.markdown("### 🎵 Resultados")

    # Paso 36: Crear condicional en caso de encontrar resultados
    if not resultados.empty:
        for _, row in resultados.iterrows():
            with st.container():
                st.image(row["url_imagen"], width=100) #mostrar imagen con 100px de anchura
                st.subheader(row["track_name"]) #mostrar nombre de la canción
                st.write(f"**Artista:** {row['artist_name']}") #mostrar nombre del artista
                st.write(f"**Año de lanzamiento:** {row['released_year']}") #mostrar año de lanzamiento
                st.write(f"**Reproducciones:** {row['streams']:,}") #mostrar número de reproducciones
                st.markdown("---") #separar canciones
    # Paso 37: Finalizar condicional en caso de no encontrar resultados
    else:
        st.warning("No se encontraron resultados con los filtros aplicados.")

#siguiente página del panel lateral
elif pagina_seleccionada == '🎮 Juego': 
    # Paso 38: Utilizar cache de streamlit y cargar canciones del .xlsx
    @st.cache_data
    def cargar_canciones(ruta):
        df = pd.read_excel(ruta, sheet_name="Hoja 1") #Leer la hoja 1 del excel
        df = df[["track_name", "artist_name"]].dropna() # Seleccionar columnas a utilizar
        return df.to_dict(orient="records") #Convertir a diccionarios
        
    # Paso 39: Crear nueva partida con canción aleatoria
    def nueva_partida(canciones):
        seleccion = random.choice(canciones) # escoger canción aleatoria
        st.session_state.titulo = seleccion["track_name"].upper() # utilizar dato de la columna track_name (nombre de la canción)
        st.session_state.artista = seleccion["artist_name"] # utilizar dato de la columna artist_name (artista(s) autor de la canción)
        st.session_state.adivinadas = [] #establecer sin ninguna letra desbloqueada
        st.session_state.intentos = 6 # asignar número de intentos
        st.session_state.estado = "jugando" # establecer estado como "jugando"

    # Paso 40: Mostrar palabra actual 
    def palabra_actual(titulo, adivinadas):
        resultado = "" # Crear variable para la palabra
        for letra in titulo:
            if not letra.isalpha(): # muestra espacios y signos tal cual
                resultado += letra 
            elif letra in adivinadas: # muestra letras adivinadas mediante la suma
                resultado += letra
            else:
                resultado += "_" #no cambia el guion si no es letra correcta
        return resultado # muestra palabra

    # Paso 41: Procesar entrada del usuario
    def procesar_entrada(entrada):
        entrada = entrada.strip().upper() 
        titulo = st.session_state.titulo
        adivinadas = st.session_state.adivinadas

    # Paso 42: Interpretamos la entrada del usuario mediante condicionales
        if not entrada.replace(" ", "").isalpha(): #si el caracter insertado no es una letra
            st.warning("Ingresa solo letras.") #advertencia
            return
        elif len(entrada) == 1: 
            if entrada in adivinadas: #si la letra insertada ya fue utilizada
                st.info("Ya escribiste esa letra.") #aviso ya escribiste esa letra
            elif entrada in titulo:
                st.session_state.adivinadas.append(entrada) #si la letra es correcta
                st.success("¡Correcto!") #aviso correcto
            else:
                st.session_state.adivinadas.append(entrada) #si la letra es errónea
                st.session_state.intentos -= 1 #restar 1 intento
                st.error("Incorrecto.") #aviso incorrecto
        else:
            if entrada == titulo.strip(): #si inserta más de una letra y es igual al nombre de la canción
                st.session_state.estado = "ganado" #aviso juego ganado
                st.session_state.adivinadas.extend([letra for letra in titulo if letra.isalpha()]) #rellenar el nombre de la canción
            else:
                st.session_state.intentos -= 1 #restar 1 intentos
                st.error("Título incorrecto.") #aviso título incorrecto

        # Paso 43: Verificar fin del juego
        if all(letra in st.session_state.adivinadas or not letra.isalpha() for letra in titulo): #si todas las letras son adivinadas
            st.session_state.estado = "ganado" #ganado
        elif st.session_state.intentos <= 0: #si los intentos llegan a 0
            st.session_state.estado = "perdido" #perdido

        st.rerun() #repetir condicionales
    # Paso 44: Cargar canciones del .xlsx
    canciones = cargar_canciones("MostStreamedSpotifySongs2023.xlsx")

    # Paso 45: Agregar título del juego
    st.title("🎧 Juego del Ahorcado - Canciones de Spotify")

    # Paso 46: Inicializar partida si es la primera vez
    if "estado" not in st.session_state:
        nueva_partida(canciones)

    # Paso 47: Mostrar artista de la canción como pista
    st.write(f"🎤 *Artista:* {st.session_state.artista}")

    # Paso 48: Mostrar palabra oculta
    palabra = palabra_actual(st.session_state.titulo, st.session_state.adivinadas)
    st.markdown(f"<h3 style='letter-spacing: 4px;'>{palabra}</h3>", unsafe_allow_html=True)

    # Paso 49: Mostrar intentos restantes
    st.write(f"🧠 Intentos restantes: {st.session_state.intentos}")

    # Paso 50: Condicional segun estado del jugador
    if st.session_state.estado == "jugando": #si esta jugando
        entrada = st.text_input("🔡 Escribe una letra o el título completo (solo un intento) y presiona Enter:") #indicación del juego en la caja de texto
        if entrada:
            procesar_entrada(entrada) #procesar lo ingresado por el usuario

    # Paso 51: Mostrar resultado
    if st.session_state.estado == "ganado": #si gana
        st.success(f"🎉 ¡Ganaste! El título era: **{st.session_state.titulo}**") #aviso ganaste!
    elif st.session_state.estado == "perdido": #si pierde
        st.error(f"❌ Perdiste. El título era: **{st.session_state.titulo}**") #aviso perdiste!

    # Paso 52: Agregar botón para reiniciar
    if st.button("🔁 Jugar de nuevo"): #si se presiona
        nueva_partida(canciones) #nueva ronda
        st.rerun() #repetir
