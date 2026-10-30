from pathlib import Path
from collections import defaultdict,Counter
import json,re
ROOT=Path(__file__).resolve().parents[1];folder=ROOT/'content/hsk5-intensive'
cat=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));known=defaultdict(Counter)
for w in cat['words']:
 if w['lang']=='zh':known[w['text']][w['meaning']]+=1
for w in json.loads((folder/'vocabulary-breakthrough-draft.json').read_text(encoding='utf-8'))['items']:
 if w['meaning']:known[w['text']][w['meaning']]+=100
splits={'哎喉一':['哎','唉'],'哎喉':['哎','唉'],'一烫逃':['烫','逃'],'拦烂':['拦','烂'],'才口楼':['人才','人口'],'届供':['届'],'滚锅':['滚','锅'],'退早':['迟早'],'保':['呆'],'哎唉':['哎','唉'],'趁称':['趁','称'],'丑臭':['丑','臭'],'醋催':['醋','催'],'钓顶':['钓','顶'],'断堆':['断','堆'],'冻洞':['冻','洞'],'吨蹲顿':['吨','蹲','顿'],'靠颗':['靠','颗'],'拍派':['拍','派'],'盆碰批披':['盆','碰','批','披'],'匹片':['匹','片'],'浅欠':['浅','欠'],'墙抢':['墙','抢'],'弱酒':['弱','洒'],'傻晒':['傻','晒'],'所锁':['所','锁'],'烫逃':['烫','逃'],'闻吻':['闻','吻'],'歇斜':['歇','斜'],'腰摇咬':['腰','摇','咬'],'旦律再':['一旦','一律','一再'],'摘窄':['摘','窄'],'挣支':['挣','支'],'撞追':['撞','追']}
for word,meaning in {'改正':'sửa lại cho đúng; sửa chữa','拐弯儿':'rẽ; ngoặt','桔子':'quýt','模特':'người mẫu'}.items():known[word][meaning]+=1000
original=json.loads((folder/'book-14-draft.json').read_text(encoding='utf-8'))['items']
records=[];counts={}
for p in sorted((ROOT/'tmp/hsk5-intensive/grid').glob('*.json')):
 d=json.loads(p.read_text(encoding='utf-8'));n=d['unit'];ws=[]
 if n==63:
  d['rows']=[dict(text=t,box=[],column=0) for t in ['文学','文字','闻','吻','稳定','问候','卧室','握手','屋子','无奈','无数','无所谓','武术','勿','物理','物质']]
 for r in d['rows']:
  t=r['text'].strip()
  for text in splits.get(t,[t]):
   if not re.fullmatch('[\u3400-\u9fff]{1,10}',text):continue
   word=dict(book='book-14',lesson=n,text=text,page=d['page'],raw=t,meaning=known[text].most_common(1)[0][0] if known[text] else '',reviewed=False,box=r['box'],column=r['column'])
   ws.append(word)
 expected=20 if n==81 else 16
 if len(ws)<expected:
  alternate=[]
  for old in original:
   if old['lesson']!=n:continue
   for t in splits.get(old['text'],[old['text']]):
    alternate.append(dict(old,text=t,meaning=known[t].most_common(1)[0][0] if known[t] else ''))
  if len(alternate)==expected and all(w['meaning'] for w in alternate):ws=alternate
 records.extend(ws);counts[n]=len(ws)
(folder/'book-14-grid-draft.json').write_text(json.dumps(dict(items=records,unitCounts=counts),ensure_ascii=False,indent=2),encoding='utf-8')
print('Items',len(records),'units',len(counts),'unexpected counts',{n:v for n,v in counts.items() if v!=(20 if n==81 else 16)})
print('Unknown',[(w['lesson'],w['text']) for w in records if not w['meaning']])
