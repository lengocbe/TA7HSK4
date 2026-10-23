"""Append reviewed New HSK Course vocabulary, keeping previous IDs and fields intact."""
from pathlib import Path
import json,sys
from build_spoken_next import NEXT_PRON,pinyin
from build_spoken import PRON
from pypinyin import load_phrases_dict
from extract_hsk30 import FILES
ROOT=Path(__file__).resolve().parents[1]
LABELS={'1':'Cấp 1','2':'Cấp 2','3':'Cấp 3','4.1':'Cấp 4 · Tập 1','4.2':'Cấp 4 · Tập 2'}
def build():
 for t,pron in {**PRON,**NEXT_PRON}.items():
  if len(t)>1 and len(t)==len(pron.split()):load_phrases_dict({t:[[s] for s in pron.split()]})
 folder=ROOT/'content/hsk30';rows=json.loads((folder/'words.json').read_text(encoding='utf-8'));cat=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
 cat['words']=[w for w in cat['words'] if w.get('level')!='hsk30'];cat['lessons']=[l for l in cat['lessons'] if l.get('level')!='hsk30'];audit=[];counts={}
 for line in (folder/'lessons.tsv').read_text(encoding='utf-8').splitlines():
  book,n,start,title,vi=line.split('|');n=int(n);course='hsk30-'+book;prefix=book.replace('.','');label=LABELS[book]
  lesson=dict(id=f'zh30-{prefix}-u{n}',lang='zh',level='hsk30',course=course,kind='unit',number=n,short=f'HSK 3.0 · {label} · Bài {n:02}',title=title,description=vi,source=f'New HSK Course · {label} · Bài {n}',words=[])
  group=[r for r in rows if r['book']==book and r['lesson']==n];assert group,(book,n)
  for i,r in enumerate(group,1):
   assert r['text'] and r['meaning'],r
   id=f'zh30-{prefix}-{n:02}-{i:02}';source=lesson['source']+f' · Bảng từ vựng cuối sách · Trang PDF {r["page"]}'
   if r.get('extended'):source+=' · Từ mở rộng (*)'
   w=dict(id=id,lang='zh',level='hsk30',course=course,lesson=lesson['id'],bookNumber=i,text=r['text'],pron=r.get('pronOverride') or r.get('pron') or NEXT_PRON.get(r['text']) or PRON.get(r['text']) or pinyin(r['text']),meaning=r['meaning'],pos=r.get('pos','Từ / cụm từ'),example='',examplePron='',translation='',exampleKind='pending',exampleNote='Chưa có câu ví dụ cho mục này.',source=source,sourceFile=FILES[book],sourcePage=r['page'],examplePages=[],extended=bool(r.get('extended')),occurrences=[dict(file=FILES[book],page=r['page'])])
   if r.get('alternatives'):w['alternatives']=r['alternatives']
   if r['text'] in title and r['text']!=title:
    w.update(example=title,examplePron=pinyin(title),translation=vi,exampleKind='title',examplePages=[int(start)])
    w.pop('exampleNote',None)
   if r.get('speechText'):w['speechText']=r['speechText'];w['audioContext']='Giọng đọc trong cụm: '+r['speechText']
   cat['words'].append(w);lesson['words'].append(id);audit.append(dict(id=id,source=r))
  cat['lessons'].append(lesson);counts[f'{book}:{n}']=len(group)
 assert len(counts)==68
 cat['version']=9
 for path,obj in [(ROOT/'content/catalog.json',cat),(folder/'source-audit.json',audit),(folder/'counts.json',counts)]:path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(cat,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print('New HSK Course:',len(audit),'items,',len(counts),'lessons; total',len(cat['words']))
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');build()
