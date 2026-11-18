#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extrae las medidas DAX del modelo (.pbip) a un documento Markdown.

Las medidas referencian parametros por su clave simbolica (por ejemplo
PARAMETROS[parametro] = "ppt_0"), no por su valor, por lo que no exponen
cifras contractuales. El script verifica ademas que no queden numeros
sensibles en el texto extraido.
"""
import re
from pathlib import Path

DEF = Path(r"C:\Users\luis_\Desktop\Estudio\0001. Power BI\Gran_America_U16"
           r"\Gran_America_U16.SemanticModel\definition")
DESTINO = Path(__file__).parent

PATRON_MEDIDA = re.compile(
    r"^\tmeasure\s+(?:'((?:[^']|'')+)'|(\w+))\s*=\s*(.*?)(?=^\tmeasure\s|^\tcolumn\s|^\tpartition\s|\Z)",
    re.MULTILINE | re.DOTALL,
)


def limpiar(nombre: str) -> str:
    return nombre.replace("''", "'")


def extraer_de(archivo: Path):
    """Devuelve [(nombre, expresion, descripcion, formato)] de un archivo TMDL."""
    texto = archivo.read_text(encoding="utf-8", errors="replace")
    salida = []
    for m in PATRON_MEDIDA.finditer(texto):
        nombre = limpiar(m.group(1) or m.group(2))
        cuerpo = m.group(3)
        lineas = [l for l in cuerpo.splitlines()]
        # quitar lineas de metadatos (lineageTag, formatString, annotation...)
        expr_lineas, desc, fmt = [], None, None
        for l in lineas:
            s = l.strip()
            if s.startswith("lineageTag:"):
                continue
            if s.startswith("formatString:"):
                fmt = s.split(":", 1)[1].strip()
                continue
            if s.startswith("annotation Description ="):
                desc = s.split("=", 1)[1].strip().strip('"')
                continue
            if s.startswith("annotation ") or s.startswith("changedProperty"):
                continue
            if s.startswith("\t\t\t") or s.startswith("\t\t") or not s:
                if expr_lineas or s:
                    expr_lineas.append(l.replace("\t\t", "", 1))
                continue
            expr_lineas.append(l)
        expr = "\n".join(expr_lineas).strip()
        salida.append((nombre, expr, desc, fmt))
    return salida


# ---------------------------------------------------------------------------
filas = []
for tmdl in sorted((DEF / "tables").glob("*.tmdl")):
    for nombre, expr, desc, fmt in extraer_de(tmdl):
        filas.append((tmdl.stem, nombre, expr, desc, fmt))

print(f"Medidas encontradas: {len(filas)}")
tablas = {}
for tabla, nombre, expr, desc, fmt in filas:
    tablas.setdefault(tabla, []).append((nombre, expr, desc, fmt))

# ---------------------------------------------------------------------------
# Verificacion de numeros sensibles (precios, ingresos, kilometros totales)
# ---------------------------------------------------------------------------
sospechosos = re.compile(
    r"\b(1313|2210|37000|3\.?615|3\.?795|180\.?750|2\.?239|82228|57771|49881|"
    r"237\.?907|306\.?487|321\.811|385)\b"
)
alertas = []
for tabla, nombre, expr, desc, fmt in filas:
    if sospechosos.search(expr):
        alertas.append((tabla, nombre, expr[:120]))

# ---------------------------------------------------------------------------
# Documento
# ---------------------------------------------------------------------------
lineas = [
    "# Medidas DAX del modelo",
    "",
    "Documento generado a partir del modelo semantico del proyecto (archivos TMDL).",
    f"El modelo contiene **{len(filas)} medidas** distribuidas en "
    f"**{len(tablas)} tablas**.",
    "",
    "Las medidas leen los parametros del contrato desde la tabla `PARAMETROS` por su clave",
    "simbolica (por ejemplo `\"ppt_0\"`), no por su valor. Por esa razon este documento no",
    "expone cifras contractuales.",
    "",
    "---",
    "",
]
for tabla in sorted(tablas):
    lineas.append(f"## Tabla `{tabla}`")
    lineas.append("")
    for nombre, expr, desc, fmt in tablas[tabla]:
        lineas.append(f"### {nombre}")
        lineas.append("")
        if desc:
            lineas.append(f"{desc}")
            lineas.append("")
        if fmt:
            lineas.append(f"Formato: `{fmt}`")
            lineas.append("")
        lineas.append("```dax")
        lineas.append(expr)
        lineas.append("```")
        lineas.append("")

(DESTINO / "medidas_dax.md").write_text("\n".join(lineas), encoding="utf-8")
print(f"Escrito: medidas_dax.md ({len(lineas)} lineas)")

# ---------------------------------------------------------------------------
# Sanear referencias a documentos internos en el documento generado
# ---------------------------------------------------------------------------
SANEAR = {
    "Anexo 3": "la programacion",
    "Anexo 4": "los eventos de operacion",
    "Anexo 5": "documentacion tecnica",
    "Ficha Técnica A.2": "parametros del contrato",
    "Ficha Técnica": "especificacion tecnica",
    "Ficha A.3": "parametros del contrato",
    "Ficha A.4": "parametros del contrato",
    "PO 2026": "",
    "DTPM": "",
    "Transantiago": "",
}
p = DESTINO / "medidas_dax.md"
t = p.read_text(encoding="utf-8")
for viejo, nuevo in SANEAR.items():
    t = t.replace(viejo, nuevo)
t = re.sub(r"Ficha A\.\d", "parametros del contrato", t)
t = re.sub(r"  +", " ", t)
p.write_text(t, encoding="utf-8")
print("Referencias a documentos internos saneadas.")


if alertas:
    print("\nADVERTENCIA: numeros potencialmente sensibles en medidas:")
    for t, n, e in alertas:
        print(f"  {t}.{n}: {e}")
else:
    print("\nSin numeros potencialmente sensibles en las medidas.")
