"""Draft only: core-word explanations in Conquering New HSK5 Vocabulary.
Original level labels are retained; exercise choices are not vocabulary entries.
"""
from pathlib import Path
from collections import Counter,defaultdict
import json,re
ROOT=Path(__file__).resolve().parents[1];folder=ROOT/'content/hsk5-intensive';known=defaultdict(Counter)
for w in json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))['words']:
 if w['lang']=='zh':known[w['text']][w['meaning']]+=1
starts=[1,22,33,50,82,113,133,188,231,247,279,305,334,377,413,430,448,461,477,509,519,528,539,547]
titles=['Sức khỏe','Internet','Hẹn hò','Công việc','Giao thông','Câu chuyện tình cảm','Động vật và con người','Tài chính và kinh tế','Môi trường và phát triển','Các thành phố Trung Quốc','Tình yêu và hôn nhân','Thế giới đa dạng','Trăm vị cuộc sống','Giáo dục và cuộc sống học đường','Tâm lý thú vị','Du lịch','Thể thao','Giải trí','Du học Trung Quốc','Chuyện cười','Số và thành ngữ','Thần thoại Trung Quốc','Văn học cổ điển Trung Quốc','Câu chuyện triết lý']
records=[];pages=[]
for path in sorted((ROOT/'tmp/hsk5-intensive/ocr').glob('book-02-*.json')):
 d=json.loads(path.read_text(encoding='utf-8'));page=d['page']
 if page<11:continue
 pages.append(page);lesson=max(n+1 for n,start in enumerate(starts) if start+9<=page)
 for r in d['rows']:
  m=re.match(r'^\s*(\d{1,2})[.．、]\s*([\u3400-\u9fff…·一]+)[：:]\s*([1-6])\s*级',r['text'])
  if not m:continue
  text=m[2];records.append(dict(book='book-02',lesson=lesson,title=titles[lesson-1],number=int(m[1]),text=text,sourceLevel=int(m[3]),page=page,raw=r['text'],meaning=known[text].most_common(1)[0][0] if known[text] else '',reviewed=False,box=r['box']))
(folder/'book-02-draft.json').write_text(json.dumps(dict(items=records,processedPages=pages,missingPages=[n for n in range(11,571) if n not in pages]),ensure_ascii=False,indent=2),encoding='utf-8')
print('Conquering draft:',len(records),'core entries;',len(pages),'OCR pages;',sum(not w['meaning'] for w in records),'unresolved meanings')
