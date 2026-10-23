"""Build the reviewed Boya courses without changing existing learning IDs."""
from pathlib import Path
import json,sys,hashlib
from build_spoken_next import pinyin,NEXT_PRON
from build_spoken import PRON
from pypinyin import load_phrases_dict
from extract_boya import FILES
ROOT=Path(__file__).resolve().parents[1]
LABELS={'1':'Sơ cấp · Tập 1','2':'Sơ cấp · Tập 2','3':'Trước trung cấp · Tập 1','4':'Trước trung cấp · Tập 2','5':'Cao cấp · Tập 1','6':'Cao cấp · Tập 2'}
PARTIAL='Dữ liệu một phần: file Boya cao cấp tập 2 có vùng chữ bị hỏng và thiếu chỉ mục cuối sách. Bài này chỉ gồm các mục đọc rõ từ bảng từ mới; chưa phải toàn bộ từ vựng của bài.'
def build():
 for t,pron in {**PRON,**NEXT_PRON}.items():
  if len(t)>1 and len(t)==len(pron.split()):load_phrases_dict({t:[[s] for s in pron.split()]})
 folder=ROOT/'content/boya';rows=json.loads((folder/'words.json').read_text(encoding='utf-8'));cat=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
 cat['words']=[w for w in cat['words'] if w.get('level')!='boya'];cat['lessons']=[l for l in cat['lessons'] if l.get('level')!='boya'];audit=[];counts={}
 for line in (folder/'lessons.tsv').read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  book,n,start,title,vi=line.split('|');n=int(n);label=LABELS[book];course='boya-'+book
  lesson=dict(id=f'zhb-{book}-u{n}',lang='zh',level='boya',course=course,kind='unit',number=n,short=f'Boya · {label} · Bài {n:02}',title=title,description=vi,source=f'Boya · {label} · Bài {n}',words=[])
  if book=='6':lesson.update(notice=PARTIAL,partial=True)
  group=[r for r in rows if r['book']==book and r['lesson']==n];assert group,(book,n)
  for i,r in enumerate(group,1):
   assert r['text'] and r['meaning'],r
   id=f'zhb-{book}-{n:02}-{i:03}';source=lesson['source']+(' · Bảng từ mới' if book=='6' else ' · Chỉ mục từ vựng')+f' · Trang PDF {r["page"]}'
   pron=r.get('pron') or NEXT_PRON.get(r['text']) or PRON.get(r['text']) or pinyin(r['text'])
   w=dict(id=id,lang='zh',level='boya',course=course,lesson=lesson['id'],bookNumber=i,text=r['text'],pron=pron,meaning=r['meaning'],pos=r.get('pos','Từ / cụm từ'),example='',examplePron='',translation='',exampleKind='pending',exampleNote='Chưa có câu ví dụ cho mục này.',source=source,sourceFile=FILES[book],sourcePage=r['page'],examplePages=[],occurrences=[dict(file=FILES[book],page=r['page'])])
   if r.get('alternatives'):w['alternatives']=r['alternatives']
   if r.get('speechText'):w['speechText']=r['speechText'];w['audioContext']='Giọng đọc trong cụm: '+r['speechText']
   cat['words'].append(w);lesson['words'].append(id);audit.append(dict(id=id,source=r))
  cat['lessons'].append(lesson);counts[f'{book}:{n}']=len(group)
 assert len(counts)==107
 cat['version']=10
 for path,obj in [(ROOT/'content/catalog.json',cat),(folder/'source-audit.json',audit),(folder/'counts.json',counts)]:path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(cat,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print('Boya:',len(audit),'items,',len(counts),'lessons; total',len(cat['words']))
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');build()
