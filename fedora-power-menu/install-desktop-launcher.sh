#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_DIR="${XDG_DESKTOP_DIR:-$HOME/Desktop}"
LAUNCHER="$DESKTOP_DIR/com.example.FedoraPowerMenu.desktop"

if ! command -v fedora-power-menu >/dev/null 2>&1; then
  echo "No se encuentra el comando fedora-power-menu." >&2
  echo "Instala primero el RPM descrito en README.md y vuelve a ejecutar este script." >&2
  exit 1
fi

mkdir -p "$DESKTOP_DIR"
install -m 0755 "$SOURCE_DIR/com.example.FedoraPowerMenu.desktop" "$LAUNCHER"

# GNOME exige que el lanzador de escritorio esté marcado como confiable.
if command -v gio >/dev/null 2>&1; then
  gio set "$LAUNCHER" metadata::trusted true || true
fi

echo "Lanzador instalado en: $LAUNCHER"
echo "Si GNOME todavía lo bloquea, haz clic derecho y selecciona 'Permitir lanzamiento'."
