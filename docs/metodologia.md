# Metodologia del MVP

## Alcance

El MVP demuestra la estructura de analisis documental del Observatorio de Fiscalizacion Electoral 2023-2024. El reporte de diputaciones federales 2024 se construye a partir de sentencias publicas del Tribunal Electoral del Poder Judicial de la Federacion (TEPJF), registros de sanciones, hallazgos del portal y datos legislativos de la LXVI Legislatura.

El corte actual no sustituye el universo completo de resoluciones administrativas del Instituto Nacional Electoral (INE) ni una revision juridica final. Su finalidad es delimitar, documentar y visualizar los expedientes judiciales pertinentes para explicar que se sanciono, cual fue el monto controvertido y que entidades tuvieron incidencia territorial identificada.

## Busqueda documental y delimitacion del corpus

Se realizo una busqueda documental en el portal de sentencias publicas del Tribunal Electoral del Poder Judicial de la Federacion (TEPJF), disponible en la seccion de sentencias publicas: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/.

Para el proceso electoral federal 2023-2024, la bitacora del corte registra consultas por proceso electoral federal 2023-2024, diputaciones, fiscalizacion, propaganda, representacion proporcional y constancia de mayoria. Las versiones publicas disponibles se descargaron en formato HTML cuando el portal lo permitio, se sometieron a extraccion de texto local y se revisaron conforme al sentido de la resolucion, la autoridad responsable, el cargo de eleccion, el medio de impugnacion y la presencia de temas de fiscalizacion electoral.

A partir de esta depuracion se delimito un corpus analitico base de 52 sentencias que contuvieron informacion pertinente para el presente reporte. El corpus validado conserva expediente, ano, organo jurisdiccional, medio de impugnacion, fragmentos relevantes y marcas tematicas sobre fiscalizacion, propaganda, representacion proporcional, nulidad, inelegibilidad, rebase de tope de gastos y constancia de mayoria.

Como ampliacion exhaustiva, se ejecuto una nueva ronda de busquedas en Chrome sobre el buscador institucional del TEPJF y busquedas indexadas oficiales sobre `sentenciasHTML`. Esta ronda identifico 41 expedientes candidatos adicionales para el periodo 2023-2025. En la corrida documentada se descargaron y extrajeron 5 nuevos HTML, se integraron 2 textos previamente descargados de 2025 y quedaron 34 candidatos pendientes de descarga por restricciones de navegacion, timeout o proteccion del portal. Estos pendientes no se incorporan al analisis sustantivo hasta contar con texto completo y validacion juridica.

## Flujo

1. Identificar documento oficial.
2. Descargarlo y registrar fuente.
3. Capturar caso, acto de origen, sanciones, agravios y sujetos.
4. Conservar fragmento y pagina de soporte.
5. Validar montos y sentido.
6. Etiquetar la revision humana.
7. Cargar CSV revisados en `data/processed/`.

## Criterios de inclusion y exclusion

Se incluyeron resoluciones vinculadas con diputaciones federales del proceso 2023-2024 cuando el texto permitio identificar al menos uno de los siguientes elementos: fiscalizacion, propaganda, representacion proporcional, nulidad, inelegibilidad, rebase de tope de gastos, constancia de mayoria, sancion o efecto jurisdiccional asociado con el proceso federal.

Se excluyeron resultados sin informacion pertinente para el analisis, expedientes sin texto publico disponible al momento de la descarga, asuntos de otros cargos no vinculados con diputaciones federales y documentos cuya relacion con fiscalizacion electoral no pudiera sostenerse con el texto de la sentencia.

Los expedientes 2025 vinculados con cumplimiento, efectos posteriores o impugnaciones relacionadas se mantienen como candidatos de ampliacion hasta completar su validacion documental.

## Reglas juridicas

- No mezclar fiscalizacion federal con procedimientos locales sin etiqueta.
- No llamar grave a una conducta si la autoridad no lo dice expresamente.
- No interpretar revocacion para efectos como eliminacion definitiva de multa.
- No llenar datos ausentes con inferencias.
- No presentar la muestra como tendencia general.
- No mostrar personas legisladoras como sujetas a sancion si el expediente no las vincula expresamente.

## Fuentes en formato APA

Tribunal Electoral del Poder Judicial de la Federacion. (s. f.). *Sentencias publicas*. https://www.te.gob.mx/sentenciasHTML/convertir/expediente/

Instituto Nacional Electoral. (2024). *Dictamenes consolidados y resoluciones de fiscalizacion del proceso electoral federal 2023-2024*. https://www.ine.mx/

Camara de Diputados. (s. f.). *Sistema de Informacion Legislativa: LXVI Legislatura*. https://sitl.diputados.gob.mx/

Instituto Nacional de Estadistica y Geografia. (s. f.). *Marco Geoestadistico: entidades federativas, servicio GeoJSON*. https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgee/
