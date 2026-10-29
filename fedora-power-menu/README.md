# Menú de sesión para Fedora

Aplicación GTK 4 + Python/PyGObject para apagar el equipo. La acción solicita confirmación antes de ejecutarse.

## Dependencias de desarrollo

En Fedora:

```bash
sudo dnf install python3-gobject gtk4 libadwaita python3-devel \
  libadwaita-devel gtk4-devel rpm-build rpmdevtools
```

## Ejecutar desde el código

```bash
python3 power_menu.py
```

## Reconstruir, reinstalar o actualizar

Este bloque reconstruye el paquete desde el código actual, elimina la versión instalada si existe y luego instala el RPM recién generado. Cópialo y ejecútalo completo desde cualquier carpeta. Ajusta `REPO_DIR` si el repositorio no está en `~/dashboard`.

```bash
set -e
REPO_DIR="$HOME/dashboard"
cd "$REPO_DIR"

mkdir -p "$HOME/rpmbuild"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

# Regenerar el tarball desde los archivos actuales, con el directorio raíz
# que espera %autosetup.
tar --exclude=.git --transform='s,^fedora-power-menu,fedora-power-menu-0.1.0,' \
  -czf "$HOME/rpmbuild/SOURCES/fedora-power-menu-0.1.0.tar.gz" -C . fedora-power-menu

# Evitar que quede disponible por error un RPM de una compilación anterior.
rm -f "$HOME"/rpmbuild/RPMS/noarch/fedora-power-menu-*.rpm
rpmbuild -ba fedora-power-menu/fedora-power-menu.spec

# Eliminar la instalación previa si existe.
if rpm -q fedora-power-menu >/dev/null 2>&1; then
  sudo dnf remove -y fedora-power-menu
fi

# Instalar exactamente el RPM recién construido.
RPM_FILE=$(find "$HOME/rpmbuild/RPMS/noarch" -maxdepth 1 -type f \
  -name 'fedora-power-menu-*.noarch.rpm' -print -quit)
test -n "$RPM_FILE"
sudo dnf install -y "$RPM_FILE"
rpm -q fedora-power-menu
```

No ejecutes `rpmbuild` con `sudo`: eso usa `/root/rpmbuild` en vez de `~/rpmbuild`. El bloque regenera el tarball cada vez para incluir los cambios recientes (por ejemplo, quitar Reiniciar y Cerrar sesión). Cierra cualquier instancia abierta antes de probar. La aplicación aparece como **Menú de sesión** en el menú de aplicaciones.

## Desinstalar

Para eliminar la aplicación:

```bash
sudo dnf remove -y fedora-power-menu
```

Si también instalaste el acceso directo en el escritorio, elimínalo con:

```bash
rm -f "${XDG_DESKTOP_DIR:-$HOME/Desktop}/com.example.FedoraPowerMenu.desktop"
```

## Crear un acceso directo en el escritorio

Después de instalar el RPM, puedes copiar el lanzador al escritorio con:

```bash
cd ~/dashboard/fedora-power-menu
./install-desktop-launcher.sh
```

El script detecta la carpeta configurada para el escritorio y copia allí `com.example.FedoraPowerMenu.desktop`. En GNOME, si el archivo aparece como documento de texto, haz clic derecho sobre él y selecciona **Permitir lanzamiento**.

Si el escritorio utiliza una carpeta distinta, puedes indicar su ubicación mediante `XDG_DESKTOP_DIR`:

```bash
XDG_DESKTOP_DIR="$HOME/Escritorio" ./install-desktop-launcher.sh
```

El acceso directo inicia el comando instalado `fedora-power-menu`; por eso es necesario instalar primero el RPM.

## Notas

- `systemctl poweroff` puede estar sujeto a las políticas de la sesión y del sistema.
- El paquete está orientado a Fedora Workstation con GNOME y depende de GTK 4, libadwaita y PyGObject del sistema.
- El dashboard web original permanece sin cambios.
