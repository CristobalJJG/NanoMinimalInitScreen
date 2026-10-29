# AGENTS.md

## Descripción del proyecto

`minimal_dashboard` es un dashboard estático de inicio, escrito con HTML, CSS y JavaScript sin frameworks ni sistema de build. Muestra un buscador de Google y una cuadrícula de accesos directos cargados desde `sites.json`.

## Estructura

- `dashboard.html`: página principal y marcado base.
- `script.js`: búsqueda y carga dinámica de sitios.
- `style.css`: tema visual, cuadrícula y responsive design.
- `sites.json`: configuración de los accesos directos (`name`, `url` y `photo`).
- `images/`: recursos gráficos locales, si se incorporan.
- `README.md`: instrucciones para servir el dashboard mediante `python3 -m http.server` y configurarlo como servicio systemd.

## Cómo ejecutar

El dashboard debe servirse mediante HTTP porque `script.js` usa `fetch('sites.json')`; abrir `dashboard.html` directamente con `file://` puede impedir la carga del JSON.

```bash
python3 -m http.server 8000
```

Después, abrir:

```text
http://localhost:8000/dashboard.html
```

El README también documenta una instalación como servicio systemd en `/opt/minimal-dashboard`.

## Convenciones de desarrollo

- Mantener la solución sencilla y sin dependencias externas salvo que exista una necesidad clara.
- Usar HTML semántico y conservar `lang="es"`.
- Mantener el código JavaScript compatible con navegadores modernos, sin transpilación.
- Escapar o construir de forma segura cualquier contenido que pase a la interfaz. Actualmente los sitios se insertan mediante `innerHTML`; si `sites.json` pasa a ser editable por terceros, sustituirlo por creación de nodos y `textContent`.
- Codificar las consultas con `encodeURIComponent` antes de construir la URL de Google.
- Mantener las entradas de `sites.json` como JSON válido y con los campos `name`, `url` y opcionalmente `photo`.
- Preferir rutas relativas para recursos propios. Las imágenes de favicon configuradas actualmente proceden de Google y requieren conexión de red.
- Preservar el diseño responsive, especialmente la cuadrícula de dos columnas en pantallas de hasta 600 px.

## Cambios habituales

### Añadir o modificar un acceso directo

Editar `sites.json`, sin añadir comentarios ni trailing commas:

```json
{
  "name": "Nombre visible",
  "url": "https://ejemplo.com",
  "photo": "https://www.google.com/s2/favicons?domain=ejemplo.com"
}
```

Si se omite `photo`, `script.js` usa una imagen placeholder remota.

### Cambiar el buscador

La lógica está en `handleSearch()` dentro de `script.js`. La función debe devolver `false` para evitar el envío tradicional del formulario y validar la consulta vacía antes de redirigir.

### Cambiar la apariencia

Editar `style.css`. Los colores principales están definidos como variables CSS en `:root`. No introducir estilos inline salvo que sea imprescindible.

## Verificación

No hay suite de tests automatizada ni `package.json`. Antes de entregar cambios:

1. Validar que `sites.json` sigue siendo JSON válido.
2. Servir el proyecto con `python3 -m http.server 8000`.
3. Comprobar en el navegador que se carga la cuadrícula y que cada enlace funciona.
4. Probar una búsqueda vacía y una búsqueda con caracteres especiales.
5. Revisar el comportamiento en una ventana estrecha, especialmente hasta 600 px.

Comprobación rápida del JSON:

```bash
python3 -m json.tool sites.json
```

## Restricciones y notas

- No hay backend, compilación, gestor de paquetes ni base de datos.
- El archivo que debe abrirse como página es `dashboard.html`.
- Los cambios en `README.md` pueden formar parte del estado de trabajo del usuario; no sobrescribir cambios no relacionados.
- No modificar archivos de `.git/`.
