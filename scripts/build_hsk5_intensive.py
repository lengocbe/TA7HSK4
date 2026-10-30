"""Publish reviewed intensive vocabulary; fail closed on incomplete OCR/review.
Input is content/hsk5-intensive/reviewed.json. Never publish OCR drafts directly.
"""
from pathlib import Path
from hashlib import sha256
import json,sys
ROOT=Path(__file__).resolve().parents[1]
def merge(catalog,collection,books):
 assert collection.get('reviewComplete') is True,'Review has not been completed'
 source_by_id={b['id']:b for b in books};courses=collection['courses'];words=[];lessons=[]
 for course in courses:
  b=source_by_id[course['book']];assert b['category']=='vocabulary'
  assert course.get('coverageNote'),'Document source coverage before publishing'
  assert course.get('lessons'),'Empty course'
  for number,l in enumerate(course['lessons'],1):
   lid=f"zhi5-{b['id']}-u{number}";ids=[]
   assert l['title'] and l['words']
   for r in l['words']:
    assert r.get('reviewed') is True and all(r.get(k) for k in ['text','pron','meaning','page','raw'])
    assert 1<=r['page']<=b['pages']
    wid=lid+'-'+sha256(r['text'].encode()).hexdigest()[:12];assert wid not in ids
    ids.append(wid)
    word=dict(id=wid,lang='zh',level='intensive5',course=course['id'],lesson=lid,bookNumber=len(ids),text=r['text'],pron=r['pron'],meaning=r['meaning'],pos=r.get('pos','Từ / cụm từ'),example='',examplePron='',translation='',exampleKind='pending',exampleNote='Chưa có câu ví dụ cho mục này.',source=f"{b['title']} · {l['title']} · Trang PDF {r['page']}",sourceFile=b['file'],sourcePage=r['page'],examplePages=[],occurrences=[dict(file=b['file'],page=r['page'])])
    for k in ['speechText','audioContext']:
     if r.get(k):word[k]=r[k]
    words.append(word)
   lessons.append(dict(id=lid,lang='zh',level='intensive5',course=course['id'],courseTitle=course['title'],kind='unit',number=number,short=f"{course['title']} · {number:02}",title=l['title'],description=course['coverageNote'],source=b['title'],words=ids))
 old_words=[w for w in catalog['words'] if w.get('level')!='intensive5'];old_lessons=[l for l in catalog['lessons'] if l.get('level')!='intensive5']
 assert len({w['id'] for w in old_words+words})==len(old_words)+len(words)
 return dict(catalog,words=old_words+words,lessons=old_lessons+lessons)
def main():
 folder=ROOT/'content/hsk5-intensive';path=folder/'reviewed.json'
 if not path.exists():raise SystemExit('No reviewed.json: OCR drafts are not publishable')
 cat=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));result=merge(cat,json.loads(path.read_text(encoding='utf-8')),json.loads((folder/'books.json').read_text(encoding='utf-8')))
 (ROOT/'content/catalog.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(result,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print(len(result['words'])-len(cat['words']),'items added')
if __name__=='__main__':main()
