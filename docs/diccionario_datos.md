# Diccionario de datos minimo

## casos

- `caso_id`: identificador interno unico.
- `nivel`: Federal o CDMX.
- `expediente`: clave del medio de impugnacion o clave interna demo.
- `sentido`: resultado de la resolucion.
- `efectos_resumen`: efecto juridico sintetico.
- `revision_humana`: si, validado, revision_parcial, pendiente o descartado.
- `confianza_global`: nivel de confianza o `demo`.
- `monto_final_estado`: firme, pendiente, desconocido o no aplica.

## sanciones

- `monto_original`: monto impuesto en sede administrativa.
- `monto_controvertido`: monto discutido.
- `monto_confirmado`: monto confirmado por el organo jurisdiccional.
- `monto_revocado`: monto dejado sin efectos, si se conoce.
- `monto_final`: monto firme conocido.
- `gravedad_textual`: calificacion expresa, no inferida.

## agravios

- `categoria`: tema juridico principal.
- `calificacion`: fundado, infundado, inoperante u otro.
- `fragmento_fuente`: soporte textual para revision.

