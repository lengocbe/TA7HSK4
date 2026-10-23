"""Append HSK 6 textbook content; existing word IDs and records are preserved."""
from pathlib import Path
import json,sys
from pypinyin import lazy_pinyin,Style,load_phrases_dict
ROOT=Path(__file__).resolve().parents[1]
TITLES='''孩子给我们的启示|Điều con trẻ dạy chúng ta
父母之爱|Tình yêu của cha mẹ
一盒月饼|Một hộp bánh Trung thu
完美的胜利|Chiến thắng hoàn hảo
学一门外语需要理由吗？|Học ngoại ngữ có cần lý do?
当好职场插班生|Làm tốt vai trò người mới nơi làm việc
我的人生我做主|Tôi làm chủ cuộc đời mình
遇见原来的我|Gặp lại tôi ngày trước
不用手机的日子|Những ngày không dùng điện thoại
全球化视野中的中国饮食|Ẩm thực Trung Quốc trong tầm nhìn toàn cầu
我不在时，猫在干什么？|Khi tôi vắng nhà, mèo làm gì?
我们都爱白噪音|Chúng ta đều thích tiếng ồn trắng
从旅游指南看世事变迁|Nhìn sự đổi thay qua sách hướng dẫn du lịch
背着电饭锅拍北极|Mang nồi cơm điện đi chụp ảnh Bắc Cực
山脉上的雕刻|Những nét chạm khắc trên núi
徐健和他的野生动物摄影师们|Từ Kiện và những nhiếp ảnh gia động vật hoang dã
小动物眼中的慢世界|Thế giới chậm trong mắt động vật nhỏ
神奇的丝瓜|Quả mướp kỳ diệu
无阳光的深海世界|Thế giới biển sâu không có ánh mặt trời
金鸡窝|Ổ gà vàng
未来商店|Cửa hàng tương lai
2050年的汽车什么样？|Ô tô năm 2050 sẽ như thế nào?
大数据时代|Thời đại dữ liệu lớn
体育明星们的离奇遭遇|Những chuyện kỳ lạ của các ngôi sao thể thao
草船借箭|Thuyền cỏ mượn tên
奇异的灯光|Ánh đèn kỳ lạ
完璧归赵|Trả ngọc nguyên vẹn về nước Triệu
高山流水遇知音|Núi cao nước chảy gặp tri âm
“笑”的备忘录|Bản ghi nhớ về tiếng cười
你睡好了吗？|Bạn đã ngủ ngon chưa?
运动的学问|Kiến thức về vận động
有时，不妨悲伤|Đôi khi, cứ buồn cũng được
怀念慢生活|Hoài niệm cuộc sống chậm
为文物而生的人|Người sống vì di sản văn hóa
走近木版年画|Tìm hiểu tranh Tết khắc gỗ
中国古代书院|Các học viện Trung Quốc thời cổ
警察的故事|Câu chuyện của cảnh sát
慧眼捕捉商机|Tinh mắt nắm bắt cơ hội kinh doanh
互联网时代的生活|Cuộc sống thời Internet
人类超能力会改变世界纪录吗？|Siêu năng lực con người có thay đổi kỷ lục thế giới?'''.splitlines()
PRON={'嚷':'rǎng','老公':'lǎo gong','别扭':'biè niu','唠叨':'láo dao','沏':'qī','任':'rèn','哼':'hng','折':'zhé','横':'héng','挨':'ái','哇':'wa','啦':'la','盛':'chéng','嗨':'hēi','哄':'hǒng','扒':'bā','晃':'huàng','幢':'zhuàng','扎':'zhā','撇':'piē','翘':'qiào','曝光':'bào guāng','恶心':'ě xin','供不应求':'gōng bù yìng qiú','丢三落四':'diū sān là sì','肖像':'xiào xiàng','琢磨':'zuó mo','踏实':'tā shi','大伙儿':'dà huǒr','模样':'mú yàng','心眼儿':'xīn yǎnr','馅儿':'xiànr','纳闷儿':'nà mènr','玩意儿':'wán yìr','衣裳':'yī shang','枕头':'zhěn tou','舌头':'shé tou','媳妇':'xí fu','斯文':'sī wen','恭敬':'gōng jìng','而已':'ér yǐ','唾弃':'tuò qì','敞开':'chǎng kāi','叮嘱':'dīng zhǔ','迸发':'bèng fā','磋商':'cuō shāng','攒':'zǎn','蹬':'dēng','眯':'mī','侥幸':'jiǎo xìng','瘸':'qué','拣':'jiǎn','歹徒':'dǎi tú','宽敞':'kuān chang'}
PRON.update({'颈椎':'jǐng zhuī','播种':'bō zhòng','纽扣儿':'niǔ kòur','墨水儿':'mò shuǐr','扎实':'zhā shi','哦':'ò','娃娃':'wá wa','含糊':'hán hu','水龙头':'shuǐ lóng tóu'})
SPEECH={(1,35):'第一任老师',(6,18):'哼，太不像话了',(26,22):'挨饿受冻',(10,44):'折起来',(24,8):'横着',(26,42):'哇，萤火虫',(26,47):'做成啦',(31,7):'哦，原来如此'}
CONTEXT={'盛':'盛着菜','哄':'哄孩子','扒':'扒开','晃':'晃来晃去','幢':'一幢楼','扎':'扎进草丛','撇':'撇过去','翘':'翘着尾巴','嗨':'嗨，坐在金鸡窝上'}
FORMS={'举动':['一举一动'],'刹车':['刹不住车'],'打仗':['打了一场嘴仗'],'叹气':['叹着气'],'出神':['出了神'],'过瘾':['过过网瘾'],'沾光':['沾父亲的光']}
POS={'dgt.':'Động từ','dt.':'Danh từ','tt.':'Tính từ','pho.':'Phó từ','trg.':'Trợ từ','gioi.':'Giới từ','lt.':'Lượng từ','st.':'Số từ','lien.':'Liên từ','dai.':'Đại từ','trợ.':'Trợ từ'}
def pinyin(s):return ' '.join(lazy_pinyin(s,style=Style.TONE)).replace(' ，','，').replace(' 。','。').replace(' ？','？').replace(' ！','！')
def build():
 for text,pron in PRON.items():
  if len(text)>1 and len(text)==len(pron.split()):load_phrases_dict({text:[[s] for s in pron.split()]})
 groups={};n=0
 for line in (ROOT/'content/hsk6/words.txt').read_text(encoding='utf-8').splitlines():
  if line.startswith('#'):n=int(line[1:]);groups[n]=[]
  elif line:groups[n].append(line.split('|'))
 assert sorted(groups)==list(range(1,41))
 examples={}
 for line in (ROOT/'content/hsk6/examples.tsv').read_text(encoding='utf-8').splitlines():
  if not line or line.startswith('#'):continue
  n,nums,pages,ex,tr=line.split('|')
  for num in map(int,nums.split(',')):
   key=int(n),num;assert key not in examples,key
   examples[key]=(list(map(int,pages.split(','))),ex,tr)
 meta=json.loads((ROOT/'content/hsk6/provenance.json').read_text(encoding='utf-8'))
 base=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
 base['words']=[w for w in base['words'] if w.get('level')!=6];base['lessons']=[l for l in base['lessons'] if l.get('level')!=6]
 audit=[]
 for n,rows in sorted(groups.items()):
  book='6.1' if n<=20 else '6.2';title,vi=TITLES[n-1].split('|');file=f'Giáo trình chuẩn HSK{book}.pdf'
  lesson=dict(id=f'zh6-u{n}',lang='zh',level=6,course=book,kind='unit',number=n,short=f'HSK {book} · Bài {n:02}',title=title,description=vi,source=f'Giáo trình chuẩn HSK {book} · Bài {n}',words=[])
  for num,(text,meaning) in enumerate(rows,1):
   id=f'zh6-{n:02}-{num:02}';m=meta[id];pages,ex,tr=examples[n,num];assert any(s in ex for s in [text]+FORMS.get(text,[])),id
   assert m['text']==text and m['num']==num
   kind='title' if ex.replace(' ','') in [title.replace(' ',''),'丙融合数字生活方式','丁长途行车仍靠汽油','年画的起源'] else 'excerpt'
   pos=next((v for k,v in POS.items() if k in m['ocr']+' '+m['near']),'Từ / cụm từ')
   source=f'HSK {book} · Bài {n} · Từ mới số {num}, trang PDF {m["page"]} · '+('Trích tiêu đề' if kind=='title' else 'Trích giáo trình')+' trang PDF '+', '.join(map(str,pages))
   if m['extended']:source+=' · Từ mở rộng (*)'
   w=dict(id=id,lang='zh',level=6,course=book,lesson=lesson['id'],bookNumber=num,text=text,pron=PRON.get(text,pinyin(text)),pos=pos,meaning=meaning,example=ex,examplePron=pinyin(ex),translation=tr,exampleKind=kind,source=source,sourceFile=file,sourcePage=m['page'],examplePages=pages,extended=m['extended'],occurrences=[dict(file=file,page=m['page'])])
   if text in FORMS:w['exampleForms']=FORMS[text]
   speech=SPEECH.get((n,num),CONTEXT.get(text,text))
   if speech!=text:w['speechText']=speech;w['audioContext']='Giọng đọc trong cụm: '+speech
   base['words'].append(w);lesson['words'].append(id);audit.append(dict(id=id,text=text,source=m,examplePages=pages,example=ex))
  base['lessons'].append(lesson)
 base['version']=6
 (ROOT/'content/hsk6/source-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'content/catalog.json').write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(base,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print('HSK 6:',len(audit),'words, 40 lessons; total:',len(base['words']),'words,',len(base['lessons']),'lessons')
if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8');build()
