# Compilación preliminar de criterios en materia de fiscalización electoral

Fecha de elaboración: 23 de julio de 2026  
Materia: diputaciones federales, proceso electoral federal 2023-2024  
Estado: versión 0.1 para reunión de trabajo

## Propósito

Este documento organiza criterios derivados del corte local del Observatorio de Fiscalización Electoral. La finalidad es contar con una base de conversación para analizar dictámenes, resoluciones administrativas del INE y sentencias del TEPJF relacionadas con diputaciones federales 2024.

El documento no sustituye una revisión jurídica exhaustiva de cada sentencia. Presenta una sistematización preliminar con base en `casos.csv`, `agravios.csv`, `sanciones.csv`, `hallazgos_portal.csv`, `actos_origen.csv`, `votos.csv` y el corpus local de 52 sentencias TEPJF.

## Universo documental del corte

- 52 sentencias TEPJF revisadas en el corpus local.
- 11 expedientes con marca de fiscalización.
- 5 expedientes con tema de rebase o tope de gastos.
- 16 expedientes con tema de propaganda.
- 7 expedientes base vinculados directamente con registros de sanción o quejas de fiscalización de diputaciones federales.
- 12 agravios sistematizados en materia de fiscalización.
- 19 registros de sanción del INE, de los cuales 15 tienen monto positivo y 4 se conservan como casos consultables sin sumarse al total.

## Referente metodológico localizado en el equipo

Archivo de referencia revisado: `/Users/amluis/Downloads/rpe_compilacion_v7.html`.

Ese material de responsabilidad patrimonial del Estado funciona como referencia de organización, no como fuente jurídica para fiscalización electoral. La estructura que conviene trasladar al Observatorio es:

- Un universo documental claramente delimitado por periodo, materia, órgano y fuente.
- Una taxonomía temática estable para poder filtrar criterios.
- Fichas individuales con rubro, fuente, órgano, tema, criterio jurídico, carga argumentativa o probatoria, efecto y cita.
- Un índice ejecutivo que permita exponer el material sin leer cada sentencia completa.
- Campos normalizados para que el mismo insumo alimente documento, app y PDF.

Adaptación para fiscalización electoral:

| Elemento del modelo RPE | Adaptación al Observatorio |
|---|---|
| Fuente jurisdiccional | Sala Superior, Sala Regional Ciudad de México y salas regionales auxiliares del corpus |
| Tipo de criterio | Fiscalización, queja, rebase, propaganda, competencia, procedencia o efectos |
| Criterio jurídico | Regla extraída de dictamen, resolución administrativa y sentencia |
| Implicación jurídica | Consecuencia práctica para defensa, autoridad fiscalizadora o validez de elección |
| Cita y localización | Expediente TEPJF, acto INE de origen y URL oficial |

## Actos administrativos de origen

| Acto | Tipo | Relación con diputaciones federales | Expedientes TEPJF vinculados |
|---|---|---|---|
| INE/CG1928/2024 e INE/CG1929/2024 | Dictamen y resolución | Revisión de informes de ingresos y gastos de campaña federal 2023-2024 | SUP-RAP-342/2024; SUP-RAP-413/2024 |
| INE/CG1929/2024 e INE/CG1930/2024 | Dictamen y resolución | Revisión de informes de campaña federal 2023-2024 | SUP-RAP-352/2024 |
| INE/CG1955/2024 | Resolución | Fiscalización de campaña federal y concurrente | SUP-RAP-357/2024 |
| INE/CG1501/2024 | Resolución de queja | Queja por presuntos eventos no reportados y aportaciones prohibidas | SCM-RAP-47/2024 |
| INE/CG1098/2024 | Resolución de queja | Queja por presunta omisión de reportar gastos y subvaluación | ST-RAP-74/2024 y acumulado |
| INE/CG838/2024 | Resolución de queja | Precampaña a diputación federal; gasto no reportado y deslinde | ST-RAP-50/2024 |

## Matriz preliminar de criterios

| Tema | Criterio operativo | Carga argumentativa o probatoria | Efecto observado | Expedientes fuente |
|---|---|---|---|---|
| Exhaustividad del dictamen y sus anexos | La autoridad debe explicar de forma suficiente la relación entre hallazgos, anexos, conclusiones y sanción. Cuando la motivación no permite reconstruir la conclusión, procede revocar para efectos. | Identificar conclusión, anexo, hallazgo y omisión concreta de análisis. No basta una inconformidad genérica. | Revocación para efectos o revocación parcial. | SUP-RAP-342/2024; SCM-RAP-47/2024 |
| Fallas del Sistema Integral de Fiscalización | Las fallas del SIF requieren planteamiento particularizado y elementos objetivos que muestren cómo impidieron cumplir una obligación concreta. | Precisar fecha, operación, módulo, obligación afectada y evidencia de la falla. Alegaciones genéricas se califican como inoperantes o ineficaces. | Confirmación de conclusiones cuando no se acredita afectación concreta. | SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024 |
| Documentación soporte faltante | La falta de comprobación, avisos, XML o complementos fiscales puede sostener sanciones si el sujeto obligado no desvirtúa la observación con documentación idónea. | Aportar soporte fiscal, contractual y contable que corresponda con el gasto observado. | Confirmación de resolución o sanción. | SUP-RAP-352/2024; SUP-RAP-357/2024 |
| Comprobantes electrónicos de pago | En controversias sobre CEP, la defensa debe explicar de manera individualizada por qué el comprobante no firmado, gratuito u oneroso no actualiza la infracción. | Particularizar cada CEP y justificar su modificación, gratuidad o imposibilidad de firma. | Confirmación cuando no se acredita impedimento real o explicación suficiente. | SUP-RAP-352/2024; SUP-RAP-357/2024; SUP-RAP-413/2024 |
| Registro en tiempo real | La duplicidad, extemporaneidad o falta de registro oportuno exige revisar si la autoridad valoró adecuadamente el momento, el soporte y la consecuencia aplicable. | Acreditar que el registro existió, que fue oportuno o que la autoridad duplicó la consecuencia. | Revocación parcial cuando se advierte error de individualización o duplicidad. | SUP-RAP-357/2024 |
| Prorrateo y candidaturas beneficiadas | El prorrateo debe reflejar con precisión los ámbitos, candidaturas, distritos y beneficios reales de la propaganda o gasto. Si la autoridad no identifica con claridad esos elementos, puede proceder revocación parcial. | Vincular pieza propagandística, gasto, candidatura beneficiada, ámbito territorial y regla de distribución. | Revocación parcial o confirmación según precisión del análisis. | SUP-RAP-413/2024 |
| Omisión de reportar propaganda o gastos | La omisión de reportar propaganda, eventos, lonas, espectaculares, bardas, inserciones o internet se analiza a partir de existencia del gasto, beneficio electoral, obligación de reporte y suficiencia del soporte. | Probar existencia del gasto o propaganda; identificar sujeto obligado o candidatura beneficiada; valorar deslindes y registros. | Confirmación, revocación para efectos o revocación según valoración probatoria. | SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024; ST-RAP-50/2024; SCM-RAP-47/2024 |
| Aportaciones prohibidas | Cuando se denuncia posible aportación de entes impedidos, la autoridad debe valorar los hechos denunciados, la fuente de la aportación y el beneficio electoral. | Precisar aportante, bien o servicio, valor, beneficiario y nexo con campaña. | Revocación para nueva resolución si el análisis de la queja fue insuficiente. | SCM-RAP-47/2024 |
| Deslinde | El deslinde frente a propaganda o actos de terceros debe cumplir parámetros de eficacia, oportunidad, idoneidad y razonabilidad. Un deslinde genérico o tardío no elimina por sí mismo la responsabilidad. | Acreditar actuación oportuna, eficaz y jurídicamente idónea para cesar o rechazar el beneficio. | Revocación o confirmación según valoración del deslinde y hechos. | ST-RAP-50/2024 |
| Rebase de tope de gastos | Para traducir una irregularidad fiscalizable en consecuencia sobre validez de elección se requiere acreditar monto, acumulación al tope, determinancia y vínculo con la elección impugnada. | No basta invocar una sanción administrativa; debe probarse impacto cuantitativo o cualitativo y relación con el resultado electoral. | En el corpus de nulidad, las infracciones administrativas aisladas no bastan por sí mismas para anular. | SCM-JIN-27/2024; SG-JIN-114/2024; SUP-REC-764/2024; SUP-RAP-352/2024; SUP-RAP-357/2024; SUP-RAP-413/2024 |
| Competencia entre Sala Superior y Salas Regionales | La competencia se define por tipo de elección, principio, cargo, ámbito territorial y vínculo con la candidatura o elección impugnada. Las diputaciones de mayoría relativa tienden a Sala Regional; asuntos de RP o criterios generales pueden ir a Sala Superior. | Identificar cargo, principio, entidad, distrito y acto reclamado. | Acuerdos de competencia o remisión a Sala Regional. | SUP-RAP-414/2024; SUP-RAP-415/2024 |
| Procedencia y firma | La falta de firma autógrafa o autenticidad procesal puede impedir el estudio de fondo incluso cuando el asunto de fondo sea fiscalización. | Verificar firma, personería, oportunidad y presentación válida. | Sobreseimiento. | ST-RAP-74/2024 y acumulado |
| Efectos de la revocación | La revocación puede ser lisa y llana, parcial o para efectos. La diferencia importa porque define si la autoridad debe emitir nueva resolución, recalcular montos o simplemente dejar sin efectos una conclusión. | Precisar conclusión afectada, alcance del agravio fundado y consecuencia administrativa posterior. | Revoca para efectos, revoca parcialmente, confirma el resto. | SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024; SCM-RAP-47/2024; ST-RAP-50/2024 |

## Índice ejecutivo de criterios

| Clave | Criterio | Tema | Órgano principal | Utilidad para la reunión |
|---|---|---|---|---|
| FIS-01 | Exhaustividad del dictamen, anexos y conclusiones | Dictamen y resolución | Sala Superior / SCM | Permite explicar cuándo una resolución debe reconstruir mejor el nexo entre hallazgo, conclusión y sanción |
| FIS-02 | Fallas del SIF y necesidad de prueba específica | Sistema Integral de Fiscalización | Sala Superior | Ordena defensas sobre fallas técnicas sin convertirlas en argumentos genéricos |
| FIS-03 | Documentación soporte y comprobación fiscal | Comprobación de gasto | Sala Superior | Distingue omisiones documentales que sostienen sanción de errores subsanables |
| FIS-04 | Comprobantes electrónicos de pago | CEP / XML / soporte de operación | Sala Superior | Sirve para revisar defensa por comprobante, operación y consecuencia |
| FIS-05 | Registro oportuno y duplicidad de consecuencias | Registro en tiempo real | Sala Superior | Ayuda a detectar errores de individualización o duplicidad |
| FIS-06 | Prorrateo y candidaturas beneficiadas | Beneficio electoral | Sala Superior | Exige vincular gasto, candidatura, distrito, ámbito y regla de distribución |
| FIS-07 | Omisión de reportar propaganda, eventos o gastos | Propaganda y gasto no reportado | Sala Superior / SCM / ST | Permite ordenar hechos, soporte, beneficio y deslinde |
| FIS-08 | Aportaciones prohibidas | Quejas de fiscalización | SCM | Foco en aportante, bien o servicio, valor, beneficiario y nexo de campaña |
| FIS-09 | Deslinde eficaz | Responsabilidad frente a terceros | ST | Útil para evaluar oportunidad, idoneidad y eficacia del deslinde |
| FIS-10 | Rebase de tope y nulidad | Validez de elección | Sala Superior / Salas regionales | Separa sanción administrativa de determinancia electoral |
| FIS-11 | Competencia por cargo, principio y territorio | Competencia | Sala Superior | Evita mezclar MR, RP, entidad, distrito y órgano competente |
| FIS-12 | Efectos de revocación | Efectos | Sala Superior / SCM / ST | Define si hay nueva resolución, recálculo o simple eliminación de conclusión |

## Fichas de criterio

### FIS-01. Exhaustividad del dictamen, anexos y conclusiones

**Rubro:** La autoridad debe permitir reconstruir la relación entre hallazgo, anexo, conclusión y sanción.  
**Fuente:** SUP-RAP-342/2024; SCM-RAP-47/2024.  
**Tipo:** Criterio de control sobre motivación y exhaustividad.  
**Criterio jurídico:** Cuando la resolución administrativa no explica de manera suficiente cómo llega del hallazgo a la conclusión sancionatoria, procede revisar el acto para verificar si la motivación es completa y congruente.  
**Carga argumentativa:** La parte inconforme debe señalar conclusión, anexo, conducta y omisión concreta de valoración; una inconformidad general no basta.  
**Efecto observado:** Revocación para efectos, revocación parcial o confirmación, según el alcance del defecto.  
**Uso en app:** Campo `criterio=exhaustividad`, ligado a conclusión sancionatoria, acto INE y URL oficial TEPJF.

### FIS-02. Fallas del Sistema Integral de Fiscalización

**Rubro:** Las fallas del SIF requieren evidencia específica de afectación.  
**Fuente:** SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024.  
**Tipo:** Criterio probatorio y operativo.  
**Criterio jurídico:** La sola referencia a fallas del sistema no desvirtúa una infracción si no se acredita cómo afectaron una obligación concreta de reporte, carga o comprobación.  
**Carga argumentativa:** Identificar fecha, módulo, operación, evidencia técnica, obligación afectada y oportunidad de la actuación.  
**Efecto observado:** Confirmación cuando el agravio es genérico; posible revocación parcial si la falla incide en una conclusión específica.  
**Uso en app:** Campo `incidencia_sif`, con evidencia y estado de validación.

### FIS-03. Documentación soporte y comprobación fiscal

**Rubro:** La falta de soporte idóneo puede sostener la sanción.  
**Fuente:** SUP-RAP-352/2024; SUP-RAP-357/2024.  
**Tipo:** Criterio de comprobación de gasto.  
**Criterio jurídico:** La autoridad puede confirmar observaciones cuando el sujeto obligado no presenta documentación fiscal, contractual o contable que corresponda con el gasto observado.  
**Carga argumentativa:** Aportar soporte completo, explicar correspondencia con la operación y controvertir la valoración de la autoridad.  
**Efecto observado:** Confirmación de conclusiones o sanciones si no se desvirtúa la observación.  
**Uso en app:** Campos `documentacion_soporte`, `monto_observado`, `monto_final` y `efecto`.

### FIS-04. Comprobantes electrónicos de pago

**Rubro:** La defensa debe individualizar cada comprobante controvertido.  
**Fuente:** SUP-RAP-352/2024; SUP-RAP-357/2024; SUP-RAP-413/2024.  
**Tipo:** Criterio sobre CEP, XML y soporte de operación.  
**Criterio jurídico:** Los planteamientos sobre comprobantes electrónicos requieren explicación individualizada; no basta afirmar que el comprobante era gratuito, no firmado o modificado.  
**Carga argumentativa:** Precisar operación, comprobante, modificación, imposibilidad de firma o razón por la que no actualiza infracción.  
**Efecto observado:** Confirmación cuando falta explicación específica.  
**Uso en app:** Campo `soporte_cep`, con vínculo a conclusión y monto.

### FIS-05. Registro oportuno y duplicidad de consecuencias

**Rubro:** La temporalidad del registro debe valorarse sin duplicar consecuencias.  
**Fuente:** SUP-RAP-357/2024.  
**Tipo:** Criterio de individualización.  
**Criterio jurídico:** La autoridad debe explicar si el registro fue inexistente, extemporáneo o duplicado, y ajustar la consecuencia a esa diferencia.  
**Carga argumentativa:** Acreditar fecha de registro, soporte cargado, conducta atribuida y posible duplicidad.  
**Efecto observado:** Revocación parcial cuando se advierte error de individualización; confirmación cuando la observación permanece acreditada.  
**Uso en app:** Campos `fecha_operacion`, `fecha_registro`, `conducta` y `efecto`.

### FIS-06. Prorrateo y candidaturas beneficiadas

**Rubro:** El prorrateo debe corresponder al beneficio real.  
**Fuente:** SUP-RAP-413/2024.  
**Tipo:** Criterio de distribución de gasto.  
**Criterio jurídico:** Para sostener el prorrateo, debe identificarse gasto, propaganda, candidatura beneficiada, ámbito territorial y regla de distribución aplicable.  
**Carga argumentativa:** Vincular pieza propagandística, sujeto obligado, candidatura, distrito, entidad y beneficio.  
**Efecto observado:** Revocación parcial o confirmación según la precisión del análisis.  
**Uso en app:** Campos `candidatura_beneficiada`, `entidad`, `distrito`, `regla_prorrateo` y `monto_observado`.

### FIS-07. Omisión de reportar propaganda, eventos o gastos

**Rubro:** El gasto no reportado exige acreditar existencia, beneficio y obligación de reporte.  
**Fuente:** SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024; SCM-RAP-47/2024; ST-RAP-50/2024.  
**Tipo:** Criterio de fiscalización de propaganda y eventos.  
**Criterio jurídico:** La omisión se sostiene cuando existen elementos suficientes para vincular gasto o propaganda con campaña, sujeto obligado y deber de reporte.  
**Carga argumentativa:** Identificar material, evento, proveedor, valor, candidatura beneficiada, temporalidad y, en su caso, deslinde.  
**Efecto observado:** Confirmación, revocación para efectos o revocación parcial.  
**Uso en app:** Tema central para mapa y tabla de expedientes consultables.

### FIS-08. Aportaciones prohibidas

**Rubro:** La autoridad debe estudiar aportante, beneficio y nexo con campaña.  
**Fuente:** SCM-RAP-47/2024.  
**Tipo:** Criterio de queja de fiscalización.  
**Criterio jurídico:** Si se denuncia una posible aportación de ente impedido, la resolución debe valorar hechos, fuente de aportación, bien o servicio, beneficiario y relación con campaña.  
**Carga argumentativa:** Precisar aportante, valor, conducta, candidatura, evento o propaganda y soporte probatorio.  
**Efecto observado:** Revocación para nueva resolución si el estudio administrativo fue insuficiente.  
**Uso en app:** Campo `aportacion_prohibida`, con estado de validación.

### FIS-09. Deslinde eficaz

**Rubro:** El deslinde debe ser oportuno, idóneo, eficaz y razonable.  
**Fuente:** ST-RAP-50/2024.  
**Tipo:** Criterio auxiliar para gastos de terceros.  
**Criterio jurídico:** La existencia de propaganda o gasto de terceros no se neutraliza con un deslinde genérico; debe acreditarse una actuación real para rechazar o cesar el beneficio.  
**Carga argumentativa:** Probar fecha, medio, solicitud de retiro, comunicación a autoridad y eficacia material.  
**Efecto observado:** Confirmación o revocación según valoración probatoria.  
**Uso en app:** Campo `deslinde`, útil para fichas de propaganda.

### FIS-10. Rebase de tope y nulidad

**Rubro:** La sanción administrativa no equivale por sí misma a nulidad electoral.  
**Fuente:** SCM-JIN-27/2024; SG-JIN-114/2024; SUP-REC-764/2024; SUP-RAP-352/2024; SUP-RAP-357/2024; SUP-RAP-413/2024.  
**Tipo:** Criterio puente entre fiscalización y validez de elección.  
**Criterio jurídico:** Para que una irregularidad fiscalizable incida en la validez de la elección se requiere acreditar monto, acumulación al tope, determinancia y vínculo con la elección impugnada.  
**Carga argumentativa:** Probar impacto cuantitativo o cualitativo y conexión con resultado electoral.  
**Efecto observado:** En el corpus de nulidad, infracciones administrativas aisladas no bastan por sí solas para anular.  
**Uso en app:** Campo `rebase_tope`, separado de `monto_observado` para no confundir sumatoria con nulidad.

### FIS-11. Competencia por cargo, principio y territorio

**Rubro:** La competencia depende de elección, principio, cargo y ámbito territorial.  
**Fuente:** SUP-RAP-414/2024; SUP-RAP-415/2024.  
**Tipo:** Criterio procesal.  
**Criterio jurídico:** La distribución competencial exige identificar si se trata de mayoría relativa, representación proporcional, distrito, entidad, cargo o criterio general.  
**Carga argumentativa:** Precisar acto reclamado, candidatura, cargo, principio y territorio.  
**Efecto observado:** Acuerdos de competencia o remisión a sala regional.  
**Uso en app:** Campos `organo_competente`, `principio`, `cargo`, `entidad` y `distrito`.

### FIS-12. Efectos de revocación

**Rubro:** Los efectos deben distinguir confirmación, revocación parcial, modificación y nueva resolución.  
**Fuente:** SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024; SCM-RAP-47/2024; ST-RAP-50/2024.  
**Tipo:** Criterio de seguimiento.  
**Criterio jurídico:** El sentido de una sentencia no siempre elimina toda la resolución administrativa; puede confirmar una parte, revocar otra o exigir un nuevo pronunciamiento.  
**Carga argumentativa:** Identificar conclusión afectada, agravio fundado, alcance de la revocación y obligación posterior de la autoridad.  
**Efecto observado:** Confirmación parcial, revocación para efectos, recálculo o nueva resolución.  
**Uso en app:** Campo `efecto`, indispensable para reportes actualizables y para distinguir montos observados de montos firmes.

## Criterios por órgano jurisdiccional

### Sala Superior

La Sala Superior concentra los expedientes base más cuantificados del corte: `SUP-RAP-342/2024`, `SUP-RAP-352/2024`, `SUP-RAP-357/2024` y `SUP-RAP-413/2024`. De esos asuntos sale la sumatoria exacta de $20,700,473.59 en montos originales observados por el INE.

Criterios preliminares:

- Las fallas del SIF no prosperan si se exponen de manera genérica.
- La documentación soporte y los XML faltantes sostienen sanción cuando no se desvirtúa la observación.
- El prorrateo exige correspondencia entre gasto, candidatura beneficiada, ámbito territorial y regla de distribución.
- La autoridad puede confirmar parte de las conclusiones y revocar otras; el análisis debe hacerse conclusión por conclusión.
- En asuntos de competencia, debe separarse elección de mayoría relativa, representación proporcional, cargo, entidad y vínculo territorial.

### Sala Regional Ciudad de México

El asunto identificado en el corte es `SCM-RAP-47/2024`, relacionado con la resolución `INE/CG1501/2024` y la queja `INE/Q-COF-UTF/2028/2024`, vinculada con diputación federal del distrito 7 en Ciudad de México.

Criterios preliminares:

- Las quejas de fiscalización exigen análisis suficiente de eventos presuntamente no reportados y posibles aportaciones prohibidas.
- Si la resolución administrativa no estudia de manera suficiente los hechos denunciados, procede revocar para que la autoridad emita nueva determinación.
- La relación con candidatura y distrito permite ubicar territorialmente el expediente, aunque no exista monto positivo integrado a la sumatoria.

### Salas regionales vinculadas al corpus ampliado

Aunque la solicitud prioriza Sala Superior y Sala Regional Ciudad de México, el corte incluye asuntos útiles de Sala Regional Toluca y Guadalajara para completar el modelo:

- `ST-RAP-50/2024`: gasto no reportado en precampaña, espectacular/lona y análisis de deslinde.
- `ST-RAP-74/2024`: sobreseimiento por requisito procesal, sin estudio de fondo fiscal.
- `SG-JIN-114/2024`: juicio de inconformidad con planteamiento de rebase de tope de gastos de campaña.

## Criterios para lectura de montos

- La sumatoria no cuenta expedientes; cuenta pesos.
- Solo se agregan registros con monto original positivo observado por el INE.
- Los casos con `$0.00` o “No integrado” aparecen como consultables porque ubican una controversia, candidatura, entidad o distrito.
- Esos casos no modifican la sumatoria porque no contienen una cantidad económica positiva fijada, confirmada o modificada para agregar al cálculo.
- Las sentencias TEPJF no siempre reproducen como suma textual el monto acumulado por causa; por eso el modelo vincula sentencia, acto administrativo y matriz de sanciones.

## Modelo propuesto para compilar criterios en tiempo real

El modelo recomendado funciona como una matriz viva, no como un documento cerrado. Cada fila debe poder alimentar la app, el PDF y una ficha jurídica.

Campos mínimos:

| Campo | Uso |
|---|---|
| expediente | Identificar sentencia o medio de impugnación |
| órgano | Separar Sala Superior, Sala Regional Ciudad de México y otras salas |
| tipo de medio | RAP, JIN, REC, JDC, PSD, PSC u otro |
| acto de origen | Dictamen, resolución, queja o acuerdo INE |
| clave administrativa | INE/CG, INE/Q-COF-UTF u otra clave |
| tema | Fiscalización, propaganda, rebase, nulidad, RP, inelegibilidad |
| criterio | Regla jurídica u operativa extraída |
| carga probatoria | Qué debe acreditar la parte inconforme o la autoridad |
| efecto | Confirma, revoca, revoca para efectos, sobresee, desecha |
| monto positivo | Monto que sí se suma, si existe |
| territorio | Entidad, distrito o sin entidad estatal |
| URL oficial | Enlace TEPJF o INE |
| estado de validación | Pendiente, revisión parcial, validado |
| observaciones | Riesgos de interpretación o pendientes |

Flujo operativo:

1. Fuente oficial: localizar sentencia, dictamen o resolución.
2. Extracción: convertir texto a corpus local y conservar URL oficial.
3. Clasificación: marcar tema, órgano, cargo, proceso, entidad y distrito.
4. Criterio: redactar regla en lenguaje claro.
5. Validación jurídica: revisar que la regla no sobreinterprete la sentencia.
6. Integración: alimentar app, PDF y fichas de reunión.
7. Actualización: registrar fecha de corte y estado de validación.

## Pendientes para robustecer la versión 1.0

- Cotejar las fichas contra el texto íntegro oficial de cada sentencia antes de presentarlas como criterio definitivo.
- Separar criterios estrictamente de fiscalización de criterios auxiliares de propaganda, nulidad, competencia y procedencia.
- Completar descarga o revisión de expedientes candidatos 2023-2025 antes de ampliar el universo.
- Preparar una tabla ejecutiva con solo Sala Superior y Sala Regional Ciudad de México si la reunión requiere máxima brevedad.

## Anexo: expedientes clave

| Expediente | Órgano | Tema principal | Acto origen | Lectura para reunión |
|---|---|---|---|---|
| SUP-RAP-342/2024 | Sala Superior | Fiscalización federal; omisión de reportar gastos | INE/CG1928/2024 e INE/CG1929/2024 | Exhaustividad, SIF, revocación parcial y confirmación de conclusiones |
| SUP-RAP-352/2024 | Sala Superior | Documentación soporte, XML, CEP, rebase por representantes | INE/CG1929/2024 e INE/CG1930/2024 | Confirmación de resolución y carga de comprobación |
| SUP-RAP-357/2024 | Sala Superior | Registro extemporáneo, propaganda federal no reportada, CEP | INE/CG1955/2024 | Revocación parcial e individualización |
| SUP-RAP-413/2024 | Sala Superior | Prorrateo, gastos no reportados, propaganda y aportación impedida | INE/CG1928/2024 e INE/CG1929/2024 | Reglas de prorrateo, beneficio y efectos de revocación |
| SCM-RAP-47/2024 | Sala Regional Ciudad de México | Queja de fiscalización por eventos y aportaciones prohibidas | INE/CG1501/2024 | Exhaustividad de quejas y nueva resolución |
| ST-RAP-50/2024 | Sala Regional Toluca | Gasto no reportado de precampaña y deslinde | INE/CG838/2024 | Valoración probatoria y eficacia del deslinde |
| ST-RAP-74/2024 | Sala Regional Toluca | Queja por gastos y subvaluación | INE/CG1098/2024 | Procedencia: sobreseimiento por falta de firma/autenticidad |
