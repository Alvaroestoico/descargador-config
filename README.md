# descargador-config

Configuración remota del Descargador (Android/iOS): `clients.json` lista los clientes de YouTube
que dan URLs directas (sin firma JS, sin cuenta, sin poToken obligatorio), copiados cada día de
[yt-dlp](https://github.com/yt-dlp/yt-dlp) por una GitHub Action. La app lo lee (caché 12 h) y,
si falla o no hay red, usa sus valores de fábrica. Solo contiene versiones de cliente: nada personal.
