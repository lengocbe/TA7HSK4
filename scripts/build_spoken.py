"""Build reviewed vocabulary and spoken phrases without changing existing courses."""
from pathlib import Path
import json,re,sys
from pypinyin import lazy_pinyin,Style,load_phrases_dict
from build_hsk23 import PRON as BASIC_PRON
ROOT=Path(__file__).resolve().parents[1]
FILES={'upper':'01_汉语口语速成入门篇上_926408bf3b3b5aa3663761c385eed649.pdf','lower':'02_汉语口语速成入门篇下_3215736ea23c2c5e8b59d73e7e186a2c.pdf'}
PRON=dict(BASIC_PRON,**{'你好':'nǐ hǎo','谢谢':'xiè xie','不客气':'bú kè qi','对不起':'duì bu qǐ','没关系':'méi guān xi','你们':'nǐ men','他们':'tā men','爸爸':'bà ba','妈妈':'mā ma','爱人':'ài ren','本子':'běn zi','杯':'bēi','块':'kuài','毛':'máo','分':'fēn','家':'jiā','个':'gè','聊天儿':'liáo tiānr','哪儿':'nǎr','这儿':'zhèr','那儿':'nàr','一点儿':'yì diǎnr','一下儿':'yí xiàr','小孩儿':'xiǎo háir','一会儿':'yí huìr','一块儿':'yí kuàir','玩儿':'wánr','嗬':'hē','咦':'yí','一边……一边……':'yì biān … yì biān …','除了……以外':'chú le … yǐ wài','睡懒觉':'shuì lǎn jiào','看上去':'kàn shang qu','这么':'zhè me','多少':'duō shao','衣服':'yī fu','先生':'xiān sheng','东西':'dōng xi','时候':'shí hou','怎么':'zěn me','什么':'shén me','我们':'wǒ men','朋友':'péng you','学生':'xué sheng','认识':'rèn shi','喜欢':'xǐ huan','漂亮':'piào liang','便宜':'pián yi','苹果':'píng guǒ'})
POS={'名':'Danh từ','动':'Động từ','形':'Tính từ','代':'Đại từ','数':'Số từ','量':'Lượng từ','数量':'Từ chỉ số lượng','副':'Phó từ','连':'Liên từ','介':'Giới từ','助':'Trợ từ','叹':'Thán từ','助动':'Trợ động từ'}
PRON.update({'从……到……':'cóng … dào …','又……又……':'yòu … yòu …','连……也……':'lián … yě …','空儿':'kòngr','伴儿':'bànr','贵姓':'guì xìng','有时候':'yǒu shí hou','了':'le','找钱':'zhǎo qián','开药':'kāi yào','号':'hào','星期天':'xīng qī tiān','体温表':'tǐ wēn biǎo','有点儿':'yǒu diǎnr','哪':'nǎ','谁':'shéi','教':'jiāo','还':'hái','差':'chà','数':'shǔ','长':'cháng','重':'zhòng','得':'de','咳':'hāi'})
def pinyin(t):
 result=' '.join(lazy_pinyin(t,style=Style.TONE)).replace(' ，','，').replace(' 。','。').replace(' ？','？').replace(' ！','！')
 # Context readings and erhua in the selected, reviewed textbook phrases.
 for before,after in {'nǎ ér':'nǎr','nà ér':'nàr','zhè ér':'zhèr','yí xià ér':'yí xiàr','yī diǎn ér':'yì diǎnr','diǎn ér':'diǎnr','yī huì er':'yí huìr','qǐng shù':'qǐng shǔ','yóu dé':'yóu de','guò dé':'guò de','míng zì':'míng zi','shí hòu':'shí hou','kè qì':'kè qi','shū fú':'shū fu','yī kuài':'yí kuài','yī biàn':'yí biàn','yī lù':'yí lù'}.items():result=result.replace(before,after)
 return result
def build():
 for text,pron in PRON.items():
  if len(text)>1 and len(text)==len(pron.split()):load_phrases_dict({text:[[s] for s in pron.split()]})
 rows=json.loads((ROOT/'content/spoken/words.json').read_text(encoding='utf-8'))
 phrases={}
 for line in (ROOT/'content/spoken/phrases.tsv').read_text(encoding='utf-8').splitlines():
  if not line or line.startswith('#'):continue
  n,p,text,meaning=line.split('|');phrases.setdefault(int(n),[]).append(dict(page=int(p),text=text,meaning=meaning))
 catalog=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
 catalog['words']=[w for w in catalog['words'] if w.get('course') not in ['spoken-upper','spoken-lower']];catalog['lessons']=[l for l in catalog['lessons'] if l.get('course') not in ['spoken-upper','spoken-lower']]
 audit=[];counts={}
 for line in (ROOT/'content/spoken/lessons.tsv').read_text(encoding='utf-8').splitlines():
  n,title,vi=line.split('|');n=int(n);book='upper' if n<=15 else 'lower';course='spoken-'+book;volume='Tập trên' if n<=15 else 'Tập dưới';file=FILES[book]
  lesson=dict(id=f'zhk-u{n}',lang='zh',level='spoken',course=course,kind='unit',number=n,short=f'Khẩu ngữ · {volume} · Bài {n:02}',title=title,description=vi,source=f'Hán ngữ khẩu ngữ cấp tốc · Nhập môn · {volume} · Bài {n}',words=[])
  vocab=[r for r in rows if r['lesson']==n];assert vocab and len(phrases.get(n,[]))>=3,n
  for kind,group in [('vocabulary',vocab),('phrase',phrases[n])]:
   for num,r in enumerate(group,1):
    text,meaning=r['text'],r['meaning'];assert text and meaning,(n,num)
    id=f'zhk-{n:02}-'+('p' if kind=='phrase' else '')+f'{num:02}'
    pos=r.get('pos') or POS.get(r.get('posOCR',''),'Từ / cụm từ')
    source=lesson['source']+(' · Mẫu câu từ bài khóa' if kind=='phrase' else ' · Danh sách từ mới')+f' · Trang PDF {r["page"]}'
    if r.get('extended'):source+=' · Từ xuất hiện trong ngữ pháp/bài tập (*)'
    w=dict(id=id,lang='zh',level='spoken',course=course,lesson=lesson['id'],bookNumber=num,itemKind=kind,text=text,pron=r.get('pronOverride') or (pinyin(text) if kind=='phrase' else PRON.get(text,r.get('pron') or pinyin(text))),pos='Mẫu câu giao tiếp' if kind=='phrase' else pos,meaning=meaning,example='',examplePron='',translation='',exampleKind='spoken-'+kind,source=source,sourceFile=file,sourcePage=r['page'],examplePages=[],extended=bool(r.get('extended')),occurrences=[dict(file=file,page=r['page'])])
    if kind=='vocabulary':
     # Show a selected textbook phrase when the word occurs literally in it.
     ex=next((p for p in phrases[n] if text in p['text'] and text!=p['text']),None)
     if ex:w.update(example=ex['text'],examplePron=pinyin(ex['text']),translation=ex['meaning'],examplePages=[ex['page']],exampleKind='excerpt')
     if r.get('alternatives'):w['alternatives']=r['alternatives']
    if r.get('speechText') and r['speechText']!=text:w['speechText']=r['speechText'];w['audioContext']='Giọng đọc trong cụm: '+r['speechText']
    catalog['words'].append(w);lesson['words'].append(id);audit.append(dict(id=id,source=r))
  catalog['lessons'].append(lesson);counts[n]=dict(vocabulary=len(vocab),phrases=len(phrases[n]))
 assert len(counts)==30
 catalog['version']=7
 for dest,obj in [('content/catalog.json',catalog),('content/spoken/source-audit.json',audit),('content/spoken/counts.json',counts)]:
  (ROOT/dest).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print('Spoken:',sum(c['vocabulary'] for c in counts.values()),'vocabulary;',sum(c['phrases'] for c in counts.values()),'phrases; total',len(catalog['words']))
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');build()
