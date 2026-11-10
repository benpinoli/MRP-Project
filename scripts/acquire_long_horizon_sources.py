"""Download bounded configured public issuer reports; BYU_ORC_AGENTS.md applies."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen
from datetime import datetime,timezone
import hashlib,json,argparse

def acquire(item,out):
 p=out/item['filename'];r=dict(item,retrieved_utc=datetime.now(timezone.utc).isoformat())
 try:
  if p.exists():raise FileExistsError('Refuse overwrite existing source')
  with urlopen(item['url'],timeout=45) as response:
   r['http_status']=response.status
   with p.open('xb') as f:
    for block in iter(lambda:response.read(1024*1024),b''):f.write(block)
  if not p.read_bytes()[:5]==b'%PDF-':raise ValueError('Response is not PDF')
  h=hashlib.sha256()
  with p.open('rb') as f:
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
  r.update(status='downloaded',bytes=p.stat().st_size,sha256=h.hexdigest(),local_path=str(p))
 except Exception as e:r.update(status='failed_no_retry',error=f'{type(e).__name__}: {e}')
 return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);a=ap.parse_args();cfg=json.loads(Path(a.config).read_text());out=Path(cfg['output_directory']);out.mkdir(parents=True,exist_ok=True)
 with ThreadPoolExecutor(max_workers=2) as pool: rows=list(pool.map(lambda x:acquire(x,out),cfg['sources']))
 manifest={'config':a.config,'created_utc':datetime.now(timezone.utc).isoformat(),'sources':rows,'policy':'No retries, auth/header manipulation, overwrite or publication; source timestamps unknown remain unknown.'}
 (out/'download_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'downloaded':sum(x['status']=='downloaded' for x in rows),'failed':[{k:x[k] for k in ['id','error']} for x in rows if x['status']!='downloaded'],'bytes':sum(x.get('bytes',0) for x in rows)}))
