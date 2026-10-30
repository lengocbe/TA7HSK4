"""Extract the numbered Level-5 index without mixing the Level-4 list."""
from pathlib import Path
from collections import Counter,defaultdict
import re,json
ROOT=Path(__file__).resolve().parents[1];folder=ROOT/'content/hsk5-intensive';known=defaultdict(Counter)
for w in json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))['words']:
 if w['lang']=='zh':known[w['text']][w['meaning']]+=1
records=[];processed=[]
for path in sorted((ROOT/'tmp/hsk5-intensive/ocr').glob('book-17-*.json')):
 d=json.loads(path.read_text(encoding='utf-8'));processed.append(d['page'])
 for r in d['rows']:
  m=re.match(r'^(\d{1,4})[.．、\s]+([\u3400-\u9fff]+)(.*)$',r['text'])
  if not m or not 1<=int(m[1])<=1300:continue
  number=int(m[1]);word=m[2];records.append(dict(book='book-17',number=number,text=word,lesson=(number-1)//50+1,page=d['page'],raw=r['text'],box=r['box'],meaning=known[word].most_common(1)[0][0] if known[word] else '',reviewed=False))
for number,text,page,raw in [(330,'工厂',37,'330.I厂 · gongchang'),(1119,'一旦',51,'1119.—旦 · yidan'),(1292,'祖先',54,'1292. | 祖先 | zuxian | 626'),(1299,'作为',54,'1299. | 作为 | zuowei | 627')]:
 if not any(r['number']==number for r in records):records.append(dict(book='book-17',number=number,text=text,lesson=(number-1)//50+1,page=page,raw=raw,meaning=known[text].most_common(1)[0][0] if known[text] else '',reviewed=False))
records.sort(key=lambda r:r['number'])
c=Counter(w['number'] for w in records)
result=dict(items=records,processedPages=processed,missingNumbers=[n for n in range(1,1301) if n not in c],duplicateNumbers=[n for n,v in c.items() if v>1])
(folder/'book-17-draft.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Dictionary draft:',len(records),'entries;',len(processed),'pages;',len(result['missingNumbers']),'missing numbers;',len(result['duplicateNumbers']),'duplicates')
