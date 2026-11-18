# Medidas DAX del modelo

Documento generado a partir del modelo semantico del proyecto (archivos TMDL).
El modelo contiene **122 medidas** distribuidas en **1 tablas**.

Las medidas leen los parametros del contrato desde la tabla `PARAMETROS` por su clave
simbolica (por ejemplo `"ppt_0"`), no por su valor. Por esa razon este documento no
expone cifras contractuales.

---

## Tabla `MEDIDAS`

### Kms Programados

Kilómetros comerciales programados diarios (Σ distancia_total × salidas, la programacion)

Formato: `#,##0`

```dax
SUMX(FRANJAS, FRANJAS[kmps] * FRANJAS[n_dias])
```

### Expediciones Programadas

Expediciones programadas (salidas) por día, la programacion

Formato: `#,##0`

```dax
SUMX(FRANJAS, FRANJAS[ep] * FRANJAS[n_dias])
```

### Plazas Programadas

Plazas ofertadas por día, la programacion

Formato: `#,##0`

```dax
SUMX(FRANJAS, FRANJAS[plazas] * FRANJAS[n_dias])
```

### Kms Eventos

Σ distancia de eventos C01 (los eventos de operacion) — validación cruzada con Kms Programados

Formato: `#,##0.0`

```dax
SUM(EVENTOS[distancia_km])
```

### PPT

Precio por pasajero transportado (parametros del contrato)

Formato: `#,##0`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "ppt_0"))
```

### PK Electrico

PK base bus eléctrico (parametros del contrato)

Formato: `#,##0`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "pk_electrico_0"))
```

### PK Diesel

PK base bus diésel (parametros del contrato)

Formato: `#,##0`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "pk_diesel_0"))
```

### IPK

Pasajeros por km (supuesto editable)

Formato: `0.00`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "ipk"))
```

### Tope Descuento

Tope descuento ITE+ICA (6,5% IB)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "tope_descuento"))
```

### Tope Premio

Tope premio ITE+ICA (5% IB)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "tope_premio"))
```

### Paso Escalera

Paso de escalera de descuento (1%)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "paso_escalera"))
```

### A ITE

Premio máximo ITE (4%)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "a_ite"))
```

### B ITE

Descuento máximo ITE (5%)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "b_ite"))
```

### A ICA

Premio máximo ICA (1%)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "a_ica"))
```

### B ICA

Descuento máximo ICA (1,5%)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "b_ica"))
```

### X IE1

Umbral X IE1 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_ie1"))
```

### X IE2

Umbral X IE2 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_ie2"))
```

### X IE3

Umbral X IE3 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_ie3"))
```

### X IP1

Umbral X IP1 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_ip1"))
```

### X IP2

Umbral X IP2 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_ip2"))
```

### X IP3

Umbral X IP3 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_ip3"))
```

### X ICA1

Umbral X ICA1 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_ica1"))
```

### X ICA2

Umbral X ICA2 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_ica2"))
```

### X ICA3

Umbral X ICA3 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_ica3"))
```

### X ICFP1

Umbral X ICFP1 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_icfp1"))
```

### X ICFP2

Umbral X ICFP2 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_icfp2"))
```

### X ICFP3

Umbral X ICFP3 (especificacion tecnica)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "x_icfp3"))
```

### Flota Contrato

Flota operativa base (439 buses)

Formato: `#,##0`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "flota_contrato"))
```

### PKU Bus

Precio por km según tipología (factor × PK base)

Formato: `#,##0.00`

```dax
VAR tipo = SELECTEDVALUE(EVENTOS[tipo_bus])
			RETURN SWITCH(tipo,
			 "A2V", 0.970 * [PK Electrico],
			 "B2V", 1.000 * [PK Electrico],
			 "C2D", 1.000 * [PK Diesel],
			 BLANK())
```

### PKS Teorico

Precio por km ponderado por mix de flota ponderado por días reales del mes (22L/4S/4D, cláusula 5.3.1.3, sin descuento)

Formato: `#,##0.00`

```dax
DIVIDE(SUMX(EVENTOS, EVENTOS[distancia_km] * [PKU Bus] * LOOKUPVALUE(DIAS[n_dias], DIAS[tipo_dia], EVENTOS[tipo_dia])), [Kms Eventos Ponderado])
```

### Ingreso Km Bruto

PKS × km válidos (kmp × ICFP, cláusula 5.3.1.6)

Formato: `#,##0`

```dax
[Kms Validos] * [PKS Teorico]
```

### Ingreso Pasajeros Bruto

PPT × IPK × km válidos (kmp × ICFP, cláusula 5.3.1.6)

Formato: `#,##0`

```dax
[Kms Validos] * [IPK] * [PPT]
```

### Ingreso Base

Def. 1.1.28: PPT·q + PKS·km

Formato: `#,##0`

```dax
[Ingreso Km Bruto] + [Ingreso Pasajeros Bruto]
```

### Otros

CIC terminales y otros (pendiente monetizar, 0)

Formato: `#,##0`

```dax
0
```

### YT Sin Descuento

Y_T sin descuentos (teórico)

Formato: `#,##0`

```dax
[Ingreso Base] + [Otros]
```

### ICFP Sel

ICFP simulado (slider, default 100%)

Formato: `0.0 %`

```dax
VAR icf = [ICF Sel]
			VAR icp = [ICP Sel]
			RETURN MIN(icf, icp)
```

### IE Sel

IE simulado (slider)

Formato: `0.0 %`

```dax
VALUE(SELECTEDVALUE(SIM_IE[Value], 1))
```

### IP Sel

IP simulado (slider)

Formato: `0.0 %`

```dax
VALUE(SELECTEDVALUE(SIM_IP[Value], 1))
```

### ICA Sel

ICA simulado (slider)

Formato: `0.0 %`

```dax
VALUE(SELECTEDVALUE(SIM_ICA[Value], 1))
```

### Kms Validos

kmv = kmp × ICFP (cláusula 5.3.1.6)

Formato: `#,##0`

```dax
[Kms Programados] * [ICFP Sel]
```

### P IE

Medias horas programadas con indicador IE (P_T^IE)

Formato: `#,##0`

```dax
CALCULATE(COUNTROWS(FRANJAS), FRANJAS[indicador_te] = "IE", FRANJAS[ep] > 0)
```

### P IP

Medias horas programadas con indicador IP (P_T^IP)

Formato: `#,##0`

```dax
CALCULATE(COUNTROWS(FRANJAS), FRANJAS[indicador_te] = "IP", FRANJAS[ep] > 0)
```

### %ID IE Lineal

Escala lineal del contrato (Apéndice N°6): IE

Formato: `0.0 %`

```dax
VAR v = [IE Sel]
			VAR x1 = [X IE1]
			VAR x2 = [X IE2]
			VAR x3 = [X IE3]
			VAR A = [A ITE]
			VAR B = [B ITE]
			VAR lineal = SWITCH(TRUE(),
			 v >= x3, A,
			 v >= x2, A * (v - x2) / (x3 - x2),
			 B * (v - x2) / (x2 - x1))
			RETURN MAX(-B, lineal)
```

### %ID IE Escalera

Escalera IE en pasos de 1%

Formato: `0.0 %`

```dax
ROUND([%ID IE Lineal] / [Paso Escalera], 0) * [Paso Escalera]
```

### %ID IP Lineal

Escala lineal del contrato (Apéndice N°6): IP

Formato: `0.0 %`

```dax
VAR v = [IP Sel]
			VAR x1 = [X IP1]
			VAR x2 = [X IP2]
			VAR x3 = [X IP3]
			VAR A = [A ITE]
			VAR B = [B ITE]
			VAR lineal = SWITCH(TRUE(),
			 v >= x3, A,
			 v >= x2, A * (v - x2) / (x3 - x2),
			 B * (v - x2) / (x2 - x1))
			RETURN MAX(-B, lineal)
```

### %ID IP Escalera

Escalera IP en pasos de 1%

Formato: `0.0 %`

```dax
ROUND([%ID IP Lineal] / [Paso Escalera], 0) * [Paso Escalera]
```

### %ID ICA Lineal

Escala lineal del contrato (Apéndice N°6): ICA

Formato: `0.0 %`

```dax
VAR v = [ICA Sel]
			VAR x1 = [X ICA1]
			VAR x2 = [X ICA2]
			VAR x3 = [X ICA3]
			VAR A = [A ICA]
			VAR B = [B ICA]
			VAR lineal = SWITCH(TRUE(),
			 v >= x3, A,
			 v >= x2, A * (v - x2) / (x3 - x2),
			 B * (v - x2) / (x2 - x1))
			RETURN MAX(-B, lineal)
```

### %ID ICA Escalera

Escalera ICA en pasos de 1%

Formato: `0.0 %`

```dax
ROUND([%ID ICA Lineal] / [Paso Escalera], 0) * [Paso Escalera]
```

### Modo Escalera

Conmutador: Contrato lineal vs Escalera 1%

```dax
SELECTEDVALUE(MODOS[Modo], "Escalera 1%")
```

### %ID ITE Lineal

ITE ponderado por medias horas (Apéndice N°6 D.1)

Formato: `0.0 %`

```dax
DIVIDE([P IE] * [%ID IE Lineal] + [P IP] * [%ID IP Lineal], [P IE] + [P IP])
```

### %ID ITE Escalera

ITE con escalera 1%

Formato: `0.0 %`

```dax
DIVIDE([P IE] * [%ID IE Escalera] + [P IP] * [%ID IP Escalera], [P IE] + [P IP])
```

### %ID ITE

%ID ITE según modo seleccionado

Formato: `0.0 %`

```dax
IF([Modo Escalera] = "Escalera 1%", [%ID ITE Escalera], [%ID ITE Lineal])
```

### %ID ICA

%ID ICA según modo seleccionado

Formato: `0.0 %`

```dax
IF([Modo Escalera] = "Escalera 1%", [%ID ICA Escalera], [%ID ICA Lineal])
```

### CI %

Descuento/premio por calidad con tope contractual 6,5%

Formato: `0.0 %`

```dax
MIN(MAX([%ID ITE] + [%ID ICA], -[Tope Descuento]), [Tope Premio])
```

### Descuento ITE $

Formato: `#,##0`

```dax
MIN([%ID ITE], 0) * [Ingreso Base]
```

### Descuento ICA $

Formato: `#,##0`

```dax
MIN([%ID ICA], 0) * [Ingreso Base]
```

### CI $

Monto neto por cumplimiento de indicadores (Apéndice N°6)

Formato: `#,##0`

```dax
[CI %] * [Ingreso Base]
```

### YT Neto

Pago final estimado con descuentos

Formato: `#,##0`

```dax
[YT Sin Descuento] + [CI $]
```

### % Impacto

Impacto de calidad sobre el ingreso base

Formato: `0.0 %`

```dax
DIVIDE([CI $], [Ingreso Base])
```

### Buses Franja

Buses requeridos en la franja (ciclo ÷ intervalo)

Formato: `#,##0`

```dax
SUM(BUSES_SIM_FRANJA[buses_franja])
```

### Buses Pico

Máximo de buses simultáneos en el contexto (pico)

Formato: `#,##0`

```dax
VAR flota_por_dia =
			 SUMMARIZE(
			 BUSES_SIM,
			 BUSES_SIM[tipo_dia],
			 "flota_dia", SUM(BUSES_SIM[max_dia])
			 )
			RETURN MAXX(flota_por_dia, [flota_dia])
```

### Holgura Flota

Flota contrato menos pico requerido

Formato: `#,##0`

```dax
[Flota Contrato] - [Buses Pico]
```

### ICFP Teorico

ICFP teórico con operación perfecta

Formato: `0.0 %`

```dax
1
```

### ICF Teorico

ICF teórico

Formato: `0.0 %`

```dax
1
```

### ICP Teorico

ICP teórico

Formato: `0.0 %`

```dax
1
```

### Descuento Aplicado %

Valor absoluto del descuento por calidad (para gauge vs tope)

Formato: `0.0 %`

```dax
ABS([CI %])
```

### Ingreso Componente

Ingreso por componente (serie para gráfico apilado)

Formato: `#,##0`

```dax
SWITCH(SELECTEDVALUE(COMPONENTES[Componente]),
			 "Km comerciales", [Ingreso Km Bruto],
			 "Pasajeros", [Ingreso Pasajeros Bruto],
			 BLANK())
```

### Flota Simultanea

Buses requeridos en el contexto (franja/día/servicio)

Formato: `#,##0`

```dax
SUM(BUSES_SIM_FRANJA[buses_franja])
```

### % Utilizacion Flota

Pico requerido sobre flota contrato

Formato: `0.0 %`

```dax
DIVIDE([Buses Pico], [Flota Contrato])
```

### Km Ciclo

Kilómetros de ciclo (ida+retorno) por servicio

Formato: `#,##0.0`

```dax
MAX(BUSES_REQUERIDOS[km_ciclo])
```

### Velocidad Media

Velocidad media comercial (km/h)

Formato: `#,##0.0`

```dax
AVERAGE(BUSES_REQUERIDOS[velocidad])
```

### Buses PMA

Buses punta (máx en ventana) por servicio-tipo-día — método simulación

Formato: `#,##0`

```dax
VAR por_dia =
			 SUMMARIZE(BUSES_SIM, BUSES_SIM[tipo_dia], "val", SUM(BUSES_SIM[pma]))
			RETURN MAXX(por_dia, [val])
```

### Buses PMD

Buses punta (máx en ventana) por servicio-tipo-día — método simulación

Formato: `#,##0`

```dax
VAR por_dia =
			 SUMMARIZE(BUSES_SIM, BUSES_SIM[tipo_dia], "val", SUM(BUSES_SIM[pmd]))
			RETURN MAXX(por_dia, [val])
```

### Buses PTA

Buses punta (máx en ventana) por servicio-tipo-día — método simulación

Formato: `#,##0`

```dax
VAR por_dia =
			 SUMMARIZE(BUSES_SIM, BUSES_SIM[tipo_dia], "val", SUM(BUSES_SIM[pta]))
			RETURN MAXX(por_dia, [val])
```

### Buses Max Dia

Buses punta (máx en ventana) por servicio-tipo-día — método simulación

Formato: `#,##0`

```dax
VAR por_dia =
			 SUMMARIZE(BUSES_SIM, BUSES_SIM[tipo_dia], "val", SUM(BUSES_SIM[max_dia]))
			RETURN MAXX(por_dia, [val])
```

### ICF Sel

ICF simulado (ev/ep, slider)

Formato: `0.0 %`

```dax
VALUE(SELECTEDVALUE(SIM_ICF[Value], 1))
```

### ICP Sel

ICP simulado (plvd/plprog, slider)

Formato: `0.0 %`

```dax
VALUE(SELECTEDVALUE(SIM_ICP[Value], 1))
```

### EC ICFP1

Revisión excepcional ICFP 1 (95%)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "ec_icfp1"))
```

### EC ICFP2

Revisión excepcional ICFP 2 (75%)

Formato: `0.0 %`

```dax
VALUE(LOOKUPVALUE(PARAMETROS[valor], PARAMETROS[parametro], "ec_icfp2"))
```

### Zona ICFP

Zona del ICFP según umbrales contractuales

```dax
VAR icf = VALUE(SELECTEDVALUE(SIM_ICF[Value], 1))
			VAR icp = VALUE(SELECTEDVALUE(SIM_ICP[Value], 1))
			VAR icfp = MIN(icf, icp)
			RETURN SWITCH(TRUE(),
			 icfp >= 0.95, "Óptimo",
			 icfp >= 0.90, "Aceptable",
			 icfp >= 0.85, "Alerta",
			 icfp >= 0.75, "Revisión excepcional",
			 "Crítico")
```

### Valor Indicador

Valor por fila del marco contractual

Formato: `0.0 %`

```dax
SWITCH(SELECTEDVALUE(INDICADORES[Indicador]),
			 "ICFP", [ICFP Sel],
			 "ICF", [ICF Sel],
			 "ICP", [ICP Sel],
			 "Umbral 85%", [X ICFP1],
			 "Umbral 90%", [X ICFP2],
			 "Umbral 95%", [X ICFP3],
			 "EC 95%", [EC ICFP1],
			 "EC 75%", [EC ICFP2],
			 BLANK())
```

### Valor Afect

Valor simulado del indicador

Formato: `0.0 %`

```dax
SWITCH(SELECTEDVALUE(AFECTACION[Indicador]),
			 "ICF", [ICF Sel],
			 "ICP", [ICP Sel],
			 "IE", [IE Sel],
			 "IP", [IP Sel],
			 "ICA", [ICA Sel],
			 BLANK())
```

### Umbral Afect

Umbrales donde el cumplimiento afecta el pago

```dax
SWITCH(SELECTEDVALUE(AFECTACION[Indicador]),
			 "ICF", "alerta 85% · aceptable 90% · óptimo 95%",
			 "ICP", "alerta 85% · aceptable 90% · óptimo 95%",
			 "IE", "neutro 87,5% · descuento −5% en ≤80% · premio +4% en ≥95%",
			 "IP", "neutro 80% · descuento −5% en ≤60% · premio +4% en ≥90%",
			 "ICA", "neutro 90% · descuento −1,5% en ≤80% · premio +1% en ≥95%",
			 "CONJUNTO", "premio máx +5% · descuento máx −6,5% del ingreso base",
			 BLANK())
```

### %ID Afect

%ID del indicador (o CI% en el conjunto)

Formato: `0.0 %`

```dax
SWITCH(SELECTEDVALUE(AFECTACION[Indicador]),
			 "IE", [%ID IE],
			 "IP", [%ID IP],
			 "ICA", [%ID ICA],
			 "CONJUNTO", [CI %],
			 BLANK())
```

### Ingreso Base Full

Ingreso base con cumplimiento perfecto (ICFP = 100%)

Formato: `#,##0`

```dax
[Kms Programados] * ([PKS Teorico] + [IPK] * [PPT])
```

### Efecto Afect $

Efecto en $ del indicador vs cumplimiento perfecto (+ premio, − pérdida)

Formato: `#,##0`

```dax
SWITCH(SELECTEDVALUE(AFECTACION[Indicador]),
			 "ICF", IF([ICF Sel] <= [ICP Sel], [Ingreso Base] - [Ingreso Base Full], 0),
			 "ICP", IF([ICP Sel] < [ICF Sel], [Ingreso Base] - [Ingreso Base Full], 0),
			 "IE", [%ID IE] * [Ingreso Base] * DIVIDE([P IE], [P IE] + [P IP]),
			 "IP", [%ID IP] * [Ingreso Base] * DIVIDE([P IP], [P IE] + [P IP]),
			 "ICA", [%ID ICA] * [Ingreso Base],
			 "CONJUNTO", [YT Neto] - [Ingreso Base Full],
			 BLANK())
```

### Esc Visibles

Número de escenarios visibles según filtros

Formato: `#,##0`

```dax
COUNTROWS(ESCENARIOS)
```

### Esc YT Min

YT Neto menor del conjunto filtrado

Formato: `#,##0`

```dax
MIN(ESCENARIOS[yt_neto])
```

### Esc YT Max

YT Neto mayor del conjunto filtrado

Formato: `#,##0`

```dax
MAX(ESCENARIOS[yt_neto])
```

### Esc Efecto Peor

Efecto peor caso vs cumplimiento perfecto (pérdida máx.)

Formato: `#,##0`

```dax
MIN(ESCENARIOS[efecto])
```

### Esc ICFP Min

ICFP mínimo del conjunto filtrado

Formato: `0.0 %`

```dax
MIN(ESCENARIOS[icfp])
```

### Participación kmps

% de kmps de la fila sobre el total filtrado

Formato: `0.0 %`

```dax
DIVIDE(SUM(FRANJAS[kmps]), CALCULATE(SUM(FRANJAS[kmps]), ALLSELECTED(FRANJAS)))
```

### Sens YT Min

YT Neto menor de la curva de sensibilidad

Formato: `#,##0`

```dax
MIN(SENSIBILIDAD[yt_neto])
```

### Sens YT Max

YT Neto mayor de la curva de sensibilidad

Formato: `#,##0`

```dax
MAX(SENSIBILIDAD[yt_neto])
```

### Sens Perdida Max

Pérdida máxima vs cumplimiento perfecto en la curva

Formato: `#,##0`

```dax
MIN(SENSIBILIDAD[efecto])
```

### Sens Costo Punto Max

Costo máximo de un punto % de incumplimiento

Formato: `#,##0`

```dax
MAX(SENSIBILIDAD[costo_punto])
```

### Per IB

Ingreso base del período y tipo de día filtrados

Formato: `#,##0`

```dax
MAX(INGRESOS_PERIODO[ingreso_base])
```

### Per kmps

km programados del período y tipo de día filtrados

Formato: `#,##0`

```dax
MAX(INGRESOS_PERIODO[kmps])
```

### Per dias

Días que representa el período filtrado

Formato: `0`

```dax
MAX(INGRESOS_PERIODO[dias])
```

### Kmps Dia

km programados de UN día de ese tipo (frecuencia por franja)

Formato: `#,##0`

```dax
SUMX(FRANJAS, FRANJAS[kmps])
```

### Expediciones Dia

Expediciones de UN día de ese tipo

Formato: `#,##0`

```dax
SUM(FRANJAS[ep])
```

### Plazas Dia

Plazas de UN día de ese tipo

Formato: `#,##0`

```dax
SUM(FRANJAS[plazas])
```

### Kms Eventos Ponderado

km de eventos ponderados por días reales del mes (22L/4S/4D vía DIAS[n_dias])

Formato: `#,##0`

```dax
SUMX(EVENTOS, EVENTOS[distancia_km] * LOOKUPVALUE(DIAS[n_dias], DIAS[tipo_dia], EVENTOS[tipo_dia]))
```

### Participación Ingreso

% del ingreso base del servicio sobre el total filtrado

Formato: `0.0 %`

```dax
DIVIDE([Ingreso Base], CALCULATE([Ingreso Base], ALLSELECTED(SERVICIOS)))
```

### Kms Eléctrico

km programados de buses eléctricos (A2V+B2V), prorrateados por mix de eventos

Formato: `#,##0`

```dax
[Kms Programados] * DIVIDE(SUMX(FILTER(EVENTOS, EVENTOS[tipo_bus] = "A2V" || EVENTOS[tipo_bus] = "B2V"), EVENTOS[distancia_km] * LOOKUPVALUE(DIAS[n_dias], DIAS[tipo_dia], EVENTOS[tipo_dia])), [Kms Eventos Ponderado])
```

### Kms Diésel

km programados de buses diésel (C2D), prorrateados por mix de eventos

Formato: `#,##0`

```dax
[Kms Programados] * DIVIDE(SUMX(FILTER(EVENTOS, EVENTOS[tipo_bus] = "C2D"), EVENTOS[distancia_km] * LOOKUPVALUE(DIAS[n_dias], DIAS[tipo_dia], EVENTOS[tipo_dia])), [Kms Eventos Ponderado])
```

### PKS Eléctrico

precio por km ponderado solo con buses eléctricos, ponderado por días reales del mes (A2V 0,970 / B2V 1,000 sobre PK eléctrico)

Formato: `#,##0.00`

```dax
VAR km = CALCULATE([Kms Eventos Ponderado], EVENTOS[tipo_bus] = "A2V" || EVENTOS[tipo_bus] = "B2V")
			RETURN DIVIDE(SUMX(FILTER(EVENTOS, EVENTOS[tipo_bus] = "A2V" || EVENTOS[tipo_bus] = "B2V"), EVENTOS[distancia_km] * [PKU Bus] * LOOKUPVALUE(DIAS[n_dias], DIAS[tipo_dia], EVENTOS[tipo_dia])), km)
```

### PKS Diésel

precio por km ponderado solo con buses diésel, ponderado por días reales del mes (C2D 1,000 sobre PK diésel)

Formato: `#,##0.00`

```dax
VAR km = CALCULATE([Kms Eventos Ponderado], EVENTOS[tipo_bus] = "C2D")
			RETURN DIVIDE(SUMX(FILTER(EVENTOS, EVENTOS[tipo_bus] = "C2D"), EVENTOS[distancia_km] * [PKU Bus] * LOOKUPVALUE(DIAS[n_dias], DIAS[tipo_dia], EVENTOS[tipo_dia])), km)
```

### Kms Validos Eléctrico

km válidos eléctricos (km programados × ICFP)

Formato: `#,##0`

```dax
[Kms Eléctrico] * [ICFP Sel]
```

### Kms Validos Diésel

km válidos diésel (km programados × ICFP)

Formato: `#,##0`

```dax
[Kms Diésel] * [ICFP Sel]
```

### Ingreso Km Eléctrico

ingreso por km de buses eléctricos

Formato: `#,##0`

```dax
[Kms Validos Eléctrico] * [PKS Eléctrico]
```

### Ingreso Km Diésel

ingreso por km de buses diésel

Formato: `#,##0`

```dax
[Kms Validos Diésel] * [PKS Diésel]
```

### Ingreso Pasajeros Eléctrico

ingreso por pasajeros asociado a km eléctricos

Formato: `#,##0`

```dax
[Kms Validos Eléctrico] * [IPK] * [PPT]
```

### Ingreso Pasajeros Diésel

ingreso por pasajeros asociado a km diésel

Formato: `#,##0`

```dax
[Kms Validos Diésel] * [IPK] * [PPT]
```

### Ingreso Base Eléctrico

ingreso base total atribuible a buses eléctricos

Formato: `#,##0`

```dax
[Ingreso Km Eléctrico] + [Ingreso Pasajeros Eléctrico]
```

### Ingreso Base Diésel

ingreso base total atribuible a buses diésel

Formato: `#,##0`

```dax
[Ingreso Km Diésel] + [Ingreso Pasajeros Diésel]
```

### % Ingreso Eléctrico

% del ingreso base que aportan los buses eléctricos

Formato: `0.0 %`

```dax
DIVIDE([Ingreso Base Eléctrico], [Ingreso Base])
```

### % Ingreso Diésel

% del ingreso base que aportan los buses diésel

Formato: `0.0 %`

```dax
DIVIDE([Ingreso Base Diésel], [Ingreso Base])
```

### Ingreso por Tecnología

ingreso base según la tecnología seleccionada (tabla TIPO_TECNOLOGIA)

Formato: `#,##0`

```dax
SWITCH(SELECTEDVALUE(TIPO_TECNOLOGIA[Tecnologia]),
			 "Eléctrico", [Ingreso Base Eléctrico],
			 "Diésel", [Ingreso Base Diésel],
			 BLANK())
```

### Kms por Tecnología

km programados según la tecnología seleccionada (tabla TIPO_TECNOLOGIA)

Formato: `#,##0`

```dax
SWITCH(SELECTEDVALUE(TIPO_TECNOLOGIA[Tecnologia]),
			 "Eléctrico", [Kms Eléctrico],
			 "Diésel", [Kms Diésel],
			 BLANK())
```

### % Kms Eléctrico

% de los km programados que aportan los buses eléctricos

Formato: `0.0 %`

```dax
DIVIDE([Kms Eléctrico], [Kms Eléctrico] + [Kms Diésel])
```

### % Kms Diésel

% de los km programados que aportan los buses diésel

Formato: `0.0 %`

```dax
DIVIDE([Kms Diésel], [Kms Eléctrico] + [Kms Diésel])
```
