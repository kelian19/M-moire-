#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_garde_sorties.py : le garde-fou du support de soutenance fait-il son travail ?

POURQUOI CE FICHIER EXISTE. Les graphiques et les tableaux construits du support
lisent leurs nombres dans sorties_verif/, et chaque lecture est controlee contre
la valeur que le memoire publie. Un controle qui passe a vide est le pire defaut
possible, parce qu'il rassure : le projet en a deja connu deux, le grep sur
« undefined » dans la sortie de tectonic, et la ligne de sources posee avant la
premiere section. Celui-ci est donc TESTE, pas suppose.

ET LE TEST A SERVI DES LE PREMIER JOUR. La tolerance avait ete recopiee sous la
forme max(0,6 % ; 0,5), avec un plancher absolu : elle acceptait un indice de
queue lu a 0,5954 pour une valeur attendue de 0,62. C'est exactement le defaut
que le harnais du memoire avait corrige en aout, reproduit a l'identique. Sans ce
fichier il serait passe.

Lancement, depuis exploratory/slides/ :
    ..\\..\\.venv\\Scripts\\python.exe test_garde_sorties.py
"""

import importlib.util
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "build_soutenance_ppt", os.path.join(ICI, "build_soutenance_ppt.py"))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

XI = r"indice de queue xi\s+([\d.]+)\s*$"
EXCES = r"exces au-dessus du seuil\s+(\d+)\s*$"
SEUIL = r"seuil POT u \(percentile 85\)\s+([\d.]+) M EUR"
CANAL = r"^\s*frequence\s+(\d+)\s*\+-(\d+)\s+(\d+)\s*\+-(\d+)\s+(\d+)\s*\+-(\d+)"

# (libelle, script, motif, valeurs annoncees, le garde-fou doit-il refuser)
CAS = [
    ("derive sur une petite valeur : 0,5954 lu, 0,62 annonce",
     63, XI, (0.62,), True),
    ("derive sur un entier : 91 lu, 140 annonce",
     63, EXCES, (140,), True),
    ("derive d'une seule unite sur un entier : 91 lu, 92 annonce",
     63, EXCES, (92,), True),
    ("motif introuvable dans la sortie",
     68, r"^\s*canal_inexistant\s+(\d+)", (1,), True),
    ("mauvais nombre de valeurs capturees",
     68, CANAL, (4328, 463), True),
    ("valeur publiee : doit passer",
     63, XI, (0.5954,), False),
    ("arrondi legitime d'ecriture : doit passer",
     63, SEUIL, (20.03,), False),
    ("les six valeurs d'un canal : doivent passer",
     68, CANAL, (4328, 463, 8775, 1004, 6546, 457), False),
]


def principal():
    bons = 0
    for libelle, numero, motif, annonces, doit_refuser in CAS:
        try:
            b.extraire(numero, motif, annonces)
            refuse = False
        except SystemExit:
            refuse = True
        bon = refuse == doit_refuser
        bons += bon
        print(("  ok   " if bon else "ECHEC  ")
              + ("refuse   " if refuse else "accepte  ") + libelle)
    print(f"\n{bons} / {len(CAS)} controles du garde-fou")
    return 0 if bons == len(CAS) else 1


if __name__ == "__main__":
    sys.exit(principal())
