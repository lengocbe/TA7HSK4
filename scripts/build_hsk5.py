"""Append the edited HSK 5.1 course without changing existing word identifiers.
The checked-in editorial files suffice; the scanned PDF is not redistributed.
"""
from pathlib import Path
import json,re,sys
from pypinyin import lazy_pinyin,Style,load_phrases_dict
ROOT=Path(__file__).resolve().parents[1]
SOURCE='Giáo trình chuẩn HSK5.1_c9f3aee3070d412769f85e5c79f1c5f9.pdf'
STARTS=[4,11,18,28,36,45,56,65,73,82,90,99,108,116,125,136,144,152]
TITLES=[('爱的细节','Những điều nhỏ nhặt trong tình yêu'),('留串钥匙给父母','Để chìa khóa cho bố mẹ'),('人生有选择，一切可改变','Đời người có lựa chọn, mọi thứ có thể đổi thay'),('子路背米','Tử Lộ cõng gạo'),('济南的泉水','Nước suối Tế Nam'),('除夕的由来','Nguồn gốc đêm giao thừa'),('成语故事两则','Hai câu chuyện thành ngữ'),('“朝三暮四”的古今义','Nghĩa xưa và nay của Sáng ba chiều bốn'),('别样鲁迅','Một Lỗ Tấn khác'),('争论的奇迹','Kỳ tích của cuộc tranh luận'),('闹钟的危害','Tác hại của đồng hồ báo thức'),('海外用户玩儿微信','Người dùng WeChat ở nước ngoài'),('锯掉生活的“筐底”','Cưa bỏ đáy giỏ trong cuộc sống'),('北京的四合院','Tứ hợp viện Bắc Kinh'),('纸上谈兵','Bàn việc binh trên giấy'),('体重与节食','Cân nặng và ăn kiêng'),('在最美好的时刻离开','Rời đi vào thời khắc tốt đẹp nhất'),('抽象艺术美不美','Nghệ thuật trừu tượng có đẹp không?')]
EXPECTED=[38,39,41,40,46,41,45,43,38,37,41,43,37,41,39,41,33,40]
POS={'n':'Danh từ','v':'Động từ','a':'Tính từ','d':'Phó từ','r':'Đại từ','m':'Số / lượng từ','i':'Thành ngữ','p':'Giới từ','c':'Liên từ','u':'Trợ từ','e':'Thán từ'}
VARIANTS={'屋子':['屋'],'银子':['银'],'治疗':['治'],'躲藏':['藏'],'骨头':['骨'],'代替':['替'],'盆子':['盆'],'射击':['射'],'大象':['象'],'尽力':['尽'],'蹄子':['蹄'],'慌张':['慌'],'锯子':['锯'],'敌人':['敌'],'调动':['调'],'丑陋':['丑']}
PRON={'挣':'zhèng','铺':'pū','杆':'gǎn','铺好':'pū hǎo','挣的':'zhèng de','箭杆':'jiàn gǎn','背米':'bēi mǐ','吵过架':'chǎo guo jià','射死':'shè sǐ','系着':'jì zhe','种草':'zhòng cǎo','种竹子':'zhòng zhú zi','为人们':'wèi rén men','背':'bēi','系':'jì','种':'zhòng','为':'wéi','数':'shù','称':'chēng','晕':'yūn','宁可':'nìng kě','好客':'hào kè','结实':'jiē shi','干活儿':'gàn huór','不耐烦':'bù nài fán','不得了':'bù dé liǎo','一辈子':'yí bèi zi','老婆':'lǎo po','脑袋':'nǎo dai','相处':'xiāng chǔ','处':'chǔ','蒙胧':'méng lóng','骨头':'gǔ tou','主意':'zhǔ yi','调皮':'tiáo pí','调动':'diào dòng','暖和':'nuǎn huo','关系':'guān xi','便':'biàn','地道':'dì dao','行家':'háng jia','扇子':'shàn zi','朝三暮四':'zhāo sān mù sì','似的':'shì de','钥匙':'yào shi','翟峰':'Zhái Fēng','吵醒':'chǎo xǐng','睡着':'shuì zháo','着地':'zháo dì','长辈':'zhǎng bèi','得到':'dé dào','觉得':'jué de','随之':'suí zhī','吓得':'xià de','上当':'shàng dàng','说服':'shuō fú','使得':'shǐ de','舍得':'shě de','凑合':'còu he','重复':'chóng fù','结局':'jié jú','为人':'wéi rén','为了':'wèi le','因为':'yīn wèi','认为':'rèn wéi','作为':'zuò wéi','称为':'chēng wéi','为此':'wèi cǐ','行为':'xíng wéi','无奈':'wú nài','似乎':'sì hū','哈':'hā','哎':'āi','唉':'ài'}
# Same-sound characters disambiguate isolated polyphonic words for the TTS engine.
SPEECH={'zh5-02-12':'正','zh5-02-35':'扑','zh5-07-40':'敢','zh5-07-42':'爱','zh5-04-01':'杯','zh5-05-41':'围','zh5-10-18':'记','zh5-14-23':'众','zh5-14-30':'位'}
def pinyin(text):
 return ' '.join(lazy_pinyin(text,style=Style.TONE)).replace(' ，','，').replace(' 。','。').replace(' ！','！').replace(' ？','？')
def append_hsk5(base):
 base['words']=[w for w in base['words'] if not (w.get('level')==5 and w.get('course','5.1')=='5.1')]
 base['lessons']=[l for l in base['lessons'] if not (l.get('level')==5 and l.get('course','5.1')=='5.1')]
 for group in ('words','lessons'):
  for item in base[group]:
   if item['lang']=='zh':item.setdefault('level',4)
 provenance=json.loads((ROOT/'content/hsk5/provenance.json').read_text(encoding='utf-8'))
 examples={}
 for line in (ROOT/'content/hsk5/examples.tsv').read_text(encoding='utf-8-sig').splitlines():
  if not line or line.startswith('#'):continue
  n,ids,pages,ex,tr=line.split('|')
  for num in map(int,ids.split(',')):
   key=(int(n),num)
   if key in examples:raise ValueError(f'Duplicate example mapping {key}')
   examples[key]=(list(map(int,pages.split(','))),ex,tr)
 for text,pron in PRON.items():
  syllables=pron.split()
  if len(text)==len(syllables):load_phrases_dict({text:[[x] for x in syllables]})
 lessons=[]
 for n,(cn,vi) in enumerate(TITLES,1):
  lessons.append(dict(id=f'zh5-u{n}',lang='zh',level=5,kind='unit',number=n,short=f'HSK 5.1 · Bài {n:02}',title=cn,description=vi,source=f'Giáo trình chuẩn HSK 5.1 · Bài {n} · Trang sách {STARTS[n-1]+10} (PDF {STARTS[n-1]})',words=[]))
 words=[];n=0;num=0
 for line in (ROOT/'content/hsk5/words.txt').read_text(encoding='utf-8-sig').splitlines():
  if line.startswith('#'):n=int(line[1:]);num=0;continue
  if not line:continue
  num+=1;text,pos,meaning=line.split('|');id=f'zh5-{n:02}-{num:02}';meta=provenance[id]
  ep,ex,tr=examples[(n,num)]
  pron=PRON.get(text,pinyin(text))
  if id=='zh5-14-30':pron='wèi'
  # Titles and missing full sentences are explicitly distinguished from examples.
  kind='title' if '(Tiêu đề bài)' in tr else 'excerpt'
  note=''
  if id=='zh5-13-14' and ex=='投篮':
   ex='';tr='';kind='pending';note='Chưa tìm được câu ví dụ phù hợp trong giáo trình; cần đối chiếu thêm.'
  source=f'HSK 5.1 · Bài {n} · Từ mới số {num}, tr. sách {meta["page"]+10} (PDF {meta["page"]})'
  if ex:source+=' · '+('Trích tiêu đề' if kind=='title' else 'Trích giáo trình')+' tr. '+', '.join(str(p+10) for p in ep)+' (PDF '+', '.join(map(str,ep))+')'
  if meta['extended']:source+=' · Từ mở rộng (*)'
  w=dict(id=id,lang='zh',level=5,text=text,pron=pron,pos=POS[pos],meaning=meaning,example=ex,examplePron=pinyin(ex),translation=tr,source=source,sourceFile=SOURCE,sourcePage=meta['page'],examplePages=ep,exampleKind=kind,exampleNote=note,lesson=f'zh5-u{n}',bookNumber=num,extended=meta['extended'],occurrences=[dict(file=SOURCE,page=meta['page'])])
  if text in VARIANTS:w['alternatives']=VARIANTS[text]
  if id in SPEECH:w['speechText']=SPEECH[id]
  words.append(w);lessons[n-1]['words'].append(id)
 for n,l in enumerate(lessons):assert len(l['words'])==EXPECTED[n],l['id']
 assert len(words)==723 and len(examples)==723
 base['words']+=words;base['lessons']+=lessons;base['version']=max(base.get('version',1),2)
 return base
if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8')
 result=append_hsk5(json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8')))
 (ROOT/'content/catalog.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(result,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print('Built',len(result['words']),'words;',len(result['lessons']),'lesson views; HSK 5.1 = 723 words / 18 lessons.')
