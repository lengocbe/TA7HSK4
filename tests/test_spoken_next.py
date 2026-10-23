"""Four follow-on books: source integrity, legacy preservation and UI migration."""
from pathlib import Path
import json,zipfile,hashlib,sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8');ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));byid={w['id']:w for w in data['words']}
courses={'spoken-basic-upper':(12,1),'spoken-basic-lower':(12,13),'spoken-intermediate':(14,1),'spoken-advanced':(20,1)}
with zipfile.ZipFile(ROOT/'output/Lingo-SoTuVung-1.7.0.apk') as z:
 old=json.loads(z.read('assets/www/data.js').decode().removeprefix('const DATA = ').strip().removesuffix(';'))
 assert len(old['words'])==5882
 for w in old['words']:
  assert byid[w['id']]==w,w['id']
  assert z.read('assets/www/audio/'+w['id']+'.mp3')==(ROOT/'www/audio'/(w['id']+'.mp3')).read_bytes(),w['id']
 for l in old['lessons']:assert next(x for x in data['lessons'] if x['id']==l['id'])==l
new=[w for w in data['words'] if w.get('course') in courses]
assert len(new)==1935 and len([w for w in data['words'] if w.get('level') not in ['hsk30','boya']])==7817 and len([l for l in data['lessons'] if l.get('level') not in ['hsk30','boya']])==258
for course,count in zip(courses,[302,310,491,658]):
 assert sum(w['course']==course and w['itemKind']=='vocabulary' for w in new)==count
assert sum(w['itemKind']=='phrase' for w in new)==174
assert [(w['pron'],w.get('speechText')) for w in new if w['lesson']=='zhk-bu-u10' and w['text']=='得']==[('děi','得回去了'),('dé','得病')]
assert next(w for w in new if w['lesson']=='zhk-bl-u18' and w['text']=='长')['pron']=='zhǎng'
assert next(w for w in new if w['text']=='这真是以不变应万变。')['pron'].endswith('yǐ bù biàn yìng wàn biàn。')
assert next(w for w in new if w['text']=='让丈夫自己去处理吧。')['pron'].endswith('chǔ lǐ ba。')
assert all(not any(s in w['text'] for s in ['j心','瞬啪','咪当','筒萝','奥论','毕竞']) for w in new)
audit={r['id']:r for r in json.loads((ROOT/'content/spoken-next/source-audit.json').read_text(encoding='utf-8'))}
manifest=json.loads((ROOT/'content/audio-manifest.json').read_text(encoding='utf-8'))
for c,(count,start) in courses.items():
 ls=[l for l in data['lessons'] if l.get('course')==c]
 assert [l['number'] for l in ls]==list(range(start,start+count))
 for l in ls:
  ws=[byid[id] for id in l['words']]
  assert sum(w['itemKind']=='phrase' for w in ws)>=3
  assert sum(w['itemKind']=='vocabulary' for w in ws)>0
  for w in ws:
   assert w['course']==c and all(w[k] for k in ['text','pron','meaning','source','sourcePage','sourceFile'])
   assert audit[w['id']]['source']['page']==w['sourcePage']
   spoken=w.get('speechText',w['text'])
   h=hashlib.sha256(('zh-CN-XiaoxiaoNeural|'+w['text']+('|'+spoken if spoken!=w['text'] else '')).encode()).hexdigest()
   assert manifest[w['id']]['textHash']==h
errors=[]
backup={'schema':1,'progress':{'zhk-01-01':{'due':1,'interval':4,'reps':3,'lapses':1,'last':'2026-10-15'}},'mistakes':{'zhk-01-01':{'count':2,'lastWrong':1234,'mastered':True,'mode':'meaning'}},'favorites':['zhk-01-01'],'last':{'en':'en-u1','zh':'zhk-u1'},'lastCourses':{'spoken-upper':'zhk-u1','6.2':'zh6-u21'},'daily':{},'settings':{'dark':False,'slow':False,'goal':15}}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 ctx=b.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
 ctx.add_init_script("window.audioCalls=[];window.Android={load(){return localStorage.getItem('test-state')||''},save(s){localStorage.setItem('test-state',s);return true},theme(){},stop(){},play(id,slow){audioCalls.push({id,slow})}}")
 page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 page.goto((ROOT/'www/index.html').as_uri());assert page.evaluate('Object.keys(state.progress).length')==0
 page.evaluate('(s)=>receiveBackup(JSON.stringify(s))',backup)
 page.locator('[data-action="open-language"][data-lang="zh"]').click();page.locator('[data-action="hsk-level"][data-level="spoken"]').click()
 assert page.locator('[data-action="hsk-book"]').count()==6
 for c,(count,start) in courses.items():
  l=next(l for l in data['lessons'] if l.get('course')==c)
  page.locator(f'[data-action="hsk-book"][data-book="{c}"]').click();assert page.locator('[data-action="lesson"]').count()==count
  page.locator(f'[data-action="lesson"][data-id="{l["id"]}"]').click()
  page.locator('[data-action="learn"][data-mode="new"]').click();assert page.evaluate('(c)=>study.queue.every(w=>w.course===c&&w.itemKind==="vocabulary")',c)
  page.evaluate("study=null;page='lesson';render()")
  page.locator('[data-action="spoken-section"][data-section="phrases"]').click()
  page.locator('[data-action="quiz-menu"]').click();page.locator('[data-action="start-quiz"][data-mode="meaning"]').click()
  assert page.evaluate('(c)=>study.queue.every(w=>w.course===c&&w.itemKind==="phrase")&&study.options.every(w=>w.course===c&&w.itemKind==="phrase")',c)
  id=page.evaluate('study.queue[0].id');page.evaluate("answerQuestion('wrong');answerQuestion('wrong')");assert page.evaluate('(id)=>state.mistakes[id].count',id)==1
  page.locator('[data-action="next-question"]').click()
  while page.evaluate('study.index<study.queue.length'):
   page.evaluate('answerQuestion(study.queue[study.index].id)');page.locator('[data-action="next-question"]').click()
  page.locator('[data-action="retry-wrong"]').click();assert page.evaluate('study.queue.map(w=>w.id)')==[id]
  page.evaluate('answerQuestion(study.queue[0].id)');page.locator('[data-action="next-question"]').click()
  page.locator('[data-action="open-mistakes"]').click();page.locator('[data-action="mistake-scope"][data-scope="zh"]').click()
  assert page.locator('.mistake-item').count()==1
  page.locator('[data-action="audio"]').first.click();assert page.evaluate('audioCalls.at(-1).id')==id
  page.locator('[data-action="master-mistake"]').click();assert page.locator('.mistake-item').count()==0
  assert page.evaluate('(id)=>state.mistakes[id].mastered&&state.mistakes[id].count===1',id)
  page.evaluate("(id)=>{startStudy([BYID[id]],'meaning','Test','lesson');answerQuestion('wrong')}",id)
  assert page.evaluate('(id)=>state.mistakes[id].count===2&&!state.mistakes[id].mastered',id)
  page.evaluate("(id)=>{startStudy([BYID[id]],'typing','Test','lesson')}",id)
  page.locator('#typed-answer').fill(byid[id]['text']);page.locator('[data-action="check-typing"]').click();assert page.evaluate('study.correct')==1
  page.evaluate("(id)=>{state.progress[id].due=1;study=null;page='library';render()}",id)
  assert page.evaluate('(c)=>dueWords("zh","spoken",c).length>0&&dueWords("zh","spoken",c).every(w=>w.course===c)',c)
 saved=page.evaluate('state');raw=page.evaluate('backup()');page.evaluate('state=defaults()');page.evaluate('(s)=>receiveBackup(s)',raw);assert page.evaluate('state')==saved
 page.reload();assert page.evaluate('state')==saved
 assert page.evaluate("state.progress['zhk-01-01'].reps===3&&state.lastCourses['spoken-upper']==='zhk-u1'")
 for width in [320,360,390,700]:
  page.set_viewport_size({'width':width,'height':844})
  for c in courses:
   longest=max((w for w in new if w['course']==c and w['itemKind']=='phrase'),key=lambda w:len(w['text']))
   for dark in [False,True]:
    for view in ['library','detail','mistakes','words']:
     page.evaluate('(a)=>{lang="zh";hskLevel="spoken";spokenBook=a.c;currentWord=a.id;state.settings.dark=a.dark;mistakeScope="zh";page=a.view;render()}',dict(c=c,id=longest['id'],dark=dark,view=view))
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,c,dark,view)
     assert page.evaluate("[...document.querySelectorAll('.spoken-books .pill')].every(b=>b.scrollWidth<=b.clientWidth+1)"),(width,c,dark,view)
 page.set_viewport_size({'width':390,'height':844});page.evaluate("lang='zh';hskLevel='spoken';spokenBook='spoken-basic-upper';page='library';state.settings.dark=false;render()")
 page.screenshot(path=str(ROOT/'output/screenshots/spoken-next-courses.png'),full_page=True)
 assert not errors,errors;b.close()
report=dict(result='passed',newVocabulary=sum(w['itemKind']=='vocabulary' for w in new),newPhrases=sum(w['itemKind']=='phrase' for w in new),newLessons=58,legacyItemsUnchanged=5882,physicalDeviceTested=False)
(ROOT/'output/spoken-next-test-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
