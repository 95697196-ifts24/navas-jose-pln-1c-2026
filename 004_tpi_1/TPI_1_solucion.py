"""
TPI 1 — Adquisición y Análisis Lingüístico de Medios
Solución completa: scraping web + transcripción de audio + análisis NLP + visualización + dashboard

Ejecutar desde terminal:
    pip install spacy trafilatura pandas matplotlib seaborn plotly wordcloud openai-whisper yt-dlp gradio
    python -m spacy download es_core_news_lg
    python TPI_1_solucion.py
"""

# =============================================================================
# IMPORTACIONES
# =============================================================================
import os
import json
import subprocess

import spacy
import pandas as pd
import trafilatura
import whisper
import gradio as gr
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from collections import Counter
from wordcloud import WordCloud

print("Librerías importadas correctamente.")


# =============================================================================
# CONFIGURACIÓN DE FUENTES DE DATOS
# =============================================================================
# Se eligieron noticias de tecnología e IA en español porque:
# - Tienen vocabulario específico y rico en entidades (PER, ORG, LOC)
# - Los modelos de spaCy entrenados en noticias funcionan mejor en este dominio
# - Son textos formales: puntuación correcta, buena estructura para el parser

URLS_NOTICIAS = [
    "https://www.bbc.com/mundo/articles/c0d1vr17y95o",
    "https://elpais.com/tecnologia/inteligencia-artificial/",
    "https://www.infobae.com/tecno/2024/12/15/que-es-la-inteligencia-artificial-y-como-funciona/",
]

# Video de YouTube corto (~3-5 min) en español claro y formal — ideal para Whisper.
# IMPORTANTE: reemplazá esta URL por un video educativo en español si falla la descarga.
# Condiciones óptimas para Whisper: un solo hablante, sin música de fondo, español neutro.
URL_VIDEO_YOUTUBE = "https://www.youtube.com/watch?v=kRaHQpzMOFM"

# Ruta al JSON de corpus previo (opcional — si no existe, la función lo omite sin error)
RUTA_JSON_PREVIO = os.path.join(os.path.dirname(__file__), "corpus_previo.json")


# =============================================================================
# PARTE 1: ADQUISICIÓN MULTIMODAL DEL CORPUS
# =============================================================================

# ---- 1.1 Scraping en vivo con Trafilatura ----

def extraer_noticias_web(urls):
    """Extrae el texto limpio de una lista de URLs usando Trafilatura."""
    noticias = []

    for url in urls:  # Iteramos sobre cada URL de la lista
        try:
            # Descargamos el HTML de la URL (Trafilatura maneja headers y redirects)
            contenido_html = trafilatura.fetch_url(url)

            if contenido_html:  # Solo procesamos si la descarga fue exitosa
                # Extraemos el texto editorial del HTML eliminando menús, ads y sidebars
                texto = trafilatura.extract(
                    contenido_html,
                    include_comments=False,  # Sin comentarios de usuarios (ruido)
                    include_tables=False,    # Sin tablas (datos no narrativos)
                    no_fallback=False,       # Usamos fallback si falla el extractor principal
                    favor_recall=True,       # Priorizamos extraer más contenido aunque haya algo de ruido
                )

                # Filtramos textos demasiado cortos para análisis NLP significativo
                if texto and len(texto) > 100:
                    noticias.append({
                        "titulo_o_fuente": url,  # URL como identificador único del documento
                        "texto": texto,           # Texto limpio extraído
                        "origen": "web",          # Etiqueta de origen para análisis diferencial
                    })
                    print(f"  ✓ web: {url[:65]}... ({len(texto)} chars)")
                else:
                    print(f"  ✗ web: texto insuficiente en {url}")
            else:
                print(f"  ✗ web: no se pudo descargar {url}")

        except Exception as e:
            # Capturamos cualquier excepción para que una URL caída no detenga el pipeline
            print(f"  ✗ web: error en {url} → {e}")

    return noticias


# POR QUÉ se usó Trafilatura:
# Trafilatura aplica algoritmos de densidad de texto (similar a readability.js) para
# separar el contenido editorial del ruido HTML. Es superior a BeautifulSoup + regex
# manuales porque no requiere personalizar el parser para cada sitio. El manejo de
# excepciones garantiza que el pipeline continúe aunque una URL falle por red o paywalls.


# ---- 1.2 Transcripción de audio desde YouTube con Whisper ----

def transcribir_audio_youtube(url_video):
    """Descarga el audio de un video de YouTube y lo transcribe con Whisper."""
    resultado = []
    nombre_base = "audio_tpi1"
    archivo_mp3 = f"{nombre_base}.mp3"

    try:
        import yt_dlp  # Importación local para no fallar si no está instalado

        # Configuración de yt-dlp: solo descargamos el audio en formato mp3
        opciones = {
            "format": "bestaudio/best",     # Mejor calidad de audio disponible
            "outtmpl": nombre_base,          # Nombre base del archivo de salida
            "postprocessors": [{
                "key": "FFmpegExtractAudio", # Convertimos con FFmpeg a mp3
                "preferredcodec": "mp3",
                "preferredquality": "192",   # 192 kbps: buena calidad sin archivo enorme
            }],
            "quiet": True,                  # Suprimimos verbose de yt-dlp
        }

        print("  Descargando audio de YouTube...")
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url_video, download=True)  # Extraemos info y descargamos
            titulo = info.get("title", "Video sin título")      # Título del video para metadatos

        print(f"  ✓ Audio descargado: {titulo}")

        # Cargamos el modelo Whisper en tamaño 'small':
        # - 'base'  → más rápido, menor precisión en español
        # - 'small' → buen equilibrio velocidad/precisión sin necesitar GPU
        # - 'medium'/'large' → mejor precisión, pero requieren más RAM y tiempo
        print("  Cargando modelo Whisper (small)...")
        modelo = whisper.load_model("small")

        # Transcribimos forzando idioma español para evitar errores de detección automática
        # cuando hay música de fondo o el inicio del video es en silencio
        print("  Transcribiendo (esto puede tardar 1-3 minutos en CPU)...")
        transcripcion = modelo.transcribe(
            archivo_mp3,
            language="es",   # Español forzado → mejora precisión y velocidad
            fp16=False,       # Desactivamos float16 (solo útil con GPU CUDA)
        )

        texto = transcripcion["text"]  # Extraemos solo el texto de la respuesta de Whisper

        resultado.append({
            "titulo_o_fuente": titulo,  # Título del video como identificador
            "texto": texto,             # Texto transcrito
            "origen": "audio",          # Etiqueta de origen
        })
        print(f"  ✓ audio: '{titulo}' ({len(texto)} chars)")

        # Eliminamos el archivo mp3 temporal para liberar espacio en disco
        if os.path.exists(archivo_mp3):
            os.remove(archivo_mp3)

    except Exception as e:
        print(f"  ✗ audio: error durante la transcripción → {e}")

    return resultado


# POR QUÉ se usó Whisper:
# Whisper (OpenAI) es el estado del arte en ASR (Automatic Speech Recognition) para español.
# A diferencia de APIs en la nube, corre localmente sin costo. El modelo 'small' tiene
# ~244M parámetros y logra WER (Word Error Rate) bajo en español neutro sin GPU.
# Forzar language="es" evita confusión cuando el video tiene música de fondo en inglés.


# ---- 1.3 Carga de JSON local ----

def cargar_json_previo(ruta_json):
    """Carga un corpus pre-extraído en formato JSON y lo normaliza al esquema estándar."""
    datos = []

    # Verificamos la existencia del archivo antes de abrirlo
    if not os.path.exists(ruta_json):
        print(f"  ℹ json: archivo no encontrado en {ruta_json}, se omite.")
        return datos

    try:
        # Abrimos con UTF-8 para soportar caracteres del español (ñ, tildes, ü)
        with open(ruta_json, "r", encoding="utf-8") as f:
            contenido = json.load(f)  # Parseamos el JSON a estructura Python nativa

        # Normalizamos: el JSON puede ser una lista o un dict con distintas claves
        if isinstance(contenido, list):
            registros = contenido             # Lista de objetos directa
        elif isinstance(contenido, dict) and "datos" in contenido:
            registros = contenido["datos"]    # Dict con clave "datos"
        else:
            registros = [contenido]           # Objeto único → lo envolvemos en lista

        # Mapeamos cada registro al esquema mínimo común del pipeline
        for r in registros:
            texto = r.get("texto", r.get("content", r.get("body", "")))
            fuente = r.get("titulo", r.get("fuente", r.get("url", "JSON local")))
            if texto and len(texto) > 50:   # Filtramos registros con texto insuficiente
                datos.append({
                    "titulo_o_fuente": fuente,
                    "texto": texto,
                    "origen": "json",
                })

        print(f"  ✓ json: {len(datos)} registros cargados desde {ruta_json}")

    except json.JSONDecodeError as e:
        print(f"  ✗ json: formato inválido → {e}")
    except Exception as e:
        print(f"  ✗ json: error inesperado → {e}")

    return datos


# POR QUÉ se carga JSON como tercera fuente:
# Permite reutilizar corpus ya procesados sin re-scrapear (respeta rate limits y paywalls).
# La normalización de campos (texto/content/body, titulo/fuente/url) hace el loader
# tolerante a distintos esquemas de exportación de otras herramientas o APIs.


# ---- 1.4 Consolidación en un DataFrame unificado ----

def unificar_corpus(datos_web, datos_audio, datos_json):
    """Concatena las tres fuentes en un DataFrame con columnas estándar."""
    todos = datos_web + datos_audio + datos_json  # Concatenamos las tres listas

    if not todos:  # No hay datos → retornamos DataFrame vacío con el esquema correcto
        print("  ⚠ No hay datos para unificar.")
        return pd.DataFrame(columns=["titulo_o_fuente", "texto", "origen"])

    df = pd.DataFrame(todos)  # Pandas convierte automáticamente dicts a columnas

    # Eliminamos filas con texto nulo o vacío
    df = df.dropna(subset=["texto"])
    df = df[df["texto"].str.strip() != ""]

    # Agregamos columna de longitud para análisis posterior (ej: promedio por origen)
    df["longitud_texto"] = df["texto"].apply(len)

    # Reseteamos el índice para tener numeración limpia y secuencial
    df = df.reset_index(drop=True)

    print(f"  ✓ Corpus unificado: {len(df)} documentos")
    print(f"    Distribución:\n{df['origen'].value_counts().to_string()}")

    return df


# POR QUÉ elegimos el esquema mínimo común (titulo_o_fuente | texto | origen):
# Las tres fuentes tienen metadatos distintos: las noticias web tienen URL y fecha,
# el audio tiene título y duración, el JSON puede tener cualquier estructura.
# Un esquema mínimo garantiza interoperabilidad sin suponer metadatos que quizás no existan.
# La columna 'origen' es clave para el análisis diferencial: permite comparar rendimiento
# de spaCy sobre texto estructurado (web) vs. transcripción oral (audio).


# =============================================================================
# PARTE 2: ANÁLISIS LINGÜÍSTICO CON SPACY
# =============================================================================

class AnalizadorCorpus:
    """Encapsula el análisis lingüístico del corpus usando spaCy."""

    def __init__(self, df, modelo_spacy="es_core_news_lg"):
        self.df = df.copy()  # Trabajamos sobre copia para no alterar el DataFrame original
        print("  Cargando modelo de lenguaje spaCy...")
        # es_core_news_lg: modelo grande de español, entrenado en noticias y Wikipedia
        # Incluye tagger (POS), parser (dependencias), NER (entidades) y vectores de palabras
        self.nlp = spacy.load(modelo_spacy)

        print("  Procesando textos (puede tardar unos segundos)...")
        # nlp.pipe() procesa en batches → más eficiente que aplicar nlp() en un loop
        # disable=[] activa todos los componentes del pipeline (tagger, parser, ner, lemmatizer)
        self.df["doc"] = list(
            self.nlp.pipe(
                self.df["texto"],   # Serie de textos a procesar
                batch_size=10,      # Tamaño de batch: equilibrio entre RAM y velocidad
                disable=[],         # No deshabilitamos ningún componente
            )
        )
        print(f"  ✓ {len(self.df)} documentos procesados con spaCy")

    def extraer_entidades(self):
        """Devuelve un dict: tipo_entidad → Counter con frecuencias de cada entidad."""
        resultado = {}  # Estructura: {"PER": Counter({"Argentina": 5, ...}), ...}

        for doc in self.df["doc"]:   # Iteramos sobre cada documento procesado
            for ent in doc.ents:     # Iteramos sobre cada entidad reconocida
                tipo = ent.label_            # Tipo: PER, ORG, LOC, MISC (según modelo spaCy)
                texto_ent = ent.text.strip() # Texto de la entidad (ej: "Argentina")

                if tipo not in resultado:
                    resultado[tipo] = Counter()  # Inicializamos el Counter para ese tipo

                resultado[tipo][texto_ent] += 1  # Incrementamos la frecuencia

        return resultado  # Dict de Counters: permite llamar a .most_common() por tipo

    def extraer_verbos_principales(self, n=15):
        """Retorna los n verbos lematizados más frecuentes del corpus completo."""
        contador = Counter()

        for doc in self.df["doc"]:
            for token in doc:
                # Filtramos: solo verbos (VERB), no stopwords, no puntuación, lema mínimo
                if (
                    token.pos_ == "VERB"    # Part-of-speech: verbo principal (no AUX)
                    and not token.is_stop   # Excluimos ser, estar, haber (verbos auxiliares)
                    and not token.is_punct  # Excluimos puntuación
                    and len(token.lemma_) > 2  # Descartamos lemas triviales de 1-2 chars
                ):
                    contador[token.lemma_.lower()] += 1  # Lema en minúsculas para normalizar

        return contador.most_common(n)  # Lista de tuplas (verbo, frecuencia) ordenadas

    def extraer_palabras_clave(self, n=20):
        """Retorna los n lemas más frecuentes de NOUN, PROPN y ADJ, filtrados."""
        contador = Counter()
        # Stopwords adicionales que spaCy no siempre filtra pero son poco informativas
        stopwords_extra = {"más", "todo", "cada", "otro", "mismo", "solo", "así", "según",
                           "bien", "gran", "nuevo", "parte", "vez", "año", "forma"}

        for doc in self.df["doc"]:
            for token in doc:
                if (
                    token.pos_ in {"NOUN", "PROPN", "ADJ"}  # Solo sustantivos, propios y adjetivos
                    and not token.is_stop     # Stopwords del modelo (artículos, prep., etc.)
                    and not token.is_punct    # Sin puntuación
                    and not token.is_space    # Sin tokens de espacio en blanco
                    and token.is_alpha        # Solo tokens alfabéticos (sin números ni URLs)
                    and len(token.lemma_) > 3 # Lemas con al menos 4 caracteres
                    and token.lemma_.lower() not in stopwords_extra  # Sin stopwords extra
                ):
                    contador[token.lemma_.lower()] += 1

        return contador.most_common(n)  # Lista de tuplas (lema, frecuencia) ordenadas

    def estadisticas_corpus(self):
        """Retorna un dict con métricas generales del corpus."""
        total_tokens = 0
        total_oraciones = 0
        vocabulario = set()  # Set → elimina duplicados automáticamente

        for doc in self.df["doc"]:
            # Contamos tokens excluyendo espacios en blanco (artefactos del tokenizer)
            tokens = [t for t in doc if not t.is_space]
            total_tokens += len(tokens)

            # Contamos oraciones: el parser de spaCy detecta límites de oración
            total_oraciones += len(list(doc.sents))

            # Lemas únicos: solo palabras alfabéticas sin stopwords (vocabulario informativo)
            vocabulario.update(
                t.lemma_.lower()
                for t in tokens
                if t.is_alpha and not t.is_stop
            )

        n_docs = max(len(self.df), 1)  # Evitamos división por cero
        return {
            "total_documentos": len(self.df),
            "total_tokens": total_tokens,
            "vocabulario_unico": len(vocabulario),
            "total_oraciones": total_oraciones,
            "promedio_tokens_por_doc": round(total_tokens / n_docs, 1),
            # Type-Token Ratio: diversidad léxica (1.0 = cada token es único, 0 = todo repetido)
            "type_token_ratio": round(len(vocabulario) / max(total_tokens, 1), 4),
        }


# POR QUÉ encapsular en una clase:
# El objeto AnalizadorCorpus mantiene el DataFrame con la columna 'doc' (objetos spaCy)
# en memoria, evitando reprocesar con nlp.pipe() en cada consulta.
# La distinción PER/ORG/LOC de spaCy es estadística: el modelo la aprendió del corpus
# de entrenamiento (noticias). En textos transcritos de audio (sin mayúsculas, sin comas)
# el NER falla más porque esas señales ortográficas son features clave del modelo.


# =============================================================================
# PARTE 3: VISUALIZACIÓN PROFESIONAL
# =============================================================================

# Configuración global de accesibilidad visual — aplicada a todas las figuras de matplotlib
sns.set_theme(style="ticks", palette="colorblind", font_scale=1.1)
COLOR_ACENTO = sns.color_palette("colorblind")[0]  # Azul accesible → elemento principal
COLOR_BASE = "#b0b0b0"                             # Gris neutro → elementos secundarios


def visualizar_origen(df):
    """Barplot horizontal con la distribución de documentos por fuente de adquisición."""
    conteo = df["origen"].value_counts()  # Frecuencia de cada origen

    fig, ax = plt.subplots(figsize=(7, 3.5))  # Tamaño compacto para dashboards

    # Color de acento en la barra más larga, gris en el resto (guía el ojo al dato clave)
    colores = [COLOR_ACENTO if i == 0 else COLOR_BASE for i in range(len(conteo))]

    # Barplot horizontal → mejor para etiquetas de texto (evita rotación)
    ax.barh(conteo.index, conteo.values, color=colores, edgecolor="none")

    # Etiqueta de valor al extremo de cada barra (evita que el lector estime a ojo)
    for i, val in enumerate(conteo.values):
        ax.text(val + 0.05, i, str(val), va="center", fontsize=11, color="#333333")

    ax.set_title("Documentos por Fuente de Adquisición", fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Cantidad de documentos", fontsize=10)

    # Data-Ink Ratio: eliminamos bordes innecesarios (arriba e izquierda)
    sns.despine(left=True, bottom=False)
    ax.xaxis.grid(True, alpha=0.3)  # Grid suave solo en X
    ax.set_axisbelow(True)          # Grid detrás de las barras

    plt.tight_layout()
    return fig


def visualizar_palabras_clave_lollipop(palabras_clave):
    """Lollipop Chart de las palabras clave lematizadas más frecuentes."""
    if not palabras_clave:
        print("  ⚠ No hay palabras clave para visualizar.")
        return plt.figure()

    palabras = [p[0] for p in palabras_clave]    # Eje Y: nombres
    frecuencias = [p[1] for p in palabras_clave] # Eje X: frecuencias

    fig, ax = plt.subplots(figsize=(9, 6))

    # Componente 1: líneas horizontales desde 0 hasta el valor (el "palo" del lollipop)
    ax.hlines(
        y=palabras,
        xmin=0,
        xmax=frecuencias,
        color=COLOR_BASE,  # Gris neutro para no competir con los círculos
        linewidth=1.5,
        alpha=0.7,
    )

    # Componente 2: círculos al final de cada línea (la "paleta" del lollipop)
    ax.plot(
        frecuencias,
        palabras,
        "o",              # Marcador circular
        color=COLOR_ACENTO,
        markersize=8,
        zorder=3,         # Dibujamos sobre las líneas
    )

    ax.set_title("Palabras Clave más Frecuentes (lemas)", fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Frecuencia de aparición", fontsize=10)

    sns.despine(left=True)
    ax.xaxis.grid(True, alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    plt.tight_layout()
    return fig


def visualizar_entidades_plotly(entidades_dict):
    """Panel interactivo de Plotly con las entidades más frecuentes por tipo."""
    if not entidades_dict:
        return go.Figure()

    # Colores semánticos por tipo de entidad (variable visual: matiz → categoría)
    COLORES = {
        "PER": "#2196F3",   # Azul → personas
        "ORG": "#FF9800",   # Naranja → organizaciones
        "LOC": "#4CAF50",   # Verde → lugares
        "MISC": "#9C27B0",  # Violeta → misceláneos
    }

    fig = go.Figure()

    for tipo, counter in entidades_dict.items():
        top = counter.most_common(10)  # Top 10 entidades de cada tipo

        if not top:
            continue

        nombres = [e[0] for e in top]
        freqs = [e[1] for e in top]

        fig.add_trace(go.Bar(
            name=tipo,
            x=freqs,
            y=nombres,
            orientation="h",  # Barras horizontales para etiquetas largas
            marker_color=COLORES.get(tipo, "#607D8B"),
            # Tooltip interactivo con contexto completo
            hovertemplate=f"<b>%{{y}}</b><br>Tipo: {tipo}<br>Frecuencia: %{{x}}<extra></extra>",
        ))

    fig.update_layout(
        title="Entidades Nombradas por Tipo (Top 10 cada uno)",
        xaxis_title="Frecuencia",
        barmode="group",        # Barras agrupadas por tipo en el mismo eje
        height=500,
        template="plotly_white",
        legend_title="Tipo",
        font=dict(size=11),
    )

    return fig  # Retornamos el objeto fig para usarlo directamente en gr.Plot()


# POR QUÉ Lollipop + Barplot sobre WordCloud:
# El WordCloud codifica frecuencia como área de texto → cognitivamente difícil comparar
# áreas (principio de Cleveland & McGill: la longitud es más precisa que el área).
# El Lollipop Chart permite comparar valores exactos con alta Data-Ink Ratio: mínima tinta,
# máxima información cuantitativa. Para toma de decisiones se requiere precisión, no estética.
# Plotly agrega interactividad (hover, zoom, filtro por tipo) que Matplotlib no provee.


# =============================================================================
# PARTE 4: PIPELINE INTEGRADO (ORQUESTACIÓN)
# =============================================================================

class PipelineMediatico:
    """Orquesta la adquisición, análisis y exportación del corpus mediático."""

    def __init__(self, urls_web=None, url_audio=None, ruta_json=None):
        self.urls_web = urls_web or []   # Lista de URLs a scrapear
        self.url_audio = url_audio        # URL del video de YouTube
        self.ruta_json = ruta_json        # Ruta al JSON de corpus previo
        self.df = None                    # DataFrame unificado (se llena al ejecutar)
        self.analizador = None            # Instancia de AnalizadorCorpus

    def ejecutar_pipeline(self):
        """Orquesta las tres etapas: adquisición → unificación → análisis."""
        print("=" * 55)
        print("INICIANDO PIPELINE MEDIÁTICO")
        print("=" * 55)

        # PASO 1: Adquisición desde las tres fuentes en secuencia
        print("\n[1/3] Adquisición de datos...")
        datos_web = extraer_noticias_web(self.urls_web) if self.urls_web else []
        datos_audio = transcribir_audio_youtube(self.url_audio) if self.url_audio else []
        datos_json = cargar_json_previo(self.ruta_json) if self.ruta_json else []

        # PASO 2: Unificamos las tres listas en un DataFrame estándar
        print("\n[2/3] Unificando corpus...")
        self.df = unificar_corpus(datos_web, datos_audio, datos_json)

        if self.df.empty:
            print("  ✗ Corpus vacío — verificá las fuentes de datos.")
            return

        # PASO 3: Análisis lingüístico con spaCy (instanciamos el analizador con el DF)
        print("\n[3/3] Análisis lingüístico con spaCy...")
        self.analizador = AnalizadorCorpus(self.df)

        print("\n" + "=" * 55)
        print("✓ PIPELINE EJECUTADO EXITOSAMENTE")
        print("=" * 55)

    def generar_reporte_y_exportar(
        self,
        ruta_csv="corpus_resultante.csv",
        ruta_json_out="estadisticas.json",
    ):
        """Exporta el DataFrame como CSV y las estadísticas como JSON jerárquico."""
        if self.df is None or self.analizador is None:
            print("  ✗ Primero ejecutá ejecutar_pipeline()")
            return

        # PASO 3: CSV — datos planos, un registro por documento
        # Dropeamos 'doc' porque los objetos spaCy no son serializables a texto plano
        df_export = self.df.drop(columns=["doc"], errors="ignore")
        df_export.to_csv(
            ruta_csv,
            index=False,
            encoding="utf-8-sig",  # utf-8-sig garantiza compatibilidad con Excel en Windows
        )
        print(f"  ✓ CSV exportado → {ruta_csv}")

        # PASO 4: JSON — estadísticas jerárquicas no tabulares
        estadisticas = self.analizador.estadisticas_corpus()
        entidades_raw = self.analizador.extraer_entidades()

        # Convertimos Counter a dict para que sea JSON-serializable
        entidades_serial = {
            tipo: dict(counter.most_common(20))  # Top 20 por tipo
            for tipo, counter in entidades_raw.items()
        }

        reporte = {
            "estadisticas_generales": estadisticas,
            "entidades_nombradas": entidades_serial,
            "palabras_clave": dict(self.analizador.extraer_palabras_clave(30)),
            "verbos_principales": dict(self.analizador.extraer_verbos_principales(15)),
        }

        with open(ruta_json_out, "w", encoding="utf-8") as f:
            json.dump(reporte, f, ensure_ascii=False, indent=2)
        print(f"  ✓ JSON exportado → {ruta_json_out}")


# POR QUÉ dos formatos de exportación (CSV + JSON):
# El CSV es para análisis tabular: un periodista puede abrirlo en Excel y filtrar por origen.
# El JSON preserva la jerarquía natural de las entidades agrupadas por tipo (PER/ORG/LOC),
# que no se puede representar sin pérdida de información en una tabla plana.
# Separar ambos formatos sigue el principio de responsabilidad única: cada archivo
# responde a una naturaleza distinta de consulta analítica.


# =============================================================================
# PARTE 5: DASHBOARD INTERACTIVO CON GRADIO
# =============================================================================

def construir_dashboard(pipeline: PipelineMediatico):
    """Construye el dashboard Gradio a partir de un pipeline ya ejecutado."""

    # Obtenemos todos los datos analíticos antes de construir la interfaz
    estadisticas = pipeline.analizador.estadisticas_corpus()
    palabras_clave = pipeline.analizador.extraer_palabras_clave(20)
    entidades = pipeline.analizador.extraer_entidades()

    # Pre-generamos las figuras estáticas (no cambian con la interacción del usuario)
    fig_origen = visualizar_origen(pipeline.df)
    fig_lollipop = visualizar_palabras_clave_lollipop(palabras_clave)
    fig_entidades = visualizar_entidades_plotly(entidades)

    # DataFrame de estadísticas formateado para la tabla del dashboard
    df_stats = pd.DataFrame([
        {"Métrica": k.replace("_", " ").title(), "Valor": str(v)}
        for k, v in estadisticas.items()
    ])

    # ---- Función de búsqueda de entidades ----
    def buscar_entidad(nombre):
        """Filtra oraciones del corpus que mencionan la entidad buscada."""
        if not nombre or not nombre.strip():
            return pd.DataFrame([{"Resultado": "Ingresá un nombre para buscar."}])

        nombre_lower = nombre.strip().lower()
        encontradas = []

        for _, fila in pipeline.df.iterrows():
            doc = fila["doc"]                      # Objeto Doc de spaCy ya procesado
            for sent in doc.sents:                 # Iteramos sobre oraciones del documento
                if nombre_lower in sent.text.lower():  # Búsqueda case-insensitive
                    encontradas.append({
                        # Truncamos la fuente para que quepa en la tabla del dashboard
                        "Fuente": str(fila["titulo_o_fuente"])[:60] + "...",
                        "Origen": fila["origen"],
                        "Oración": sent.text.strip(),
                    })

        if not encontradas:
            return pd.DataFrame([{"Resultado": f"No se encontró '{nombre}' en el corpus."}])

        return pd.DataFrame(encontradas)

    # ---- Construcción del layout con gr.Blocks y pestañas ----
    # Se eligió layout de Pestañas (gr.Tab) porque:
    # - Separa contextos temáticos sin scroll infinito (descarta Columna Vertical)
    # - Muestra contenido por defecto (descarta Acordeón que oculta secciones)
    # - Facilita la navegación evaluativa: el profesor puede saltar entre secciones
    with gr.Blocks(theme=gr.themes.Soft()) as dashboard:

        gr.Markdown("# Explorador de Agenda Mediática")
        gr.Markdown("**TPI 1 — Adquisición y Análisis Lingüístico de Medios · PLN 2026**")

        # ---- PESTAÑA 1: Panorama y Métricas ----
        with gr.Tab("Panorama y Métricas"):
            gr.Markdown("## Estadísticas Generales del Corpus")

            # Tabla con métricas numéricas del corpus
            gr.DataFrame(
                value=df_stats,
                label="Métricas del Corpus",
                interactive=False,  # Solo lectura — no queremos que el usuario edite
            )

            gr.Markdown("## Distribución por Fuente de Adquisición")
            gr.Plot(value=fig_origen, label="Origen de los Datos")

            gr.Markdown("## Palabras Clave más Frecuentes")
            gr.Plot(value=fig_lollipop, label="Palabras Clave (Lollipop Chart)")

        # ---- PESTAÑA 2: Explorador de Entidades ----
        with gr.Tab("Explorador de Entidades"):
            gr.Markdown("## Entidades Nombradas Detectadas por spaCy")
            gr.Markdown(
                "**PER** = personas &nbsp;|&nbsp; **ORG** = organizaciones "
                "&nbsp;|&nbsp; **LOC** = lugares &nbsp;|&nbsp; **MISC** = otros"
            )

            # Gráfico interactivo de Plotly con entidades por tipo
            gr.Plot(value=fig_entidades, label="Entidades por Tipo")

            gr.Markdown("## Buscar menciones de una entidad en el corpus")

            # Fila con input de búsqueda y botón
            with gr.Row():
                input_entidad = gr.Textbox(
                    label="Nombre de entidad",
                    placeholder="Ej: Argentina, Google, OpenAI, Milei...",
                    scale=4,  # El textbox ocupa más espacio que el botón
                )
                btn_buscar = gr.Button("Buscar", variant="primary", scale=1)

            # Tabla de resultados — se llena solo al hacer click en el botón
            resultado_busqueda = gr.DataFrame(
                label="Oraciones donde aparece la entidad",
                interactive=False,
            )

            # Conectamos el evento click del botón a la función de búsqueda
            btn_buscar.click(
                fn=buscar_entidad,
                inputs=[input_entidad],       # Input: el texto del Textbox
                outputs=[resultado_busqueda], # Output: el DataFrame de resultados
            )

    return dashboard


# POR QUÉ se eligió el layout de Pestañas (Tabs):
# Acordeón → descartado porque oculta contenido por defecto, generando clics extra
#             innecesarios en una evaluación donde el tiempo es limitado.
# Columna Vertical → descartada porque la longitud del scroll dificulta la presentación
#             oral de 10 minutos (el evaluador perdería contexto al bajar/subir).
# Pestañas → elegidas porque separan "ver métricas" de "explorar entidades" como
#             contextos mentales distintos, sin sacrificar acceso inmediato al contenido.


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TPI 1 — Adquisición y Análisis Lingüístico de Medios")
    print("=" * 60)

    # Instanciamos el pipeline con las fuentes definidas al inicio del archivo
    # Podés modificar URLS_NOTICIAS y URL_VIDEO_YOUTUBE arriba para cambiar el corpus
    pipeline = PipelineMediatico(
        urls_web=URLS_NOTICIAS,
        url_audio=URL_VIDEO_YOUTUBE,
        ruta_json=RUTA_JSON_PREVIO,  # Se omite automáticamente si el archivo no existe
    )

    # Ejecutamos adquisición + unificación + análisis
    pipeline.ejecutar_pipeline()

    # Solo continuamos si el pipeline generó datos válidos
    if pipeline.df is not None and not pipeline.df.empty:

        # Exportamos CSV (datos planos) y JSON (estadísticas jerárquicas)
        pipeline.generar_reporte_y_exportar(
            ruta_csv=os.path.join(os.path.dirname(__file__), "corpus_resultante.csv"),
            ruta_json_out=os.path.join(os.path.dirname(__file__), "estadisticas.json"),
        )

        # Construimos y lanzamos el dashboard interactivo en el navegador
        print("\nIniciando dashboard Gradio en http://localhost:7860 ...")
        dashboard = construir_dashboard(pipeline)
        dashboard.launch(
            share=False,      # Sin enlace público (solo acceso local)
            inbrowser=True,   # Abre el navegador automáticamente
            server_port=7860, # Puerto estándar de Gradio
        )

    else:
        print("\n✗ No se pudo lanzar el dashboard — corpus vacío.")
        print("  Verificá que las URLs sean accesibles y que yt-dlp + FFmpeg estén instalados.")
