"""Extract draft headwords, retaining OCR evidence and unresolved rows for review.
Does not publish data or modify the app catalog.
"""
from pathlib import Path
from collections import Counter,defaultdict
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 folder=ROOT/'content/hsk5-intensive';cache=ROOT/'tmp/hsk5-intensive/ocr'
 known=defaultdict(Counter)
 catalog=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
 for w in catalog['words']:
  if w['lang']=='zh':known[w['text']][w['meaning']]+=1
 books=json.loads((folder/'books.json').read_text(encoding='utf-8'));book=next(b for b in books if b['id']=='book-19')
 correction_path=folder/'draft-corrections.json'
 corrections=json.loads(correction_path.read_text(encoding='utf-8')) if correction_path.exists() else {}
 records=[];issues=[];seen=set();pages=[]
 for path in sorted(cache.glob('book-19-*.json')):
  data=json.loads(path.read_text(encoding='utf-8'));pages.append(data['page'])
  for r in data['rows']:
   t=r['text'];m=re.match(r'^([\u3400-\u9fff]{1,10})\s*([A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùüǖǘǚǜ].*)$',t)
   if not m or 'HSK' in t or max(p[1] for p in r['box'])/data['height']<.07:continue
   word=m[1]
   fix=corrections.get(str(data['page'])+':'+word,corrections.get(word,{}))
   canonical=fix.get('text',word)
   if canonical in seen:issues.append(dict(reason='duplicate headword',text=word,page=data['page'],raw=t));continue
   seen.add(canonical)
   rec=dict(book='book-19',text=word,page=data['page'],raw=t,box=r['box'],confidence=r['confidence'],meaning=known[word].most_common(1)[0][0] if known[word] else '',reviewed=False)
   if fix:rec['originalText']=word;rec.update(fix)
   records.append(rec)
 manual_path=folder/'manual-headers.json'
 if manual_path.exists():records.extend(json.loads(manual_path.read_text(encoding='utf-8')))
 records.sort(key=lambda r:(r['page'],min(v[1] for v in r.get('box',[[0,0]]))))
 missing=[n for n in range(2,134) if n not in pages]
 result=dict(source=book,processedPages=pages,missingPages=missing,items=records,issues=issues)
 (folder/'vocabulary-breakthrough-draft.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(dict(items=len(records),missingMeanings=sum(not w['meaning'] for w in records),processedPages=len(pages),missingPages=len(missing),issues=len(issues))))
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');main()
