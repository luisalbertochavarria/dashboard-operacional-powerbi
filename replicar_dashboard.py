#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Genera datos sinteticos y la demostracion interactiva de la replica del tablero.

Reproduce en Python/Plotly el modelo analitico del tablero original (que esta en
Power BI) usando datos SINTETICOS: servicios, terminales, programacion, parametros
economicos e indicadores son ficticios.

Salida:
    datos_sinteticos/*.csv      tablas del modelo
    docs/index.html             demostracion interactiva

Uso:
    python replicar_dashboard.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

RAIZ = Path(__file__).parent
DATOS = RAIZ / "datos_sinteticos"
DOCS = RAIZ / "docs"

SEED = 20260301
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------------------
# Escenario ficticio
# ---------------------------------------------------------------------------
TERMINALES = ["Terminal Norte", "Terminal Poniente", "Terminal Sur",
              "Terminal Oriente", "Terminal Central"]
N_SERVICIOS = 30
DIAS = {"Laboral": 22, "Sábado": 4, "Domingo": 4}
FRANJAS = [f"{h:02d}:00" for h in range(5, 24)]

# Parametros economicos FICTICIOS (no corresponden a ningun contrato real)
PARAMETROS = {
    "PPT (precio por pasajero)": 150.0,
    "PKS (precio por km)": 1200.0,
    "IPK (pasajeros por km)": 1.80,
    "Tope de descuento": 0.065,
    "Tope de premio": 0.030,
}

# Umbrales e incumplimientos simulados de indicadores
INDICADORES = [
    # nombre, descripcion, umbral, valor simulado (mayor = mejor)
    ("ICF", "Cumplimiento de frecuencia", 0.975, 0.981),
    ("ICP", "Cumplimiento de puntualidad", 0.950, 0.943),
    ("ICFP", "Cumplimiento de programación", 0.980, 0.988),
    ("IE", "Expediciones efectivas", 0.970, 0.974),
    ("IP", "Puntualidad de salidas", 0.960, 0.951),
    ("ICA", "Calidad de atención", 0.940, 0.938),
]


def generar_franjas() -> pd.DataFrame:
    """Programacion por servicio, sentido, tipo de dia y franja horaria."""
    filas = []
    for i in range(1, N_SERVICIOS + 1):
        serv = f"S{i:02d}"
        terminal = TERMINALES[(i - 1) % len(TERMINALES)]
        tipo_bus = "Eléctrico" if i % 3 != 0 else "Diésel"
        for sentido in ("Ida", "Ret"):
            for tipo_dia in DIAS:
                factor = {"Laboral": 1.0, "Sábado": 0.70, "Domingo": 0.55}[tipo_dia]
                for franja in FRANJAS:
                    hora = int(franja[:2])
                    # perfil: punta manana 7-9, punta tarde 17-19, valle el resto
                    if 7 <= hora <= 9:
                        intensidad = 1.55
                    elif 17 <= hora <= 19:
                        intensidad = 1.60
                    elif 10 <= hora <= 16:
                        intensidad = 0.85
                    else:
                        intensidad = 0.45
                    ep = max(0, int(round(rng.normal(6 * factor * intensidad, 1.2))))
                    if ep == 0:
                        continue
                    dist = float(rng.uniform(12, 26))  # km por vuelta
                    kmps = round(ep * dist, 1)
                    plazas = int(ep * rng.choice([60, 80, 90]))
                    filas.append({
                        "servicio": serv, "terminal": terminal, "sentido": sentido,
                        "tipo_dia": tipo_dia, "franja": franja, "tipo_bus": tipo_bus,
                        "ep": ep, "kmps": kmps, "plazas": plazas,
                        "n_dias": DIAS[tipo_dia],
                        "hora": hora,
                    })
    return pd.DataFrame(filas)


def calcular_kpis(fr: pd.DataFrame) -> dict:
    """Calcula los indicadores del modelo con las definiciones del original."""
    km_dia = (fr.groupby("tipo_dia")["kmps"].sum()).to_dict()
    ep_dia = (fr.groupby("tipo_dia")["ep"].sum()).to_dict()
    plazas_dia = (fr.groupby("tipo_dia")["plazas"].sum()).to_dict()

    # mes tipo: suma ponderada por dias
    km_mes = sum(km_dia[t] * DIAS[t] for t in DIAS)
    ep_mes = sum(ep_dia[t] * DIAS[t] for t in DIAS)
    plazas_mes = sum(plazas_dia[t] * DIAS[t] for t in DIAS)

    icfp = dict((n, v) for n, _, _, v in [(i[0], i[1], i[2], i[3]) for i in INDICADORES])["ICFP"]
    km_validos = km_mes * icfp

    pks = PARAMETROS["PKS (precio por km)"]
    ppt = PARAMETROS["PPT (precio por pasajero)"]
    ipk = PARAMETROS["IPK (pasajeros por km)"]

    ing_km = km_validos * pks
    ing_pas = km_validos * ipk * ppt
    ing_base = ing_km + ing_pas

    # desviaciones: (valor - umbral) / umbral
    desv = {n: (v - u) / u for n, _, u, v in INDICADORES}
    pct_ite = sum(min(d, 0) for d in desv.values())
    pct_ite = max(pct_ite, -PARAMETROS["Tope de descuento"])
    descuento = pct_ite * ing_base
    yt_neto = ing_base + descuento

    return {
        "km_dia": km_dia, "ep_dia": ep_dia, "plazas_dia": plazas_dia,
        "km_mes": km_mes, "ep_mes": ep_mes, "plazas_mes": plazas_mes,
        "km_validos": km_validos, "ing_km": ing_km, "ing_pas": ing_pas,
        "ing_base": ing_base, "icfp": icfp, "pct_ite": pct_ite,
        "descuento": descuento, "yt_neto": yt_neto, "desv": desv,
    }


def clp(v: float) -> str:
    return f"${v:,.0f}".replace(",", ".")


# ---------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------
def fig_ingresos_por_dia(fr: pd.DataFrame, k: dict) -> go.Figure:
    tipos = list(DIAS)
    valores = []
    for t in tipos:
        km = k["km_dia"][t] * k["icfp"]
        valores.append(km * PARAMETROS["PKS (precio por km)"] + km * PARAMETROS["IPK (pasajeros por km)"] * PARAMETROS["PPT (precio por pasajero)"])
    fig = go.Figure(go.Bar(
        x=tipos, y=valores, marker_color=["#1d4ed8", "#0891b2", "#0f766e"],
        text=[clp(v) for v in valores], textposition="outside",
        hovertemplate="%{x}<br>%{y:,.0f} CLP<extra></extra>",
    ))
    fig.update_layout(title="Ingreso base por tipo de día",
                      yaxis_title="CLP", height=420, showlegend=False,
                      margin=dict(l=80, r=20, t=60, b=50))
    return fig


def fig_composicion(k: dict) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=["Componente kilómetros", "Componente pasajeros"],
        values=[k["ing_km"], k["ing_pas"]],
        hole=0.55, marker_colors=["#1d4ed8", "#f59e0b"],
        hovertemplate="%{label}<br>%{value:,.0f} CLP (%{percent})<extra></extra>",
    ))
    fig.update_layout(title="Composición del ingreso base (mes tipo)",
                      height=420, margin=dict(l=20, r=20, t=60, b=20),
                      legend=dict(orientation="h", y=-0.08))
    return fig


def fig_flota(fr: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    colores = {"Laboral": "#1d4ed8", "Sábado": "#0891b2", "Domingo": "#0f766e"}
    for tipo_dia in DIAS:
        d = fr[fr["tipo_dia"] == tipo_dia].groupby("hora")["ep"].sum().reset_index()
        fig.add_trace(go.Scatter(
            x=d["hora"], y=d["ep"], mode="lines+markers", name=tipo_dia,
            line=dict(color=colores[tipo_dia], width=2.5),
            hovertemplate=f"<b>{tipo_dia}</b><br>%{{x}}:00 h<br>%{{y}} expediciones<extra></extra>",
        ))
    fig.update_layout(title="Expediciones por hora y tipo de día",
                      xaxis_title="Hora", yaxis_title="Expediciones",
                      height=440, margin=dict(l=60, r=20, t=90, b=50),
                      legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0))
    return fig


def fig_por_terminal(fr: pd.DataFrame) -> go.Figure:
    d = fr.groupby("terminal").agg(km=("kmps", "sum"), serv=("servicio", "nunique")).reset_index()
    d = d.sort_values("km", ascending=False)
    fig = go.Figure(go.Bar(
        x=d["terminal"], y=d["km"], marker_color="#334155",
        text=[f"{s} servicios" for s in d["serv"]], textposition="outside",
        hovertemplate="%{x}<br>%{y:,.0f} km/día<extra></extra>",
    ))
    fig.update_layout(title="Kilómetros diarios por terminal",
                      xaxis_title="Terminal", yaxis_title="km por día",
                      height=420, showlegend=False,
                      margin=dict(l=70, r=20, t=60, b=90))
    return fig


def fig_indicadores(k: dict) -> go.Figure:
    nombres = [n for n, _, _, _ in INDICADORES]
    umbrales = [u * 100 for _, _, u, _ in INDICADORES]
    valores = [v * 100 for _, _, _, v in INDICADORES]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=nombres, y=valores, name="Cumplimiento simulado",
        marker_color=["#16a34a" if v >= u else "#dc2626" for v, u in zip(valores, umbrales)],
        hovertemplate="%{x}<br>Cumplimiento: %{y:.2f}%<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=nombres, y=umbrales, mode="markers", name="Umbral exigido",
        marker=dict(symbol="line-ew-open", size=26, color="#0f172a", line=dict(width=3)),
        hovertemplate="%{x}<br>Umbral: %{y:.2f}%<extra></extra>",
    ))
    fig.update_layout(title="Indicadores de calidad: cumplimiento contra umbral",
                      yaxis_title="%", height=440,
                      margin=dict(l=60, r=20, t=100, b=50),
                      legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0))
    fig.update_yaxes(range=[93, 100])
    return fig


def fig_impacto(k: dict) -> go.Figure:
    filas = []
    for n, _, u, v in INDICADORES:
        d = (v - u) / u
        filas.append((n, d * k["ing_base"]))
    filas.sort(key=lambda x: x[1])
    nombres = [f[0] for f in filas]
    valores = [f[1] for f in filas]
    fig = go.Figure(go.Bar(
        x=valores, y=nombres, orientation="h",
        marker_color=["#16a34a" if v >= 0 else "#dc2626" for v in valores],
        hovertemplate="%{y}<br>%{x:,.0f} CLP<extra></extra>",
    ))
    fig.update_layout(title="Efecto económico de cada indicador (mes tipo)",
                      xaxis_title="CLP", height=420, showlegend=False,
                      margin=dict(l=60, r=30, t=60, b=50))
    return fig


# ---------------------------------------------------------------------------
# Construccion
# ---------------------------------------------------------------------------
print("Generando datos sinteticos...")
fr = generar_franjas()
k = calcular_kpis(fr)
DATOS.mkdir(exist_ok=True)
fr.to_csv(DATOS / "franjas.csv", index=False, encoding="utf-8")
pd.DataFrame([{"tipo_dia": t, "n_dias": n} for t, n in DIAS.items()]).to_csv(
    DATOS / "dias.csv", index=False, encoding="utf-8")
pd.DataFrame([{"parametro": p, "valor": v} for p, v in PARAMETROS.items()]).to_csv(
    DATOS / "parametros.csv", index=False, encoding="utf-8")
pd.DataFrame([{"indicador": n, "descripcion": d, "umbral": u, "simulado": v}
              for n, d, u, v in INDICADORES]).to_csv(
    DATOS / "indicadores.csv", index=False, encoding="utf-8")
print(f"  {len(fr):,} filas de programacion")

print("Generando figuras...")
figuras = [
    ("ingresos_dia", "Ingreso por día", fig_ingresos_por_dia(fr, k)),
    ("composicion", "Composición", fig_composicion(k)),
    ("flota", "Flota por hora", fig_flota(fr)),
    ("terminal", "Por terminal", fig_por_terminal(fr)),
    ("indicadores", "Indicadores", fig_indicadores(k)),
    ("impacto", "Impacto económico", fig_impacto(k)),
]

bloques = []
for i, (ident, titulo, fig) in enumerate(figuras):
    bloques.append({
        "id": ident, "titulo": titulo,
        "html": pio.to_html(fig, full_html=False,
                            include_plotlyjs=("cdn" if i == 0 else False),
                            div_id=f"g_{ident}", config={"responsive": True}),
    })

kp = [
    ("Km programados (mes)", f"{k['km_mes']:,.0f}"),
    ("Expediciones (mes)", f"{k['ep_mes']:,.0f}"),
    ("Plazas ofertadas (mes)", f"{k['plazas_mes'] / 1e6:,.1f} M"),
    ("Ingreso base (mes)", clp(k["ing_base"])),
    ("Descuento aplicado", f"{k['pct_ite'] * 100:.2f}%"),
    ("Pago neto estimado", clp(k["yt_neto"])),
]
tarjetas = "\n".join(
    f'<div class="kpi"><span class="valor">{v}</span><span class="etiqueta">{e}</span></div>'
    for e, v in kp)

botones = "\n".join(
    f'<button class="tab{" activo" if i == 0 else ""}" data-tab="{b["id"]}">{b["titulo"]}</button>'
    for i, b in enumerate(bloques))
paneles = "\n".join(
    f'<section id="tab-{b["id"]}" class="panel{" activo" if i == 0 else ""}">{b["html"]}</section>'
    for i, b in enumerate(bloques))

plantilla = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tablero operacional y económico — réplica en Python</title>
<style>
  :root {{ --fondo:#f8fafc; --tarjeta:#fff; --borde:#e2e8f0; --texto:#0f172a;
           --suave:#64748b; --acento:#1d4ed8; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding:0 0 3rem; background:var(--fondo); color:var(--texto);
          font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  header {{ background:var(--tarjeta); border-bottom:1px solid var(--borde);
            padding:1.75rem 2rem 1.25rem; }}
  h1 {{ margin:0 0 .35rem; font-size:1.55rem; font-weight:650; letter-spacing:-.01em; }}
  .sub {{ color:var(--suave); font-size:.92rem; margin:0 0 .9rem; }}
  .aviso {{ display:inline-block; background:#fff7ed; color:#9a3412; border:1px solid #fed7aa;
            border-radius:6px; padding:.35rem .7rem; font-size:.8rem; }}
  .kpis {{ display:flex; flex-wrap:wrap; gap:.75rem; margin-top:1.15rem; }}
  .kpi {{ background:var(--fondo); border:1px solid var(--borde); border-radius:8px;
          padding:.6rem .9rem; min-width:150px; }}
  .kpi .valor {{ display:block; font-size:1.15rem; font-weight:650; }}
  .kpi .etiqueta {{ display:block; font-size:.72rem; color:var(--suave);
                    text-transform:uppercase; letter-spacing:.04em; margin-top:.15rem; }}
  nav {{ display:flex; flex-wrap:wrap; gap:.4rem; padding:1rem 2rem .5rem; }}
  .tab {{ border:1px solid var(--borde); background:var(--tarjeta); color:var(--texto);
          padding:.5rem .95rem; border-radius:7px; font-size:.86rem; cursor:pointer; }}
  .tab.activo {{ background:var(--acento); border-color:var(--acento); color:#fff; font-weight:600; }}
  main {{ padding:0 2rem; }}
  .panel {{ display:none; background:var(--tarjeta); border:1px solid var(--borde);
            border-radius:10px; padding:.5rem; margin-top:.75rem; }}
  .panel.activo {{ display:block; }}
  footer {{ color:var(--suave); font-size:.8rem; padding:1.5rem 2rem 0; }}
  footer a {{ color:var(--acento); }}
</style>
</head>
<body>
<header>
  <h1>Tablero operacional y económico</h1>
  <p class="sub">Réplica en Python del modelo analítico del tablero original (Power BI).
     Mismo modelo de datos y mismas definiciones de cálculo.</p>
  <span class="aviso">Datos <strong>sintéticos</strong>: servicios, terminales, precios e
     indicadores son ficticios. No contiene información contractual.</span>
  <div class="kpis">{tarjetas}</div>
</header>
<nav>{botones}</nav>
<main>
{paneles}
</main>
<footer>
  Gráficos interactivos: zoom, desplazamiento y detalle al pasar el cursor.
  <br>Proyecto: <a href="https://github.com/luisalbertochavarria/dashboard-operacional-powerbi">
  dashboard-operacional-powerbi</a>.
</footer>
<script>
document.querySelectorAll('.tab').forEach(function (b) {{
  b.addEventListener('click', function () {{
    document.querySelectorAll('.tab').forEach(function (x) {{ x.classList.remove('activo'); }});
    document.querySelectorAll('.panel').forEach(function (p) {{ p.classList.remove('activo'); }});
    b.classList.add('activo');
    var panel = document.getElementById('tab-' + b.dataset.tab);
    if (panel) {{
      panel.classList.add('activo');
      panel.querySelectorAll('.js-plotly-plot').forEach(function (g) {{
        if (window.Plotly) {{ Plotly.Plots.resize(g); }}
      }});
    }}
  }});
}});
</script>
</body>
</html>
"""

DOCS.mkdir(exist_ok=True)
salida = DOCS / "index.html"
salida.write_text(plantilla, encoding="utf-8")
print(f"Listo: {salida}  ({salida.stat().st_size / 1_048_576:.2f} MB)")
print(f"Ingreso base (mes): {clp(k['ing_base'])}")
print(f"Descuento: {k['pct_ite']*100:.2f}%  ->  {clp(k['descuento'])}")
print(f"Pago neto: {clp(k['yt_neto'])}")