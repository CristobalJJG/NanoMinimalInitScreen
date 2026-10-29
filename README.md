Esto instala el gestor de Extensiones de GNOME, que permite instalar y administrar extensiones de GNOME Shell.
```
flatpak install flathub com.mattjakeman.ExtensionManager
```

Para el dashboard:
```bash
python3 --version
sudo dnf install python3
sudo nano /etc/systemd/system/minimal-dashboard.service
```
```bash
[Unit]
Description=Minimal Dashboard HTTP Server
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/opt/minimal-dashboard
ExecStart=/usr/bin/python3 -m http.server 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# Recargar systemd para detectar el nuevo servicio
sudo systemctl daemon-reload

# Habilitar el servicio para que inicie con el sistema
sudo systemctl enable minimal-dashboard.service

# Iniciar el servicio inmediatamente
sudo systemctl start minimal-dashboard.service

# Ver estado del servicio
sudo systemctl status minimal-dashboard.service

# Ver logs si hay problemas
sudo journalctl -u minimal-dashboard.service -f
```