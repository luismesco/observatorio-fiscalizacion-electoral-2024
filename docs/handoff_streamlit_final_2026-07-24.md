# Handoff tecnico y editorial

## Proyecto

Observatorio de Fiscalizacion Electoral 2023-2024, version publica en Streamlit Community Cloud y GitHub.

Repositorio remoto:

`https://github.com/luismesco/observatorio-fiscalizacion-electoral-2024`

Aplicacion publica:

`https://observatorio-fiscalizacion-electoral-2024-luismesco.streamlit.app/`

## Estado al 24 de julio de 2026

La app se simplifico a una sola pagina publica en `app.py`. Se elimino la carpeta `pages/` del despliegue para evitar la barra lateral automatica de Streamlit y retirar vistas antiguas que ya no pertenecian a la version final.

La version final debe operar como experiencia editorial unica:

- portada institucional;
- navegacion por anclas internas;
- descargas de PDF siempre disponibles;
- lectura dinamica con secciones editoriales dentro de la pagina;
- analisis de fiscalizacion legible en la app, no solo descargable;
- fichas de criterios consultables dentro de la app;
- panel de datos con filtros dentro del cuerpo de la pagina;
- mapa territorial de incidencias;
- composicion final de curules de la LXVI Legislatura;
- sujeto mas sancionado y sujeto con menor monto positivo observado;
- tabla editorial de expedientes con enlace oficial, sujeto, conducta, sentido, monto y efecto;
- filtros tipo pill en el cuerpo de la pagina;
- filtros independientes para panel, graficas y tabla de expedientes;
- cierre metodologico con relevancia, metodo y referencias antes de descargas;
- propuesta independiente de sistematizacion del flujo, navegable desde el encabezado;
- graficas y tabla sin depender de paginas secundarias.

## PDFs integrados

Los archivos usados por la app son:

- `exports/diputaciones_electas_reporte.pdf`
- `exports/criterios_fiscalizacion_diputaciones_2024.pdf`

Ambos se ofrecen desde:

- selector principal de descargas;
- dock fijo inferior con botones tipo pill para descarga inmediata.

Los PDF son respaldo editorial descargable. El contenido central tambien debe poder leerse en la pagina mediante:

- seccion `Analisis en pagina / Que se sanciono`;
- conductas con mayor monto observado;
- fichas `Criterios emitidos`;
- panel de datos exploratorio.

## Decisiones tomadas

### Streamlit en una sola pagina

Se retiro `pages/` porque Streamlit genera automaticamente una barra lateral cuando detecta esa carpeta. Esa barra contradecia la experiencia editorial solicitada y exponia secciones de trabajo que ya no eran parte de la version publica.

### KPI sin cortes

Los montos largos ya no se muestran como cifra completa en el headline de la tarjeta. La tarjeta usa lectura editorial compacta:

- ejemplo: `$20.7 M`;
- debajo se conserva el monto exacto: `$20,700,473.59`.

Esto evita cortes visuales en desktop, tablet y smartphone sin perder informacion.

### Descarga siempre visible

Se agrego un dock fijo inferior con dos pills:

- Fiscalizacion;
- Criterios.

El dock usa enlaces `data:application/pdf;base64` para permitir descarga directa sin abrir una nueva seccion ni depender de botones flotantes nativos de Streamlit.

La seccion formal de descargas se movio al final de la pagina para que el flujo sea: leer, interactuar, contrastar datos y descargar.

### Analisis dentro de la pagina

Se agrego una seccion editorial antes del panel de datos. Incluye:

- hallazgo central;
- monto administrativo con lectura ejecutiva;
- lectura jurisdiccional;
- conductas con mayor monto observado;
- nota de uso para conectar conducta, monto, sentencia y efecto.

### Criterios consultables

Se agregaron fichas expandibles con:

- organo;
- expediente;
- tema;
- regla o criterio;
- efecto;
- relevancia para dictamen/resolucion;
- utilidad antes, durante y despues.

### Filtros fuera del sidebar

Los filtros del panel se movieron al cuerpo de la pagina como pills multiseleccion:

`Filtros de lectura / Delimita el corte`

Si no hay seleccion activa, el corte conserva el corpus completo. La seleccion de uno o mas pills acota el panel sin usar desplegables ni reactivar sidebar. Los filtros del panel general, de las graficas y de la tabla usan llaves de estado independientes para evitar que una consulta vacie otra seccion. La grafica `Casos por partido` conserva filtro por partido, ademas de nivel, conducta y sentido.

El tema de Streamlit se fija en `.streamlit/config.toml` con `primaryColor = "#6B1531"` para evitar el rojo/coral nativo en widgets.

### Tabla editorial de expedientes

Se sustituyo la tabla nativa por una tabla HTML con paleta guinda, negro, dorado y dorado claro. Incluye:

- expediente con enlace oficial TEPJF;
- fecha de sentencia;
- sujeto;
- conducta;
- sentido;
- monto observado compacto y monto exacto;
- efecto de la resolucion.

La fila de encabezados usa fondo guinda y texto blanco.

### Curules, mapa y sanciones por sujeto

Se agregaron:

- grafica de composicion final de 500 curules;
- mapa de incidencias territoriales;
- tarjeta de sujeto mas sancionado;
- tarjeta de sujeto con menor monto positivo observado.

Estos bloques se alimentan desde `data/analysis/diputados_lxvi_electos.csv`, `data/processed/hallazgos_portal.csv` y `data/processed/sanciones.csv`.

El mapa se renderiza como componente HTML interactivo para permitir seleccion directa de entidades. Al seleccionar una entidad activa en el mapa o en la lista lateral, la vista muestra solo la ficha del estado correspondiente. Cada ficha incluye expediente, tema, explicacion breve de prioridad y enlace a la sentencia oficial cuando existe URL disponible.

El componente del mapa usa altura compacta para evitar espacio blanco antes de la siguiente seccion. El panel de ficha tiene scroll interno cuando una entidad acumula varias referencias, de modo que el bloque no empuja artificialmente la lectura.

La seleccion territorial ya no se superpone al mapa: las entidades activas se presentan en una franja de botones de gran superficie, sincronizada con el SVG y con una sola ficha visible. Ciudad de Mexico incorpora un marcador accesible adicional sobre su posicion geografica para evitar que su contorno reducido dificulte la seleccion. El componente comunica su altura real a Streamlit para adaptarse sin dejar vacios artificiales.

La tabla de expedientes explica los montos en cero: si no existe monto firme, si el asunto fue sobreseido o si falta nueva determinacion, la celda de monto incorpora una nota de lectura para evitar interpretar `$0` como ausencia de irregularidad.

El cierre metodologico se presenta como aparato academico en tres apartados: relevancia del analisis, metodologia y referencias. La propuesta de sistematizacion se separa en una seccion autonoma con ancla propia y cinco etapas: capturar expediente y fuente oficial, normalizar sujeto/conducta/monto/sentido, vincular criterio y entidad, validar estados de monto y publicar PDF, datos y ficha navegable.

### Estilo editorial

Se reforzo la continuidad visual con los PDF mediante:

- Montserrat;
- paleta guinda, dorado, verde, tinta negra y papel claro;
- reticula editorial;
- tarjetas con borde superior;
- jerarquia tipografica en mayusculas;
- animaciones de entrada y hover;
- scroll suave en navegacion por anclas;
- revelado progresivo al entrar al viewport para secciones, graficas, mapa, filtros y fichas;
- secuencia visual escalonada en KPI y bloques metodologicos;
- alternativa sin movimiento mediante `prefers-reduced-motion`;
- observador JavaScript de interseccion instalado desde un componente Streamlit para mantener el revelado por scroll en Safari y navegadores sin `animation-timeline`;
- barra de progreso de lectura y actualizacion del apartado activo en la navegacion;
- transiciones en mapa, tarjetas, filas de analisis y fichas de criterios;
- secciones de lectura guiada.

El texto visible al lector debe mantener tono institucional y academico: observatorio, consulta, analisis, corpus, criterio, expediente, sentencia y efecto. Evitar lenguaje de producto como "app", "experiencia", "primero lee, despues explora" o explicaciones internas de componentes.

## Archivos principales

- `app.py`: experiencia publica final.
- `src/observatorio/ui.py`: estilos globales, Montserrat, reticula, dock, KPI, animaciones y helpers visuales.
- `.streamlit/config.toml`: tema base de Streamlit con color primario guinda.
- `src/observatorio/data_loader.py`: carga y filtros de datos.
- `src/observatorio/metrics.py`: KPIs, conteos y agregados.
- `requirements.txt`: dependencias para Streamlit Cloud.
- `runtime.txt`: version de Python para Streamlit Cloud.

## Verificaciones realizadas

Comandos usados:

```bash
python3 -m py_compile app.py src/observatorio/*.py
git diff --cached --check
rg -n "pages/|st\\.page_link|st\\.sidebar|add_global_filters|from observatorio\\.ui .*responsive_kpi_grid|st\\.metric|use_container_width=True" app.py src scripts tests -g '*.py'
```

Resultado esperado:

- compilacion sin errores;
- diff sin problemas de whitespace;
- sin referencias a multipagina/sidebar;
- sin `st.metric`;
- sin `use_container_width=True`.

## Incidencias resueltas

### Fly.io

Fly.io se descarto por friccion de cuenta/tarjeta.

### GitHub

Se creo y uso una nueva cuenta GitHub despues de suspension de cuenta previa.

### Streamlit Cloud

Se eligio Streamlit Community Cloud por menor friccion y despliegue directo desde GitHub.

Problemas corregidos:

- conflicto de version de Python;
- archivos de configuracion duplicados;
- `FileNotFoundError` por fuente local ausente en Cloud;
- barra lateral automatica de Streamlit;
- `ImportError` por helper agregado durante redeploy;
- KPI monetarios cortados;
- warnings por `use_container_width=True`.

## Riesgos actuales

El dock fijo usa PDFs embebidos como base64. Los archivos actuales son razonables para este enfoque:

- criterios: alrededor de 629 KB;
- fiscalizacion: alrededor de 1.1 MB.

Si los PDFs crecen mucho, conviene servirlos desde archivos estaticos o GitHub Releases y cambiar los pills a enlaces directos.

## Criterio de version final

La version final en linea debe verse sin sidebar, con dos descargas siempre visibles, con KPI sin cortes, y con lectura editorial similar al lenguaje grafico de los PDF.

Adicionalmente, el lector debe poder comprender el analisis principal sin descargar los PDF.

En movil, el contenedor principal usa `border-box` para impedir recortes por padding y el titulo de portada reduce su escala para conservar palabras completas desde 320 px. Los pills fijos identifican de forma explicita la accion y el documento: `Descargar / Fiscalizacion` y `Descargar / Criterios`.

### Adaptacion al viewport real de iPhone

La vista movil no depende solo de `@media`. El componente de movimiento consulta
`window.visualViewport`, publica el ancho efectivo en la variable
`--app-viewport-width` y vuelve a calcularlo cuando cambia la orientacion, el zoom
visual o el tamano disponible. La regla se aplica a la raiz de Streamlit, al
contenedor principal y a la portada para impedir desbordamientos laterales
producidos por la combinacion de `width: 100%` y padding.

Despues de cargar Montserrat se verifica tambien que cada linea del titulo de
portada quepa en su caja. Solo si una palabra excede el ancho disponible se reduce
progresivamente ese titulo, con un limite inferior legible.

La banda movil de Streamlit puede aparecer despues de renderizar la pagina y
cubrir controles fijos. Un `MutationObserver` detecta especificamente la insignia
`Hosted with Streamlit`; cuando esta presente, el dock de descargas se desplaza
hacia arriba. No se oculta ni se modifica la insignia de la plataforma.

Validacion Playwright realizada en anchos de 320, 360, 375, 393 y 430 px:

- ancho desplazable del documento igual al ancho del viewport;
- portada y titulo contenidos dentro del viewport;
- pills completos, con etiqueta explicita de descarga;
- atributos `download` y PDF base64 conservados;
- dock visible por encima de una insignia Streamlit simulada;
- tabla ancha confinada a su propio contenedor con desplazamiento horizontal;
- comportamiento de movimiento reducido conservado.

### Rendimiento y activacion temprana de movimiento

Los PDF dejaron de codificarse como `data:` base64 en el HTML. Streamlit sirve las
copias finales desde `static/` mediante `server.enableStaticServing`, y los enlaces
del dock y de la seccion final apuntan a `/app/static/`. Esto elimina la lectura,
codificacion y envio repetido de aproximadamente 1.7 MB de PDF en cada render y
mantiene el atributo `download`.

El observador de movimiento se instala inmediatamente despues de la portada y del
dock. Un observador del DOM registra de forma incremental las secciones, graficas,
mapa, metodologia y propuesta que Streamlit incorpora despues. De este modo las
transiciones no dependen de esperar a que termine de renderizar toda la pagina.

Medicion local de control en viewport movil de 393 px:

- portada y dock visibles: aproximadamente 2.2 segundos;
- documento completo disponible: aproximadamente 4.8 segundos;
- ancho del documento: 393 px;
- PDF servidos con `application/pdf`, sin URL base64;
- revelado por scroll confirmado en contenido tardio.

Un arranque en frio de Streamlit Community Cloud puede tardar mas que la medicion
local, pero el lector recibe ahora la portada antes que los bloques analiticos
posteriores.

### Descarga binaria fuera de la envoltura de Streamlit

Las rutas `/app/static/` funcionan en el servidor local, pero Streamlit Community
Cloud puede interceptarlas desde su envoltura autenticada y devolver HTML con
nombre `.pdf`. Los documentos finales se publicaron por ello como activos de la
version GitHub `analisis-diputaciones-2024-v1`.

Los pills fijos y el selector final usan las URL de GitHub Releases. La respuesta
final incorpora `Content-Disposition: attachment`, entrega el binario completo y
evita que Safari guarde la pagina de autenticacion de Streamlit.

Comprobaciones:

- fiscalizacion: PDF de 8 paginas, 1,127,525 bytes;
- criterios: PDF de 8 paginas, 643,896 bytes;
- hashes SHA-256 identicos a los originales del repositorio;
- respuesta HTTP final `200` con disposicion `attachment`.
