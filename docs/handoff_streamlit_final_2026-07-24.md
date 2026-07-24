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

Los filtros del panel se movieron a un expander dentro de la pagina:

`Ajustar corte de datos`

Esto conserva la interactividad sin reactivar sidebar.

### Tabla editorial de expedientes

Se sustituyo la tabla nativa por una tabla HTML con paleta guinda, negro, dorado y dorado claro. Incluye:

- expediente con enlace oficial TEPJF;
- fecha de sentencia;
- sujeto;
- conducta;
- sentido;
- monto observado compacto y monto exacto;
- efecto de la resolucion.

### Curules, mapa y sanciones por sujeto

Se agregaron:

- grafica de composicion final de 500 curules;
- mapa de incidencias territoriales;
- tarjeta de sujeto mas sancionado;
- tarjeta de sujeto con menor monto positivo observado.

Estos bloques se alimentan desde `data/analysis/diputados_lxvi_electos.csv`, `data/processed/hallazgos_portal.csv` y `data/processed/sanciones.csv`.

### Estilo editorial

Se reforzo la continuidad visual con los PDF mediante:

- Montserrat;
- paleta guinda, dorado, verde, tinta negra y papel claro;
- reticula editorial;
- tarjetas con borde superior;
- jerarquia tipografica en mayusculas;
- animaciones de entrada y hover;
- secciones de lectura guiada.

## Archivos principales

- `app.py`: experiencia publica final.
- `src/observatorio/ui.py`: estilos globales, Montserrat, reticula, dock, KPI, animaciones y helpers visuales.
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
