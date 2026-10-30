"""Han/office content, legacy preservation, course filters and backup regression."""
from pathlib import Path
import json,zipfile,sys,hashlib
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8');ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));byid={w['id']:w for w in data['words']}
with zipfile.ZipFile(ROOT/'output/Lingo-SoTuVung-1.10.0.apk') as z:
 old=json.loads(z.read('assets/www/data.js').decode().removeprefix('const DATA = ').strip().removesuffix(';'))
 assert len(old['words'])==13794
 for w in old['words']:
  assert byid[w['id']]==w,w['id']
  assert z.read('assets/www/audio/'+w['id']+'.mp3')==(ROOT/'www/audio'/(w['id']+'.mp3')).read_bytes(),w['id']
 for l in old['lessons']:assert next(x for x in data['lessons'] if x['id']==l['id'])==l
new=[w for w in data['words'] if w.get('level') in ('han','office')]
courses={'han-1':(15,1),'han-2':(15,16),'han-3':(10,1),'han-4':(10,11),'han-5':(13,1),'han-6':(13,14),'office-standard':(22,1)}
assert len(new)==3565 and len([l for l in data['lessons'] if l.get('level')!='intensive5'])==531
assert len(byid)==len(data['words'])
manifest=json.loads((ROOT/'content/audio-manifest.json').read_text(encoding='utf-8'))
for w in new:
 spoken=w.get('speechText',w['text'])
 checksum=hashlib.sha256(('zh-CN-XiaoxiaoNeural|'+w['text']+('|'+spoken if spoken!=w['text'] else '')).encode()).hexdigest()
 assert manifest[w['id']]['textHash']==checksum,w['id']
checks={('han-1','zhh-1-u7','米'):('mǐ','gạo'),('han-2','zhh-2-u27','得'):('dé','được'),('han-5','zhh-5-u4','系'):('xì','khoa'),('office-standard','zho-u20','得'):('děi','phải')}
for (course,lesson,text),(pron,meaning) in checks.items():
 w=next(w for w in new if w['course']==course and w['lesson']==lesson and w['text']==text)
 assert w['pron']==pron and meaning in w['meaning']

for c,(count,start) in courses.items():
 ls=[l for l in data['lessons'] if l.get('course')==c]
 assert [l['number'] for l in ls]==list(range(start,start+count))
 for l in ls:
  assert l['words'] and len(set(l['words']))==len(l['words'])
  for id in l['words']:
   w=byid[id];assert w['course']==c and w['lesson']==l['id']
   assert all(w[k] for k in ['text','pron','meaning','sourceFile','sourcePage'])
   assert not any(c in w['text'] for c in ['+','（名）','huiyiting','duiwai'])
errors=[]
backup={'schema':1,'progress':{'zh30-1-01-01':{'due':1,'interval':4,'reps':3,'lapses':1,'last':'2026-10-17'}},'mistakes':{'zh30-1-01-01':{'count':2,'lastWrong':1234,'mastered':True,'mode':'meaning'}},'favorites':['zh30-1-01-01'],'last':{'zh':'zh30-1-u1'},'lastCourses':{'hsk30-1':'zh30-1-u1','4.2':'zh4-u11'},'daily':{},'settings':{'dark':False,'slow':False,'goal':15}}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 ctx=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');ctx.add_init_script("window.audioCalls=[];window.Android={load(){return localStorage.getItem('test-state')||''},save(s){localStorage.setItem('test-state',s);return true},theme(){},stop(){},play(id,slow){audioCalls.push({id,slow})}}")
 page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.goto((ROOT/'www/index.html').as_uri());assert page.evaluate('Object.keys(state.progress).length')==0
 page.evaluate('(s)=>receiveBackup(JSON.stringify(s))',backup);page.locator('[data-action="open-language"][data-lang="zh"]').click();page.locator('[data-action="hsk-level"][data-level="han"]').click()
 assert page.locator('[data-action="hsk-book"]').count()==6
 for c,(count,start) in courses.items():
  page.evaluate('(c)=>{lang="zh";hskLevel=c==="office-standard"?"office":"han";hanBook=c;page="library";render()}',c)
  l=next(l for l in data['lessons'] if l.get('course')==c)
  page.locator(f'[data-action="hsk-book"][data-book="{c}"]').click();assert page.locator('[data-action="lesson"]').count()==count
  assert page.evaluate('(c)=>WORDS.filter(inCourse).every(w=>w.course===c)',c)
  page.locator(f'[data-action="lesson"][data-id="{l["id"]}"]').click();assert page.evaluate('(c)=>state.lastCourses[c]',c)==l['id']
  page.locator('[data-action="quiz-menu"]').click();page.locator('[data-action="start-quiz"][data-mode="meaning"]').click()
  assert page.evaluate('(c)=>study.queue.every(w=>w.course===c)&&study.options.every(w=>w.course===c)',c)
  id=page.evaluate('study.queue[0].id');page.evaluate("answerQuestion('wrong');answerQuestion('wrong')");assert page.evaluate('(id)=>state.mistakes[id].count',id)==1
  page.locator('[data-action="next-question"]').click()
  while page.evaluate('study.index<study.queue.length'):
   page.evaluate('answerQuestion(study.queue[study.index].id)');page.locator('[data-action="next-question"]').click()
  page.locator('[data-action="retry-wrong"]').click();assert page.evaluate('study.queue.map(w=>w.id)')==[id]
  page.evaluate('answerQuestion(study.queue[0].id)');page.locator('[data-action="next-question"]').click();page.locator('[data-action="open-mistakes"]').click();page.locator('[data-action="mistake-scope"][data-scope="zh"]').click();assert page.locator('.mistake-item').count()==1
  page.locator('[data-action="audio"]').first.click();assert page.evaluate('audioCalls.at(-1).id')==id
  page.locator('[data-action="master-mistake"]').click();assert page.evaluate('(id)=>state.mistakes[id].mastered',id)
  page.evaluate("(id)=>{startStudy([BYID[id]],'typing','Test','lesson')}",id);page.locator('#typed-answer').fill(byid[id]['text']);page.locator('[data-action="check-typing"]').click();assert page.evaluate('study.correct')==1
  for mode in ['reverse','listening']:
   page.evaluate('(a)=>startStudy(WORDS.filter(w=>w.course===a.c).slice(0,3),a.mode,"Test","library")',dict(c=c,mode=mode))
   assert page.evaluate('(c)=>study.options.every(w=>w.course===c)',c)
   page.evaluate('answerQuestion(study.queue[0].id)');assert page.evaluate('study.correct')==1
  page.evaluate("(id)=>{state.progress[id].due=1;study=null;page='library';render()}",id)
  assert page.evaluate('(c)=>dueWords("zh",c==="office-standard"?"office":"han",c).length>0&&dueWords("zh",c==="office-standard"?"office":"han",c).every(w=>w.course===c)',c)
 saved=page.evaluate('state');raw=page.evaluate('backup()');page.evaluate('state=defaults()');page.evaluate('(s)=>receiveBackup(s)',raw);assert page.evaluate('state')==saved;page.reload();assert page.evaluate('state')==saved
 assert page.evaluate("state.progress['zh30-1-01-01'].reps===3&&state.lastCourses['hsk30-1']==='zh30-1-u1'")
 for width in [320,390,700]:
  page.set_viewport_size({'width':width,'height':844})
  for c in courses:
   for dark in [False,True]:
    for view in ['library','words','stats','mistakes']:
     page.evaluate('(a)=>{lang="zh";hskLevel=a.c==="office-standard"?"office":"han";hanBook=a.c;state.settings.dark=a.dark;mistakeScope="zh";page=a.view;render()}',dict(c=c,dark=dark,view=view))
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,c,dark,view)
 for c in ['han-1','office-standard']:
  page.set_viewport_size({'width':390,'height':844})
  page.evaluate('(c)=>{lang="zh";hskLevel=c==="office-standard"?"office":"han";hanBook=c;page="library";state.settings.dark=false;render()}',c)
  page.screenshot(path=str(ROOT/'output/screenshots'/f'{c}-courses.png'))
 assert not errors,errors;b.close()
report=dict(result='passed',newItems=len(new),newLessons=98,legacyItemsUnchanged=13794,physicalDeviceTested=False)
(ROOT/'output/han-office-test-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
