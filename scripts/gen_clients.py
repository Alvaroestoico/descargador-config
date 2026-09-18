"""Genera clients.json: clientes de YouTube que dan URLs DIRECTAS (sin firma JS, sin cuenta,
sin poToken obligatorio), copiados de yt-dlp. El Descargador los lee para arreglarse solo."""
import json, sys, datetime
import yt_dlp
from yt_dlp.extractor.youtube._base import INNERTUBE_CLIENTS
from yt_dlp.extractor.youtube._video import YoutubeIE

def usable(cfg):
    if cfg.get('REQUIRE_JS_PLAYER', True) or cfg.get('REQUIRE_AUTH', False):
        return False
    if getattr(cfg.get('PLAYER_PO_TOKEN_POLICY'), 'required', False):
        return False
    gvs = cfg.get('GVS_PO_TOKEN_POLICY', {})
    return not any(getattr(p, 'required', False) for p in gvs.values())

def entry(key, cfg):
    c = cfg['INNERTUBE_CONTEXT']['client']
    return {
        'key': key,
        'clientName': c['clientName'],
        'clientVersion': c['clientVersion'],
        'clientNameId': cfg['INNERTUBE_CONTEXT_CLIENT_NAME'],
        'userAgent': c.get('userAgent', ''),
        'host': cfg.get('INNERTUBE_HOST', 'www.youtube.com'),
        # Resto de campos del contexto (deviceMake/Model, osName/Version, androidSdkVersion…)
        'extra': {k: v for k, v in c.items() if k not in ('clientName', 'clientVersion', 'userAgent', 'hl', 'gl')},
    }

default = [k for k in YoutubeIE._DEFAULT_CLIENTS if k in INNERTUBE_CLIENTS]
keys = default + sorted(k for k in INNERTUBE_CLIENTS if k not in default)
clients = [entry(k, INNERTUBE_CLIENTS[k]) for k in keys if usable(INNERTUBE_CLIENTS[k])]
if not clients:
    sys.exit('ningún cliente directo: no se toca clients.json')
out = {
    'schema': 1,
    'ytdlp': yt_dlp.version.__version__,
    'generated': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'),
    'clients': clients,
}
print(json.dumps(out, indent=2, ensure_ascii=False))
