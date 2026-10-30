"""Build reviewed Han and office vocabulary, preserving every legacy record."""
from pathlib import Path
import json,sys
from build_spoken_next import pinyin,NEXT_PRON
from build_spoken import PRON
from extract_han_office import FILES
ROOT=Path(__file__).resolve().parents[1]
def build():
 folder=ROOT/'content/han-office';rows=json.loads((folder/'words.json').read_text(encoding='utf-8'));lessons=json.loads((folder/'lessons.json').read_text(encoding='utf-8'))
 cat=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
 cat['words']=[w for w in cat['words'] if w.get('level') not in ('han','office')];cat['lessons']=[l for l in cat['lessons'] if l.get('level') not in ('han','office')]
 audit=[];counts={}
 for spec in lessons:
  book=spec['book'];n=spec['number'];office=book=='office';level='office' if office else 'han';course='office-standard' if office else 'han-'+book;prefix='zho' if office else 'zhh-'+book;label='Tiếng Trung công sở' if office else 'Hán ngữ · Quyển '+book
  l=dict(id=f'{prefix}-u{n}',lang='zh',level=level,course=course,kind='unit',number=n,short=f'{label} · Bài {n:02}',title=spec['title'],description=spec['description'],source=f'{label} · Bài {n}',words=[])
  group=[r for r in rows if r['book']==book and r['lesson']==n];assert group,(book,n)
  for i,r in enumerate(group,1):
   assert r['text'] and r['meaning'] and r['page']>0
   id=f'{prefix}-{n:02}-{i:03}';source=l['source']+f' · Trang PDF {r["page"]}'
   w=dict(id=id,lang='zh',level=level,course=course,lesson=l['id'],bookNumber=i,text=r['text'],pron=r.get('pron') or NEXT_PRON.get(r['text']) or PRON.get(r['text']) or pinyin(r['text']),meaning=r['meaning'],pos=r.get('pos','Từ / cụm từ'),example='',examplePron='',translation='',exampleKind='pending',exampleNote='Chưa có câu ví dụ cho mục này.',source=source,sourceFile=FILES[book],sourcePage=r['page'],examplePages=[],occurrences=[dict(file=FILES[book],page=r['page'])])
   for k in ['alternatives','speechText','audioContext']:
    if r.get(k):w[k]=r[k]
   cat['words'].append(w);l['words'].append(id);audit.append(dict(id=id,source=r))
  cat['lessons'].append(l);counts[f'{book}:{n}']=len(group)
 cat['version']=11
 for path,obj in [(ROOT/'content/catalog.json',cat),(folder/'source-audit.json',audit),(folder/'counts.json',counts)]:path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(cat,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print(len(audit),'new items;',len(counts),'lessons;',len(cat['words']),'total')
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');build()
