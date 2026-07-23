# Estado del MVP del Observatorio

Fecha de corte: 23 de julio de 2026

## Objetivo del MVP

Construir una página interactiva con diseño editorial para explicar, de forma entendible, expedientes, sanciones, sentencias e incidencias vinculadas con la elección federal de diputaciones 2024.

La prioridad del MVP es que cualquier espectador pueda responder tres preguntas:

1. Qué conducta originó la observación o sanción.
2. Qué monto o consecuencia estuvo en controversia.
3. Qué resolvió la justicia electoral y dónde consultar el expediente.

## Datos integrados

Fuentes locales usadas en la app:

- `data/processed/casos.csv`: 7 expedientes base con sala, fecha, sentido, efectos y liga oficial al TEPJF.
- `data/processed/sanciones.csv`: 19 registros de sanción con conducta, sujeto, monto original, monto final y estado.
- `data/processed/hallazgos_portal.csv`: hallazgos prioritarios con candidatura, entidad, distrito, tema y URL oficial.
- `data/analysis/tepjf_corpus_resumen.csv`: 52 sentencias revisadas del corpus TEPJF.
- `data/analysis/diputados_lxvi_electos.csv`: 500 diputaciones electas de la LXVI Legislatura.
- `data/analysis/ganadores_constancia.csv`: personas con constancia o mención relevante en expedientes.
- `data/analysis/tfja_fisel_screening.csv`: verificación nominal preliminar sobre sanciones administrativas y delitos electorales.

## Pantalla principal actual

Archivo:

- `pages/13_Diputaciones_electas.py`

Diseño compartido:

- `src/observatorio/ui.py`

Secciones actuales:

- Introducción editorial: “Qué se sancionó en la elección”.
- Resumen cuantificado: 7 expedientes base, 19 registros de sanción y 52 sentencias localizadas.
- Monto observado por el INE: $20.7 M, calculado como suma de los montos originales de 15 registros de sanción del INE con importe mayor a cero, relacionados con los expedientes base; 4 registros se muestran como expedientes consultables pero no se suman porque no contienen una cantidad económica positiva para agregar al cálculo.
- Monto firme identificado en el corte: $19.7 M.
- Causas principales por monto observado por el INE.
- Lectura en tres pasos: causa, sanción y sentencia.
- Gráficas de causas y estado de los montos.
- Expedientes consultables con enlace directo al TEPJF.
- Contexto de 500 curules de la Cámara de Diputados.
- Mapa de incidencias por entidad.
- Filtros por grupo parlamentario, vía de acceso y entidad.
- Galería de rostros y registro de curules.

## Mapa de incidencias

El mapa ya no muestra concentración de curules. Ahora marca entidades con incidencias territoriales identificadas en `hallazgos_portal.csv`.

Entidades marcadas en el corte actual:

- Ciudad de México.
- Michoacán.
- Chihuahua.

Los asuntos de alcance nacional o representación proporcional se contabilizan aparte para no forzar una ubicación estatal.

## Enlaces a sentencias

Cada expediente del bloque “Sentencias y expedientes consultables” incluye enlace directo al portal del TEPJF desde la columna `url_sentencia` en `casos.csv`.

Ejemplos integrados:

- `SUP-RAP-342/2024 y acumulado`
- `SUP-RAP-352/2024 y acumulado`
- `SUP-RAP-357/2024`
- `SUP-RAP-413/2024`
- `SCM-RAP-47/2024`
- `ST-RAP-74/2024 y acumulado`
- `ST-RAP-50/2024`

## Decisiones visuales

- Fondo blanco, sin cuadrícula de fondo.
- Retícula editorial mediante líneas, columnas y jerarquía tipográfica.
- Paleta institucional con guinda, dorado, verde y negro.
- Tipografía Montserrat.
- Sin barra lateral de Streamlit.
- Sin etiquetas visibles como “PNG”, “B/N”, “carta horizontal” o referencias a herramientas generativas.
- Títulos con acentos y redacción editorial.
- Titular principal separado por líneas para evitar choque visual entre letras.

## Responsividad

Se añadieron breakpoints para:

- Escritorio: retícula amplia, mapa y texto en dos columnas.
- Tablet: columnas apiladas cuando el ancho baja de 900 px; listas en dos columnas.
- Smartphone: una sola columna cuando el ancho baja de 640 px; reducción de márgenes, tipografía más contenida y métricas apiladas.

## Verificaciones realizadas

- `python3 -m py_compile src/observatorio/ui.py pages/13_Diputaciones_electas.py`
- Ejecución local del archivo de página con `runpy` para detectar errores de columnas o datos.
- Revisión textual para retirar etiquetas técnicas visibles no deseadas.
- Capturas exportadas en `exports/`.
- Exportación PDF de diputaciones electas con HTML dedicado y Chromium/Playwright.
- Verificación del PDF con `pypdf`: 6 páginas con texto extraíble y enlaces/anotaciones.

## Exportación PDF de diputaciones electas

Se implementó un botón profesional “Descargar PDF” en `pages/13_Diputaciones_electas.py`.

Estrategia adoptada:

- HTML editorial dedicado generado desde las mismas fuentes CSV del MVP.
- Render a PDF con Chromium mediante Playwright.
- Tamaño carta horizontal con `@page`, sin controles de Streamlit, sin barra del navegador y sin textos técnicos.
- Captura de verificación generada desde la misma vista HTML usada para producir el PDF.

Archivos relevantes:

- `src/observatorio/pdf_export.py`: constructor HTML y exportador PDF.
- `exports/diputaciones_electas_reporte.html`: vista limpia de exportación.
- `exports/diputaciones_electas_reporte.pdf`: PDF generado.
- `exports/captura_diputaciones_pdf.png`: captura de portada del resultado.
- `exports/captura_diputaciones_pdf_mapa.png`: captura de la página del mapa.
- `exports/tepjf_verificacion_enlaces_descargas.csv`: auditoría de enlaces oficiales y copias locales.
- `exports/tepjf_candidatas_revision_2025.csv`: primer inventario de sentencias 2025 candidatas para robustecer el corpus.
- `data/geo/mexico_states_inegi_svg_paths.json`: geometría estatal vectorial simplificada desde el servicio GeoJSON de INEGI.
- `exports/tepjf_bitacora_busquedas_chrome.json`: bitácora de consultas ejecutadas en Chrome sobre el buscador institucional del TEPJF.
- `exports/captura_tepjf_buscador_consulta.png`: captura de evidencia de la consulta en el buscador del TEPJF.
- `data/interim/tepjf_diputaciones_2023_2025_exhaustive_manifest.csv`: manifest ampliado de 41 expedientes candidatos 2023-2025.
- `exports/tepjf_bitacora_descarga_exhaustiva_resumen.csv`: resumen de descarga de la ronda exhaustiva.

Contenido del PDF:

- Encabezado editorial del Observatorio.
- Título de portada actualizado a “Qué se sancionó en diputaciones federales 2024”, con mayor separación entre la marca del Observatorio y el titular.
- Entradilla de portada con nota breve del método: 52 sentencias TEPJF analizadas para explicar causa, monto controvertido y resolución jurisdiccional.
- Resumen de registros de sanción del INE, montos administrativos vinculados y estado jurisdiccional.
- Causas principales por monto observado por el INE; no se presentan como una suma textual contenida en cada sentencia TEPJF.
- Contexto de diputaciones electas y composición parlamentaria.
- Mapa de México por entidad federativa con geometría INEGI: estados sin incidencia en gris editorial y entidades con incidencia en guinda.
- Tarjetas de Chihuahua, Ciudad de México y Michoacán reposicionadas en la parte superior derecha del mapa para evitar encimarse con la silueta nacional.
- Expedientes consultables con URL oficial TEPJF.
- Fuentes y alcance del corte documental.
- Se retiró la muestra de retratos de diputaciones para evitar inferir vínculos personales con sanciones si el expediente no lo establece expresamente.
- La página de fuentes y método se reescribió con redacción académica: búsqueda en el portal público y buscador institucional del TEPJF, descarga de versiones públicas disponibles, extracción de texto, revisión del sentido de la resolución y delimitación del corpus base a 52 sentencias pertinentes.
- La ronda de ampliación identificó 41 expedientes candidatos 2023-2025; en la corrida documentada se descargaron 5 nuevos HTML, se integraron 2 textos previos de 2025 y quedaron 34 candidatos pendientes por restricciones de navegación, timeout o protección del portal.
- Se incorporaron referencias en formato APA para TEPJF, INE, Cámara de Diputados e INEGI.

Verificación posterior:

- Se corroboraron 11 URLs oficiales del portal TEPJF entre expedientes base y hallazgos prioritarios.
- Las 11 sentencias/hallazgos tienen copia HTML local descargada y sin CAPTCHA.
- La página de expedientes del PDF conserva 7 enlaces clicables a sentencia oficial.
- El coloreado del mapa corresponde a 5 incidencias territoriales: 2 en Ciudad de México, 2 en Michoacán y 1 en Chihuahua.
- Un hallazgo de representación proporcional se mantiene fuera del mapa para no asignar ubicación estatal artificial.
- Se reforzó la página de expedientes consultables: la columna de conducta y efectos ahora identifica quién incurrió en la conducta, partido o coalición, candidatura vinculada cuando existe, conducta específica y sentido/efecto de la sentencia.
- Se aclaró la frontera metodológica de los montos: provienen de `data/processed/sanciones.csv`, matriz administrativa construida a partir de registros de sanción del INE relacionados con expedientes TEPJF. Las sentencias revisadas confirman, modifican, revocan o sobreseen actos de autoridad, pero no siempre reproducen el monto acumulado por causa dentro del texto jurisdiccional.
- En app y PDF, los rótulos se ajustaron a “Monto observado por el INE”, “Causas por monto observado por el INE” y “Monto observado por el INE”.
- La nota sobre cuantificación de montos se colocó al final de la hoja de “Expedientes consultables”, con separador propio y redacción sustantiva para lector general: explica que la búsqueda TEPJF delimitó 52 sentencias, que 7 expedientes base se seleccionaron por fiscalización de diputaciones federales y que los $20.7 M observados por el INE provienen de 15 registros monetarios relacionados con cuatro sentencias específicas: `SUP-RAP-342/2024`, `SUP-RAP-352/2024`, `SUP-RAP-357/2024` y `SUP-RAP-413/2024`, con sujeto obligado y monto agregado por expediente. También aclara que el mapa y la tabla pueden mostrar expedientes sin que se añadan a la sumatoria: el mapa ubica casos por entidad o distrito, mientras que la sumatoria solo agrega pesos cuando existe una cantidad económica positiva en el registro.
- En “Expedientes consultables”, los registros con `$0.00` ahora explican en la columna de conducta que aparecen en el mapa por la ubicación de la controversia, pero no se añaden al total porque la sumatoria no cuenta expedientes, sino cantidades económicas positivas. La columna de monto usa la regla breve: “No se suma: no hay cantidad económica”.
- Se corrigió la nota para mostrar montos exactos por sentencia y evitar descuadres por redondeo: $7,303,754.15 + $10,312,470.58 + $2,638,887.56 + $445,361.30 = $20,700,473.59, abreviado visualmente como $20.7 M.
- Se auditó la correspondencia expediente-URL en `casos.csv` y `hallazgos_portal.csv`; los enlaces oficiales normalizados coinciden con el expediente principal mostrado en cada fila.
- La columna de URL oficial ya no muestra la copia local; muestra el enlace oficial TEPJF como texto clicable.
- Las tarjetas del mapa de incidencias ahora incluyen número de expedientes por entidad y un párrafo narrativo que sintetiza candidatura o sujeto vinculado, tema, fecha, territorio, vía procesal y relevancia del expediente.
- En PDF y app, las tarjetas inferiores del mapa quedaron agrupadas en tres columnas fijas: Chihuahua, Ciudad de México y Michoacán.
- La redacción del mapa identifica el corte documental de llegada: “Corte documental al 23 de julio de 2026”, con singular/plural correcto: “1 expediente” o “2 expedientes”.
- La app de Streamlit reutiliza el mismo mapa SVG estatal del PDF: México se muestra por entidad federativa, las entidades sin incidencia permanecen en gris y solo Chihuahua, Ciudad de México y Michoacán aparecen en guinda.
- Se corrigió la salida HTML del mapa para que las notas laterales se rendericen como elementos visuales y no como código literal dentro de Streamlit.
- El pie de página se homologó en las 4 páginas: “Observatorio de Fiscalización Electoral - Proceso Federal 2023-2024 · Corte: 23 de julio de 2026”.
- Se retiró de la página final la banda de “52 sentencias analizadas” y la nota operativa sobre siguiente fase.
- El alcance se reescribió con tono formal: el reporte parte de un corte documental y no sustituye el universo completo de resoluciones administrativas del INE, sentencias del TEPJF ni determinaciones posteriores.
- Los resúmenes de expedientes e incidencias se transformaron de etiquetas visibles a párrafos narrativos formales para lectura editorial.
- La sección “Expedientes consultables” se amplió con columnas de entidad y distrito tanto en la app como en el PDF.
- La columna territorial de expedientes consultables se rotuló como correspondencia del mapa: “Mapa: Chihuahua”, “Mapa: Ciudad de México” o “Mapa: Michoacán” cuando el expediente corresponde a una entidad coloreada; los asuntos de representación proporcional o alcance nacional se mantienen como “Sin entidad estatal”.
- El PDF divide los expedientes consultables en dos páginas para conservar legibilidad en carta horizontal.
- El orden de expedientes consultables prioriza las entidades del mapa: Chihuahua, Ciudad de México y Michoacán; después aparecen asuntos de representación proporcional o alcance nacional.
- Se incorporaron a la tabla consultable los hallazgos del mapa que no estaban en los expedientes base de sanciones, para que cada entidad coloreada tenga correspondencia identificable.
- Se corrigió la semántica de la columna “Entidad”: los asuntos de representación proporcional o alcance nacional ahora aparecen como “Sin entidad estatal”, y su ámbito se explica en la columna de distrito/ámbito.

Recomendación de ampliación:

- Para robustecer el proyecto con 2023-2025 conviene abrir una fase separada de inventario controlado, no descargar “todo el Tribunal” sin filtros.
- Criterios sugeridos: diputaciones federales, fiscalización, propaganda, nulidad, rebase de tope, RP, elegibilidad, medios RAP/JIN/REC/JDC/PSD/PSC vinculados con Cámara de Diputados.
- El flujo recomendado es: construir manifest de URLs oficiales, descargar HTML oficial con control de CAPTCHA, extraer texto local, clasificar por categorías, revisar muestra humana y solo después incorporar nuevos hallazgos al mapa y al PDF.
- Primeros candidatos 2025 detectados: `SUP-RAP-18/2025` y `SUP-RAP-108/2025` descargados y marcados con pertinencia preliminar alta; `SUP-RAP-104/2025` detectado como relevante por buscador público, pero pendiente de descarga local por protección del portal.
- Para publicación externa se recomienda resolver los pendientes de descarga del manifest ampliado desde una sesión manual estable del portal TEPJF o con exportación institucional del buscador, antes de incorporar esos expedientes al análisis sustantivo.

## Pendientes recomendados

- Añadir una captura automática confiable por viewport: smartphone, tablet y escritorio.
- Continuar la validación documental de expedientes candidatos 2023-2025 antes de incorporar nuevos hallazgos al mapa.
