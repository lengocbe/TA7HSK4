from pathlib import Path
import json,re
from collections import Counter,defaultdict
root=Path('tmp/hsk5-intensive/ocr');out=Path('content/hsk5-intensive');cat=json.loads(Path('content/catalog.json').read_text(encoding='utf-8'));known=defaultdict(Counter)
for w in cat['words']:
 if w['lang']=='zh':known[w['text']][w['meaning']]+=1
for w in json.loads((out/'vocabulary-breakthrough-draft.json').read_text(encoding='utf-8'))['items']:
 if w['meaning']:known[w['text']][w['meaning']]+=100
for b in ['book-14','book-08']:
 records=[];issues=[];pages=[]
 for p in sorted(root.glob(b+'-*.json')):
  d=json.loads(p.read_text(encoding='utf-8'));pages.append(d['page'])
  for r in d['rows']:
   t=r['text'].strip();x=min(v[0] for v in r['box'])/d['width'];y=min(v[1] for v in r['box'])/d['height']
   if b=='book-14':
    if not (.22<x<.8 and y>.55) or not re.fullmatch('[\u3400-\u9fff一—]{1,10}',t):continue
    words=['哎','唉'] if d['page']==9 and t=='哎喉一' else [t]
    lesson=(d['page']-9)//4+1
    for word in words:records.append(dict(book=b,lesson=lesson,text=word,page=d['page'],raw=t,box=r['box'],meaning=known[word].most_common(1)[0][0] if known[word] else '',reviewed=False))
   else:
    m=re.match(r'^(\d{1,4})[.．、\s]+(.*)$',t)
    if not m:continue
    n=int(m[1]);word=m[2].strip()
    if not 1<=n<=2500 or not re.search('[\u3400-\u9fff]',word):continue
    records.append(dict(book=b,number=n,lesson=(n-1)//50+1,text=word,page=d['page'],raw=t,box=r['box'],meaning=known[word].most_common(1)[0][0] if known[word] else '',reviewed=False))
 result=dict(items=records,processedPages=pages,issues=issues)
 (out/f'{b}-draft.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(b,len(records),'missing',sum(not r['meaning'] for r in records),'lessons',dict(Counter(r['lesson'] for r in records)))
 print('UNKNOWN',[(r.get('lesson'),r['text']) for r in records if not r['meaning']][:100])
