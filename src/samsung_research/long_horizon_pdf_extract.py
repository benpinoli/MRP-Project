"""Extract page-indexed issuer PDF text for manual verification; see BYU_ORC_AGENTS.md."""
import argparse,hashlib,json,os
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(os.environ['SAMSUNG_REPO'])

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def render_pages(pages):
    """PDF page number is 1-based; record failed page extraction, never hide gaps."""
    for index,page in enumerate(pages,1):
        try:text=page.extract_text() or '';error=None
        except Exception as exc:text='';error=f'{type(exc).__name__}: {exc}'
        yield index,text,error

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',required=True);ap.add_argument('--run',required=True);a=ap.parse_args();manifest_path=Path(a.manifest);manifest=json.loads(manifest_path.read_text());files=manifest['sources']
    for item in files:
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('source hash mismatch '+item['path'])
    run=Path(a.run);run.mkdir(parents=True,exist_ok=False);index=[];seen=set()
    for item in files:
        label=str(item['id'])
        if label in seen or not label.replace('_','').replace('-','').isalnum():raise ValueError('invalid/duplicate id')
        seen.add(label);source=ROOT/item['path'];reader=PdfReader(source);out=run/(label+'.txt');errors=[];empty=[]
        with out.open('w',encoding='utf-8',buffering=1024*1024) as f:
            for page,text,error in render_pages(reader.pages):
                f.write(f'\n\n===== PDF PAGE {page} =====\n\n');f.write(text)
                if error:errors.append({'page':page,'error':error})
                elif not text.strip():empty.append(page)
        index.append({'id':label,'source_path':item['path'],'source_sha256':item['sha256'],'page_count':len(reader.pages),'text_path':out.name,'text_sha256':digest(out),'empty_pages':empty,'page_errors':errors})
    for item in files:
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('source changed '+item['path'])
    (run/'index.json').write_text(json.dumps({'manifest_sha256':digest(manifest_path),'code_sha256':digest(__file__),'scope':'Machine-extracted text only; page-level human verification required; no automatic numeric claims','documents':index},indent=2)+'\n')
    if any(r['page_errors'] for r in index):raise RuntimeError('some pages failed; inspect index.json')
if __name__=='__main__':main()
