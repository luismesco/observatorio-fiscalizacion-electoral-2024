# Corte de trabajo: diputaciones federales 2024

Fecha de corte operativo: 2026-07-23.

## Alcance

Este corte integra tres capas de informacion:

1. Sentencias TEPJF 2023-2024 relacionadas con diputaciones federales.
2. Universo de 500 diputaciones federales de la LXVI Legislatura consultado en el Sistema de Informacion Legislativa de la Camara de Diputados.
3. Verificacion nominal preliminar en fuentes publicas de sanciones administrativas y delitos electorales para nombres priorizados del corpus.

La informacion se presenta como corte documental verificable. No sustituye una certificacion de autoridad ni una opinion juridica definitiva.

## Fuentes principales

- Portal del TEPJF: sentencias descargadas y extraidas en `documents/diputaciones_2023_2024/` y `data/interim/diputaciones_2023_2024_text/`.
- Camara de Diputados, LXVI Legislatura: listado y fichas publicas de diputaciones en `https://sitl.diputados.gob.mx/LXVI_leg/listado_diputados_gpnp.php`.
- Fichas individuales de Camara: `https://sitl.diputados.gob.mx/LXVI_leg/curricula.php?dipt=...`.
- Registro federal de Servidores Publicos Sancionados de Buen Gobierno/SFP: consulta nominal documentada en `data/interim/buengobierno_*.html`.
- TFJA/FISEL/FGR: fuentes oficiales consultadas para ubicar coincidencias nominales publicas.

## Datos generados

- `data/analysis/tepjf_corpus_resumen.csv`: 52 sentencias TEPJF analizadas.
- `data/analysis/tepjf_corpus_fragmentos.csv`: fragmentos por tema juridico.
- `data/analysis/tepjf_personas_detectadas.csv`: menciones nominales y no nominales detectadas en expedientes.
- `data/analysis/tfja_fisel_screening.csv`: verificacion nominal documentada de personas priorizadas.
- `data/analysis/ganadores_constancia.csv`: ganadores y personas mencionadas curadas para expedientes relevantes.
- `data/analysis/diputados_lxvi_electos.csv`: 500 diputaciones federales LXVI con ficha, principio, entidad, distrito/circunscripcion, partido, suplencia, fuente y ruta de retrato.

## Retratos

- Originales capturados desde fichas publicas de Camara: `static/img/diputados_lxvi_raw/`.
- Version editorial final: `static/img/diputados_lxvi_bn/`.
- Total final: 500 archivos PNG en blanco y negro, recorte vertical 4:5, plano medio, contraste editorial.
- Ganadores priorizados del corpus: `static/img/ganadores/`.

## Visualizacion

- `pages/12_Infografia_editorial.py`: portada editorial con corpus TEPJF, control nominal, composicion parlamentaria y tabla de 500 diputaciones.
- `pages/13_Diputaciones_electas.py`: vista interactiva para filtrar por partido, principio y entidad; incluye galeria de retratos y descarga CSV.
- CSS global: `src/observatorio/ui.py`, con reglas de impresion carta horizontal.

## Control de sanciones

El resultado `sin_indicio_publico_confirmado` significa que no se localizaron coincidencias publicas en las fuentes consultadas bajo el nombre revisado. No significa inexistencia certificada de sancion, responsabilidad administrativa, carpeta de investigacion o sentencia penal.

Nombres priorizados revisados en esta etapa:

- David Alejandro Cortes Mendoza.
- Juan Guillermo Rendon Gomez.
- Alejandro Correa Gomez.
- Julieta Andrea Ramirez Padilla.

## Pendientes

- Convertir las menciones detectadas en expedientes a un padron depurado solo de personas fisicas.
- Ejecutar busqueda nominal sistematica para cada persona fisica depurada.
- Cotejar el universo de Camara contra acuerdos INE/CG2129/2024 y resultados distritales INE para distinguir personas electas originalmente, suplencias y licencias vigentes.
- Incorporar trazabilidad de cada consulta nominal con fecha, fuente, parametros usados y evidencia local.
