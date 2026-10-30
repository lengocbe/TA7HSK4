"""Draft glossary rows; retain raw OCR fields for manual IPA/meaning review."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'content/english-grades';out.mkdir(exist_ok=True);records=[]
for book,pages in {1:[71,72],2:[72,73],3:[137,138,139,140],4:[138,139,140,141]}.items():
 unit=0;grade={1:6,2:6,3:8,4:9}[book]
 for page in pages:
  p=ROOT/f'tmp/english-grades/ocr/{book}-{page}.json'
  if not p.exists():continue
  data=json.loads(p.read_text(encoding='utf-8'));rows=[]
  for r in data['rows']:
   xs=[v[0]/data['width'] for v in r['box']];ys=[v[1]/data['height'] for v in r['box']];rows.append(dict(t=r['text'],x=min(xs),y=sum(ys)/4,box=r['box']))
  for left,right in [(0,.5),(.5,1)]:
   heads=sorted([r for r in rows if left+(.005 if left else .075)<r['x']<left+(.11 if left else .24) and .07<r['y']<.93 and re.match(r'^[A-Za-z]',r['t'])],key=lambda r:r['y'])
   for i,r in enumerate(heads):
    m=re.match(r'Unit\s*(\d+)',r['t'],re.I)
    if m:unit=int(m[1]);continue
    if not unit:continue
    end=heads[i+1]['y'] if i+1<len(heads) else r['y']+.03
    near=[v for v in rows if left<v['x']<right and r['y']-.009<v['y']<end-.008 and v is not r]
    text=re.split(r'\s*\(',r['t'])[0].strip()
    records.append(dict(grade=grade,book=book,unit=unit,text=text,raw=r['t']+' | '+' | '.join(v['t'] for v in near),page=page,file=data['file'],reviewed=False))
(out/'glossary-draft.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
from collections import Counter
print('Counts',dict(Counter((r['grade'],r['unit']) for r in records)))
(ROOT/'tmp/english-grades/rows.txt').write_text('\n'.join(f"{r['grade']}:{r['unit']}:{r['text']} | {r['raw']}" for r in records),encoding='utf-8')
