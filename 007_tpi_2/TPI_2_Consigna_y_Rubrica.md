# TPI 2: Text Mining y análisis discursivo comparado

**Modalidad:** trabajo en duplas.

**Entrega:** notebook completo + corpus estructurado + reflexión interpretativa dentro del notebook.

## Propósito

Este segundo trabajo integrador del módulo les pide pasar de la guía al uso autónomo y comparativo de las herramientas vistas hasta acá. Ya no se trata de seguir un laboratorio paso a paso, sino de construir un recorte, justificarlo, producir observables y sostener una interpretación situada.

El eje del trabajo es la comparación entre **dos grupos de textos** sobre una misma temática o problema discursivo.

## Modalidades posibles del corpus

Elijan una de estas rutas:

1. **Medio vs. medio**
   - Ejemplo: `Cenital` y `Anfibia` frente a una temática como IA, guerra, plataforma, educación, ciencia o trabajo.
2. **Columnista vs. columnista**
   - Dos autoras o autores que escriben sobre un mismo problema.
3. **Mismo columnista en contextos distintos**
   - Mismo autor en dos medios o en dos series diferentes.
4. **Podcast vs. podcast** o **serie vs. serie**
   - Permitido, pero más exigente por la calidad de la transcripción.

## Restricciones obligatorias

- El corpus debe tener entre **6 y 10 textos**.
- Tiene que haber exactamente **dos grupos comparables**.
- La temática debe ser consistente.
- La comparación debe estar escrita en la columna `grupo_comparacion`.
- El corpus debe incluir estas columnas mínimas:
  - `id`
  - `fecha`
  - `medio`
  - `autor`
  - `titulo`
  - `texto`
  - `grupo_comparacion`

## Qué tienen que hacer

En el notebook deben:

1. justificar el corpus y la comparación elegida;
2. cargar y validar el corpus;
3. procesarlo con `spaCy`;
4. construir observables iniciales con frecuencias, entidades y bigramas;
5. comparar `Bag of Words` y `TF-IDF`;
6. usar al menos dos visualizaciones analíticas legibles;
7. volver al menos a tres fragmentos concretos del corpus;
8. cerrar con una interpretación comparativa y una sección de límites del método.

## Qué no vale como resolución suficiente

No alcanza con:

- pegar tablas sin comentario;
- listar términos frecuentes sin interpretar;
- usar la IA para redactar conclusiones sin evidencia del corpus;
- reemplazar la lectura cercana por gráficos;
- saltear la comparación entre grupos;
- usar embeddings, vectores densos o LLMs como sustituto del recorrido pedido.

## Trabajo con IA

Pueden usar IA como apoyo de programación, auditoría o discusión metodológica. Pero deben dejar registro breve de ese uso en el notebook y sostener ustedes las decisiones finales.

## Entregables

- `TPI_2_Text_Mining_y_Analisis_Discursivo_Comparado.ipynb` completo;
- archivo del corpus en `csv` o `jsonl`;
- visualizaciones incluidas en el notebook;
- reflexión final con interpretación y límites.

## Rúbrica de evaluación

| Criterio | Peso | Qué se espera |
|---|---:|---|
| Recorte y justificación del corpus | 20% | Corpus pertinente, comparable y bien delimitado |
| Corrección técnica del procesamiento | 20% | Carga, validación, spaCy y representaciones sparse bien implementadas |
| Calidad de tablas y visualizaciones | 20% | Gráficos legibles, pertinentes y bien rotulados |
| Interpretación discursiva con evidencia | 25% | Hallazgos apoyados en tablas, figuras y fragmentos |
| Reflexión metodológica y límites | 15% | Conciencia de qué muestra y qué no muestra este enfoque |

## Condiciones mínimas para aprobar

La entrega no alcanza el mínimo si:

- no hay comparación real entre dos grupos;
- falta el corpus estructurado;
- no aparece `TF-IDF` junto con `Bag of Words`;
- no hay vuelta al fragmento;
- la interpretación se reduce a descripción superficial.

## Recomendación final

Mantengan el corpus pequeño, comparable y defendible. En este trabajo vale más una comparación bien justificada de ocho textos que un corpus enorme mal curado y mal leído.

---

# Resolución del TPI 2

**Alumno:** José Navas  
**Materia:** Procesamiento de Lenguaje Natural — IFTS N° 24  
**Cuatrimestre:** 1° cuatrimestre 2026  
**Modalidad elegida:** Medio vs. medio — *Cenital* y *Anfibia* frente a la temática de Inteligencia Artificial

---

## Registro breve de trabajo con IA

| Bloque | Objetivo de la consulta | Prompt o pedido a la IA | Qué respondió (resumen) | Qué conservaron y por qué | Qué descartaron y por qué |
|---|---|---|---|---|---|
| Definición del corpus | Verificar que el archivo CSV tenía la estructura correcta según la consigna | "Analiza el archivo corpus_tpi2.csv y dime qué tiene mal" | La IA identificó que las columnas tenían los nombres de las variables Python (`COLUMNA_TEXTO`, `COLUMNA_GRUPO`) en lugar de los valores correctos (`texto`, `grupo_comparacion`), que la columna `grupo_comparacion` estaba vacía (todo NaN) y que el encoding era `latin-1` en lugar de UTF-8 | Se adoptó la corrección de nombres de columna, el relleno de `grupo_comparacion` desde la columna `medio`, y la conversión a UTF-8. Fueron cambios estructurales necesarios para que el notebook pudiera ejecutarse | No se alteró ninguna columna de contenido (`texto`, `medio`, etc.) porque los datos en sí eran correctos |
| Procesamiento con spaCy | Entender qué hace cada función del bloque de procesamiento lingüístico | "Explicame qué hace `nlp.pipe()`, `token.is_stop` y la función `normalizar_lemma`" | Explicó que `nlp.pipe()` procesa lotes de texto de forma eficiente, que `is_stop` filtra palabras funcionales sin contenido semántico y que lematizar normaliza las formas flexionadas a su raíz común | Se incorporaron estas explicaciones como comentarios de código en las celdas correspondientes | No se modificó el código base porque la consigna prohíbe alterar la estructura |
| Representaciones sparse | Clarificar la diferencia entre BoW y TF-IDF aplicada al corpus propio | "¿Por qué `latamgpt` y `china` no aparecen entre los términos más frecuentes pero sí en el top de TF-IDF?" | Explicó que BoW cuenta frecuencias brutas y que TF-IDF penaliza los términos compartidos entre grupos y premia los exclusivos. Un término puede ser poco frecuente en términos absolutos pero muy diagnóstico de un grupo | Esta distinción se conservó íntegramente en la sección de escritura interpretativa, porque clarifica el hallazgo central del análisis | Se descartó la sugerencia de filtrar los términos en inglés presentes en Anfibia, porque forman parte del estilo académico genuino de ese corpus |
| Visualización | Interpretar el heatmap de TF-IDF generado por el notebook | "¿Cómo leer el mapa de calor de términos distintivos?" | Señaló que las celdas con color más intenso indican mayor especificidad: términos frecuentes en un grupo y casi ausentes en el otro son los más útiles para caracterizar cada serie | Se usó esta lectura en la interpretación de la sección 10, señalando los ejes de contraste más claros | No se cambió la paleta de colores ni el tipo de gráfico porque el resultado era legible y pertinente |
| Interpretación final | Auditar la coherencia entre los datos y la interpretación discursiva redactada | "¿El contraste que describimos entre Cenital y Anfibia está sostenido por los observables?" | Confirmó que el contraste geopolítico/económico (Cenital) vs. crítico/latinoamericano (Anfibia) está respaldado por los datos de TF-IDF y bigramas, y señaló el desbalance de extensión como un límite metodológico que debía mencionarse | Se incorporó el señalamiento del desbalance en la sección de límites. La interpretación principal se mantuvo | No se adoptó una conclusión más contundente porque el corpus pequeño (10 textos) no lo justifica estadísticamente |

---

## Corpus

### Descripción del corpus

| id | fecha | medio | autor | título | grupo |
|---|---|---|---|---|---|
| C-1 | 2021-01-06 | Cenital | Valentín Muro | La burbuja de la inteligencia artificial | Cenital |
| C-2 | — | Cenital | Valentín Muro | La inteligencia artificial no muestra el pasado, lo reescribe | Cenital |
| C-3 | — | Cenital | Alejandro Giuffrida | Una nueva vida no biológica: ¿qué tan gobernados estamos por la IA? | Cenital |
| C-4 | 2025-10-11 | Cenital | Federico Merke | La nueva fase de la competencia tecnológica: chips, datos y poder | Cenital |
| C-5 | — | Cenital | Agostina Mileo | La inteligencia artificial no previene la estupidez natural | Cenital |
| C-6 | 2025-07-07 | Anfibia | Ernesto Picco | Una IA latinoamericana es posible | Anfibia |
| C-7 | — | Anfibia | Sofía Trejo | Inteligencia artificial, pero ¿a qué costo? | Anfibia |
| C-8 | 2021-01-06 | Anfibia | Iván Meza Ruiz, Sofía Trejo, Fernanda López | ¿Quién controla los sistemas de Inteligencia Artificial? | Anfibia |
| C-9 | 2021-12-05 | Anfibia | Esteban Magnani | ¿Hacia dónde nos lleva la inteligencia artificial? | Anfibia |
| C-10 | 2024-02-09 | Anfibia | Martín Mazzini | Es lo que AI | Anfibia |

### Métricas del corpus

| Métrica | Valor |
|---|---|
| Total de documentos | 10 |
| Palabras aproximadas totales | 23.964 |
| Promedio por texto | 2.396 palabras |
| Palabras totales — Cenital | 8.748 (~1.749 por texto) |
| Palabras totales — Anfibia | 15.216 (~3.043 por texto) |

---

## Justificación del recorte

**¿Qué comparamos exactamente?**

Comparamos cómo dos medios digitales argentinos de periodismo de largo aliento —*Cenital* y *Anfibia*— abordan el fenómeno de la inteligencia artificial en el período 2021–2025. El corpus reúne 5 artículos de cada medio sobre IA, seleccionados por tratar la temática de forma central y sostenida.

**¿Por qué este corpus y no otro?**

La elección responde a tres razones. Primero, ambas publicaciones tienen perfil editorial definido y público identificable: Cenital produce periodismo de datos y análisis de coyuntura; Anfibia produce periodismo narrativo y ensayo académico-cultural. Segundo, la IA es un tema que ambas cubren con suficiente densidad como para encontrar piezas comparables. Tercero, la diferencia de enfoque editorial es lo suficientemente marcada como para esperar contrastes discursivos observables con herramientas de text mining.

**¿Qué hace comparables a los dos grupos?**

Los hace comparables el hecho de que comparten: (a) mismo universo temático (inteligencia artificial); (b) mismo formato textual (artículo de opinión o análisis periodístico extenso); (c) mismo período temporal aproximado; (d) mismo idioma (español rioplatense); (e) misma plataforma de distribución (digital, acceso abierto). La diferencia radica en la posición editorial y el encuadre analítico, que es precisamente lo que queremos contrastar.

**¿Qué límites iniciales ya vemos en el recorte?**

- **Desbalance de extensión:** los textos de Anfibia son significativamente más largos (~3.043 palabras promedio) que los de Cenital (~1.749 palabras). Anfibia aportará más términos de forma bruta, lo que puede inflar sus frecuencias absolutas. TF-IDF mitiga parcialmente este problema al trabajar con pesos relativos.
- **Heterogeneidad de autores en Cenital:** los 5 artículos tienen 5 autores distintos, introduciendo variación de estilo. En Anfibia hay mayor recurrencia de autoras.
- **Corpus pequeño:** 10 textos son suficientes para la consigna pero insuficientes para generalizar. Cualquier afirmación sobre "el discurso de Cenital" o "el discurso de Anfibia" debe leerse como tendencia observable en esta muestra, no como caracterización de la publicación completa.

---

## Análisis del corpus

### Auditoría del desbalance (sección 5)

Los gráficos confirman lo anticipado: ambos grupos tienen la misma cantidad de textos (5 cada uno), pero Anfibia casi **duplica** el total de palabras de Cenital (≈15.200 vs. ≈8.700).

**Consecuencias metodológicas:**

1. Las frecuencias absolutas de Anfibia serán sistemáticamente más altas simplemente porque hay más texto. Cualquier comparación del tipo "Anfibia usa X más que Cenital" debe ajustarse por el factor de escala.
2. TF-IDF mitiga el problema al trabajar con pesos relativos. La lectura de TF-IDF será más confiable que la de BoW para detectar términos genuinamente distintivos.
3. Los bigramas también se ven afectados: hay que comparar proporciones, no valores absolutos.

> **Las diferencias cualitativas de vocabulario importan más que las diferencias cuantitativas de frecuencia.**

---

### Observables iniciales: términos, entidades y bigramas (sección 7)

#### Términos compartidos — lo que no diferencia

Tanto Cenital como Anfibia tienen entre sus términos más frecuentes "inteligencia", "artificial", "IA", "sistema" y "dato". Son el vocabulario nuclear del tema. Su alta frecuencia en ambos grupos no dice nada sobre el posicionamiento editorial de cada medio.

#### Términos que diferencian — primera señal de contraste

| Cenital | Anfibia |
|---|---|
| china, empresa, millón, nvidia, chip | sistema, tarea, campo, desarrollo, exactitud |
| Sam Altman, OpenAI, Facebook | LatamGPT, Cenia, ChatGPT |
| Marco: geopolítico y económico | Marco: técnico-crítico y regional |

#### Bigramas más frecuentes

| Anfibia | frec. | Cenital | frec. |
|---|---|---|---|
| sistema ia | 34 | inteligencia artificial | 22 |
| inteligencia artificial | 29 | mil millón | 9 |
| sistema inteligente | 17 | red social | 5 |
| crear sistema | 13 | centro dato | 4 |
| base dato | 9 | sam altman | 3 |

Anfibia organiza el discurso en torno a **arquitectura de sistemas y datasets**. Cenital lo organiza en torno a **economía y actores de la industria**.

#### Entidades nombradas más frecuentes

| Cenital | veces | Anfibia | veces |
|---|---|---|---|
| IA | 17 | IA | 77 |
| China | 15 | LatamGPT | 15 |
| OpenAI | 12 | Cenia | 12 |
| Nvidia | 6 | ChatGPT | 6 |
| Facebook | 6 | Google | 10 |

Cenital nombra **corporaciones y estados** como protagonistas de una disputa tecnológica. Anfibia nombra **herramientas y proyectos regionales latinoamericanos**.

---

### BoW vs. TF-IDF: volumen versus especificidad (sección 8)

#### Lo que BoW muestra

El Bag of Words confirma lo visto con Counter: Anfibia acumula más ocurrencias brutas por su mayor extensión. Los términos de mayor frecuencia absoluta —"sistema", "dato", "desarrollo", "modelo"— aparecen en ambos grupos, simplemente en mayor volumen en Anfibia. BoW no distingue entre "este término es importante para este grupo" y "este término aparece más porque el texto es más largo".

#### Lo que TF-IDF revela

TF-IDF cambia radicalmente la imagen al penalizar los términos compartidos y premiar los exclusivos:

**Cenital — términos más distintivos (TF-IDF)**

| Término | Peso TF-IDF |
|---|---|
| china | 0.3141 |
| chip | 0.1767 |
| nvidia | 0.1767 |
| trump | 0.0982 |
| estadounidense | 0.0982 |
| elección | 0.0982 |
| votar | 0.0982 |

**Anfibia — términos más distintivos (TF-IDF)**

| Término | Peso TF-IDF |
|---|---|
| latamgpt | 0.1484 |
| exactitud | 0.1391 |
| colección | 0.1391 |
| deep | 0.1391 |
| acm | 0.1298 |
| cenia | 0.1206 |
| acceso | 0.1020 |

#### La diferencia central

> BoW dice: *Anfibia habla más de "sistema".*  
> TF-IDF dice: *lo que verdaderamente define a Anfibia es hablar de **qué sistemas**, desde **dónde** y con **qué métricas**. Lo que define a Cenital es enmarcar la IA como objeto de competencia entre Estados y empresas.*

#### Artefacto metodológico a señalar

La alta presencia de términos en inglés en el top TF-IDF de Anfibia ("and", "the", "in", "deep") revela que al menos un texto incluye referencias bibliográficas académicas en inglés (citas de papers de la ACM). Estos términos no son parte del discurso periodístico del medio sino un artefacto del formato de citación académica.

---

## Escritura interpretativa

### 1. Recorte y comparación

Comparamos el tratamiento discursivo de la inteligencia artificial en dos medios digitales argentinos con perfiles editoriales diferenciados: *Cenital* (periodismo de datos, análisis de coyuntura) y *Anfibia* (periodismo narrativo, ensayo cultural-académico). Ambos cubren la IA en el período 2021–2025, con 5 artículos cada uno.

Lo que los vuelve comparables es la compartición del universo temático, el formato y el período. Lo que los vuelve contrastables es la diferencia de posición editorial: Cenital encuadra la IA desde la geopolítica tecnológica y la economía; Anfibia la encuadra desde la política tecnológica latinoamericana y el análisis técnico-crítico. Esta diferencia de marco no se asume: es lo que el análisis debía confirmar o refutar.

### 2. Lectura distante

*Cenital* se organiza alrededor de actores e instituciones de poder: China (15 menciones), EE.UU., Nvidia, OpenAI, Sam Altman, Facebook. Los bigramas refuerzan el encuadre económico: "mil millón", "red social", "centro dato". El vocabulario es el del periodismo tecnológico-financiero de coyuntura internacional.

*Anfibia* se organiza alrededor de conceptos técnicos y proyectos regionales: "sistema IA" (bigrama dominante, 34 apariciones), "sistema inteligente" (17), "crear sistema" (13), "base dato" (9). Las entidades nombradas son herramientas y organizaciones latinoamericanas: LatamGPT, Cenia, ChatGPT. El vocabulario combina técnica de sistemas con preocupaciones de acceso y soberanía regional.

**¿Qué diferencias aparecen con TF-IDF que no aparecen con frecuencias?**

Con frecuencias brutas (BoW), ambos grupos comparten el podio: "inteligencia", "artificial", "sistema", "dato". La diferencia es de cantidad, no de naturaleza. Con TF-IDF el contraste es nítido: los términos diagnósticos de Cenital son geopolíticos (china, chip, nvidia, trump, elección); los de Anfibia son técnico-regionales (latamgpt, exactitud, cenia, acceso).

La diferencia más importante que TF-IDF hace visible es que *Cenital habla de **quién tiene el poder** sobre la IA*, mientras que *Anfibia habla de **cómo funciona** la IA y **quién debería poder acceder** a ella desde América Latina*.

### 3. Lectura cercana

**Fragmento 1 — "china" en Cenital (C-4, Federico Merke)**

> *"La disputa entre Estados Unidos y China por el control de la inteligencia artificial ingresó en una etapa estructural..."*

La palabra no funciona como referencia geográfica neutral sino como nombre de uno de los dos polos de una guerra de posición tecnológica. El artículo no describe China desde adentro sino como amenaza o competidor desde la mirada estadounidense. El encuadre geopolítico es el que organiza toda la pieza.

**Fragmento 2 — "latamgpt" en Anfibia (C-6, Ernesto Picco)**

> *"...Hay inteligencia artificial más allá de las big tech. Mientras el noventa por ciento de la información en internet está en inglés, el Cenia trabaja en LatamGPT..."*

El término ancla toda la argumentación del artículo: la soberanía tecnológica requiere datos propios, modelos propios y financiamiento público. La presencia de "latamgpt" como término con alto TF-IDF no es solo frecuencia: es el nombre del argumento central del grupo.

**Fragmento 3 — "chip" en Cenital (C-4, Federico Merke)**

> *"...EE.UU. restringió las exportaciones de chips de alta gama a China. Nvidia, el principal fabricante de procesadores para IA..."*

Volver al fragmento muestra que el artículo construye la IA como **problema de cadena de suministro de hardware**, no como problema de algoritmos o datos. Esta lectura es imposible de hacer solo mirando la tabla de bigramas; requiere el regreso al texto.

### 4. Visualización y método

**¿Qué gráfico fue el más útil?**

El heatmap de TF-IDF fue el más útil. A diferencia del gráfico de barras de frecuencias (que solo confirmaba el desbalance de extensión), el heatmap mostró que los grupos se separan en dimensiones cualitativas: Cenital tiene color alto en términos geopolíticos; Anfibia en términos técnico-regionales.

**Límites del enfoque**

1. **No captura sintaxis ni argumento.** Que "china" aparezca 15 veces no dice si el texto critica, celebra o describe a China. La posición discursiva requiere lectura cercana.
2. **No distingue citas de voz propia.** El alto TF-IDF de términos en inglés en Anfibia revela referencias bibliográficas, no discurso periodístico. BoW y TF-IDF no separan ambas voces.
3. **El desbalance de extensión contamina el BoW.** Con textos de longitud tan diferente, las comparaciones de frecuencias absolutas son poco confiables sin normalización.
4. **El corpus pequeño limita la generalización.** 10 textos no permiten afirmar tendencias robustas. Los resultados son descriptivos de esta muestra.

**¿Qué no se puede afirmar solo con representaciones sparse?**

No se puede afirmar que un medio "tiene una posición crítica" o "defiende a las big tech" solo mirando frecuencias. Tampoco se puede inferir intención ni efecto sobre el lector. No se detectan ironías, negaciones ni variaciones de sentido del mismo término en distintos contextos. Las representaciones sparse son un primer filtro que orienta la lectura, no un sustituto de ella.

---

## Checklist final de entrega

| Ítem | Estado | Detalle |
|---|:---:|---|
| Corpus con 6–10 textos y dos grupos comparables | ✅ | 10 textos: 5 Cenital + 5 Anfibia |
| Columna `grupo_comparacion` completa y sin nulos | ✅ | Dos valores exactos: "Cenital" y "Anfibia" |
| Procesamiento con spaCy (lematización + entidades) | ✅ | Sección 6 del notebook |
| Bigramas | ✅ | Sección 7 del notebook |
| Bag of Words | ✅ | Sección 8 del notebook |
| TF-IDF con comparación explícita vs. BoW | ✅ | Sección 8 del notebook |
| Al menos dos visualizaciones analíticas legibles | ✅ | Gráfico de barras (términos) + heatmap TF-IDF + gráficos de extensión |
| Vuelta a tres fragmentos concretos del corpus | ✅ | Sección 9 (automática) + sección 10 (china, latamgpt, chip) |
| Interpretación final con evidencia | ✅ | Sección 10, cuatro partes |
| Sección explícita de límites del método | ✅ | Sección 10.4 |
| Notebook ejecutable de principio a fin | ✅ | Sin ediciones manuales intermedias; corpus en misma carpeta |
| Registro de trabajo con IA | ✅ | Tabla completa con 5 bloques |
