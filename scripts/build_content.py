"""Build reviewed lesson content with PDF provenance; no network required."""
from pathlib import Path
import json, re, sys
from pypdf import PdfReader
from pypinyin import lazy_pinyin, Style, load_phrases_dict, load_single_dict

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
titles_en=['Hobbies','Healthy Living','Community Service','Music and Arts','Food and Drink','A Visit to a School','Traffic','Films','Festivals Around the World','Energy Sources','Travelling in the Future','English-speaking Countries']
titles_zh=['Công việc & trách nhiệm','Học tập & ngôn ngữ','Đi lại & du lịch','Sức khỏe & nghỉ ngơi','Mua sắm & ăn uống','Nhà cửa & sinh hoạt','Cảm xúc & giao tiếp','Môi trường & thiên nhiên','Kế hoạch & phát triển','Văn hóa & giải trí']
chinese_rows=[line.split('|') for line in (ROOT/'content/chinese.tsv').read_text(encoding='utf-8').splitlines() if line and not line.startswith('#')]
# Keep contextual readings and neutral tones consistent with reviewed word cards.
load_phrases_dict({row[1]:[[syllable] for syllable in row[2].split()] for row in chinese_rows if len(row[1])>1})
load_single_dict({ord('脏'):'zāng,zàng'})
load_phrases_dict({'弄得':[['nòng'],['de']], '咳嗽得':[['ké'],['sou'],['de']], '收拾得':[['shōu'],['shi'],['de']], '整理得':[['zhěng'],['lǐ'],['de']], '说得':[['shuō'],['de']], '进行得':[['jìn'],['xíng'],['de']]})
lessons=[];words=[]
for number,title in enumerate(titles_en,1):
    lessons.append(dict(id=f'en-u{number}',lang='en',kind='unit',number=number,short=f'Unit {number}',title=title,description='Từ trọng tâm theo Glossary. Câu ví dụ được biên soạn bổ sung, phù hợp trình độ lớp 7.',source='Tiếng Anh 7 Global Success · Glossary, trang sách 136–139',words=[]))

for line in (ROOT/'content/english.tsv').read_text(encoding='utf-8').splitlines():
    if not line or line.startswith('#'):continue
    number,text,pron,pos,meaning,example,translation=line.split('|')
    n=int(number);lesson=lessons[n-1]
    page=136 if n<=3 else 137 if n<=6 else 138 if n<=9 else 139
    id=f'en-{n:02d}-{len(lesson["words"])+1:02d}'
    words.append(dict(id=id,lang='en',text=text,pron=f'/{pron}/',pos=pos,meaning=meaning,example=example,translation=translation,source=f'Global Success 7 · Unit {n} · Glossary tr. {page} · Ví dụ biên soạn',sourceFile='Tiếng Anh 7 Global Success.pdf',sourcePage=page+2,lesson=lesson['id']))
    lesson['words'].append(id)
for n in range(1,5):
    ids=[id for l in lessons if l['kind']=='unit' and (n-1)*3<int(l['number'])<=n*3 for id in l['words']]
    lessons.append(dict(id=f'en-r{n}',lang='en',kind='review',short=f'Review {n}',title=f'Ôn tập Unit {(n-1)*3+1}–{n*3}',description='Ôn chung các từ trọng tâm của ba Unit. Tiến độ dùng chung với bài gốc.',source='Nhóm ôn tập theo cấu trúc sách Global Success 7',words=ids,symbol='↻'))

names=['H41001','H41002','H41003','H41004','H41005','H41006','H41008','H41327','H41328','H41329','H41330','H41332','H41333']
pages=[]
for name in names:
    reader=PdfReader(Path('D:/Desktop/SSS')/(name+'.pdf'))
    for i,p in enumerate(reader.pages):
        text=p.extract_text() or ''
        clean=re.sub(r'\s+','',text)
        pages.append(dict(name=name,page=i+1,text=clean))
for number,title in enumerate(titles_zh,1):
    lessons.append(dict(id=f'zh-t{number}',lang='zh',kind='unit',number=number,short=f'Bài {number:02d}',title=title,description='15 từ trong ngữ cảnh HSK 4 · chữ giản thể, pinyin và nghĩa tiếng Việt.',source='Biên soạn từ các PDF HSK 4 đã cung cấp. Nguồn cụ thể ghi trên mỗi từ.',words=[]))
for row in chinese_rows:
    number,text,pron,pos,meaning,example,translation=row
    n=int(number);lesson=next(l for l in lessons if l['id']==f'zh-t{n}')
    hits=[p for p in pages if text in p['text']]
    if not hits:raise ValueError('Chinese word not found in supplied PDFs: '+text)
    exact=[p for p in hits if example in p['text']]
    source=(exact or hits)[0]
    id=f'zh-{n:02d}-{len(lesson["words"])+1:02d}'
    provenance=f'{source["name"]} · Trang PDF {source["page"]}'
    if not exact:provenance+=' · Ví dụ biên soạn'
    example_pron=' '.join(lazy_pinyin(example,style=Style.TONE,neutral_tone_with_five=False)).replace(' 。','。').replace(' ，','，').replace(' ？','？').replace(' ！','！')
    words.append(dict(id=id,lang='zh',text=text,pron=pron,pos=pos,meaning=meaning,example=example,examplePron=example_pron,translation=translation,source=provenance,sourceFile=source['name']+'.pdf',sourcePage=source['page'],lesson=lesson['id'],occurrences=[dict(file=p['name']+'.pdf',page=p['page']) for p in hits]))
    lesson['words'].append(id)
for name in names:
    ids=[w['id'] for w in words if w['lang']=='zh' and any(o['file']==name+'.pdf' for o in w['occurrences'])]
    lessons.append(dict(id='zh-'+name.lower(),lang='zh',kind='test',short=name,title='Từ vựng theo đề '+name,description='Các từ đã biên soạn xuất hiện trong đề này. Tiến độ dùng chung với bài theo chủ đề.',source=name+'.pdf · Từ vựng đối chiếu trên toàn bộ đề',words=ids,symbol='卷'))
result=dict(version=1,lessons=lessons,words=words)
(ROOT/'www/data.js').write_text('const DATA = '+json.dumps(result,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
(ROOT/'content/catalog.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Built {len(words)} words in {len(lessons)} lesson views: '+str({lang:sum(w['lang']==lang for w in words) for lang in ['en','zh']}))
