# Handoff: página y PDF de diputaciones electas

Fecha de corte: 23 de julio de 2026

## Proyecto

App Streamlit local del Observatorio de Fiscalización Electoral 2023-2024.

Ruta local:

- `/Users/amluis/observatorio-fiscalizacion-2023-2024`

Página principal trabajada:

- `pages/13_Diputaciones_electas.py`

CSS global:

- `src/observatorio/ui.py`

Exportador PDF:

- `src/observatorio/pdf_export.py`

Documento de estado general:

- `docs/estado_mvp_observatorio_2026-07-23.md`

## Estado funcional

La página `pages/13_Diputaciones_electas.py` ya incluye:

- Diseño editorial premium con Montserrat, fondo blanco, retícula, guinda, dorado, verde y negro.
- Sin sidebar visible de Streamlit.
- Introducción editorial del Observatorio.
- Encabezado “Qué se sancionó en diputaciones federales 2024”.
- Resumen de 7 expedientes base, 19 registros de sanción y 52 sentencias TEPJF revisadas.
- Botón profesional “Descargar PDF”.
- Gráficas de causas y estado de montos.
- Mapa de México por entidad federativa con geometría estatal.
- Estados en gris cuando no tienen incidencia y en guinda solo cuando tienen incidencia.
- Tarjetas inferiores del mapa en tres columnas: Chihuahua, Ciudad de México y Michoacán.
- Sección de expedientes consultables con entidad, distrito, conducta, monto y URL oficial del TEPJF.
- Contexto de diputaciones electas y galería de curules.

## PDF

El botón “Descargar PDF” genera un reporte limpio, sin controles de Streamlit ni navegador.

Estrategia técnica:

- HTML dedicado construido desde los CSV del proyecto.
- Render con Chromium/Playwright.
- Tamaño carta horizontal.
- Estilos editoriales propios del reporte.
- Enlaces oficiales TEPJF preservados como anotaciones clicables.

Artefactos actuales:

- `exports/diputaciones_electas_reporte.html`
- `exports/diputaciones_electas_reporte.pdf`
- `exports/captura_diputaciones_pdf.png`
- `exports/captura_diputaciones_pdf_mapa.png`
- `exports/captura_diputaciones_pdf_montos_cero.png`
- `exports/captura_diputaciones_pdf_sentencias_montos.png`

Última verificación:

- PDF con 6 páginas.
- PDF con 23 enlaces/anotaciones.
- Compilación Python correcta para `src/observatorio/pdf_export.py`, `pages/13_Diputaciones_electas.py` y `src/observatorio/ui.py`.

## Datos y fuentes locales

Fuentes principales:

- `data/processed/casos.csv`: 7 expedientes base con sentencia TEPJF.
- `data/processed/sanciones.csv`: 19 registros de sanción.
- `data/processed/hallazgos_portal.csv`: hallazgos prioritarios para mapa y expedientes complementarios.
- `data/analysis/tepjf_corpus_resumen.csv`: corpus validado de 52 sentencias.
- `data/analysis/diputados_lxvi_electos.csv`: 500 diputaciones electas.
- `data/geo/mexico_states_inegi_svg_paths.json`: geometría SVG estatal de México.

Archivos de auditoría:

- `exports/tepjf_verificacion_enlaces_descargas.csv`
- `exports/tepjf_bitacora_busquedas_chrome.json`
- `exports/captura_tepjf_buscador_consulta.png`
- `data/interim/tepjf_diputaciones_2023_2025_exhaustive_manifest.csv`
- `exports/tepjf_bitacora_descarga_exhaustiva_resumen.csv`
- `exports/tepjf_revision_pertinencia_corpus.csv`

## Criterio del mapa

El mapa no representa dinero ni número de sanciones monetarias.

El mapa representa expedientes ubicables por entidad o distrito en el corte documental.

Entidades coloreadas:

- Chihuahua: 1 expediente.
- Ciudad de México: 2 expedientes.
- Michoacán: 2 expedientes.

Los asuntos sin entidad estatal clara, de alcance nacional o de representación proporcional no se fuerzan al mapa.

## Criterio de montos

El total observado por el INE es:

- `$20,700,473.59`, abreviado visualmente como `$20.7 M`.

Ese total se obtiene de 15 registros con `monto_original` mayor a cero en `data/processed/sanciones.csv`.

Sentencias que alimentan el monto:

- `SUP-RAP-342/2024`: Movimiento Ciudadano, `$7,303,754.15`.
- `SUP-RAP-352/2024`: Partido Acción Nacional, `$10,312,470.58`.
- `SUP-RAP-357/2024`: Partido del Trabajo, `$2,638,887.56`.
- `SUP-RAP-413/2024`: Morena, `$445,361.30`.

Regla editorial acordada:

- El mapa cuenta expedientes ubicados por entidad o distrito.
- La sumatoria no cuenta expedientes, cuenta pesos.
- Si un expediente aparece en el mapa o en la tabla, pero no tiene una cantidad económica positiva fijada, confirmada o modificada, se muestra como caso consultable, pero no altera el total.
- En esos casos la columna de monto dice: “No se suma: no hay cantidad económica.”

## Enlaces TEPJF

Se auditó la correspondencia expediente-URL.

Resultado:

- `casos.csv`: enlaces normalizados coinciden con el expediente principal mostrado.
- `hallazgos_portal.csv`: enlaces normalizados coinciden con el expediente principal mostrado.
- No se debe mostrar ruta local en la columna URL del PDF; debe mostrarse URL oficial TEPJF.

## Redacción y decisiones editoriales

Cambios ya aplicados:

- Se retiró la sección final que decía “52 sentencias” como banda operativa.
- Se retiró la frase sobre “siguiente fase”.
- Se reescribió “Alcance” con tono formal.
- Se retiraron fotos de candidaturas para evitar sugerir vínculos personales no establecidos por los expedientes.
- Se sustituyeron etiquetas tipo 5W+1H por párrafos narrativos.
- Se evitó “ranking”; se usa “sumatoria”.
- Se explica que los montos no necesariamente aparecen como suma textual dentro de cada sentencia TEPJF, porque el reporte integra registros de sanción del INE relacionados con expedientes jurisdiccionales.

## Despliegue

Opciones discutidas:

- GitHub sirve como repositorio y para publicar artefactos estáticos, como PDF/HTML exportado.
- GitHub Pages no ejecuta Streamlit ni una base de datos dinámica.
- Streamlit Community Cloud podría funcionar si la app usa CSV locales y dependencias compatibles.
- Fly.io es una mejor opción si se requiere app Streamlit persistente con base de datos, almacenamiento o proceso backend.

Recomendación práctica:

- Para mostrar el reporte como PDF/HTML estático: GitHub Pages o repositorio público.
- Para app Streamlit interactiva: Streamlit Community Cloud si no hay base de datos persistente; Fly.io si habrá base de datos, más control de entorno o crecimiento del proyecto.

## Pendientes importantes

- Revisar visualmente la página final “Fuentes y método” después de cada cambio de texto largo.
- Mejorar acentos y normalización de nombres en algunos resúmenes automáticos, por ejemplo “Coalicion”, “omision”, “Michoacan”.
- Continuar la revisión documental 2023-2025 antes de incorporar nuevos expedientes al análisis sustantivo.
- Resolver pendientes de descarga del manifest ampliado desde una sesión manual estable del portal TEPJF o con exportación institucional.
- Si se añaden nuevas sentencias, actualizar `casos.csv`, `sanciones.csv`, `hallazgos_portal.csv`, documentación, mapa, PDF y auditoría de enlaces.

## Comandos útiles

Compilar:

```bash
python3 -m py_compile src/observatorio/pdf_export.py pages/13_Diputaciones_electas.py src/observatorio/ui.py
```

Regenerar PDF:

```bash
PYTHONPATH=src python3 -c 'from observatorio.pdf_export import export_diputaciones_report_pdf; print(export_diputaciones_report_pdf())'
```

Verificar páginas y enlaces del PDF:

```bash
python3 -c 'from pypdf import PdfReader; r=PdfReader("exports/diputaciones_electas_reporte.pdf"); print("pages", len(r.pages)); print("annots", sum(len(p.get("/Annots", [])) for p in r.pages))'
```

Buscar términos problemáticos:

```bash
rg -n "ranking|trazabilidad|No se suma|sumatoria|monto que agregar" pages/13_Diputaciones_electas.py src/observatorio/pdf_export.py docs
```

## Prompt para continuar en otra conversación

```text
Estoy trabajando en el proyecto local `/Users/amluis/observatorio-fiscalizacion-2023-2024`, una app Streamlit del Observatorio de Fiscalización Electoral 2023-2024.

Necesito continuar desde el estado documentado en:

- `docs/estado_mvp_observatorio_2026-07-23.md`
- `docs/handoff_diputaciones_pdf_2026-07-23.md`

Página principal:

- `pages/13_Diputaciones_electas.py`

Exportador PDF:

- `src/observatorio/pdf_export.py`

CSS global:

- `src/observatorio/ui.py`

Estado actual:

- La página tiene diseño editorial premium, sin sidebar de Streamlit.
- Ya existe botón “Descargar PDF”.
- El PDF se genera con HTML dedicado y Chromium/Playwright en carta horizontal.
- Artefacto actual: `exports/diputaciones_electas_reporte.pdf`.
- Última verificación: 6 páginas y 23 enlaces/anotaciones.
- El mapa usa geometría estatal de México y solo colorea Chihuahua, Ciudad de México y Michoacán.
- El mapa cuenta expedientes ubicados por entidad o distrito; la sumatoria cuenta pesos, no expedientes.
- Los registros con `$0.00` o “No integrado” deben explicarse así: aparecen como casos consultables porque ubican una controversia, pero no se suman porque no hay una cantidad económica positiva fijada, confirmada o modificada para agregar al cálculo.
- No usar la palabra “ranking”; usar “sumatoria”.
- No usar “trazabilidad” para explicar al lector general.
- Las URL deben ser enlaces oficiales del TEPJF, no rutas locales.
- Los montos exactos son: $7,303,754.15 + $10,312,470.58 + $2,638,887.56 + $445,361.30 = $20,700,473.59, abreviado como $20.7 M.

Antes de editar, revisa la estructura actual de la app y los dos documentos de handoff. Después implementa cambios con alcance acotado, regenera el PDF, verifica compilación Python, verifica páginas/enlaces del PDF con pypdf y genera captura visual si modificas layout.

Quiero seguir mejorando la claridad editorial y metodológica del reporte sin romper el diseño actual.
```
