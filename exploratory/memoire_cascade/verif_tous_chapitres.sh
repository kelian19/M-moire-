#!/usr/bin/env bash
# Passe verif_chiffres.py sur TOUS les chapitres et resume en une ligne chacun.
# Equivalent macOS / Linux de verif_tous_chapitres.ps1, meme sortie, memes colonnes.
# Usage : bash verif_tous_chapitres.sh
#
# Les accents de la sortie Python ne survivent pas toujours au pipeline :
# la regex evite donc tout caractere accentue.

set -u

ICI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$ICI/../../.venv/bin/python"
OUT="$ICI/../../sorties_verif"

if [ ! -x "$PY" ]; then
  echo "Interpreteur introuvable : $PY" >&2
  echo "Creer l'environnement : python3 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 1
fi

tot=0
ok=0

printf '%-34s%8s%10s%9s\n' "chapitre" "verif." "confirmes" "taux"
printf '%.0s-' {1..61}; printf '\n'

for f in "$ICI"/chapitres/*.tex; do
  base="$(basename "$f" .tex)"
  r="$("$PY" "$ICI/verif_chiffres.py" "$OUT" "$f" 2>&1)"
  ligne="$(printf '%s\n' "$r" | grep -Eo '[0-9]+ nombres [^,]+, [0-9]+ confirm' | head -1)"
  if [ -n "$ligne" ]; then
    v="$(printf '%s' "$ligne" | awk '{print $1}')"
    c="$(printf '%s' "$ligne" | awk '{print $4}')"
    tot=$((tot + v))
    ok=$((ok + c))
    if [ "$v" -gt 0 ]; then
      taux="$(awk -v c="$c" -v v="$v" 'BEGIN{printf "%.1f %%", 100*c/v}')"
    else
      taux="n/a"
    fi
    printf '%-34s%8s%10s%9s\n' "$base" "$v" "$c" "$taux"
  else
    printf '%-34s%8s%10s%9s\n' "$base" "-" "-" "sans script"
  fi
done

printf '%.0s-' {1..61}; printf '\n'
if [ "$tot" -gt 0 ]; then
  printf '%-34s%8s%10s%9s\n' "TOTAL" "$tot" "$ok" \
    "$(awk -v c="$ok" -v v="$tot" 'BEGIN{printf "%.1f %%", 100*c/v}')"
fi
