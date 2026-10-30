"""Build reviewed Global Success grade 6, 8, 9 glossaries; preserve old IDs."""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
TITLES={6:['My New School','My House','My Friends','My Neighbourhood','Natural Wonders of Viet Nam','Our Tet Holiday','Television','Sports and Games','Cities of the World','Our Houses in the Future','Our Greener World','Robots'],8:['Leisure Time','Life in the Countryside','Teenagers','Ethnic Groups of Viet Nam','Our Customs and Traditions','Lifestyles','Environmental Protection','Shopping','Natural Disasters','Communication in the Future','Science and Technology','Life on Other Planets'],9:['Local Community','City Life','Healthy Living for Teens','Remembering the Past','Our Experiences','Vietnamese Lifestyle: Then and Now','Natural Wonders of the World','Tourism','World Englishes','Planet Earth','Electronic Devices','Career Choices']}
FIX={'recydle':'recycle','musde':'muscle','lanterm':'lantern','inahumy':'inahurry','stomm':'storm','wam':'warn','camierpigeon':'carrierpigeon','briliant':'brilliant','thrlling':'thrilling'}
def norm(t):
 t=re.sub('[^a-z]','',t.lower());return FIX.get(t,t)
def build():
 folder=ROOT/'content/english-grades';raw=json.loads((folder/'glossary-draft.json').read_text(encoding='utf-8'));cat=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));cat['words']=[w for w in cat['words'] if w.get('grade') not in [6,8,9]];cat['lessons']=[l for l in cat['lessons'] if l.get('grade') not in [6,8,9]];audit=[];counts={}
 for grade in [6,8,9]:
  records=[]
  for line in (folder/f'grade{grade}.tsv').read_text(encoding='utf-8-sig').splitlines():
   if line and not line.startswith('#'):
    unit,text,pron,meaning=line.split('|');records.append(dict(unit=int(unit),text=text,pron=pron,meaning=meaning))
  lessons=[]
  for n,title in enumerate(TITLES[grade],1):
   l=dict(id=f'en{grade}-u{n}',lang='en',grade=grade,course=f'en-{grade}',kind='unit',number=n,short=f'Lớp {grade} · Unit {n}',title=title,description='Từ trọng tâm theo Glossary trong sách. Chưa bổ sung câu ví dụ cho mục mới.',source=f'Tiếng Anh {grade} Global Success · Glossary',words=[])
   group=[r for r in records if r['unit']==n];assert group
   assert len({r['text'].lower() for r in group})==len(group)
   source=[r for r in raw if r['grade']==grade and r['unit']==n]
   for i,r in enumerate(group,1):
    key=norm(r['text']);matches=[s for s in source if norm(s['text'])==key]
    if not matches:matches=[s for s in source if len(norm(s['text']))>=3 and (norm(s['text']) in key or key in norm(s['text']))]
    assert matches,(grade,n,r['text'])
    evidence=matches[0];wid=f'en{grade}-{n:02}-{i:02}';posmatch=re.search(r'\(([^)]+)\)',evidence['raw']);pos=posmatch[1] if posmatch and len(posmatch[1])<12 else 'Từ / cụm từ'
    w=dict(id=wid,lang='en',grade=grade,course=f'en-{grade}',lesson=l['id'],text=r['text'],pron='/'+r['pron']+'/',pos=pos,meaning=r['meaning'],example='',translation='',exampleKind='pending',exampleNote='Chưa có câu ví dụ cho mục này.',source=f'Tiếng Anh {grade} Global Success · Unit {n} · Glossary · Trang PDF {evidence["page"]}',sourceFile=evidence['file'],sourcePage=evidence['page'])
    w['pos']={'adi':'adj','adij':'adj','adj.':'adj','n.':'n','v.':'v'}.get(w['pos'],w['pos'])
    if r['text'] in ['live','permit','estimate']:
     spoken={'live':'live broadcast','permit':'to permit','estimate':'to estimate'}[r['text']];w.update(speechText=spoken,audioContext=f'Giọng đọc dùng cụm “{spoken}” để làm rõ cách phát âm.')
    cat['words'].append(w);l['words'].append(wid);audit.append(dict(id=wid,source=evidence,reviewed=r))
   cat['lessons'].append(l);lessons.append(l);counts[f'{grade}:{n}']=len(group)
  for n in range(1,5):
   ids=[wid for l in lessons[(n-1)*3:n*3] for wid in l['words']]
   cat['lessons'].append(dict(id=f'en{grade}-r{n}',lang='en',grade=grade,course=f'en-{grade}',kind='review',number=n,short=f'Lớp {grade} · Review {n}',title=f'Ôn tập Unit {(n-1)*3+1}–{n*3}',description='Ôn từ của ba Unit; dùng chung tiến độ với bài gốc.',source=f'Tiếng Anh {grade} Global Success',words=ids,symbol='↻'))
 cat['version']=13
 (ROOT/'content/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2),encoding='utf-8');(ROOT/'www/data.js').write_text('const DATA = '+json.dumps(cat,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 for name,obj in [('source-audit.json',audit),('counts.json',counts)]: (folder/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Added',len(audit),'words; total',len(cat['words']),'words in',len(cat['lessons']),'lesson views')
if __name__=='__main__':build()
