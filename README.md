# Observatorio de Fiscalizacion y Justicia Electoral 2023-2024

Observatorio publico para consultar sanciones, efectos jurisdiccionales, criterios
del TEPJF y diputaciones federales electas del proceso 2023-2024. La version final
combina lectura editorial, filtros, graficas, mapa, tabla de expedientes y
documentos descargables en una sola pagina.

Aplicacion:

`https://observatorio-fiscalizacion-electoral-2024-luismesco.streamlit.app/`

## Estado del corte

- La aplicacion abre por defecto con casos documentados en `data/processed/`.
- Las plantillas para carga real estan en `data/templates/`.
- La muestra real inicial se limita a sentencias localizadas sobre fiscalizacion de campana federal 2023-2024 con incidencia en diputaciones federales.
- El universo de 500 diputaciones federales LXVI se encuentra en `data/analysis/diputados_lxvi_electos.csv`.
- Los retratos oficiales procesados en PNG blanco y negro estan en `static/img/diputados_lxvi_bn/`.

## Ejecutar

```bash
git clone https://github.com/luismesco/observatorio-fiscalizacion-electoral-2024.git
cd observatorio-fiscalizacion-electoral-2024
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publicar en Streamlit Community Cloud

La app esta preparada para publicarse desde GitHub en Streamlit Community Cloud.

- Repository: `luismesco/observatorio-fiscalizacion-electoral-2024`
- Branch: `main`
- Main file path: `app.py`
- Python version: `3.12`

Los PDF fuente se incluyen en `exports/` y sus copias publicas en `static/`.
Las descargas en produccion se sirven desde GitHub Releases para evitar que la
envoltura autenticada de Streamlit entregue HTML con extension `.pdf`.

- `exports/diputaciones_electas_reporte.pdf`
- `exports/criterios_fiscalizacion_diputaciones_2024.pdf`

Release:

`https://github.com/luismesco/observatorio-fiscalizacion-electoral-2024/releases/tag/analisis-diputaciones-2024-v1`

No se requieren secretos para el despliegue actual.

## Estructura

- `app.py`: pagina publica unica, filtros, graficas y lectura editorial.
- `src/observatorio/`: carga, metricas, validacion, estilos y exportacion.
- `data/templates/`: archivos CSV para capturar casos reales.
- `docs/`: metodologia, diccionario de datos y checklist.
- `exports/`: salidas generadas.
- `static/`: copias versionadas de los PDF finales.

No debe restaurarse `pages/`: Streamlit genera una barra lateral automatica y
expone vistas retiradas de la version final.

## Flujo recomendado de actualizacion

1. Colocar documentos oficiales en `documents/federal/` y `documents/cdmx/`.
2. Capturar cada expediente en las plantillas de `data/templates/`.
3. Registrar fuente, ruta local, fragmento y estado de revision.
4. Validar montos, sentido, agravios y competencia.
5. Copiar los CSV revisados a `data/processed/`.
6. Sustituir los PDF en `exports/` y `static/`.
7. Actualizar los activos del release con `gh release upload --clobber`.
8. Ejecutar la app con `streamlit run app.py`.
9. Probar viewport movil, animaciones, filtros y ambas descargas.
10. Generar Excel con `python scripts/export_excel.py` cuando corresponda.

## Documentacion de cierre

El estado tecnico, editorial y de despliegue se encuentra en:

`docs/handoff_streamlit_final_2026-07-24.md`

## Principio rector

Ningun dato sin fuente, ninguna inferencia presentada como hecho y ninguna comparacion que mezcle competencias distintas.
