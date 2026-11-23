#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quita auxiliares del repositorio del tablero y vuelve a publicar."""
import os
import subprocess
from pathlib import Path

REPO = Path(__file__).parent
ENV = Path(r"C:\Users\luis_\AppData\Local\hermes\.env")
LOGIN = "luisalbertochavarria"

token = None
for linea in ENV.read_text(encoding="utf-8", errors="replace").splitlines():
    if linea.strip().startswith("GITHUB_TOKEN="):
        token = linea.split("=", 1)[1].strip()
        break

env_git = dict(os.environ)
env_git["GIT_TERMINAL_PROMPT"] = "0"
env_git["GCM_INTERACTIVE"] = "never"


def git(args):
    r = subprocess.run(["git", "-c", "credential.helper="] + args, cwd=REPO,
                       capture_output=True, text=True, env=env_git, timeout=180)
    return r.returncode, (r.stdout + r.stderr).strip().replace(token, "<token>")


for nombre in ("publicar_replica.py", "pub.log"):
    git(["rm", "--cached", "--ignore-unmatch", nombre])
    f = REPO / nombre
    if f.exists():
        os.remove(f)
        print(f"{nombre} eliminado")

# regla para futuros auxiliares
gi = REPO / ".gitignore"
texto = gi.read_text(encoding="utf-8")
if "auxiliares locales" not in texto:
    texto += "\n# Auxiliares locales (no se publican)\npub.log\npublicar_replica.py\nverificar_replica.py\n"
    gi.write_text(texto, encoding="utf-8")
    print("regla agregada a .gitignore")

git(["add", "-A"])
code, out = git(["commit", "-m", "Excluir auxiliares locales del repositorio"])
print("commit:", out.splitlines()[0] if out else code)

url = f"https://{LOGIN}:{token}@github.com/{LOGIN}/dashboard-operacional-powerbi.git"
code, out = git(["push", url, "main:main"])
print("push:", "OK" if code == 0 else f"ERROR {out[:300]}")

code, out = git(["ls-files"])
archivos = out.splitlines()
print(f"\narchivos versionados: {len(archivos)}")
for a in archivos:
    print("   ", a)