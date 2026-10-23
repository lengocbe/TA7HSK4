"""New HSK 3.0 courses: exact legacy preservation, filtering and progress migration."""
from pathlib import Path
import json,zipfile,hashlib,sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8');ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));byid={w['id']:w for w in data['words']}
with zipfile.ZipFile(ROOT/'output/Lingo-SoTuVung-1.8.0.apk') as z:
 old=json.loads(z.read('assets/www/data.js').decode().removeprefix('const DATA = ').strip().removesuffix(';'))
 assert len(old['words'])==7817 and len(old['lessons'])==258
 for w in old['words']:
  assert byid[w['id']]==w,w['id']
  assert z.read('assets/www/audio/'+w['id']+'.mp3')==(ROOT/'www/audio'/(w['id']+'.mp3')).read_bytes(),w['id']
 for l in old['lessons']:assert next(x for x in data['lessons'] if x['id']==l['id'])==l
new=[w for w in data['words'] if w.get('level')=='hsk30'];courses={'hsk30-1':(15,1),'hsk30-2':(15,1),'hsk30-3':(18,1),'hsk30-4.1':(10,1),'hsk30-4.2':(10,11)}
assert len([l for l in data['lessons'] if l.get('level')!='boya'])==326
assert len(new)==1823 and len([w for w in data['words'] if w.get('level')!='boya'])==9640
assert {c:sum(w['course']==c for w in new) for c in courses}=={'hsk30-1':330,'hsk30-2':211,'hsk30-3':483,'hsk30-4.1':392,'hsk30-4.2':407}
assert next(w for w in new if w['course']=='hsk30-1' and w['text']=='一')['pron']=='yī'
assert next(w for w in new if w['course']=='hsk30-2' and w['text']=='得')['pron']=='de'
assert next(w for w in new if w['course']=='hsk30-3' and w['text']=='长')['pron']=='zhǎng'
assert next(w for w in new if w['text']=='笔记本电脑')['alternatives']==['笔记本']
audit={r['id']:r for r in json.loads((ROOT/'content/hsk30/source-audit.json').read_text(encoding='utf-8'))}
manifest=json.loads((ROOT/'content/audio-manifest.json').read_text(encoding='utf-8'))
for c,(count,start) in courses.items():
 ls=[l for l in data['lessons'] if l.get('course')==c];assert [l['number'] for l in ls]==list(range(start,start+count))
 for l in ls:
  ws=[byid[id] for id in l['words']];assert ws and all(w['course']==c for w in ws)
  for w in ws:
   assert all(w[k] for k in ['text','pron','meaning','sourceFile','sourcePage','pos'])
   assert audit[w['id']]['source']['lesson']==l['number'] and audit[w['id']]['source']['page']==w['sourcePage']
   spoken=w.get('speechText',w['text']);h=hashlib.sha256(('zh-CN-XiaoxiaoNeural|'+w['text']+('|'+spoken if spoken!=w['text'] else '')).encode()).hexdigest()
   assert manifest[w['id']]['textHash']==h
errors=[]
backup={'schema':1,'progress':{'zhk-bu-01-01':{'due':1,'interval':4,'reps':3,'lapses':1,'last':'2026-10-17'}},'mistakes':{'zhk-bu-01-01':{'count':2,'lastWrong':1234,'mastered':True,'mode':'meaning'}},'favorites':['zhk-bu-01-01'],'last':{'zh':'zhk-bu-u1'},'lastCourses':{'spoken-basic-upper':'zhk-bu-u1','4.2':'zh4-u11'},'daily':{},'settings':{'dark':False,'slow':False,'goal':15}}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 ctx=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');ctx.add_init_script("window.audioCalls=[];window.Android={load(){return localStorage.getItem('test-state')||''},save(s){localStorage.setItem('test-state',s);return true},theme(){},stop(){},play(id,slow){audioCalls.push({id,slow})}}")
 page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.goto((ROOT/'www/index.html').as_uri());assert page.evaluate('Object.keys(state.progress).length')==0
 page.evaluate('(s)=>receiveBackup(JSON.stringify(s))',backup);page.locator('[data-action="open-language"][data-lang="zh"]').click();page.locator('[data-action="hsk-level"][data-level="hsk30"]').click()
 assert page.locator('[data-action="hsk-book"]').count()==5
 for c,(count,start) in courses.items():
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
  page.evaluate("(id)=>{state.progress[id].due=1;study=null;page='library';render()}",id)
  assert page.evaluate('(c)=>dueWords("zh","hsk30",c).length>0&&dueWords("zh","hsk30",c).every(w=>w.course===c)',c)
 saved=page.evaluate('state');raw=page.evaluate('backup()');page.evaluate('state=defaults()');page.evaluate('(s)=>receiveBackup(s)',raw);assert page.evaluate('state')==saved;page.reload();assert page.evaluate('state')==saved
 assert page.evaluate("state.progress['zhk-bu-01-01'].reps===3&&state.lastCourses['spoken-basic-upper']==='zhk-bu-u1'")
 for width in [320,360,390,700]:
  page.set_viewport_size({'width':width,'height':844})
  for c in courses:
   for dark in [False,True]:
    for view in ['library','words','stats','mistakes']:
     page.evaluate('(a)=>{lang="zh";hskLevel="hsk30";hsk30Book=a.c;state.settings.dark=a.dark;mistakeScope="zh";page=a.view;render()}',dict(c=c,dark=dark,view=view));assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,c,dark,view)
 page.set_viewport_size({'width':390,'height':844});page.evaluate("lang='zh';hskLevel='hsk30';hsk30Book='hsk30-1';page='library';state.settings.dark=false;render()");page.screenshot(path=str(ROOT/'output/screenshots/hsk30-courses.png'))
 assert not errors,errors;b.close()
report=dict(result='passed',newItems=len(new),newLessons=68,legacyItemsUnchanged=7817,physicalDeviceTested=False)
(ROOT/'output/hsk30-test-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
