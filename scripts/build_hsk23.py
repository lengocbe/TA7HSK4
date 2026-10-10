"""Append reviewed HSK 2/3 textbook vocabulary without modifying earlier records."""
from pathlib import Path
import json,re,sys
from pypinyin import lazy_pinyin,Style,load_phrases_dict
ROOT=Path(__file__).resolve().parents[1]
PRON={'觉得':'jué de','为什么':'wèi shén me','眼睛':'yǎn jing','运动':'yùn dòng','一起':'yì qǐ','休息':'xiū xi','丈夫':'zhàng fu','便宜':'pián yi','意思':'yì si','时候':'shí hou','告诉':'gào su','事情':'shì qing','孩子':'hái zi','弟弟':'dì di','妹妹':'mèi mei','姐姐':'jiě jie','哥哥':'gē ge','得':'de','着':'zhe','玩儿':'wánr','长':'cháng','打算':'dǎ suan','着急':'zháo jí','南方':'nán fāng','北方':'běi fāng','容易':'róng yì','太太':'tài tai','经理':'jīng lǐ','舒服':'shū fu','蛋糕':'dàn gāo','为':'wèi','照顾':'zhào gu','清楚':'qīng chu','明白':'míng bai','睡着':'shuì zháo','聊天':'liáo tiān','兴趣':'xìng qù','差':'chà','一会儿':'yí huìr','一样':'yí yàng','了解':'liǎo jiě','个子':'gè zi','方便':'fāng biàn','还':'hái','筷子':'kuài zi','瓶子':'píng zi','教':'jiāo','爷爷':'yé ye','奶奶':'nǎi nai','起来':'qǐ lái','应该':'yīng gāi','干净':'gān jìng','盘子':'pán zi','叔叔':'shū shu','阿姨':'ā yí','故事':'gù shi','声音':'shēng yīn','其他':'qí tā','句子':'jù zi','注意':'zhù yì','鼻子':'bí zi','头发':'tóu fa','关系':'guān xi','邻居':'lín jū','爱好':'ài hào','办法':'bàn fǎ','耳朵':'ěr duo','经过':'jīng guò','多么':'duō me','不但……而且……':'bù dàn … ér qiě …','只有……才……':'zhǐ yǒu … cái …'}
ALIASES={'南方':['南'],'北方':['北'],'出院':['出'],'粉色':['粉'],'红色':['红'],'聊天':['聊天儿'],'笔记本':['笔记本电脑'],'春天':['春'],'夏天':['夏'],'秋天':['秋'],'冬天':['冬'],'极了':['极']}
POS={'dgt.':'Động từ','dt.':'Danh từ','tt.':'Tính từ','pho.':'Phó từ','trg.':'Trợ từ','gioi.':'Giới từ','lt.':'Lượng từ','st.':'Số từ','lien.':'Liên từ','dai.':'Đại từ'}
POS_OVERRIDES={}
for word in ['它','每','大家','自己','其他']:POS_OVERRIDES[word]='Đại từ'
for word in ['千','百','零','两','万','半']:POS_OVERRIDES[word]='Số từ'
for word in ['件','次','辆','条','元','把','层','双','段','种','张','位','口']:POS_OVERRIDES[word]='Lượng từ'
for word in ['着','得','地','啊','吧']:POS_OVERRIDES[word]='Trợ từ'
for word in ['因为','所以','虽然','但是','或者','如果','为了','不但……而且……','只有……才……']:POS_OVERRIDES[word]='Liên từ'
for word in ['跟','比','离','从','往','向','关于','为','根据']:POS_OVERRIDES[word]='Giới từ'
for word in ['只','也','最','再','更','就','还','已经','正在','一共','一直','当然','几乎','总是','一定','马上','越','极了','多么']:POS_OVERRIDES[word]='Phó từ'
for word in ['踢足球','出院','打篮球','带','搬','明白','感兴趣','参加']:POS_OVERRIDES[word]='Động từ'
for word in ['左边','公共汽车','小时','意思','面包','地图','最近','笔记本','电子邮件','特点','嘴']:POS_OVERRIDES[word]='Danh từ'
for word in ['米','公斤','刻']:POS_OVERRIDES[word]='Lượng từ'
POS_OVERRIDES.update({'为什么':'Đại từ nghi vấn','要':'Trợ động từ','一下':'Từ chỉ số lượng','第一':'Số thứ tự','还是':'Liên từ','新鲜':'Tính từ','久':'Tính từ'})
EXAMPLE_FORMS={'睡着':['睡不着'],'离开':['离不开'],'帮忙':['帮帮忙'],'洗澡':['洗了个澡'],'请假':['请几天假']}
COMPLETED_EXERCISES={'坐火车的时候，我喜欢向外看。','这家饭馆不但菜很好吃，而且环境很好。','你是从哪个国家来的？'}
SOURCE_GAPS={(3,18):{'万','嘴'}}
PRON.update({'啊':'a','地':'de','极了':'jí le','感兴趣':'gǎn xìng qù','几乎':'jī hū','种':'zhǒng','一边':'yì biān','一般':'yì bān','一直':'yì zhí','一共':'yí gòng','一定':'yí dìng','不但……而且……':'bú dàn … ér qiě …'})
PRON.update({'妻子':'qī zi','一下':'yí xià','电子邮件':'diàn zǐ yóu jiàn'})
def pinyin(text):return ' '.join(lazy_pinyin(text,style=Style.TONE)).replace(' ，','，').replace(' 。','。').replace(' ？','？').replace(' ！','！')
def build():
 for text,pron in PRON.items():
  if len(text)==len(pron.split()):load_phrases_dict({text:[[s] for s in pron.split()]})
 load_phrases_dict({'长着':[['zhǎng'],['zhe']],'长得':[['zhǎng'],['de']],'还书':[['huán'],['shū']],'还给':[['huán'],['gěi']],'还了':[['huán'],['le']],'一只':[['yì'],['zhī']],'两只':[['liǎng'],['zhī']],'睡不着':[['shuì'],['bù'],['zháo']]})
 groups=[]
 for line in (ROOT/'content/hsk23/words.txt').read_text(encoding='utf-8').splitlines():
  if line.startswith('#'):
   level,n,start,title,vi=line[1:].split('|');groups.append(dict(level=int(level),n=int(n),start=int(start),title=title,vi=vi,rows=[]))
  elif line:
   text,meaning=line.split('|');groups[-1]['rows'].append((text.lstrip('*'),meaning,text.startswith('*')))
 examples={};key=None
 provenance_path=ROOT/'content/hsk23/provenance.json'
 provenance=json.loads(provenance_path.read_text(encoding='utf-8')) if provenance_path.exists() else {}
 for line in (ROOT/'content/hsk23/examples.tsv').read_text(encoding='utf-8').splitlines():
  if line.startswith('#'):key=tuple(map(int,line[1:].split('|')));examples[key]=[]
  elif line:
   page,text,tr=line.split('|');examples[key].append((int(page),text,tr))
 base=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
 base['words']=[w for w in base['words'] if w.get('course') not in ['2','3']];base['lessons']=[l for l in base['lessons'] if l.get('course') not in ['2','3']]
 audit=[];missing=[]
 for g in groups:
  level,n=g['level'],g['n'];course=str(level);file=f'Giáo trình chuẩn HSK{level}.pdf'
  lesson=dict(id=f'zh{level}-u{n}',lang='zh',level=level,course=course,kind='unit',number=n,short=f'HSK {level} · Bài {n:02}',title=g['title'],description=g['vi'],source=f'Giáo trình chuẩn HSK {level} · Bài {n}',words=[])
  if (level,n)==(3,18):
   lesson['description']+=' · PDF nguồn thiếu trang sách 168–169. Từ vựng và thứ tự được đối chiếu từ mục lục; tham khảo thêm từ vựng tổng hợp. Hai từ chưa có ví dụ đã đối chiếu.'
   lesson['sourceNote']='PDF nguồn thiếu trang sách 168–169; thứ tự từ trong bài này theo mục lục, không phải số thứ tự đã xác minh trên trang từ mới.'
  candidates=[]
  for page in range(g['start']+1,g['start']+3):
   if all(f'zh{level}-{n:02}-{num:02}' in provenance for num in range(1,len(g['rows'])+1)):break
   source=ROOT/f'tmp/hsk23/hsk{level}-{page:03}.json'
   rows=json.loads(source.read_text(encoding='utf-8'))
   for r in rows:
    m=re.search(r'(?<!\d)(\d+)[.．、]?\s*([*＊]?[\u4e00-\u9fff（）、儿…]+)',r['text'])
    if m:
     near=' '.join(t['text'] for t in rows if abs(t['box'][0][1]-r['box'][0][1])<15 and t['box'][0][0]>r['box'][0][0])
     candidates.append(dict(num=int(m[1]),text=m[2].lstrip('*＊'),page=page,ocr=r['text'],near=near,confidence=r['confidence']))
  for num,(text,meaning,extended) in enumerate(g['rows'],1):
   id=f'zh{level}-{n:02}-{num:02}'
   variants=[text]+ALIASES.get(text,[])
   match=provenance.get(id) or next((c for c in candidates if c['num']==num and any(v.split('……')[0] in c['text'].replace('（','').replace('）','') for v in variants)),None)
   if (level,n)==(3,18) and not match:
    # Both body/vocabulary pages are absent in the supplied scan. The reviewed contents page lists all 17 words.
    index=[]
    for index_page in range(192,204):
     ip=ROOT/f'tmp/hsk23/hsk3-{index_page:03}.json'
     if not ip.exists():continue
     ir=json.loads(ip.read_text(encoding='utf-8'))
     for row in ir:
      if row['box'][0][0]<270 and row['text'].strip().startswith(text.split('……')[0]):
       near=' '.join(t['text'] for t in ir if abs(t['box'][0][1]-row['box'][0][1])<20)
       index.append(dict(page=index_page,ocr=near))
    match=dict(num=num,text=text,page=14,ocr=text,near=' '.join(r['ocr'] for r in index),confidence=None,kind='contents-index',index=index)
   if not match:raise ValueError(f'No numbered source row: {id} {text}')
   ex=next((e for e in examples.get((level,n),[]) if (all(v in e[1] for v in text.split('……') if v) if '……' in text else any(v in e[1] for v in variants+EXAMPLE_FORMS.get(text,[])))),None)
   if not ex and text not in SOURCE_GAPS.get((level,n),set()):missing.append((id,text));continue
   page,excerpt,tr=ex if ex else (None,'','');pos=next((vi for token,vi in POS.items() if token in match['ocr']+' '+match['near']),'Từ / cụm từ')
   pos=POS_OVERRIDES.get(text,pos)
   if level==3 and n==17 and text=='口':pos='Danh từ'
   pron=PRON.get(text,pinyin(text));spoken=text;context=None
   if level==3 and n==11 and text=='还':pron='huán';pos='Động từ';spoken='还书';context='Cách đọc trong cụm 还书 (trả sách)'
   if level==2 and n==13 and text=='长':pron='zhǎng';spoken='长着眼睛';context='Cách đọc trong cụm 长着眼睛 (có đôi mắt)'
   if level==3 and n==16 and text=='长':pron='zhǎng';spoken='长得漂亮';context='Cách đọc trong cụm 长得漂亮 (có vẻ ngoài đẹp)'
   if text=='为':spoken='为你';context='Cách đọc trong cụm 为你 (vì bạn)'
   if text=='教':spoken='教汉语';context='Cách đọc trong cụm 教汉语 (dạy tiếng Trung)'
   if text=='得':spoken='做得好';context='Cách đọc trong cụm 做得好 (làm tốt)'
   if text=='着':spoken='开着';context='Cách đọc trong cụm 开着 (đang mở)'
   if text=='地':spoken='慢慢地';context='Cách đọc trong cụm 慢慢地 (một cách chậm rãi)'
   if text=='只' and level==3 and n==18:pron='zhī';pos='Lượng từ';spoken='一只猫';context='Cách đọc trong cụm 一只猫 (một con mèo)'
   if text=='不但……而且……':spoken='不但，而且'
   if text=='只有……才……':spoken='只有，才'
   kind='pending' if not ex else 'exercise-completed' if excerpt in COMPLETED_EXERCISES else 'title' if (level,n)==(3,18) and page==167 else 'excerpt'
   location=f'Thứ tự theo mục lục: {num}, trang PDF 14 (PDF thiếu trang sách 168–169)' if (level,n)==(3,18) else f'Từ mới số {num}, trang PDF {match["page"]}'
   example_source=' · Chưa có ví dụ đã đối chiếu' if not ex else f' · '+('Bài tập đã điền đáp án' if kind=='exercise-completed' else 'Trích tiêu đề' if kind=='title' else 'Trích giáo trình')+f' trang PDF {page}'
   source=f'HSK {level} · Bài {n} · {location}{example_source}'+(' · Từ mở rộng (*)' if extended else '')
   w=dict(id=id,lang='zh',level=level,course=course,lesson=lesson['id'],bookNumber=num,text=text,pron=pron,pos=pos,meaning=meaning,example=excerpt,examplePron=pinyin(excerpt),translation=tr,exampleKind=kind,source=source,sourceFile=file,sourcePage=match['page'],examplePages=[page] if page else [],extended=extended,occurrences=[dict(file=file,page=match['page'])])
   if (level,n)==(3,18):w['sourceKind']='contents-index';w['sourceNote']=lesson['sourceNote']
   if not ex:w['exampleNote']='PDF nguồn thiếu trang sách 168–169. Chưa có câu ví dụ đã đối chiếu cho từ này.'
   if text in ALIASES:w['alternatives']=ALIASES[text]
   if text in EXAMPLE_FORMS:w['exampleForms']=EXAMPLE_FORMS[text]
   if spoken!=text:w['speechText']=spoken
   if context:w['audioContext']=context
   base['words'].append(w);lesson['words'].append(id);audit.append(dict(id=id,text=text,source=match,examplePage=page,example=excerpt))
  base['lessons'].append(lesson)
 if missing:raise ValueError('Missing examples: '+repr(missing))
 base['version']=5
 (ROOT/'content/hsk23/source-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'content/catalog.json').write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(base,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print('HSK 2/3 built:',len(audit),'new words / 35 lessons;',len(base['words']),'total words')
if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8');build()
