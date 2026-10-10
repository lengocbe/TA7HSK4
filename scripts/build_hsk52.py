"""Append HSK 5.2 from curated textbook entries; retain all earlier word IDs."""
from pathlib import Path
import json,sys
from pypinyin import lazy_pinyin,Style,load_phrases_dict
ROOT=Path(__file__).resolve().parents[1]
SOURCE='Giáo trình chuẩn HSK5.2.pdf'
TITLES=[('家乡的萝卜饼','Bánh củ cải quê nhà'),('小人书摊','Quầy truyện tranh'),('汉字叔叔：一个美国人的汉字情缘','Ông chú chữ Hán: duyên chữ Hán của một người Mỹ'),('阅读与思考','Đọc và suy nghĩ'),('放手','Buông tay'),('支教行动','Hoạt động dạy học tình nguyện'),('给自己加满水','Bơm đầy nước cho mình'),('你属于哪一种“忙”？','Bạn thuộc kiểu bận rộn nào?'),('下棋','Đánh cờ'),('最受欢迎的毕业生','Sinh viên tốt nghiệp được chào đón nhất'),('培养对手','Đào tạo đối thủ'),('竞争让市场更高效','Cạnh tranh khiến thị trường hiệu quả hơn'),('登门槛效应','Hiệu ứng bước qua ngưỡng cửa'),('身边的环保','Bảo vệ môi trường quanh ta'),('以堵治堵——缓解交通有妙招','Dùng tắc trị tắc: mẹo giảm ùn tắc giao thông'),('鸟儿的护肤术','Cách chăm sóc da của chim'),('植物会出汗','Thực vật cũng ra mồ hôi'),('老舍与养花','Lão Xá và việc trồng hoa')]
EXPECTED=[44,36,41,34,40,37,40,35,34,40,36,36,29,39,38,34,35,37]
POS={'n':'Danh từ','v':'Động từ','a':'Tính từ','d':'Phó từ','r':'Đại từ','m':'Số / lượng từ','i':'Thành ngữ','p':'Giới từ','c':'Liên từ','u':'Trợ từ','e':'Thán từ'}
VARIANTS={'繁体字':['繁体'],'简体字':['简体'],'使劲儿':['使劲'],'象棋':['棋'],'初中':['初级中学'],'鲇鱼':['鲶鱼'],'八成儿':['八成'],'私人':['私'],'招儿':['招'],'扩大':['扩'],'受伤':['受'],'悲伤':['悲']}
PRON={'萝卜':'luó bo','般':'bān','油炸':'yóu zhá','薄':'báo','擀':'gǎn','圈':'quān','糊':'hú','橘子':'jú zi','淋':'lín','少许':'shǎo xǔ','酱油':'jiàng yóu','棚子':'péng zi','砖头':'zhuān tou','木头':'mù tou','涨':'zhǎng','系':'xì','规矩':'guī ju','某':'mǒu','横':'héng','使劲儿':'shǐ jìnr','朝':'cháo','反省':'fǎn xǐng','纪录':'jì lù','雇':'gù','答应':'dā ying','教练':'jiào liàn','将军':'jiāng jūn','不假思索':'bù jiǎ sī suǒ','舍不得':'shě bu de','屡':'lǚ','乘':'chéng','行业':'háng yè','执着':'zhí zhuó','不见得':'bù jiàn de','鲇鱼':'nián yú','设备':'shè bèi','的确':'dí què','门槛':'mén kǎn','嗯':'ńg','八成儿':'bā chéngr','了不起':'liǎo bu qǐ','尽量':'jǐn liàng','招儿':'zhāor','角色':'jué sè','知更鸟':'zhī gēng niǎo','梳子':'shū zi','沙子':'shā zi','肥皂':'féi zào','枝干':'zhī gàn','树干':'shù gàn','冰激凌':'bīng jī líng','玻璃':'bō li','荫凉':'yìn liáng','劳驾':'láo jià','应付':'yìng fu','昙花':'tán huā','反正':'fǎn zhèng','背过':'bèi guò','重重':'zhòng zhòng','似的':'shì de','尽':'jǐn','尽自己':'jìn zì jǐ','薄利':'bó lì','长时间':'cháng shí jiān','长虫':'zhǎng chóng','种种':'zhǒng zhǒng','好种':'hǎo zhòng','养活':'yǎng huó','占用':'zhàn yòng','看不起':'kàn bu qǐ','忍不住':'rěn bu zhù','不如':'bù rú','差':'chà','过于':'guò yú','为图':'wèi tú','为了':'wèi le','因为':'yīn wèi','认为':'rèn wéi','成为':'chéng wéi','作为':'zuò wéi','称为':'chēng wéi','为人':'wéi rén','给':'gěi','处':'chǔ','处理':'chǔ lǐ','处于':'chǔ yú','共处':'gòng chǔ','一处':'yí chù','得罪':'dé zuì','得':'de','得再':'děi zài','还得':'hái děi','就得':'jiù děi','又得':'yòu děi','取得':'qǔ dé','获得':'huò dé','得到':'dé dào','觉得':'jué de','不得不':'bù dé bù','调':'tiáo','调整':'tiáo zhěng','调动':'diào dòng','转转':'zhuàn zhuan','转变':'zhuǎn biàn','干燥':'gān zào','喜干':'xǐ gān','背着':'bēi zhe','背点':'bēi diǎn','上了年纪':'shàng le nián jì'}
PRON['嗯']='ǹg'
SPEECH={'zh5-19-24':('薄如白纸','薄如白纸 (mỏng như giấy)'), 'zh5-23-22':('本系','本系 (khoa của mình)'), 'zh5-25-08':('朝里面','朝里面 (hướng vào trong)')}
def pinyin(text):
 return ' '.join(lazy_pinyin(text,style=Style.TONE)).replace(' ，','，').replace(' 。','。').replace(' ！','！').replace(' ？','？')
def append_hsk52(base):
 for word,pron in PRON.items():
  if len(word)==len(pron.split()):load_phrases_dict({word:[[s] for s in pron.split()]})
 meta=json.loads((ROOT/'content/hsk52/provenance.json').read_text(encoding='utf-8'));examples={};rows={};n=0
 for line in (ROOT/'content/hsk52/examples.tsv').read_text(encoding='utf-8-sig').splitlines():
  if not line or line.startswith('#'):continue
  lesson,nums,pages,text,tr=line.split('|')
  for num in map(int,nums.split(',')):
   key=(int(lesson),num);assert key not in examples,key
   examples[key]=(list(map(int,pages.split(','))),text,tr)
 for line in (ROOT/'content/hsk52/words.txt').read_text(encoding='utf-8-sig').splitlines():
  if line.startswith('#'):n=int(line[1:]);rows[n]=[]
  elif line:rows[n].append(line.split('|'))
 assert sorted(rows)==list(range(19,37))
 base['words']=[w for w in base['words'] if w.get('course')!='5.2'];base['lessons']=[l for l in base['lessons'] if l.get('course')!='5.2']
 for n in range(19,37):
  assert len(rows[n])==EXPECTED[n-19]
  cn,vi=TITLES[n-19];lesson=dict(id=f'zh5-u{n}',lang='zh',level=5,course='5.2',kind='unit',number=n,short=f'HSK 5.2 · Bài {n:02}',title=cn,description=vi,source=f'Giáo trình chuẩn HSK 5.2 · Bài {n}',words=[])
  for num,(text,pos,meaning) in enumerate(rows[n],1):
   id=f'zh5-{n:02}-{num:02}';m=meta[id];ep,ex,tr=examples[(n,num)];kind='title' if '(Tiêu đề bài)' in tr else 'excerpt'
   source=f'HSK 5.2 · Bài {n} · Từ mới số {num}, trang sách {m["page"]-1} (PDF {m["page"]}) · '+('Trích tiêu đề' if kind=='title' else 'Trích giáo trình')+' trang PDF '+', '.join(map(str,ep))
   if m['extended']:source+=' · Từ mở rộng (*)'
   w=dict(id=id,lang='zh',level=5,course='5.2',lesson=lesson['id'],bookNumber=num,text=text,pron=PRON.get(text,pinyin(text)),pos=POS[pos],meaning=meaning,example=ex,examplePron=pinyin(ex),translation=tr,exampleKind=kind,source=source,sourceFile=SOURCE,sourcePage=m['page'],examplePages=ep,extended=m['extended'],occurrences=[dict(file=SOURCE,page=m['page'])])
   if text in VARIANTS:w['alternatives']=VARIANTS[text]
   if text=='鼓掌':w['exampleForms']=['鼓起掌']
   if text=='隐约':w['exampleForms']=['隐隐约约']
   if id in SPEECH:w['speechText'],context=SPEECH[id];w['audioContext']='Cách đọc trong cụm '+context
   base['words'].append(w);lesson['words'].append(id)
  base['lessons'].append(lesson)
 assert len(examples)==sum(EXPECTED)==665
 base['version']=4;return base
if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8')
 p=ROOT/'content/catalog.json';data=append_hsk52(json.loads(p.read_text(encoding='utf-8')));p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'www/data.js').write_text('const DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print('HSK 5.2:',665,'words, 18 lessons;',len(data['words']),'total words')
