"""Read the existing local credential without copying it; never print secrets."""
import json, urllib.request, urllib.error
from pathlib import Path
p=Path('/Users/dukefengyu/Codex/FTEC5660-HW2-main/.env')
values={k.strip():v.strip().strip('\"\'') for line in p.read_text().splitlines() if '=' in line and not line.strip().startswith('#') for k,v in [line.split('=',1)]}
key=values['DEEPSEEK_API_KEY']
base=values.get('DEEPSEEK_BASE_URL','https://api.deepseek.com')
req=urllib.request.Request(base.rstrip('/')+'/models',headers={'Authorization':'Bearer '+key})
try:
 with urllib.request.urlopen(req,timeout=30) as r: data=json.load(r)
 print(json.dumps({'status':'ok','models':[x['id'] for x in data.get('data',[])]}))
except urllib.error.HTTPError as e: print(json.dumps({'status':'http_error','code':e.code}))
except Exception as e: print(json.dumps({'status':'connection_error','type':type(e).__name__}))
