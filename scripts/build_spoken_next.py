"""Add four reviewed spoken courses while preserving every previous item."""
from pathlib import Path
import json,sys
from build_spoken import pinyin as base_pinyin,PRON,POS
from pypinyin import load_phrases_dict
ROOT=Path(__file__).resolve().parents[1]
BOOKS={
'basic-upper':('bu','Cơ sở · Tập trên','03.汉语口语速成基础篇上.pdf'),
'basic-lower':('bl','Cơ sở · Tập dưới','04_汉语口语速成基础篇下_c9f31dd8e7417dadc638df1bc09ce6fe.pdf'),
'intermediate':('i','Trung cấp','05_汉语口语速成中级篇_f6692daf032fa0179916f68392ff07ce.pdf'),
'advanced':('a','Nâng cao · 提高篇','06_汉语口语速成提高篇_50896ca734943a56de0d741f5c71947e.pdf')}
NEXT_PRON={
 '尽快':'jǐn kuài','尽量':'jǐn liàng','尽管':'jǐn guǎn','尽力':'jìn lì','来着':'lái zhe',
 '会计':'kuài jì','正当':'zhèng dàng','和稀泥':'huò xī ní','深恶痛绝':'shēn wù tòng jué',
 '强迫':'qiǎng pò','宁可':'nìng kě','骨折':'gǔ zhé','熨斗':'yùn dǒu','咣当':'guāng dāng',
 '噼啪':'pī pā','笸箩':'pǒ luo','无影无踪':'wú yǐng wú zōng','着实':'zhuó shí',
 '当晚':'dàng wǎn','还清':'huán qīng','偿还':'cháng huán','系':'jì',
 '好好':'hǎo hāo','一觉':'yí jiào','好觉':'hǎo jiào','睡不着':'shuì bu zháo',
 '我得':'wǒ děi','说得':'shuō de','起得来':'qǐ de lái','打得':'dǎ de',
 '吵得':'chǎo de','想得':'xiǎng de','做得':'zuò de','好得多':'hǎo de duō',
 '得回去':'děi huí qu','说说':'shuō shuo','看看':'kàn kan','试试':'shì shi',
 '活儿':'huór','摊儿':'tānr','插花儿':'chā huār','人缘儿':'rén yuánr','滋味儿':'zī wèir',
 '口味儿':'kǒu wèir','名牌儿':'míng páir','纳闷儿':'nà mènr','小心眼儿':'xiǎo xīn yǎnr',
 '一……就……':'yī … jiù …','越……越……':'yuè … yuè …',
 '不但……而且……':'bú dàn … ér qiě …','非……不可':'fēi … bù kě',
 '一来……二来……':'yī lái … èr lái …','以……为生':'yǐ … wéi shēng',
 '处理':'chǔ lǐ','教你':'jiāo nǐ','以不变应万变':'yǐ bù biàn yìng wàn biàn',
 '商量':'shāng liang','主意':'zhǔ yi','师傅':'shī fu','麻烦':'má fan',
 '一趟':'yí tàng','一条':'yì tiáo','一年':'yì nián','一家':'yì jiā','一份':'yí fèn',
 '一部':'yí bù','一辈子':'yí bèi zi','一分':'yì fēn','讲讲':'jiǎng jiang',
 '这下儿':'zhè xiàr','慢慢儿':'màn mānr','甜味儿':'tián wèir'}

def pinyin(text):
 result=base_pinyin(text)
 for before,after in {'wán ér':'wánr','wèi ér':'wèir','wèi er':'wèir','shì ér':'shìr','diǎn er':'diǎnr','xiǎng xiǎng':'xiǎng xiang','jué dé':'jué de','chù lǐ':'chǔ lǐ','màn màn ér':'màn mānr','zhè xià ér':'zhè xiàr','yì sī':'yì si'}.items():result=result.replace(before,after)
 return result
def build():
 for t,pron in {**PRON,**NEXT_PRON}.items():
  if len(t)>1 and len(t)==len(pron.split()):load_phrases_dict({t:[[s] for s in pron.split()]})
 folder=ROOT/'content/spoken-next';rows=json.loads((folder/'words.json').read_text(encoding='utf-8'))
 phrases={}
 for line in (folder/'phrases.tsv').read_text(encoding='utf-8').splitlines():
  if not line or line.startswith('#'):continue
  book,n,page,text,meaning=line.split('|');phrases.setdefault((book,int(n)),[]).append(dict(page=int(page),text=text,meaning=meaning))
 cat=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));courses={'spoken-'+k for k in BOOKS}
 cat['words']=[w for w in cat['words'] if w.get('course') not in courses];cat['lessons']=[l for l in cat['lessons'] if l.get('course') not in courses]
 audit=[];counts={}
 for line in (folder/'lessons.tsv').read_text(encoding='utf-8').splitlines():
  book,n,title,vi=line.split('|');n=int(n);prefix,label,file=BOOKS[book];course='spoken-'+book
  lesson=dict(id=f'zhk-{prefix}-u{n}',lang='zh',level='spoken',course=course,kind='unit',number=n,short=f'Khẩu ngữ · {label} · Bài {n:02}',title=title,description=vi,source=f'Hán ngữ khẩu ngữ cấp tốc · {label} · Bài {n}',words=[])
  vocab=[r for r in rows if r['book']==book and r['lesson']==n];ps=phrases.get((book,n),[])
  assert vocab and len(ps)>=3,(book,n)
  for kind,items in [('vocabulary',vocab),('phrase',ps)]:
   for index,r in enumerate(items,1):
    text,meaning=r['text'],r['meaning'];assert text and meaning
    id=f'zhk-{prefix}-{n:02}-'+('p' if kind=='phrase' else '')+f'{index:02}'
    source=lesson['source']+(' · Mẫu câu từ bài khóa' if kind=='phrase' else ' · Danh sách từ mới')+f' · Trang PDF {r["page"]}'
    w=dict(id=id,lang='zh',level='spoken',course=course,lesson=lesson['id'],bookNumber=index,itemKind=kind,text=text,meaning=meaning,pron=r.get('pronOverride') or (pinyin(text) if kind=='phrase' else NEXT_PRON.get(text) or r.get('pron') or PRON.get(text) or pinyin(text)),pos='Mẫu câu giao tiếp' if kind=='phrase' else r.get('pos','Từ / cụm từ'),example='',examplePron='',translation='',exampleKind='spoken-'+kind,source=source,sourceFile=file,sourcePage=r['page'],examplePages=[],extended=bool(r.get('extended')),occurrences=[dict(file=file,page=r['page'])])
    if kind=='vocabulary':
     ex=next((p for p in ps if text in p['text'] and text!=p['text']),None)
     if ex:w.update(example=ex['text'],examplePron=pinyin(ex['text']),translation=ex['meaning'],examplePages=[ex['page']],exampleKind='excerpt')
     if r.get('alternatives'):w['alternatives']=r['alternatives']
    if r.get('speechText') and r['speechText']!=text:w['speechText']=r['speechText'];w['audioContext']='Giọng đọc trong cụm: '+r['speechText']
    cat['words'].append(w);lesson['words'].append(id);audit.append(dict(id=id,source=r))
  cat['lessons'].append(lesson);counts[f'{book}:{n}']=dict(vocabulary=len(vocab),phrases=len(ps))
 assert len(counts)==58
 cat['version']=8
 for path,obj in [(ROOT/'content/catalog.json',cat),(folder/'source-audit.json',audit),(folder/'counts.json',counts)]:path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(cat,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print('Added',sum(c['vocabulary'] for c in counts.values()),'words',sum(c['phrases'] for c in counts.values()),'phrases; total',len(cat['words']))
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');build()
