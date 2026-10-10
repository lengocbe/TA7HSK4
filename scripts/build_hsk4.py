"""Build HSK 4 textbook courses from editorial files, retaining existing IDs/state."""
from pathlib import Path
import json,sys
from pypinyin import lazy_pinyin,Style,load_phrases_dict
ROOT=Path(__file__).resolve().parents[1]
TITLES=[('简单的爱情','Tình yêu đơn giản'),('真正的朋友','Người bạn chân chính'),('经理对我印象不错','Giám đốc có ấn tượng tốt về tôi'),('不要太着急赚钱','Đừng quá nóng vội kiếm tiền'),('只买对的，不买贵的','Chỉ mua thứ phù hợp, không mua thứ đắt'),('一分钱一分货','Tiền nào của nấy'),('最好的医生是自己','Bác sĩ tốt nhất là bản thân'),('生活中不缺少美','Cuộc sống không thiếu cái đẹp'),('阳光总在风雨后','Sau cơn mưa trời lại sáng'),('幸福的标准','Tiêu chuẩn hạnh phúc'),('读书好，读好书，好读书','Đọc sách có ích, đọc sách hay, thích đọc sách'),('用心发现世界','Khám phá thế giới bằng trái tim'),('喝着茶看京剧','Uống trà xem Kinh kịch'),('保护地球母亲','Bảo vệ Mẹ Trái đất'),('教育孩子的艺术','Nghệ thuật giáo dục con cái'),('生活可以更美好','Cuộc sống có thể tốt đẹp hơn'),('人与自然','Con người và thiên nhiên'),('科技与世界','Khoa học công nghệ và thế giới'),('生活的味道','Hương vị cuộc sống'),('路上的风景','Phong cảnh trên đường')]
POS={'n':'Danh từ','v':'Động từ','a':'Tính từ','d':'Phó từ','r':'Đại từ','m':'Số / lượng từ','p':'Giới từ','c':'Liên từ','u':'Trợ từ'}
PRON={'俩':'liǎ','熟悉':'shú xī','性格':'xìng gé','脾气':'pí qi','咳嗽':'ké sou','大夫':'dài fu','肚子':'dù zi','主意':'zhǔ yi','师傅':'shī fu','空儿':'kòngr','好处':'hǎo chu','得':'děi','填空':'tián kòng','商量':'shāng liang','生意':'shēng yi','知识':'zhī shi','并':'bìng','深':'shēn','空':'kōng','干':'gàn','倒':'dào','孙子':'sūn zi','暖和':'nuǎn huo','胳膊':'gē bo','钥匙':'yào shi','怪':'guài','省':'shěng','脏':'zāng','行':'xíng','重':'zhòng','种':'zhǒng','弹钢琴':'tán gāng qín','差不多':'chà bu duō','尽管':'jǐn guǎn','重新':'chóng xīn','得意':'dé yì','礼拜天':'lǐ bài tiān','厉害':'lì hai','好读书':'hào dú shū','塑料袋':'sù liào dài','随着':'suí zhe','不得不':'bù dé bù','内容':'nèi róng','竟然':'jìng rán','开玩笑':'kāi wán xiào','应聘':'yìng pìn','袜子':'wà zi','葡萄':'pú tao','自然':'zì rán','当然':'dāng rán'}
VARIANTS={'勺子':['勺'],'肚子':['肚'],'空儿':['空'],'会儿':['会']}
def pinyin(text):
 return ' '.join(lazy_pinyin(text,style=Style.TONE)).replace(' ，','，').replace(' 。','。').replace(' ？','？').replace(' ！','！')
def append_hsk4(base):
 provenance=json.loads((ROOT/'content/hsk4/provenance.json').read_text(encoding='utf-8'))
 rows={};n=0
 for line in (ROOT/'content/hsk4/words.txt').read_text(encoding='utf-8-sig').splitlines():
  if line.startswith('#'):n=int(line[1:]);rows[n]=[]
  elif line:rows[n].append(line.split('|'))
 assert sorted(rows)==list(range(1,21))
 examples={}
 for line in (ROOT/'content/hsk4/examples.tsv').read_text(encoding='utf-8-sig').splitlines():
  if not line or line.startswith('#'):continue
  n,nums,pages,ex,tr=line.split('|')
  for num in map(int,nums.split(',')):
   key=(int(n),num)
   assert key not in examples,key
   examples[key]=(list(map(int,pages.split(','))),ex,tr)
 for text,pron in PRON.items():
  if len(text)==len(pron.split()):load_phrases_dict({text:[[syllable] for syllable in pron.split()]})
 load_phrases_dict({'流血':[['liú'],['xiě']],'血':[['xiě']],'会儿':[['huìr']],'儿':[['ér']],'长大':[['zhǎng'],['dà']],'长不大':[['zhǎng'],['bu'],['dà']],'得少吃':[['děi'],['shǎo'],['chī']],'好好儿':[['hǎo'],['hāor']],'打折':[['dǎ'],['zhé']],'重新':[['chóng'],['xīn']]})
 base['words']=[w for w in base['words'] if w.get('course') not in ['4.1','4.2']]
 base['lessons']=[l for l in base['lessons'] if l.get('course') not in ['4.1','4.2']]
 new_words=[];lessons=[]
 for n in range(1,21):
  part=1 if n<=10 else 2;course=f'4.{part}';source_file=f'Giáo trình chuẩn HSK{course}.pdf';cn,vi=TITLES[n-1]
  lesson=dict(id=f'zh4-u{n}',lang='zh',level=4,course=course,kind='unit',number=n,short=f'HSK {course} · Bài {n:02}',title=cn,description=vi,source=f'Giáo trình chuẩn HSK {course} · Bài {n}',words=[])
  for num,(text,pos,meaning) in enumerate(rows[n],1):
   id=f'zh4-{n:02}-{num:02}';meta=provenance[id];ep,ex,tr=examples[(n,num)]
   pron=PRON.get(text,pinyin(text));source=f'HSK {course} · Bài {n} · Từ mới số {num}, trang PDF {meta["page"]} · Trích giáo trình trang PDF '+', '.join(map(str,ep))
   if meta['extended']:source+=' · Từ mở rộng (*)'
   w=dict(id=id,lang='zh',level=4,course=course,lesson=lesson['id'],bookNumber=num,text=text,pron=pron,pos=POS[pos],meaning=meaning,example=ex,examplePron=pinyin(ex),translation=tr,source=source,sourceFile=source_file,sourcePage=meta['page'],examplePages=ep,exampleKind='excerpt',extended=meta['extended'],occurrences=[dict(file=source_file,page=meta['page'])])
   if text in VARIANTS:w['alternatives']=VARIANTS[text]
   if n==9 and text=='得':w['speechText']='得少吃';w['audioContext']='Cách đọc trong cụm 得少吃 (phải ăn ít hơn)'
   if text=='干':w['speechText']='干什么';w['audioContext']='Cách đọc trong cụm 干什么 (làm gì)'
   if text=='倒':w['speechText']='倒是';w['audioContext']='Cách đọc trong cụm 倒是 (lại là)'
   new_words.append(w);lesson['words'].append(id)
  lessons.append(lesson)
 assert len(examples)==len(new_words)
 base['words']+=new_words;base['lessons']+=lessons;base['version']=max(base.get('version',1),3)
 return base
if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8')
 source=ROOT/'content/catalog.json';result=append_hsk4(json.loads(source.read_text(encoding='utf-8')))
 source.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(result,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print('Built HSK 4.1 / 4.2:',sum(w.get('course') in ['4.1','4.2'] for w in result['words']),'words / 20 lessons;',len(result['words']),'total words')
