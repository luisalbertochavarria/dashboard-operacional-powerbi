#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extrae las medidas DAX de un modelo tabular en formato TMDL (Power BI .pbip)
y genera un documento Markdown con el nombre, la descripcion, el formato y la
expresion de cada medida.

Uso:
    python extraer_dax.py <ruta_al_modelo_semantico>

Ejemplo:
    python extraer_dax.py "MiProyecto.SemanticModel/definition"

Genera `medidas_dax.md` en el directorio del script.

Nota: las medidas de este modelo leen los parametros desde una tabla de
parametros por su clave simbolica (por ejemplo `PARAMETROS[parametro] = "ppt_0"`),
no por su valor literal. Por eso el documento resultante no expone cifras.
"""
import re
import sys
from pathlib import Path

DESTINO = Path(__file__).parent

PATRON_MEDIDA = re.compile(
    r"^\tmeasure\s+(?:'((?:[^']|'')+)'|(\w+))\s*=\s*(.*?)"
    r"(?=^\tmeasure\s|^\tcolumn\s|^\tpartition\s|\Z)",
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
        expr_lineas, desc, fmt = [], None, None
        for l in cuerpo.splitlines():
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
            if s.startswith("\t\t") or not s:
                expr_lineas.append(l.replace("\t\t", "", 1))
                continue
            expr_lineas.append(l)
        salida.append((nombre, "\n".join(expr_lineas).strip(), desc, fmt))
    return salida


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    definicion = Path(sys.argv[1])
    tablas_dir = definicion / "tables"
    if not tablas_dir.is_dir():
        sys.exit(f"No se encontro la carpeta de tablas en: {tablas_dir}")

    tablas = {}
    total = 0
    for tmdl in sorted(tablas_dir.glob("*.tmdl")):
        medidas = extraer_de(tmdl)
        if medidas:
            tablas[tmdl.stem] = medidas
            total += len(medidas)
    print(f"Medidas encontradas: {total}")

    lineas = [
        "# Medidas DAX del modelo",
        "",
        "Documento generado a partir del modelo semantico (archivos TMDL).",
        f"El modelo contiene **{total} medidas** distribuidas en **{len(tablas)} tablas**.",
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
                lineas.append(desc)
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


if __name__ == "__main__":
    main()
