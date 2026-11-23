# Dashboard operacional y económico de una unidad de negocio de transporte

Modelo analítico y tablero en Power BI (formato .pbip, texto plano) para el seguimiento de la
programación operativa de una unidad de negocio de transporte público: kilómetros, expediciones,
flota requerida, ingresos teóricos, indicadores de calidad y sensibilidad frente a descuentos.

Desarrollo propio (proyecto personal, autodidacta).

## Demostración interactiva

**https://luisalbertochavarria.github.io/dashboard-operacional-powerbi/**

Réplica del modelo analítico en Python y Plotly, navegable en el navegador sin instalar nada.
Incluye seis vistas: ingreso por tipo de día, composición del ingreso, expediciones por hora,
kilómetros por terminal, indicadores de calidad contra su umbral e impacto económico por indicador.

Todos los datos son **sintéticos**: servicios, terminales, precios e indicadores son ficticios y no
corresponden a ninguna concesión real. Se generan con `replicar_dashboard.py`.

## Contexto

En una concesión de transporte público, el operador debe demostrar mes a mes el cumplimiento de
una programación y de indicadores normativos de calidad, y al mismo tiempo proyectar el efecto
económico de esa operación. La información suele estar dispersa en planillas y reportes, y no
existe una herramienta única que responda preguntas como:

- ¿Cuántos kilómetros y expediciones se programan al mes, y cuánto ingreso representan?
- ¿Cuántos buses se requieren en la hora punta y cuántos hay disponibles?
- ¿Qué pasa con el ingreso si un indicador de calidad baja un punto?
- ¿Cuánto cuesta, en pesos, cada punto de incumplimiento?

Este tablero construye ese modelo único y lo deja navegable.

## Modelo de datos

Esquema en estrella con dimensiones y tablas de hechos, construido sobre un modelo semántico en
DAX. Las tablas principales:

| Grupo | Tablas | Rol |
|---|---|---|
| Programación | FRANJAS, EVENTOS, SERVICIOS, TERMINALES | Kilómetros, expediciones y plazas por servicio, sentido y franja horaria |
| Flota | BUSES_REQUERIDOS, BUSES_SIM, BUSES_SIM_FRANJA | Demanda de buses por franja y simulación de asignación |
| Parámetros | PARAMETROS, DIAS, MODOS, COMPONENTES, TIPO_TECNOLOGIA | Precios del contrato, días por tipo de mes, componentes tarifarios |
| Calidad | INDICADORES, AFECTACION, SIM_ICF, SIM_ICP, SIM_ICFP, SIM_IE, SIM_IP, SIM_ICA | Indicadores normativos y su simulación |
| Economía | INGRESOS_PERIODO, ESCENARIOS, SENSIBILIDAD | Ingresos por período y análisis de escenarios |
| Medidas | MEDIDAS | 122 medidas DAX |

### Decisiones de diseño

- **Parámetros desacoplados**: los precios y umbrales del contrato se leen de la tabla
  `PARAMETROS` por su clave simbólica, no están escritos dentro de las fórmulas. Cambiar un precio
  no requiere tocar 122 medidas: se cambia el dato.
- **Dimensión de período**: el mismo modelo entrega la vista diaria, semanal y mensual, aplicando
  el número de días por tipo de semana (laborales, sábado y domingo) como factor. Así se evita el
  error clásico de sumar un solo día de cada tipo y llamarlo "mes".
- **Validación cruzada**: las medidas de kilómetros programados se contrastan contra una segunda
  fuente independiente (los eventos de operación), de modo que una inconsistencia entre ambas
  queda a la vista.
- **Explorador de escenarios**: una tabla precalculada permite simular combinaciones de
  indicadores y ver el efecto económico, en vez de analizar un caso a la vez.
- **Tabla de sensibilidad**: cuantifica cuánto ingresa o se pierde por cada punto de variación en
  cada indicador, lo que responde directamente la pregunta "cuánto cuesta cada punto".

## Páginas del tablero

| Página | Contenido |
|---|---|
| 01 Resumen ejecutivo | Indicadores principales del período |
| 02 Ingresos teóricos | Ingreso base y neto, con desglose diario, semanal y mensual |
| 03 Flota y buses requeridos | Demanda de flota por franja y comparación con la disponible |
| 04 Indicadores y calidad | Indicadores normativos y explorador de escenarios |
| 05 Franjas de medición | Detalle por franja horaria y tipo de día |
| 06 Simulador de descuentos | Efecto económico de incumplimientos |
| 07 Didáctica | Documentación de fórmulas, topes y criterios dentro del propio tablero |
| 08 Ingresos y kms por tecnología | Apertura por tipología de bus (eléctrico y diésel) |

El modelo tiene 91 visuales en total.

## Automatización de la construcción

El proyecto no se armó a mano visual por visual. Se generó mediante un pipeline de scripts en
Python que escriben directamente los archivos del proyecto en formato texto (.pbip):

- El modelo semántico se construye como archivos TMDL (tablas, relaciones, medidas y formato).
- Las páginas y visuales se generan como archivos JSON con identificadores estables.
- Las transformaciones de datos se definen como Power Query con tipos declarados por columna.
- Un script de verificación controla consistencia antes de abrir el tablero: referencias entre
  medidas y tablas, validez del JSON, orden de consultas e identificadores únicos.

Este enfoque permite versionar el tablero como código y reconstruirlo de forma reproducible.

## Sobre los datos

**Este repositorio no incluye datos.** La información de programación, flota y economía proviene de
documentación contractual de una concesión real y está sujeta a confidencialidad, por lo que no se
publica ni se replica. Tampoco se incluyen los scripts que procesan esa información.

Lo que sí se publica es el modelo analítico: la estructura de datos, las 122 medidas DAX
documentadas en `medidas_dax.md` y las decisiones de diseño. Las medidas referencian los
parámetros por su clave simbólica, no por su valor.

La réplica en Python y sus datos sintéticos son una obra independiente, creada para demostrar el
enfoque analítico sin reproducir información de terceros.

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `medidas_dax.md` | Las 122 medidas DAX del modelo, con su descripción y formato |
| `extraer_dax.py` | Script que extrae las medidas desde el modelo a este documento |
| `README.md` | Este documento |

## Licencia

MIT. Ver `LICENSE`.
