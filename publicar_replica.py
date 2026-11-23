#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Publica la replica del tablero: commit, push y activacion de Pages."""
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).parent
ENV = Path(r"C:\Users\luis_\AppData\Local\hermes\.env")
LOGIN = "luisalbertochavarria"
NOMBRE_REPO = "dashboard-operacional-powerbi"

token = None
for linea in ENV.read_text(encoding="utf-8", errors="replace").splitlines():
    if linea.strip().startswith("GITHUB_TOKEN="):
        token = linea.split("=", 1)[1].strip()
        break


def api(metodo, ruta, cuerpo=None):
    datos = json.dumps(cuerpo).encode() if cuerpo else None
    req = urllib.request.Request("https://api.github.com" + ruta, data=datos, method=metodo)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "hermes")
    if datos:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {}


env_git = dict(os.environ)
env_git["GIT_TERMINAL_PROMPT"] = "0"
env_git["GCM_INTERACTIVE"] = "never"


def git(args):
    r = subprocess.run(["git", "-c", "credential.helper="] + args, cwd=REPO,
                       capture_output=True, text=True, env=env_git, timeout=180)
    return r.returncode, (r.stdout + r.stderr).strip().replace(token, "<token>")


# limpiar herramienta de verificacion
f = REPO / "verificar_replica.py"
if f.exists():
    os.remove(f)
    print("verificar_replica.py eliminado")

git(["add", "-A"])
code, out = git(["status", "--short"])
print("archivos a subir:", len([l for l in out.splitlines() if l.strip()]))
for l in out.splitlines()[:15]:
    print("   ", l)

code, out = git(["commit", "-m",
                 "Agregar replica interactiva del tablero con datos sinteticos"])
print("commit:", out.splitlines()[0] if out else code)

url = f"https://{LOGIN}:{token}@github.com/{LOGIN}/{NOMBRE_REPO}.git"
code, out = git(["push", url, "main:main"])
print("push:", "OK" if code == 0 else f"ERROR {out[:300]}")

# Pages desde /docs
codigo, resp = api("POST", f"/repos/{LOGIN}/{NOMBRE_REPO}/pages",
                   {"source": {"branch": "main", "path": "/docs"}})
if codigo == 201:
    print("Pages activado:", resp.get("html_url"))
elif codigo == 409:
    print("Pages ya estaba activado")
else:
    print(f"Pages: {codigo} {resp.get('message')}")

print("\nesperando publicacion...")
for i in range(20):
    time.sleep(10)
    c, d = api("GET", f"/repos/{LOGIN}/{NOMBRE_REPO}/pages")
    print(f"  intento {i+1}: {d.get('status')}")
    if d.get("status") == "built":
        print("LISTO:", d.get("html_url"))
        break