# Observatorio de Fiscalizacion y Justicia Electoral 2023-2024

Observatorio de trabajo para explorar asuntos vinculados con fiscalizacion electoral federal, sentencias del TEPJF y diputaciones federales electas 2024-2027. El proyecto funciona con archivos locales, datos tabulares y documentos fuente descargados previamente.

## Estado del corte

- La aplicacion abre por defecto con casos reales iniciales en `data/processed/`.
- Las plantillas para carga real estan en `data/templates/`.
- La muestra real inicial se limita a sentencias localizadas sobre fiscalizacion de campana federal 2023-2024 con incidencia en diputaciones federales.
- El universo de 500 diputaciones federales LXVI se encuentra en `data/analysis/diputados_lxvi_electos.csv`.
- Los retratos oficiales procesados en PNG blanco y negro estan en `static/img/diputados_lxvi_bn/`.

## Ejecutar

```bash
cd /Users/amluis/observatorio-fiscalizacion-2023-2024
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Estructura

- `app.py`: resumen ejecutivo.
- `pages/`: vistas de partidos, conductas, expedientes, agravios y metodologia.
- `src/observatorio/`: carga, metricas, validacion y exportacion.
- `data/templates/`: archivos CSV para capturar casos reales.
- `docs/`: metodologia, diccionario de datos y checklist.
- `exports/`: salidas generadas.

## Flujo recomendado de actualizacion

1. Colocar documentos oficiales en `documents/federal/` y `documents/cdmx/`.
2. Capturar cada expediente en las plantillas de `data/templates/`.
3. Registrar fuente, ruta local, fragmento y estado de revision.
4. Validar montos, sentido, agravios y competencia.
5. Copiar los CSV revisados a `data/processed/`.
6. Ejecutar la app con `streamlit run app.py`.
7. Generar Excel con `python scripts/export_excel.py`.

## Imprimir

Abrir la pagina `Reporte imprimible` dentro de Streamlit y usar imprimir desde el navegador. El CSS esta optimizado para carta horizontal:

```css
@page { size: letter landscape; }
```

## Principio rector

Ningun dato sin fuente, ninguna inferencia presentada como hecho y ninguna comparacion que mezcle competencias distintas.
